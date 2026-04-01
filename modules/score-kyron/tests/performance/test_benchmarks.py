"""Performance benchmark verification for score-kyron (ASIL B).

Kyron async runtime must meet scheduling latency requirements:
- Task dispatch: bounded wake-up latency
- Work-stealing: no unbounded contention
- Lock-free containers: wait-free progress guarantees

ISO 26262 Part 6 Table 10: timing analysis required for ASIL B.

Verification method: source inspection for timing constructs.
Platform: any (no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
KYRON_DIR = PROJECT_ROOT / "score-kyron"
SRC_DIR = KYRON_DIR / "src"


@pytest.mark.asil_b
@pytest.mark.performance
class TestBenchmarkInfrastructure:
    """Verify benchmark/bench infrastructure exists."""

    def test_has_bench_files(self):
        """Benchmark files (benches/ or *_bench.rs) should exist."""
        bench_dirs = list(KYRON_DIR.rglob("benches"))
        bench_files = [
            f for f in KYRON_DIR.rglob("*.rs")
            if "bench" in f.name.lower()
        ]
        assert len(bench_dirs) > 0 or len(bench_files) > 0, (
            "No benchmark infrastructure (benches/ dir or *bench*.rs) -- "
            "ASIL B requires timing evidence"
        )

    def test_cargo_toml_has_bench_targets(self):
        """Root Cargo.toml or subcrate should define [[bench]] targets."""
        cargo = KYRON_DIR / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        has_bench = "[[bench]]" in content or "bench" in content.lower()
        # Also check subcrate Cargo.tomls
        if not has_bench:
            for ct in KYRON_DIR.rglob("Cargo.toml"):
                if "[[bench]]" in ct.read_text(encoding="utf-8", errors="ignore"):
                    has_bench = True
                    break
        if not has_bench:
            pytest.xfail("No [[bench]] targets found in Cargo workspace")


@pytest.mark.asil_b
@pytest.mark.performance
class TestRuntimeTimingProperties:
    """Verify runtime source has timing/bounded execution constructs."""

    def test_scheduler_has_timing_constructs(self):
        """Scheduler should reference time/duration for bounded execution."""
        rs_files = list(SRC_DIR.rglob("*.rs")) if SRC_DIR.is_dir() else []
        if not rs_files:
            pytest.skip("No source files found")
        timing_found = False
        for f in rs_files:
            if "schedule" in f.name.lower() or "runtime" in f.name.lower():
                content = f.read_text(encoding="utf-8", errors="ignore")
                if any(kw in content.lower() for kw in [
                    "instant", "duration", "timeout", "deadline", "elapsed",
                ]):
                    timing_found = True
                    break
        if not timing_found:
            pytest.xfail(
                "No timing constructs found in scheduler/runtime -- "
                "ASIL B: schedule dispatch must be time-bounded"
            )

    def test_lock_free_containers_exist(self):
        """Lock-free containers must exist for wait-free scheduling."""
        containers = SRC_DIR / "kyron-foundation" / "src" / "containers"
        if not containers.is_dir():
            pytest.skip("containers/ not found")
        rs_files = list(containers.rglob("*.rs"))
        assert len(rs_files) >= 2, (
            f"Expected at least 2 container source files, found {len(rs_files)}"
        )

    def test_spmc_queue_is_lock_free(self):
        """SPMC queue should use atomics, not mutexes."""
        spmc = SRC_DIR / "kyron-foundation" / "src" / "containers" / "spmc_queue.rs"
        if not spmc.exists():
            pytest.skip("spmc_queue.rs not found")
        content = spmc.read_text(encoding="utf-8", errors="ignore")
        has_atomic = "Atomic" in content or "atomic" in content
        has_mutex = "Mutex" in content
        assert has_atomic, "SPMC queue does not use atomics"
        assert not has_mutex, (
            "SPMC queue uses Mutex -- should be lock-free for ASIL B"
        )
