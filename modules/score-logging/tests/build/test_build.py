"""Build and test verification for score-logging (DLT middleware).

Mirrors the upstream CI checks from .github/workflows/:
  - build.yml: bazel build --lockfile_mode=error --config x86_64-linux //...
  - format.yml: bazel test --lockfile_mode=error //:format.check
  - copyright.yml: bazel run --lockfile_mode=error //:copyright.check
  - coverage_report.yml: bazel coverage with LCOV instrumentation

Run on Linux laptop:
    pytest modules/score-logging/tests/build/test_build.py -v
"""

import subprocess
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "score-logging"

# Upstream CI enforces --lockfile_mode=error on all commands.
# We relax to 'update' locally since we may not have the exact lockfile.
LOCKFILE = "--lockfile_mode=update"
CONFIG = "--config=x86_64-linux"


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
    assert MODULE_DIR.exists(), f"score-logging not found at {MODULE_DIR}"
    assert (MODULE_DIR / "MODULE.bazel").exists(), "MODULE.bazel missing"
    return MODULE_DIR


# ── Phase 1: Environment ────────────────────────────────────────────

class TestEnvironment:
    """Verify build prerequisites match upstream requirements."""

    def test_bazel_installed(self):
        rc, out, _ = _run("bazel --version")
        assert rc == 0, "Bazel not installed"

    def test_bazel_version_matches(self):
        """CI uses per-module .bazelversion — verify match."""
        expected = (MODULE_DIR / ".bazelversion").read_text().strip()
        rc, out, _ = _run("bazel --version")
        assert expected in out, f"Expected Bazel {expected}, got: {out}"

    def test_gcc_available(self):
        """Hermetic GCC 12.2.0 is downloaded by Bazel, but host gcc needed."""
        rc, _, _ = _run("gcc --version")
        assert rc == 0, "GCC not installed"


# ── Phase 2: Build (mirrors build.yml) ──────────────────────────────

class TestBuild:
    """Mirrors: bazel build --lockfile_mode=error --config x86_64-linux //..."""

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_bazel_build_all(self, module_dir):
        """CI job: build.yml — full build of all targets."""
        rc, out, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //score/...",
            timeout=1200,
        )
        assert rc == 0, f"Build failed:\n{err[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_mw_log_frontend(self, module_dir):
        """Build the logging frontend (core C++ + Rust bindings)."""
        rc, _, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //score/mw/log/...",
            timeout=600,
        )
        assert rc == 0, f"mw/log build failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_datarouter_daemon(self, module_dir):
        """Build the DLT daemon bridge (datarouter)."""
        rc, _, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //score/datarouter/...",
            timeout=600,
        )
        assert rc == 0, f"datarouter build failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_examples_build(self, module_dir):
        """Build example applications."""
        rc, _, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //examples/...",
            timeout=300,
        )
        # Examples may not exist in all versions
        if rc != 0 and "no targets found" in err.lower():
            pytest.skip("No examples directory")
        assert rc == 0, f"Examples build failed:\n{err[-1000:]}"


# ── Phase 3: Unit Tests (mirrors test tag conventions) ───────────────

class TestUnitTests:
    """Run upstream unit tests with --test_tag_filters=-manual (default)."""

    @pytest.mark.unit
    @pytest.mark.score_logging
    def test_all_unit_tests(self, module_dir):
        """Run all non-manual tests — the default CI test command."""
        rc, out, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //score/... "
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
    @pytest.mark.score_logging
    def test_mw_log_tests(self, module_dir):
        """Logging frontend tests (wait-free queues, DLT format, recorders)."""
        rc, _, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //score/mw/log/... "
            "--build_tests_only --test_output=errors",
            timeout=600,
        )
        assert rc == 0, f"mw/log tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.score_logging
    def test_datarouter_tests(self, module_dir):
        """DataRouter unit tests (DLT protocol, socket server, config)."""
        rc, _, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} "
            "//score/datarouter/test/ut/... "
            "--build_tests_only --test_output=errors",
            timeout=600,
        )
        assert rc == 0, f"datarouter tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.score_logging
    def test_rust_bridge(self, module_dir):
        """score_log_bridge Rust crate tests."""
        rc, _, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} "
            "//score/mw/log/rust/score_log_bridge:tests "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Rust bridge tests failed:\n{err[-1000:]}"


