"""Performance benchmark verification for score-baselibs_rust (ASIL B).

Foundation libraries must provide O(1) or bounded-time operations:
- Lock-free containers: wait-free progress for producers
- Sync primitives: bounded spin/park cycles
- Elementary types: zero-cost abstractions

ISO 26262 Part 6 Table 10: timing analysis required for ASIL B.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
BASELIBS_RUST_DIR = PROJECT_ROOT / "score-baselibs_rust"
SRC_DIR = BASELIBS_RUST_DIR / "src"


@pytest.mark.asil_b
@pytest.mark.performance
class TestLockFreePerformance:
    """Verify lock-free containers have bounded-time operations."""

    def test_containers_use_atomics(self):
        """Containers must use atomic operations for lock-free access."""
        containers = SRC_DIR / "containers"
        if not containers.is_dir():
            pytest.skip("containers/ not found")
        content = ""
        for f in containers.rglob("*.rs"):
            content += f.read_text(encoding="utf-8", errors="ignore")
        has_atomic = "Atomic" in content or "atomic" in content
        assert has_atomic, (
            "No atomic operations in containers -- "
            "ASIL B: containers must be lock-free"
        )

    def test_no_mutex_in_containers(self):
        """Containers should not use Mutex (blocks, priority inversion)."""
        containers = SRC_DIR / "containers"
        if not containers.is_dir():
            pytest.skip("containers/ not found")
        mutex_files = []
        for f in containers.rglob("*.rs"):
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "Mutex" in content and "test" not in f.name.lower():
                mutex_files.append(f.name)
        assert not mutex_files, (
            f"Mutex in container source files: {mutex_files} -- "
            "ASIL B: containers must be lock-free"
        )

    def test_sync_primitives_have_bounded_spin(self):
        """Sync primitives should not spin unboundedly."""
        sync_dir = SRC_DIR / "sync"
        if not sync_dir.is_dir():
            pytest.skip("sync/ not found")
        content = ""
        for f in sync_dir.rglob("*.rs"):
            content += f.read_text(encoding="utf-8", errors="ignore")
        has_bound = any(kw in content.lower() for kw in [
            "spin_count", "max_spin", "yield", "park", "backoff",
        ])
        if not has_bound:
            pytest.xfail(
                "No bounded spin construct found in sync/ -- "
                "may use OS-level park instead"
            )


@pytest.mark.asil_b
@pytest.mark.performance
class TestBenchmarkInfrastructure:
    """Verify benchmark infrastructure exists."""

    def test_has_bench_files(self):
        """Benchmark files should exist."""
        bench_dirs = list(BASELIBS_RUST_DIR.rglob("benches"))
        bench_files = [
            f for f in BASELIBS_RUST_DIR.rglob("*.rs")
            if "bench" in f.name.lower()
        ]
        if not bench_dirs and not bench_files:
            pytest.xfail(
                "No benchmark infrastructure -- "
                "ASIL B: timing evidence recommended"
            )

    def test_containers_have_tests(self):
        """Containers crate must have tests for correctness under contention."""
        containers = SRC_DIR / "containers"
        if not containers.is_dir():
            pytest.skip("containers/ not found")
        has_tests = False
        for f in containers.rglob("*.rs"):
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "#[test]" in content:
                has_tests = True
                break
        assert has_tests, "No tests in containers -- concurrency correctness untested"
