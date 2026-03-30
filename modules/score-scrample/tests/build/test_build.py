"""Build and test verification for score-scrample.

S-CORE middleware component with C++ and Rust implementations.
Bazel-primary build system. Contains FEO extensions and scorex components.

Mirrors upstream CI:
  - bazel build --config=x86_64-linux //...
  - bazel test --config=x86_64-linux //...
  - format and copyright checks

Run on Linux laptop:
    pytest modules/score-scrample/tests/build/test_build.py -v
"""

import subprocess
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "score-scrample"
LOCKFILE = "--lockfile_mode=update"
CONFIG = "--config=host"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def _parse_test_summary(output):
    """Parse Bazel test summary into (passed, failed, skipped) counts."""
    passed = len(re.findall(r"PASSED", output))
    failed = len(re.findall(r"FAILED", output))
    skipped = len(re.findall(r"SKIPPED", output))
    return passed, failed, skipped


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"score-scrample not found at {MODULE_DIR}"
    assert (MODULE_DIR / "MODULE.bazel").exists(), "MODULE.bazel missing"
    return MODULE_DIR


# -- Phase 1: Environment ---------------------------------------------------

class TestEnvironment:

    def test_bazel_installed(self):
        rc, out, _ = _run("bazel --version")
        assert rc == 0, "Bazel not installed"

    def test_bazel_version_matches(self):
        expected = (MODULE_DIR / ".bazelversion").read_text().strip()
        rc, out, _ = _run("bazel --version")
        assert expected in out, f"Expected Bazel {expected}, got: {out}"

    def test_gcc_available(self):
        rc, _, _ = _run("gcc --version")
        assert rc == 0, "GCC not installed"


# -- Phase 2: Build ---------------------------------------------------------

class TestBuild:

    @pytest.mark.build
    @pytest.mark.score_scrample
    def test_bazel_build_all(self, module_dir):
        rc, out, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //...",
            timeout=1200,
        )
        assert rc == 0, f"Build failed:\n{err[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_scrample
    def test_src_build(self, module_dir):
        """Build src/ components."""
        rc, _, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //src/...",
            timeout=600,
        )
        assert rc == 0, f"src/ build failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.score_scrample
    def test_feo_build(self, module_dir):
        """Build FEO extension components."""
        rc, _, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //feo/...",
            timeout=600,
        )
        if rc != 0 and "no targets found" in err.lower():
            pytest.skip("No feo/ targets")
        assert rc == 0, f"feo/ build failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.score_scrample
    def test_examples_build(self, module_dir):
        rc, _, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //examples/...",
            timeout=300,
        )
        if rc != 0 and "no targets found" in err.lower():
            pytest.skip("No examples directory")
        assert rc == 0, f"Examples build failed:\n{err[-1000:]}"


# -- Phase 3: Unit Tests ----------------------------------------------------

class TestUnitTests:

    @pytest.mark.unit
    @pytest.mark.score_scrample
    def test_all_unit_tests(self, module_dir):
        rc, out, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //... "
            "--build_tests_only --test_output=summary",
            timeout=1800,
        )
        combined = out + err
        passed, failed, skipped = _parse_test_summary(combined)
        print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
        assert rc == 0, (
            f"Unit tests failed ({failed} failures):\n"
            + "\n".join(l for l in combined.split("\n") if "FAILED" in l)[:2000]
        )

    @pytest.mark.unit
    @pytest.mark.score_scrample
    def test_cpp_tests(self, module_dir):
        """C++ middleware tests."""
        rc, _, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //tests/cpp/... "
            "--build_tests_only --test_output=errors",
            timeout=600,
        )
        if rc != 0 and "no targets found" in err.lower():
            pytest.skip("No tests/cpp/ targets")
        assert rc == 0, f"C++ tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.score_scrample
    def test_rust_tests(self, module_dir):
        """Rust middleware tests."""
        rc, _, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //tests/rust/... "
            "--build_tests_only --test_output=errors",
            timeout=600,
        )
        if rc != 0 and "no targets found" in err.lower():
            pytest.skip("No tests/rust/ targets")
        assert rc == 0, f"Rust tests failed:\n{err[-1000:]}"


# -- Phase 4: Coverage ------------------------------------------------------

class TestCoverage:

    @pytest.mark.slow
    @pytest.mark.score_scrample
    def test_coverage_report(self, module_dir):
        rc, out, err = _run(
            f"bazel coverage {LOCKFILE} //... "
            "--test_output=summary",
            timeout=3600,
        )
        combined = out + err
        passed, failed, _ = _parse_test_summary(combined)
        print(f"Coverage run: {passed} passed, {failed} failed")
        assert rc == 0, f"Coverage failed:\n{combined[-2000:]}"


# -- Phase 5: Code Quality --------------------------------------------------

class TestCodeQuality:

    @pytest.mark.build
    @pytest.mark.score_scrample
    def test_format_check(self, module_dir):
        rc, out, err = _run(
            f"bazel test {LOCKFILE} //:format.check",
            timeout=300,
        )
        combined = out + err
        passed, failed, _ = _parse_test_summary(combined)
        if rc != 0 and "no such target" in combined.lower():
            pytest.skip("No //:format.check target")
        print(f"Format check: {passed} passed, {failed} failed")

    @pytest.mark.build
    @pytest.mark.score_scrample
    def test_copyright_check(self, module_dir):
        rc, _, err = _run(
            f"bazel run {LOCKFILE} //:copyright.check",
            timeout=120,
        )
        if rc != 0 and "no such target" in err.lower():
            pytest.skip("No //:copyright.check target")
        assert rc == 0, f"Copyright check failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.score_scrample
    def test_lockfile_consistency(self, module_dir):
        lockfile = module_dir / "MODULE.bazel.lock"
        if not lockfile.exists():
            pytest.skip("No MODULE.bazel.lock (scrample may not lock)")
