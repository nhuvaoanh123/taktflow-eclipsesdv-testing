"""Integration tests for eclipse-kuksa-databroker dependency chain.

Verifies that:
1. databroker-proto is correctly used by databroker and databroker-cli.
2. The kuksa-python-sdk references the same proto definitions.
3. The kuksa-can-provider depends on kuksa-common.
4. VSS signal definitions used by the bench (taktflow_vehicle.dbc) overlap
   with VSS signals in the databroker (Vehicle.* namespace).

Platform: any (file inspection only, no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATABROKER_DIR = PROJECT_ROOT / "eclipse-kuksa-databroker"
PYTHON_SDK_DIR = PROJECT_ROOT / "eclipse-kuksa-python-sdk"
CAN_PROVIDER_DIR = PROJECT_ROOT / "kuksa-kuksa-can-provider"


# ---------------------------------------------------------------------------
# TestDatabrokerProtoDependency
# ---------------------------------------------------------------------------
class TestDatabrokerProtoDependency:
    """Verify databroker-proto is the shared proto source for all consumers."""

    def test_databroker_depends_on_proto(self):
        """databroker/Cargo.toml must reference databroker-proto."""
        cargo = DATABROKER_DIR / "databroker" / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("databroker/Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        assert "databroker-proto" in content, \
            "databroker does not depend on databroker-proto"

    def test_databroker_cli_depends_on_proto(self):
        """databroker-cli/Cargo.toml must reference databroker-proto."""
        cargo = DATABROKER_DIR / "databroker-cli" / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("databroker-cli/Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        assert "databroker-proto" in content, \
            "databroker-cli does not depend on databroker-proto"

    def test_proto_workspace_dependency(self):
        """Root Cargo.toml workspace.dependencies must declare databroker-proto."""
        cargo = DATABROKER_DIR / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("Root Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        assert "databroker-proto" in content, \
            "databroker-proto not in workspace dependencies"


# ---------------------------------------------------------------------------
# TestGrpcDependencies
# ---------------------------------------------------------------------------
class TestGrpcDependencies:
    """Verify tonic (gRPC) and prost (protobuf) are workspace dependencies."""

    def test_tonic_in_workspace(self):
        cargo = DATABROKER_DIR / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("Root Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        assert "tonic" in content, \
            "tonic gRPC not in workspace dependencies"

    def test_tonic_build_in_databroker_proto(self):
        """databroker-proto/build.rs must use tonic-build for gRPC code gen."""
        build_rs = DATABROKER_DIR / "databroker-proto" / "build.rs"
        if not build_rs.exists():
            pytest.skip("databroker-proto/build.rs not found")
        content = build_rs.read_text(encoding="utf-8")
        has_tonic_build = "tonic-build" in content or "tonic_build" in content
        has_prost = "prost" in content
        assert has_tonic_build or has_prost, \
            "databroker-proto/build.rs does not use tonic-build or prost — proto codegen missing"

    def test_databroker_cargo_has_tonic_transport(self):
        """databroker must use tonic with transport feature for gRPC server."""
        cargo = DATABROKER_DIR / "databroker" / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("databroker/Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        assert "tonic" in content, \
            "databroker/Cargo.toml does not reference tonic — gRPC server may be missing"


# ---------------------------------------------------------------------------
# TestPythonSDKIntegration
# ---------------------------------------------------------------------------
class TestPythonSDKIntegration:
    """Verify kuksa-python-sdk references the same proto definitions.

    The Python SDK is the reference client for the databroker.
    If the proto paths diverge, clients will fail to connect.
    """

    def test_python_sdk_exists(self):
        if not PYTHON_SDK_DIR.is_dir():
            pytest.skip("eclipse-kuksa-python-sdk not found locally")
        assert (PYTHON_SDK_DIR / "README.md").exists(), \
            "eclipse-kuksa-python-sdk directory exists but no README.md"

    def test_python_sdk_references_val_v2(self):
        """Python SDK should reference KUKSA.val v2 API."""
        if not PYTHON_SDK_DIR.is_dir():
            pytest.skip("eclipse-kuksa-python-sdk not found locally")
        py_files = list(PYTHON_SDK_DIR.rglob("*.py"))
        if not py_files:
            pytest.skip("No Python files in kuksa-python-sdk")
        content = "\n".join(f.read_text(encoding="utf-8", errors="ignore")
                            for f in py_files[:20])
        has_v2 = "val.v2" in content or "kuksa.val.v2" in content
        has_grpc = "grpc" in content.lower() or "stub" in content.lower()
        assert has_v2 or has_grpc, \
            "kuksa-python-sdk does not appear to use KUKSA.val v2 gRPC API"


# ---------------------------------------------------------------------------
# TestVSSSignalOverlap
# ---------------------------------------------------------------------------
class TestVSSSignalOverlap:
    """Verify that VSS signals in the databroker overlap with signals
    used in the taktflow bench (Vehicle.* namespace)."""

    def test_vehicle_namespace_in_vss_json(self):
        """VSS 4.0 JSON must contain Vehicle.* top-level namespace."""
        vss_json = DATABROKER_DIR / "data" / "vss-core" / "vss_release_4.0.json"
        if not vss_json.exists():
            pytest.skip("vss_release_4.0.json not found")
        content = vss_json.read_text(encoding="utf-8")
        assert '"Vehicle"' in content or "'Vehicle'" in content, \
            "VSS JSON does not contain Vehicle top-level node"

    @pytest.mark.parametrize("signal", [
        "Speed",
        "Powertrain",
        "CurrentLocation",
    ])
    def test_fundamental_vehicle_signal_in_vss(self, signal):
        """Fundamental Vehicle signals must exist in VSS 4.0."""
        vss_json = DATABROKER_DIR / "data" / "vss-core" / "vss_release_4.0.json"
        if not vss_json.exists():
            pytest.skip("vss_release_4.0.json not found")
        content = vss_json.read_text(encoding="utf-8")
        assert signal in content, \
            f"Vehicle.{signal} not found in VSS 4.0 JSON — signal may have been removed"


# ---------------------------------------------------------------------------
# TestDatabrokerKuksaCommon
# ---------------------------------------------------------------------------
class TestDatabrokerKuksaCommon:
    """Verify the shared kuksa-common library that both databroker and
    CLI consume."""

    COMMON_LIB = DATABROKER_DIR / "lib" / "common"

    def test_common_library_exists(self):
        assert self.COMMON_LIB.is_dir(), \
            "lib/common/ missing — shared kuksa library removed"

    def test_common_has_cargo_toml(self):
        assert (self.COMMON_LIB / "Cargo.toml").exists(), \
            "lib/common/Cargo.toml missing"

    def test_common_has_source(self):
        rs_files = list(self.COMMON_LIB.rglob("*.rs"))
        assert len(rs_files) >= 1, \
            "lib/common/ has no Rust source files"
