"""Build and test verification for score-baselibs.

Wraps the Bazel build/test commands into pytest so results integrate
with the taktflow-eclipsesdv-testing test infrastructure.

score-baselibs v0.2.4 provides foundational C++ libraries (OS abstraction,
memory, concurrency, language utilities, logging, JSON, Result types,
filesystem, networking, containers) used across all SCORE modules.

363 test files across 16 components. Build config: --config=bl-x86_64-linux.

Run on Linux laptop:
    pytest tests/score-baselibs/build/test_build.py -v
"""

import subprocess
import pytest
from pathlib import Path


BASELIBS_DIR = Path(__file__).parent.parent.parent.parent / "score-baselibs"

BAZEL_CONFIG = "--config=bl-x86_64-linux"


def _run(cmd, cwd=None, timeout=600):
    """Run a shell command and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or BASELIBS_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="session")
def baselibs_dir():
    assert BASELIBS_DIR.exists(), f"score-baselibs not found at {BASELIBS_DIR}"
    assert (BASELIBS_DIR / "MODULE.bazel").exists(), "MODULE.bazel missing"
    return BASELIBS_DIR


# ---------------------------------------------------------------------------
# Phase 1: Environment checks
# ---------------------------------------------------------------------------


@pytest.mark.score_baselibs
class TestEnvironment:
    """Phase 1: Verify build environment is ready."""

    def test_bazel_installed(self):
        """SWR-BL-001: Bazel build system must be available."""
        rc, out, _ = _run("bazel --version")
        assert rc == 0, "Bazel not installed — run scripts/setup-baselibs-env.sh"

    def test_bazel_version(self):
        """SWR-BL-002: Bazel version must match .bazelversion pinned in repo."""
        expected = (BASELIBS_DIR / ".bazelversion").read_text().strip()
        rc, out, _ = _run("bazel --version")
        assert expected in out, f"Expected Bazel {expected}, got: {out}"

    def test_gcc_installed(self):
        """SWR-BL-003: GCC toolchain must be available for native builds."""
        rc, out, _ = _run("gcc --version")
        assert rc == 0, "GCC not installed"


# ---------------------------------------------------------------------------
# Phase 2: Build verification
# ---------------------------------------------------------------------------


@pytest.mark.score_baselibs
class TestBuild:
    """Phase 2: Verify score-baselibs builds from source."""

    @pytest.mark.build
    def test_bazel_build_all(self, baselibs_dir):
        """SWR-BL-010: Full build of all score-baselibs targets must succeed.

        Uses --config=bl-x86_64-linux to select the baselibs Linux x86_64
        toolchain configuration.
        """
        rc, out, err = _run(
            f"bazel build {BAZEL_CONFIG} //score/...",
            timeout=1200,
        )
        assert rc == 0, f"Build failed:\n{err[-2000:]}"

    @pytest.mark.build
    def test_benchmarks_build(self, baselibs_dir):
        """SWR-BL-011: Google Benchmark-based performance benchmarks must build.

        Benchmarks are used to verify that library primitives meet latency
        and throughput requirements for ASIL-B real-time contexts.
        """
        rc, _, err = _run(
            f"bazel build {BAZEL_CONFIG} //score/... "
            "--build_tag_filters=benchmark",
            timeout=600,
        )
        assert rc == 0, f"Benchmarks build failed:\n{err[-1000:]}"


# ---------------------------------------------------------------------------
# Phase 3: Unit tests — all, then per-component
# ---------------------------------------------------------------------------


@pytest.mark.score_baselibs
class TestUnitTests:
    """Phase 3: Run upstream unit test suite (363 tests, 16 components)."""

    @pytest.mark.unit
    def test_all_unit_tests(self, baselibs_dir):
        """SWR-BL-020: All 363 upstream unit tests must pass.

        Excludes the toolchain sanity test that is also excluded in upstream CI.
        """
        rc, out, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/... "
            "--build_tests_only --test_output=summary "
            "--test_tag_filters=-toolchain",
            timeout=1800,
        )
        lines = (out + err).split("\n")
        failed = [l for l in lines if "FAILED" in l and "//" in l]
        assert rc == 0, (
            f"Unit tests failed ({len(failed)} failures):\n"
            + "\n".join(failed[:20])
        )

    # -- Per-component tests ------------------------------------------------

    @pytest.mark.unit
    def test_os(self, baselibs_dir):
        """SWR-BL-021: OS abstraction layer tests (73 tests, ASIL-B).

        Covers POSIX wrappers, process/thread management, and signal handling
        required for safety-critical real-time operation.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/os/test/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"OS tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_memory_shared(self, baselibs_dir):
        """SWR-BL-022: Shared memory tests (34 tests, ASIL-B).

        Validates zero-copy shared memory allocators and lifetime management
        used by score-communication (LoLa) for IPC.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/memory/shared/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Shared memory tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_concurrency(self, baselibs_dir):
        """SWR-BL-023: Lock-free concurrency primitives tests (29 tests, ASIL-B).

        Covers atomic operations, lock-free queues, and synchronization
        primitives for deterministic real-time behavior.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/concurrency/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Concurrency tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_language(self, baselibs_dir):
        """SWR-BL-024: Language utility tests (99 tests — safecpp + futurecpp).

        Tests safe C++ wrappers (safecpp) and forward-looking C++ utilities
        (futurecpp) that enforce memory safety and type safety at compile time.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/language/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Language tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_mw_log(self, baselibs_dir):
        """SWR-BL-025: Logging middleware tests (33 tests).

        Validates structured logging framework used across all SCORE modules
        for DLT-compatible diagnostic output.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/mw/log/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Logging tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_json(self, baselibs_dir):
        """SWR-BL-026: JSON parsing/serialization tests (13 tests).

        Covers the lightweight JSON library used for configuration files
        and service manifests.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/json/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"JSON tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_result(self, baselibs_dir):
        """SWR-BL-027: Result type tests (11 tests).

        Validates monadic Result<T, E> types used for explicit error handling
        without exceptions throughout SCORE.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/result/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Result type tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_filesystem(self, baselibs_dir):
        """SWR-BL-028: Filesystem abstraction tests (19 tests).

        Tests portable filesystem operations with safety-hardened error
        handling for POSIX and QNX targets.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/filesystem/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Filesystem tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_network(self, baselibs_dir):
        """SWR-BL-029: Network abstraction tests (11 tests).

        Covers socket abstractions and network utilities used by
        score-communication for transport-layer operations.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/network/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Network tests failed:\n{err[-1000:]}"

    @pytest.mark.unit
    def test_containers(self, baselibs_dir):
        """SWR-BL-030: Container library tests (5 tests).

        Tests fixed-capacity, allocation-free containers suitable for
        safety-critical real-time contexts.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //score/containers/... "
            "--test_output=errors",
            timeout=300,
        )
        assert rc == 0, f"Container tests failed:\n{err[-1000:]}"


# ---------------------------------------------------------------------------
# Phase 4: Sanitizer builds
# ---------------------------------------------------------------------------


@pytest.mark.score_baselibs
class TestSanitizers:
    """Phase 4: Run with sanitizers enabled (upstream CI parity)."""

    @pytest.mark.security
    def test_asan_ubsan_lsan(self, baselibs_dir):
        """SWR-BL-040: Address/UndefinedBehavior/Leak sanitizer pass.

        Mirrors upstream CI config asan_ubsan_lsan with baselibs build config.
        Must produce zero findings for ASIL-B compliance.
        """
        rc, _, err = _run(
            f"bazel test --config=asan_ubsan_lsan {BAZEL_CONFIG} //score/... "
            "--build_tests_only --test_output=errors",
            timeout=3600,
        )
        assert rc == 0, f"Sanitizer findings:\n{err[-2000:]}"

    @pytest.mark.security
    def test_tsan(self, baselibs_dir):
        """SWR-BL-041: Thread sanitizer pass.

        Mirrors upstream CI config tsan with baselibs build config.
        Critical for lock-free concurrency primitives correctness.
        """
        rc, _, err = _run(
            f"bazel test --config=tsan {BAZEL_CONFIG} //score/... "
            "--build_tests_only --test_output=errors",
            timeout=3600,
        )
        assert rc == 0, f"Thread sanitizer findings:\n{err[-2000:]}"


# ---------------------------------------------------------------------------
# Phase 5: Code quality checks
# ---------------------------------------------------------------------------


@pytest.mark.score_baselibs
class TestCodeQuality:
    """Phase 5: Static analysis and code quality."""

    @pytest.mark.build
    def test_format_check(self, baselibs_dir):
        """SWR-BL-050: Code formatting must comply with project style.

        Runs clang-format check via Bazel target //:format.check.
        """
        rc, _, err = _run(
            f"bazel test {BAZEL_CONFIG} //:format.check",
            timeout=120,
        )
        assert rc == 0, f"Format check failed:\n{err[-1000:]}"

    @pytest.mark.build
    def test_copyright_check(self, baselibs_dir):
        """SWR-BL-051: All source files must have valid license headers.

        Runs copyright header verification via Bazel target //:copyright.check.
        """
        rc, _, err = _run(
            f"bazel run {BAZEL_CONFIG} //:copyright.check",
            timeout=120,
        )
        assert rc == 0, f"Copyright check failed:\n{err[-1000:]}"


# ---------------------------------------------------------------------------
# Phase 6: Coverage
# ---------------------------------------------------------------------------


@pytest.mark.score_baselibs
class TestCoverage:
    """Phase 6: Code coverage must meet minimum threshold."""

    @pytest.mark.build
    def test_coverage_above_threshold(self, baselibs_dir):
        """SWR-BL-060: Line coverage must be at least 80%.

        Runs all tests with Bazel coverage instrumentation and parses the
        combined LCOV report to verify the overall line coverage percentage.
        """
        rc, out, err = _run(
            f"bazel coverage {BAZEL_CONFIG} //score/... "
            "--build_tests_only --combined_report=lcov "
            "--test_tag_filters=-toolchain",
            timeout=3600,
        )
        assert rc == 0, f"Coverage run failed:\n{err[-2000:]}"

        # Locate the combined LCOV report
        lcov_path = BASELIBS_DIR / "bazel-out" / "_coverage" / "_coverage_report.dat"
        if not lcov_path.exists():
            # Fallback: try the testlogs location
            lcov_path = (
                BASELIBS_DIR / "bazel-testlogs" / "coverage_report.dat"
            )

        if not lcov_path.exists():
            pytest.skip(
                "Coverage report not found — verify Bazel coverage output path"
            )

        # Parse LCOV: count LH (lines hit) and LF (lines found)
        total_lines = 0
        hit_lines = 0
        content = lcov_path.read_text()
        for line in content.split("\n"):
            if line.startswith("LF:"):
                total_lines += int(line[3:])
            elif line.startswith("LH:"):
                hit_lines += int(line[3:])

        if total_lines == 0:
            pytest.fail("Coverage report contains no line data")

        coverage_pct = (hit_lines / total_lines) * 100
        threshold = 80.0
        assert coverage_pct >= threshold, (
            f"Line coverage {coverage_pct:.1f}% is below {threshold}% threshold "
            f"({hit_lines}/{total_lines} lines hit)"
        )
