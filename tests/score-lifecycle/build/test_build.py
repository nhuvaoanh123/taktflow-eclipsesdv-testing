"""Build and test verification for score-lifecycle.

Wraps the Bazel build/test commands into pytest so results integrate
with the taktflow-eclipsesdv-testing test infrastructure.

score-lifecycle (score_lifecycle_health v0.0.0) is a dual C++/Rust module
providing process lifecycle management and health monitoring for SCORE.
5 components: control_client_lib, health_monitoring_lib (C++ + Rust),
launch_manager_daemon, lifecycle_client_lib, common.

5 test targets (2 Rust tests, 1 C++ gtest, 2 cc_test).
Build config: --config=x86_64-linux.

Run on Linux laptop:
    pytest tests/score-lifecycle/build/test_build.py -v
"""

import subprocess
import pytest
from pathlib import Path


LIFECYCLE_DIR = Path(__file__).parent.parent.parent.parent / "score-lifecycle"

BAZEL_CONFIG = "--config=x86_64-linux"


def _run(cmd, cwd=None, timeout=600):
    """Run a shell command and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or LIFECYCLE_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="session")
def lifecycle_dir():
    assert LIFECYCLE_DIR.exists(), f"score-lifecycle not found at {LIFECYCLE_DIR}"
    assert (LIFECYCLE_DIR / "MODULE.bazel").exists(), "MODULE.bazel missing"
    return LIFECYCLE_DIR


# ---------------------------------------------------------------------------
# Phase 1: Environment checks
# ---------------------------------------------------------------------------


@pytest.mark.score_lifecycle
class TestEnvironment:
    """Phase 1: Verify build environment is ready."""

    def test_bazel_installed(self):
        """SWR-LC-001: Bazel build system must be available."""
        rc, out, _ = _run("bazel --version")
        assert rc == 0, "Bazel not installed"

    def test_gcc_installed(self):
        """SWR-LC-002: GCC toolchain must be available for C++ builds."""
        rc, out, _ = _run("gcc --version")
        assert rc == 0, "GCC not installed"

    def test_cargo_installed(self):
        """SWR-LC-003: Cargo/Rustc must be available for Rust components."""
        rc, out, _ = _run("cargo --version")
        assert rc == 0, "Cargo not installed"
        rc, out, _ = _run("rustc --version")
        assert rc == 0, "Rustc not installed"


# ---------------------------------------------------------------------------
# Phase 2: Build verification
# ---------------------------------------------------------------------------


@pytest.mark.score_lifecycle
class TestBuild:
    """Phase 2: Verify score-lifecycle builds from source."""

    @pytest.mark.build
    def test_bazel_build_all(self, lifecycle_dir):
        """SWR-LC-010: Full build of all score-lifecycle source targets must succeed.

        Builds //src/... and //examples/... with --config=x86_64-linux to select
        the Linux x86_64 toolchain configuration.
        """
        rc, out, err = _run(
            f"bazel build {BAZEL_CONFIG} //src/... //examples/...",
            timeout=1200,
        )
        assert rc == 0, f"Build failed:\n{err[-2000:]}"

    @pytest.mark.build
    def test_examples_build(self, lifecycle_dir):
        """SWR-LC-011: All 4 example applications must build.

        Examples: control_application, cpp_lifecycle_app, cpp_supervised_app,
        rust_supervised_app.
        """
        rc, _, err = _run(
            f"bazel build {BAZEL_CONFIG} //examples/...",
            timeout=600,
        )
        assert rc == 0, f"Examples build failed:\n{err[-1000:]}"


# ---------------------------------------------------------------------------
# Phase 3: Unit tests -- all, then per-component
# ---------------------------------------------------------------------------


@pytest.mark.score_lifecycle
class TestUnitTests:
    """Phase 3: Run upstream unit test suite (5 test targets)."""

    @pytest.mark.unit
    def test_all_unit_tests(self, lifecycle_dir):
        """SWR-LC-020: All 5 upstream test targets must pass.

        Runs both //src/... and //tests/... with --config=x86_64-linux.
        Covers 2 Rust tests, 1 C++ gtest, and 2 cc_test targets.
        """
        rc, out, err = _run(
            f"bazel test {BAZEL_CONFIG} //src/... //tests/... "
            "--build_tests_only --test_output=summary",
            timeout=1800,
        )
        lines = (out + err).split("\n")
        failed = [l for l in lines if "FAILED" in l and "//" in l]
        assert rc == 0, (
            f"Unit tests failed ({len(failed)} failures):\n"
            + "\n".join(failed[:20])
        )

    @pytest.mark.unit
    def test_health_monitoring_cpp(self, lifecycle_dir):
        """SWR-LC-021: Health monitoring C++ tests must pass.

        health_monitoring_lib provides process health checking and
        watchdog management implemented in C++.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} "
            "//src/health_monitoring/... "
            "--test_output=errors --test_tag_filters=-rust",
            timeout=300,
        )
        assert rc == 0, f"Health monitoring C++ tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_health_monitoring_rust(self, lifecycle_dir):
        """SWR-LC-022: Health monitoring Rust tests must pass.

        health_monitoring_lib Rust component provides safe bindings and
        additional monitoring logic.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} "
            "//src/health_monitoring/... "
            "--test_output=errors --test_tag_filters=rust",
            timeout=300,
        )
        assert rc == 0, f"Health monitoring Rust tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_process_state(self, lifecycle_dir):
        """SWR-LC-023: Process state management tests must pass.

        Covers lifecycle state machine transitions used by
        launch_manager_daemon and lifecycle_client_lib.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} "
            "//tests/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Process state tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_common(self, lifecycle_dir):
        """SWR-LC-024: Common library tests must pass.

        Shared utilities and types used across all lifecycle components.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} "
            "//src/common/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Common library tests failed:\n{err[-1000:]}"


# ---------------------------------------------------------------------------
# Phase 4: Rust quality checks
# ---------------------------------------------------------------------------


@pytest.mark.score_lifecycle
class TestRustQuality:
    """Phase 4: Rust-specific quality checks."""

    @pytest.mark.build
    def test_cargo_clippy(self, lifecycle_dir):
        """SWR-LC-030: Cargo clippy must produce zero warnings.

        Runs clippy lint checks on all Rust components
        (health_monitoring_lib Rust, rust_supervised_app).
        """
        rc, out, err = _run(
            "cargo clippy --all-targets --all-features -- -D warnings",
            timeout=600,
        )
        assert rc == 0, f"Cargo clippy warnings:\n{err[-2000:]}"

    @pytest.mark.unit
    def test_miri(self, lifecycle_dir):
        """SWR-LC-031: Miri must find no undefined behavior in Rust tests.

        Runs the Rust test suite under Miri to detect undefined behavior,
        memory leaks, and data races in unsafe code blocks.
        """
        rc, out, err = _run(
            "cargo +nightly miri test",
            timeout=1200,
        )
        assert rc == 0, f"Miri findings:\n{err[-2000:]}"


# ---------------------------------------------------------------------------
# Phase 5: Sanitizer builds
# ---------------------------------------------------------------------------


@pytest.mark.score_lifecycle
class TestSanitizers:
    """Phase 5: Run with sanitizers enabled (upstream CI parity).

    Note: score-lifecycle uses --define sanitize=X rather than --config
    for sanitizer selection.
    """

    @pytest.mark.security
    def test_asan(self, lifecycle_dir):
        """SWR-LC-040: AddressSanitizer must produce zero findings.

        Detects out-of-bounds access, use-after-free, double-free, and
        memory leaks in C++ lifecycle components.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} --define sanitize=address "
            "//src/... //tests/... "
            "--build_tests_only --test_output=errors",
            timeout=3600,
        )
        assert rc == 0, f"ASan findings:\n{err[-2000:]}"

    @pytest.mark.security
    def test_tsan(self, lifecycle_dir):
        """SWR-LC-041: ThreadSanitizer must produce zero findings.

        Critical for launch_manager_daemon which manages concurrent
        process lifecycle transitions.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} --define sanitize=thread "
            "//src/... //tests/... "
            "--build_tests_only --test_output=errors",
            timeout=3600,
        )
        assert rc == 0, f"TSan findings:\n{err[-2000:]}"

    @pytest.mark.security
    def test_ubsan(self, lifecycle_dir):
        """SWR-LC-042: UndefinedBehaviorSanitizer must produce zero findings.

        Detects signed integer overflow, null pointer dereference, and
        other undefined behavior in C++ code.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} --define sanitize=undefined "
            "//src/... //tests/... "
            "--build_tests_only --test_output=errors",
            timeout=3600,
        )
        assert rc == 0, f"UBSan findings:\n{err[-2000:]}"


