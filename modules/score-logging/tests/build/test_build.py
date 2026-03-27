"""Build and test verification for score-logging (DLT middleware).

Run on Linux laptop:
    pytest modules/score-logging/tests/build/test_build.py -v
"""

import subprocess
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "score-logging"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"score-logging not found at {MODULE_DIR}"
    assert (MODULE_DIR / "MODULE.bazel").exists(), "MODULE.bazel missing"
    return MODULE_DIR


class TestEnvironment:

    def test_bazel_installed(self):
        rc, out, _ = _run("bazel --version")
        assert rc == 0, "Bazel not installed"

    def test_bazel_version(self):
        expected = (MODULE_DIR / ".bazelversion").read_text().strip()
        rc, out, _ = _run("bazel --version")
        assert expected in out, f"Expected Bazel {expected}, got: {out}"


class TestBuild:

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_bazel_build_all(self, module_dir):
        rc, out, err = _run(
            "bazel build --config=x86_64-linux //score/...",
            timeout=1200,
        )
        assert rc == 0, f"Build failed:\n{err[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_mw_log_build(self, module_dir):
        rc, _, err = _run(
            "bazel build --config=x86_64-linux //score/mw/log/...",
            timeout=600,
        )
        assert rc == 0, f"mw/log build failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_datarouter_build(self, module_dir):
        rc, _, err = _run(
            "bazel build --config=x86_64-linux //score/datarouter/...",
            timeout=600,
        )
        assert rc == 0, f"datarouter build failed:\n{err[-1000:]}"


class TestUnitTests:

    @pytest.mark.unit
    @pytest.mark.score_logging
    def test_all_unit_tests(self, module_dir):
        rc, out, err = _run(
            "bazel test --config=x86_64-linux //score/... "
            "--build_tests_only --test_output=summary",
            timeout=1800,
        )
        lines = (out + err).split("\n")
        passed = [l for l in lines if "PASSED" in l]
        failed = [l for l in lines if "FAILED" in l and "//" in l]
        print(f"Passed: {len(passed)}, Failed: {len(failed)}")
        assert rc == 0, (
            f"Unit tests failed ({len(failed)} failures):\n"
            + "\n".join(failed[:20])
        )

    @pytest.mark.unit
    @pytest.mark.score_logging
    def test_mw_log_tests(self, module_dir):
        rc, _, err = _run(
            "bazel test --config=x86_64-linux //score/mw/log/... "
            "--build_tests_only --test_output=errors",
            timeout=600,
        )
        assert rc == 0, f"mw/log tests failed:\n{err[-1000:]}"


class TestSanitizers:

    @pytest.mark.security
    @pytest.mark.score_logging
    @pytest.mark.slow
    def test_asan(self, module_dir):
        rc, _, err = _run(
            "bazel test --config=x86_64-linux "
            "//score/mw/log/... --build_tests_only --test_output=errors",
            timeout=3600,
        )
        assert rc == 0, f"ASan findings:\n{err[-2000:]}"


class TestCodeQuality:

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_format_check(self, module_dir):
        rc, _, err = _run(
            "bazel test --config=x86_64-linux //:format.check",
            timeout=120,
        )
        assert rc == 0, f"Format check failed:\n{err[-1000:]}"
