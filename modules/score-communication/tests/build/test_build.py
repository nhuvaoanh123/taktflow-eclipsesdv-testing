"""Build and test verification for score-communication (LoLa).

Wraps the Bazel build/test commands into pytest so results integrate
with the taktflow-eclipsesdv-testing test infrastructure.

Run on Linux laptop:
    pytest tests/build/test_score_communication_build.py -v
"""

import subprocess
import os
import json
import pytest
from pathlib import Path


LOLA_DIR = Path(__file__).parent.parent.parent / "upstream"


def _run(cmd, cwd=None, timeout=600):
    """Run a shell command and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or LOLA_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="session")
def lola_dir():
    assert LOLA_DIR.exists(), f"score-communication not found at {LOLA_DIR}"
    assert (LOLA_DIR / "MODULE.bazel").exists(), "MODULE.bazel missing"
    return LOLA_DIR


class TestEnvironment:
    """Phase 1: Verify build environment is ready."""

    def test_bazel_installed(self):
        rc, out, _ = _run("bazel --version")
        assert rc == 0, "Bazel not installed — run scripts/setup-lola-env.sh"

    def test_bazel_version(self):
        expected = (LOLA_DIR / ".bazelversion").read_text().strip()
        rc, out, _ = _run("bazel --version")
        assert expected in out, f"Expected Bazel {expected}, got: {out}"

    def test_gcc_installed(self):
        rc, out, _ = _run("gcc --version")
        assert rc == 0, "GCC not installed"

    def test_docker_available(self):
        rc, _, _ = _run("docker info")
        if rc != 0:
            pytest.skip("Docker not available — integration tests will be skipped")


class TestBuild:
    """Phase 2: Verify LoLa builds from source."""

    @pytest.mark.build
    def test_bazel_build_all(self, lola_dir):
        """ANK-B-01 equivalent: full build."""
        rc, out, err = _run("bazel build //...", timeout=1200)
        assert rc == 0, f"Build failed:\n{err[-2000:]}"

    @pytest.mark.build
    def test_examples_build(self, lola_dir):
        """Verify example applications build."""
        rc, _, err = _run("bazel build //examples/...", timeout=300)
        assert rc == 0, f"Examples build failed:\n{err[-1000:]}"

    @pytest.mark.build
    def test_benchmarks_build(self, lola_dir):
        """Verify performance benchmarks build."""
        rc, _, err = _run(
            "bazel build //score/mw/com/performance_benchmarks/...",
            timeout=300,
        )
        assert rc == 0, f"Benchmarks build failed:\n{err[-1000:]}"


class TestUnitTests:
    """Phase 3: Run upstream unit test suite."""

    @pytest.mark.unit
    def test_all_unit_tests(self, lola_dir):
        """KDB-U-01 equivalent: run all upstream unit tests."""
        rc, out, err = _run(
            "bazel test //... --build_tests_only --test_output=summary",
            timeout=1800,
        )
        # Parse test summary
        lines = (out + err).split("\n")
        failed = [l for l in lines if "FAILED" in l and "//" in l]
        assert rc == 0, (
            f"Unit tests failed ({len(failed)} failures):\n"
            + "\n".join(failed[:20])
        )

    @pytest.mark.unit
    def test_message_passing(self, lola_dir):
        """Test low-level message passing layer specifically."""
        rc, _, err = _run(
            "bazel test //score/message_passing/... --test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Message passing tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_mw_com_impl(self, lola_dir):
        """Test high-level middleware implementation."""
        rc, _, err = _run(
            "bazel test //score/mw/com/impl/... --test_output=errors",
            timeout=600,
        )
        assert rc == 0, f"mw::com impl tests failed:\n{err[-1000:]}"


class TestIntegration:
    """Phase 4: Run Docker-based integration tests."""

    @pytest.mark.integration
    def test_integration_suite(self, lola_dir):
        """Run multi-process integration tests in Docker."""
        # Check Docker first
        rc, _, _ = _run("docker info")
        if rc != 0:
            pytest.skip("Docker not available")

        rc, out, err = _run(
            "bazel test //quality/integration_testing/... --test_output=summary",
            timeout=1800,
        )
        assert rc == 0, f"Integration tests failed:\n{err[-2000:]}"


class TestSanitizers:
    """Phase 5-6: Run with sanitizers enabled."""

    @pytest.mark.security
    def test_asan_ubsan_lsan(self, lola_dir):
        """Run with Address/UndefinedBehavior/Leak sanitizers."""
        rc, _, err = _run(
            "bazel test --config=asan_ubsan_lsan //... "
            "--build_tests_only --test_output=errors",
            timeout=3600,
        )
        assert rc == 0, f"Sanitizer findings:\n{err[-2000:]}"

    @pytest.mark.security
    def test_tsan(self, lola_dir):
        """Run with Thread sanitizer."""
        rc, _, err = _run(
            "bazel test --config=tsan //... "
            "--build_tests_only --test_output=errors",
            timeout=3600,
        )
        assert rc == 0, f"Thread sanitizer findings:\n{err[-2000:]}"


class TestCodeQuality:
    """Phase 8-12: Static analysis and code quality."""

    @pytest.mark.build
    def test_format_check(self, lola_dir):
        """Verify code formatting."""
        rc, _, err = _run("bazel test //:format.check", timeout=120)
        assert rc == 0, f"Format check failed:\n{err[-1000:]}"

    @pytest.mark.build
    def test_copyright_check(self, lola_dir):
        """Verify license headers."""
        rc, _, err = _run("bazel run //:copyright.check", timeout=120)
        assert rc == 0, f"Copyright check failed:\n{err[-1000:]}"