# ---------------------------------------------------------------------------
# Phase 6: Code quality checks
# ---------------------------------------------------------------------------


@pytest.mark.score_lifecycle
class TestCodeQuality:
    """Phase 6: Static analysis and code quality."""

    @pytest.mark.build
    def test_format_check(self, lifecycle_dir):
        """SWR-LC-050: Code formatting must comply with project style.

        Runs clang-format and rustfmt checks via Bazel target //:format.check.
        """
        rc, _, err = _run(
            "bazel test //:format.check",
            timeout=120,
        )
        assert rc == 0, f"Format check failed:\n{err[-1000:]}"

    @pytest.mark.build
    def test_copyright_check(self, lifecycle_dir):
        """SWR-LC-051: All source files must have valid license headers."""
        rc, _, err = _run(
            "bazel run //:copyright.check",
            timeout=120,
        )
        assert rc == 0, f"Copyright check failed:\n{err[-1000:]}"

    @pytest.mark.build
    def test_license_check(self, lifecycle_dir):
        """SWR-LC-052: Third-party license compliance must pass.

        Verifies all dependencies have approved licenses for automotive use.
        """
        rc, _, err = _run(
            "bazel run //:license-check",
            timeout=120,
        )
        assert rc == 0, f"License check failed:\n{err[-1000:]}"


