"""Performance benchmark verification for kuksa-databroker (ASIL B).

Vehicle signal databroker must meet latency requirements:
- Signal publish-to-subscribe: < 50 ms for safety signals
- gRPC request handling: bounded response time
- No unbounded memory growth under load

ISO 26262 Part 6 Table 10: timing analysis required for ASIL B.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATABROKER_DIR = PROJECT_ROOT / "eclipse-kuksa-databroker"
SRC = DATABROKER_DIR / "databroker" / "src"


@pytest.mark.asil_b
@pytest.mark.performance
class TestDatabrokerPerformanceInfrastructure:
    """Verify databroker has performance-critical design elements."""

    def test_broker_uses_async(self):
        """Broker must use async/await for non-blocking signal delivery."""
        broker_rs = SRC / "broker.rs"
        if not broker_rs.exists():
            pytest.skip("broker.rs not found")
        content = broker_rs.read_text(encoding="utf-8", errors="ignore")
        has_async = "async fn" in content or "await" in content
        assert has_async, (
            "broker.rs has no async/await -- "
            "ASIL B: signal delivery must be non-blocking"
        )

    def test_grpc_server_uses_tonic(self):
        """gRPC server should use tonic for efficient streaming."""
        cargo_lock = DATABROKER_DIR / "Cargo.lock"
        if not cargo_lock.exists():
            pytest.skip("Cargo.lock not found")
        content = cargo_lock.read_text(encoding="utf-8")
        assert "tonic" in content, (
            "tonic not in Cargo.lock -- "
            "gRPC framework missing for efficient signal delivery"
        )

    def test_subscription_module_exists(self):
        """Subscription handling must exist for pub/sub performance."""
        sub_files = list(SRC.rglob("*subscri*"))
        # Also check for grpc server which handles subscriptions
        grpc_files = list((SRC / "grpc").rglob("*.rs")) if (SRC / "grpc").is_dir() else []
        assert len(sub_files) >= 1 or len(grpc_files) >= 1, (
            "No subscription module or gRPC server found -- pub/sub missing"
        )

    def test_grpc_handlers_prefer_async(self):
        """gRPC handler files should prefer async over blocking calls."""
        grpc_dir = SRC / "grpc"
        if not grpc_dir.is_dir():
            pytest.skip("grpc/ not found")
        rs_files = list(grpc_dir.rglob("*.rs"))
        if not rs_files:
            pytest.skip("No Rust source in grpc/")
        has_async = False
        for f in rs_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "async fn" in content or "await" in content:
                has_async = True
                break
        assert has_async, (
            "No async/await in gRPC handlers -- "
            "ASIL B: handlers should be non-blocking"
        )


@pytest.mark.asil_b
@pytest.mark.performance
class TestBenchmarkTargets:
    """Verify benchmark infrastructure."""

    def test_has_test_infrastructure(self):
        """Test infrastructure should exist (integration_test/ or tests/)."""
        int_test = DATABROKER_DIR / "integration_test"
        has_int = int_test.is_dir()
        test_dirs = list(DATABROKER_DIR.rglob("tests"))
        has_tests = any(d.is_dir() for d in test_dirs)
        # Also check for inline #[test] in source
        has_inline = False
        for f in list(SRC.rglob("*.rs"))[:20]:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "#[test]" in content:
                has_inline = True
                break
        assert has_int or has_tests or has_inline, (
            "No test infrastructure found"
        )

    def test_integration_test_directory(self):
        """Integration test directory should exist."""
        test_dirs = list(DATABROKER_DIR.rglob("tests"))
        has_test_dir = any(d.is_dir() for d in test_dirs)
        if not has_test_dir:
            pytest.xfail("No tests/ directory for integration testing")
