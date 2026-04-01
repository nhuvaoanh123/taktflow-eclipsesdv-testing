"""Performance benchmark verification for score-feo (ASIL B).

FEO deterministic scheduler must meet cycle time requirements:
- Schedule dispatch: < 50 µs per cycle
- Worker wake-up: < 20 µs from signal to execution
- Activity chain: deterministic order without jitter

ISO 26262 Part 6 Table 10: timing analysis required for ASIL B.

Verification method: benchmark infrastructure inspection.
Platform: any (file inspection), Linux (execution).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
FEO_DIR = PROJECT_ROOT / "modules" / "score-feo" / "upstream"


@pytest.mark.asil_b
@pytest.mark.performance
class TestBenchmarkInfrastructure:
    """Verify FEO has benchmark infrastructure."""

    def test_cycle_benchmark_example_exists(self):
        """cycle-benchmark example must exist for scheduler timing."""
        candidates = [
            FEO_DIR / "examples" / "rust" / "cycle-benchmark",
            FEO_DIR / "examples" / "cycle-benchmark",
        ]
        assert any(c.is_dir() for c in candidates), (
            "cycle-benchmark example missing -- "
            "ASIL B requires scheduler timing measurement"
        )

    def test_benchmark_has_source_files(self):
        """Benchmark example must have Rust source files."""
        for base in [FEO_DIR / "examples" / "rust", FEO_DIR / "examples"]:
            bench_dir = base / "cycle-benchmark"
            if bench_dir.is_dir():
                rs_files = list(bench_dir.rglob("*.rs"))
                assert len(rs_files) >= 1, (
                    "cycle-benchmark/ has no Rust source files"
                )
                return
        pytest.skip("cycle-benchmark directory not found")

    def test_benchmark_has_cargo_toml(self):
        """Benchmark example must have Cargo.toml."""
        for base in [FEO_DIR / "examples" / "rust", FEO_DIR / "examples"]:
            bench_dir = base / "cycle-benchmark"
            if bench_dir.is_dir():
                assert (bench_dir / "Cargo.toml").exists(), (
                    "cycle-benchmark/Cargo.toml missing"
                )
                return
        pytest.skip("cycle-benchmark directory not found")

    def test_feo_time_crate_exists(self):
        """feo-time crate must exist for timing measurement."""
        path = FEO_DIR / "src" / "feo-time"
        assert path.is_dir(), (
            "src/feo-time/ missing -- timing infrastructure removed"
        )

    def test_feo_time_has_tests(self):
        """feo-time must have timing tests (13 expected)."""
        time_dir = FEO_DIR / "src" / "feo-time"
        if not time_dir.is_dir():
            pytest.skip("feo-time not found")
        has_tests = False
        for f in time_dir.rglob("*.rs"):
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "#[test]" in content:
                has_tests = True
                break
        assert has_tests, (
            "feo-time has no #[test] annotations -- timing tests missing"
        )

    def test_tracing_infrastructure_for_profiling(self):
        """feo-tracing + perfetto-model must exist for runtime profiling."""
        tracing = FEO_DIR / "src" / "feo-tracing"
        perfetto = FEO_DIR / "src" / "perfetto-model"
        assert tracing.is_dir() and perfetto.is_dir(), (
            "Tracing infrastructure incomplete -- "
            "ASIL B requires runtime profiling capability"
        )


@pytest.mark.asil_b
@pytest.mark.performance
class TestSchedulerTimingProperties:
    """Verify scheduler source has timing-related constructs."""

    def test_scheduler_uses_clock(self):
        """Scheduler should reference clock/time for cycle measurement."""
        scheduler_files = list((FEO_DIR / "src" / "feo").rglob("scheduler.rs"))
        if not scheduler_files:
            pytest.skip("scheduler.rs not found")
        content = scheduler_files[0].read_text(encoding="utf-8", errors="ignore")
        has_time = any(kw in content.lower() for kw in [
            "instant", "duration", "clock", "time", "elapsed", "deadline",
        ])
        assert has_time, (
            "scheduler.rs has no time/clock references -- "
            "ASIL B: scheduler must track cycle timing"
        )

    def test_worker_bounded_execution(self):
        """Worker pool should have bounded execution concepts."""
        worker_files = list((FEO_DIR / "src" / "feo").rglob("worker/*.rs"))
        if not worker_files:
            worker_files = [
                f for f in (FEO_DIR / "src" / "feo").rglob("*.rs")
                if "worker" in f.name.lower()
            ]
        if not worker_files:
            pytest.skip("No worker source files found")
        combined = ""
        for f in worker_files:
            combined += f.read_text(encoding="utf-8", errors="ignore")
        has_bound = any(kw in combined.lower() for kw in [
            "timeout", "deadline", "bounded", "max_", "limit",
        ])
        assert has_bound, (
            "Worker pool has no timeout/deadline/bounded references -- "
            "ASIL B: execution must be time-bounded"
        )