# ---------------------------------------------------------------------------
# Phase 7: Coverage
# ---------------------------------------------------------------------------


@pytest.mark.score_lifecycle
class TestCoverage:
    """Phase 7: Code coverage must meet minimum thresholds."""

    @pytest.mark.build
    def test_cpp_coverage_above_threshold(self, lifecycle_dir):
        """SWR-LC-060: C++ line coverage must be at least 76%.

        Runs C++ test targets with Bazel coverage instrumentation and parses
        the combined LCOV report to verify the overall line coverage percentage.
        """
        rc, out, err = _run(
            f"bazel coverage {BAZEL_CONFIG} //src/... //tests/... "
            "--build_tests_only --combined_report=lcov "
            "--test_tag_filters=-rust",
            timeout=3600,
        )
        assert rc == 0, f"C++ coverage run failed:\n{err[-2000:]}"

        lcov_path = LIFECYCLE_DIR / "bazel-out" / "_coverage" / "_coverage_report.dat"
        if not lcov_path.exists():
            lcov_path = LIFECYCLE_DIR / "bazel-testlogs" / "coverage_report.dat"

        if not lcov_path.exists():
            pytest.skip(
                "C++ coverage report not found — verify Bazel coverage output path"
            )

        total_lines = 0
        hit_lines = 0
        content = lcov_path.read_text()
        for line in content.split("\n"):
            if line.startswith("LF:"):
                total_lines += int(line[3:])
            elif line.startswith("LH:"):
                hit_lines += int(line[3:])

        if total_lines == 0:
            pytest.fail("C++ coverage report contains no line data")

        coverage_pct = (hit_lines / total_lines) * 100
        threshold = 76.0
        assert coverage_pct >= threshold, (
            f"C++ line coverage {coverage_pct:.1f}% is below {threshold}% threshold "
            f"({hit_lines}/{total_lines} lines hit)"
        )

    @pytest.mark.build
    def test_rust_coverage_above_threshold(self, lifecycle_dir):
        """SWR-LC-061: Rust line coverage must be at least 93%.

        Runs Rust test targets with coverage instrumentation and verifies
        the line coverage percentage meets the higher Rust threshold.
        """
        rc, out, err = _run(
            f"bazel coverage {BAZEL_CONFIG} //src/... //tests/... "
            "--build_tests_only --combined_report=lcov "
            "--test_tag_filters=rust",
            timeout=3600,
        )
        assert rc == 0, f"Rust coverage run failed:\n{err[-2000:]}"

        lcov_path = LIFECYCLE_DIR / "bazel-out" / "_coverage" / "_coverage_report.dat"
        if not lcov_path.exists():
            lcov_path = LIFECYCLE_DIR / "bazel-testlogs" / "coverage_report.dat"

        if not lcov_path.exists():
            pytest.skip(
                "Rust coverage report not found — verify Bazel coverage output path"
            )

        total_lines = 0
        hit_lines = 0
        content = lcov_path.read_text()
        for line in content.split("\n"):
            if line.startswith("LF:"):
                total_lines += int(line[3:])
            elif line.startswith("LH:"):
                hit_lines += int(line[3:])

        if total_lines == 0:
            pytest.fail("Rust coverage report contains no line data")

        coverage_pct = (hit_lines / total_lines) * 100
        threshold = 93.0
        assert coverage_pct >= threshold, (
            f"Rust line coverage {coverage_pct:.1f}% is below {threshold}% threshold "
            f"({hit_lines}/{total_lines} lines hit)"
        )
