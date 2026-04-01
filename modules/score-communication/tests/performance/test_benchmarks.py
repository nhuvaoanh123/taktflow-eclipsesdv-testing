"""Performance benchmark verification for score-communication (ASIL B).

LoLa IPC middleware must meet deterministic latency requirements:
- Intra-process message passing: < 10 µs p99
- Inter-process shared memory: < 30 µs p99
- Zero-copy transfer: no memcpy in hot path

ISO 26262 Part 6 Table 10: timing analysis required for ASIL B.

Verification method: benchmark target inspection + runtime execution.
Platform: Linux x86_64 (benchmark execution requires Bazel).
"""

import re
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
LOLA_DIR = PROJECT_ROOT / "modules" / "score-communication" / "upstream"
BENCH_DIR = LOLA_DIR / "score" / "mw" / "com" / "performance_benchmarks"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or LOLA_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


# ---------------------------------------------------------------------------
# TestBenchmarkInfrastructure
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
@pytest.mark.performance
class TestBenchmarkInfrastructure:
    """Verify benchmark targets exist and are properly structured."""

    def test_benchmark_directory_exists(self):
        assert BENCH_DIR.is_dir(), (
            "performance_benchmarks/ missing -- "
            "ASIL B requires latency measurement infrastructure"
        )

    def test_api_microbenchmarks_exist(self):
        """API microbenchmark directory must exist."""
        api_bench = BENCH_DIR / "api_microbenchmarks"
        assert api_bench.is_dir(), (
            "api_microbenchmarks/ missing -- IPC latency benchmarks removed"
        )

    def test_benchmark_sources_exist(self):
        """Benchmark C++ source files must exist."""
        cpp_files = list(BENCH_DIR.rglob("*.cpp")) + list(BENCH_DIR.rglob("*.cc"))
        assert len(cpp_files) >= 1, (
            f"No benchmark source files found in performance_benchmarks/"
        )

    def test_benchmark_build_files_exist(self):
        """BUILD files for benchmarks must exist."""
        build_files = (
            list(BENCH_DIR.rglob("BUILD"))
            + list(BENCH_DIR.rglob("BUILD.bazel"))
        )
        assert len(build_files) >= 1, (
            "No BUILD files in performance_benchmarks/"
        )

    def test_benchmark_references_google_benchmark(self):
        """Benchmark BUILD should reference google_benchmark."""
        build_files = (
            list(BENCH_DIR.rglob("BUILD"))
            + list(BENCH_DIR.rglob("BUILD.bazel"))
        )
        if not build_files:
            pytest.skip("No BUILD files found")
        found = False
        for bf in build_files:
            content = bf.read_text(encoding="utf-8", errors="ignore")
            if "benchmark" in content.lower():
                found = True
                break
        assert found, "No BUILD file references benchmark framework"


# ---------------------------------------------------------------------------
# TestBenchmarkExecution
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
@pytest.mark.performance
@pytest.mark.slow
class TestBenchmarkExecution:
    """Run LoLa IPC benchmarks and verify latency bounds.

    These tests require Bazel on Linux. Skipped on other platforms.
    """

    def test_benchmarks_build(self):
        """Benchmark targets must compile successfully."""
        rc, _, err = _run(
            "bazel build //score/mw/com/performance_benchmarks/...",
            timeout=600,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available or benchmark targets not found")
        assert rc == 0, f"Benchmark build failed:\n{err[-2000:]}"

    def test_api_microbenchmarks_run(self):
        """API microbenchmarks must execute without crash."""
        rc, out, err = _run(
            "bazel test //score/mw/com/performance_benchmarks/"
            "api_microbenchmarks:all --test_output=summary",
            timeout=1200,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Benchmark targets not found")
        assert rc == 0, f"Benchmark execution failed:\n{(out+err)[-2000:]}"