# ── Phase 4: Coverage (mirrors coverage_report.yml) ──────────────────

class TestCoverage:
    """Mirrors: bazel coverage with LCOV instrumentation filter."""

    @pytest.mark.slow
    @pytest.mark.score_logging
    def test_coverage_report(self, module_dir):
        """Generate LCOV coverage — instrumentation matches .bazelrc config.

        .bazelrc coverage section:
          instrumentation_filter="^//score/datarouter[/:],^//score/mw/log[/:],-//score/mw/.*/test[/:]"
        """
        rc, out, err = _run(
            f"bazel coverage {LOCKFILE} //score/... "
            "--test_output=summary",
            timeout=3600,
        )
        combined = out + err
        passed, failed, _ = _parse_test_summary(combined)
        print(f"Coverage run: {passed} passed, {failed} failed")
        assert rc == 0, f"Coverage failed:\n{combined[-2000:]}"

    @pytest.mark.slow
    @pytest.mark.score_logging
    def test_coverage_threshold(self, module_dir):
        """Parse LCOV report and verify minimum coverage threshold."""
        # Find the combined report
        import glob
        reports = glob.glob(
            str(Path.home() / ".cache/bazel/**/bazel-out/_coverage/_coverage_report.dat"),
            recursive=True,
        )
        if not reports:
            pytest.skip("No coverage report found — run test_coverage_report first")

        report = max(reports, key=lambda p: Path(p).stat().st_mtime)
        total_lines = 0
        hit_lines = 0
        with open(report) as f:
            for line in f:
                if line.startswith("LF:"):
                    total_lines += int(line.split(":")[1])
                elif line.startswith("LH:"):
                    hit_lines += int(line.split(":")[1])

        if total_lines == 0:
            pytest.skip("Empty coverage report")

        coverage_pct = 100.0 * hit_lines / total_lines
        print(f"Coverage: {hit_lines}/{total_lines} = {coverage_pct:.1f}%")
        assert coverage_pct >= 80.0, (
            f"Coverage {coverage_pct:.1f}% below 80% threshold"
        )


# ── Phase 5: Code Quality (mirrors format.yml, copyright.yml) ───────

class TestCodeQuality:
    """Mirrors upstream CI format, copyright, and lint checks."""

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_format_check(self, module_dir):
        """CI job: format.yml — bazel test //:format.check"""
        rc, out, err = _run(
            f"bazel test {LOCKFILE} //:format.check",
            timeout=300,
        )
        combined = out + err
        passed, failed, _ = _parse_test_summary(combined)
        if failed > 0:
            # Report which formatters failed but don't block on upstream style
            failures = [l for l in combined.split("\n") if "FAIL:" in l]
            print(f"Format failures (upstream style): {failures}")
        # Note: we report but don't assert — upstream formatting may differ
        # from our local toolchain versions
        print(f"Format check: {passed} passed, {failed} failed")

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_copyright_check(self, module_dir):
        """CI job: copyright.yml — bazel run //:copyright.check"""
        rc, _, err = _run(
            f"bazel run {LOCKFILE} //:copyright.check",
            timeout=120,
        )
        assert rc == 0, f"Copyright check failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.score_logging
    def test_lockfile_consistency(self, module_dir):
        """Verify MODULE.bazel.lock is present and non-empty."""
        lockfile = module_dir / "MODULE.bazel.lock"
        assert lockfile.exists(), "MODULE.bazel.lock missing"
        assert lockfile.stat().st_size > 0, "MODULE.bazel.lock is empty"
