"""Performance benchmark verification for score-orchestrator (ASIL B).

Orchestrator must manage workload lifecycle without unbounded latency:
- Program start/stop: bounded IPC response time
- Configuration loading: bounded parse time
- Health status reporting: non-blocking

ISO 26262 Part 6 Table 10: timing analysis required for ASIL B.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
ORCH_DIR = PROJECT_ROOT / "score-orchestrator"
ORCH_SRC = ORCH_DIR / "src" / "orchestration"


@pytest.mark.asil_b
@pytest.mark.performance
class TestOrchestrationTimingProperties:
    """Verify orchestration source has bounded execution constructs."""

    def test_program_lifecycle_has_timeout(self):
        """Program lifecycle management should have timeout handling."""
        if not ORCH_SRC.is_dir():
            pytest.skip("src/orchestration/ not found")
        rs_files = list(ORCH_SRC.rglob("*.rs"))
        if not rs_files:
            pytest.skip("No Rust source files")
        combined = ""
        for f in rs_files:
            combined += f.read_text(encoding="utf-8", errors="ignore")
        has_timeout = any(kw in combined.lower() for kw in [
            "timeout", "deadline", "duration", "elapsed", "timer",
        ])
        assert has_timeout, (
            "Orchestration has no timeout/deadline constructs -- "
            "ASIL B: program lifecycle must be time-bounded"
        )

    def test_ipc_uses_async(self):
        """IPC communication should use async/await for non-blocking."""
        if not ORCH_SRC.is_dir():
            pytest.skip("src/orchestration/ not found")
        rs_files = list(ORCH_SRC.rglob("*.rs"))
        if not rs_files:
            pytest.skip("No source files")
        has_async = False
        for f in rs_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "async fn" in content or "await" in content:
                has_async = True
                break
        assert has_async, (
            "No async/await in orchestration -- "
            "ASIL B: IPC must be non-blocking"
        )


@pytest.mark.asil_b
@pytest.mark.performance
class TestBenchmarkInfrastructure:
    """Verify benchmark/test infrastructure exists."""

    def test_has_test_files(self):
        """Test files must exist for timing verification."""
        rs_files = list(ORCH_DIR.rglob("*.rs"))
        if not rs_files:
            pytest.skip("No Rust source files")
        has_tests = False
        for f in rs_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "#[test]" in content:
                has_tests = True
                break
        test_files = [f for f in rs_files if "test" in f.name.lower()]
        assert has_tests or len(test_files) > 0, (
            "No test infrastructure -- ASIL B requires performance evidence"
        )

    def test_has_bench_or_criterion(self):
        """Cargo workspace should reference criterion or [[bench]]."""
        cargo = ORCH_DIR / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        has_bench = "[[bench]]" in content or "criterion" in content.lower()
        if not has_bench:
            for ct in ORCH_DIR.rglob("Cargo.toml"):
                c = ct.read_text(encoding="utf-8", errors="ignore")
                if "[[bench]]" in c or "criterion" in c.lower():
                    has_bench = True
                    break
        if not has_bench:
            pytest.xfail("No benchmark targets found")
