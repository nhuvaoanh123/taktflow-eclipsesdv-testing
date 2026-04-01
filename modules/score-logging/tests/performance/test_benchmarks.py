"""Performance benchmark verification for score-logging (ASIL B).

DLT logging must not block safety-critical callers:
- Log call latency: < 5 µs (non-blocking circular buffer write)
- No lock contention: wait-free logging frontend
- Buffer overflow: graceful drop, no OOM

ISO 26262 Part 6 Table 10: timing analysis required for ASIL B.

Verification method: source inspection + benchmark target verification.
Platform: any (file inspection), Linux (execution).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
LOGGING_DIR = PROJECT_ROOT / "score-logging"
SCORE_DIR = LOGGING_DIR / "score"
MW_LOG = SCORE_DIR / "mw" / "log"


@pytest.mark.asil_b
@pytest.mark.performance
class TestLoggingPerformanceInfrastructure:
    """Verify logging has performance-critical design elements."""

    def test_circular_buffer_exists(self):
        """Logging frontend should use a circular/ring buffer."""
        detail_dir = MW_LOG / "detail"
        if not detail_dir.is_dir():
            pytest.skip("mw/log/detail/ not found")
        content = ""
        for f in detail_dir.rglob("*.h"):
            content += f.read_text(encoding="utf-8", errors="ignore")
        has_ring = any(kw in content.lower() for kw in [
            "circular", "ring", "ringbuffer", "ring_buffer",
        ])
        assert has_ring, (
            "No circular/ring buffer in mw/log/detail/ -- "
            "ASIL B: logging must use bounded non-blocking buffer"
        )

    def test_no_mutex_in_log_frontend(self):
        """Log frontend headers should not use mutex for thread safety."""
        h_files = list(MW_LOG.glob("*.h"))
        if not h_files:
            pytest.skip("No headers in mw/log/")
        mutex_files = []
        for h in h_files:
            content = h.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"\bmutex\b", content, re.IGNORECASE):
                mutex_files.append(h.name)
        assert not mutex_files, (
            f"Mutex found in log frontend headers: {mutex_files} -- "
            "ASIL B: logging must be lock-free to avoid priority inversion"
        )

    def test_wait_free_recorder_pattern(self):
        """Recorder should use wait-free or lock-free patterns."""
        detail_dir = MW_LOG / "detail"
        if not detail_dir.is_dir():
            pytest.skip("mw/log/detail/ not found")
        content = ""
        for f in list(detail_dir.rglob("*.h")) + list(detail_dir.rglob("*.cc")):
            content += f.read_text(encoding="utf-8", errors="ignore")
        has_pattern = any(kw in content.lower() for kw in [
            "atomic", "lock_free", "wait_free", "lockfree",
            "compare_exchange", "fetch_add",
        ])
        assert has_pattern, (
            "No lock-free/atomic patterns in recorder implementation -- "
            "ASIL B: recorder writes must be non-blocking"
        )


@pytest.mark.asil_b
@pytest.mark.performance
class TestBenchmarkTargets:
    """Verify benchmark targets exist in the build system."""

    def test_benchmark_sources_exist(self):
        """Benchmark C++ files should exist."""
        bench_files = (
            list(SCORE_DIR.rglob("*benchmark*.cpp"))
            + list(SCORE_DIR.rglob("*bench*.cpp"))
            + list(SCORE_DIR.rglob("*benchmark*.cc"))
            + list(SCORE_DIR.rglob("*bench*.cc"))
        )
        if not bench_files:
            pytest.xfail(
                "No benchmark source files found -- "
                "ASIL B: logging latency benchmarks recommended"
            )

    def test_datarouter_test_infrastructure(self):
        """DataRouter should have test infrastructure for throughput."""
        dr_dir = SCORE_DIR / "datarouter"
        if not dr_dir.is_dir():
            pytest.skip("datarouter/ not found")
        test_files = list(dr_dir.rglob("*test*"))
        assert len(test_files) >= 1, (
            "No test files in datarouter/ -- throughput testing missing"
        )
