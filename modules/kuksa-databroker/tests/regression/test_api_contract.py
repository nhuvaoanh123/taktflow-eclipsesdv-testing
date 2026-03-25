"""Regression tests for eclipse-kuksa-databroker API contract stability.

Verification methods: API contract verification, file existence.
Platform: any (no build required — file inspection only).

KUKSA.val Databroker v0.6.1-dev implements two API versions:
  - KUKSA.val v1 API: proto/kuksa/val/v1/val.proto (legacy)
  - KUKSA.val v2 API: proto/kuksa/val/v2/val.proto (current)

VSS signals are loaded from JSON files in data/vss-core/ at startup.
Authorization uses JWT tokens (certificates in certificates/).

If expected proto files, VSS data, or source modules are missing,
downstream consumers (providers, apps) will fail to connect.
"""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
DATABROKER_DIR = PROJECT_ROOT / "eclipse-kuksa-databroker"


# ---------------------------------------------------------------------------
# TestWorkspaceIdentity
# ---------------------------------------------------------------------------
class TestWorkspaceIdentity:
    """Verify Cargo workspace identity and structure."""

    def test_cargo_toml_exists(self):
        assert (DATABROKER_DIR / "Cargo.toml").exists(), \
            f"Root Cargo.toml not found at {DATABROKER_DIR}"

    def test_cargo_lock_exists(self):
        assert (DATABROKER_DIR / "Cargo.lock").exists(), \
            "Cargo.lock not found — dependencies not reproducibly locked"

    def test_workspace_members_declared(self):
        content = (DATABROKER_DIR / "Cargo.toml").read_text(encoding="utf-8")
        assert "[workspace]" in content, "No [workspace] section in root Cargo.toml"
        assert "members" in content, "Workspace does not declare members"

    @pytest.mark.parametrize("member", ["databroker", "databroker-proto", "databroker-cli"])
    def test_workspace_member_exists(self, member):
        assert (DATABROKER_DIR / member).is_dir(), \
            f"Workspace member {member}/ missing"

    def test_databroker_version(self):
        """Verify databroker version is as expected."""
        cargo = DATABROKER_DIR / "databroker" / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("databroker/Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        assert "0.6" in content, \
            "Expected databroker version 0.6.x — version may have changed"


# ---------------------------------------------------------------------------
# TestProtoFiles
# ---------------------------------------------------------------------------
class TestProtoFiles:
    """Verify KUKSA.val v1 and v2 protobuf definitions."""

    PROTO_DIR = DATABROKER_DIR / "proto"

    def test_proto_directory_exists(self):
        assert self.PROTO_DIR.is_dir(), \
            "proto/ directory missing — API definitions removed"

    @pytest.mark.parametrize("proto_path", [
        "kuksa/val/v1/val.proto",
        "kuksa/val/v2/val.proto",
        "kuksa/val/v2/types.proto",
    ])
    def test_proto_file_exists(self, proto_path):
        """Required .proto files must exist for API consumers."""
        path = self.PROTO_DIR / proto_path
        assert path.exists(), \
            f"proto/{proto_path} missing — API contract broken"

    def test_v2_val_proto_has_databroker_service(self):
        """v2/val.proto must define a VAL (Vehicle Abstraction Layer) service."""
        path = self.PROTO_DIR / "kuksa" / "val" / "v2" / "val.proto"
        if not path.exists():
            pytest.skip("v2/val.proto not found")
        content = path.read_text(encoding="utf-8")
        assert "service" in content.lower() or "rpc" in content.lower(), \
            "v2/val.proto has no service/RPC definitions — API removed"

    def test_v2_types_proto_has_datapoint(self):
        """v2/types.proto must define Datapoint message for signal values."""
        path = self.PROTO_DIR / "kuksa" / "val" / "v2" / "types.proto"
        if not path.exists():
            pytest.skip("v2/types.proto not found")
        content = path.read_text(encoding="utf-8")
        assert "Datapoint" in content or "datapoint" in content.lower(), \
            "types.proto has no Datapoint definition"


# ---------------------------------------------------------------------------
# TestVSSData
# ---------------------------------------------------------------------------
class TestVSSData:
    """Verify VSS signal data files for databroker startup."""

    DATA_DIR = DATABROKER_DIR / "data" / "vss-core"

    def test_vss_core_directory_exists(self):
        assert self.DATA_DIR.is_dir(), \
            "data/vss-core/ missing — VSS signal data removed"

    def test_vss_release_json_exists(self):
        """At least one VSS release JSON file must exist for startup."""
        json_files = list(self.DATA_DIR.glob("*.json"))
        assert len(json_files) >= 1, \
            f"No VSS JSON files in data/vss-core/ — startup data missing"

    def test_vss_4_0_release_available(self):
        """VSS 4.0 release must be available (referenced in KUKSA docs)."""
        path = self.DATA_DIR / "vss_release_4.0.json"
        assert path.exists(), \
            "data/vss-core/vss_release_4.0.json missing — VSS 4.0 data removed"

    def test_vss_json_has_vehicle_speed(self):
        """VSS JSON must contain Vehicle.Speed as a fundamental signal."""
        import json
        path = self.DATA_DIR / "vss_release_4.0.json"
        if not path.exists():
            # Try any available JSON
            jsons = list(self.DATA_DIR.glob("*.json"))
            if not jsons:
                pytest.skip("No VSS JSON found")
            path = jsons[0]
        data = json.loads(path.read_text(encoding="utf-8"))
        # VSS JSON has a nested tree structure
        content_str = path.read_text(encoding="utf-8")
        assert "Speed" in content_str or "speed" in content_str, \
            "VSS JSON does not contain 'Speed' signal — fundamental VSS signal missing"


# ---------------------------------------------------------------------------
# TestDatabrokerSource
# ---------------------------------------------------------------------------
class TestDatabrokerSource:
    """Verify core databroker Rust source structure."""

    SRC = DATABROKER_DIR / "databroker" / "src"

    def test_src_directory_exists(self):
        assert self.SRC.is_dir(), \
            "databroker/src/ missing — broker implementation removed"

    @pytest.mark.parametrize("source_file", [
        "lib.rs",
        "main.rs",
        "broker.rs",
        "types.rs",
        "vss.rs",
    ])
    def test_key_source_file_exists(self, source_file):
        """Key source files must exist."""
        path = self.SRC / source_file
        assert path.exists(), \
            f"databroker/src/{source_file} missing — broker module removed"

    @pytest.mark.parametrize("subdir", [
        "grpc",
        "authorization",
        "filter",
        "query",
        "viss",
    ])
    def test_key_submodule_exists(self, subdir):
        """Key broker sub-modules must exist."""
        path = self.SRC / subdir
        assert path.is_dir(), \
            f"databroker/src/{subdir}/ missing — broker module removed"

    def test_rust_source_count(self):
        rs_files = list(self.SRC.rglob("*.rs"))
        assert len(rs_files) >= 10, \
            f"Expected at least 10 Rust sources in databroker/src/, found {len(rs_files)}"

    def test_build_rs_exists(self):
        """build.rs triggers proto compilation via tonic-build."""
        path = DATABROKER_DIR / "databroker" / "build.rs"
        assert path.exists(), \
            "databroker/build.rs missing — proto compilation step removed"


# ---------------------------------------------------------------------------
# TestCertificates
# ---------------------------------------------------------------------------
class TestCertificates:
    """Verify TLS certificate files for secure gRPC connections."""

    CERT_DIR = DATABROKER_DIR / "certificates"

    def test_certificates_directory_exists(self):
        assert self.CERT_DIR.is_dir(), \
            "certificates/ missing — TLS configuration removed"

    def test_certificates_readme_exists(self):
        readme = self.CERT_DIR / "README.md"
        assert readme.exists(), \
            "certificates/README.md missing — TLS usage documentation removed"


# ---------------------------------------------------------------------------
# TestIntegrationTestInfrastructure
# ---------------------------------------------------------------------------
class TestIntegrationTestInfrastructure:
    """Verify Python integration test infrastructure."""

    INT_TEST = DATABROKER_DIR / "integration_test"

    def test_integration_test_dir_exists(self):
        assert self.INT_TEST.is_dir(), \
            "integration_test/ directory missing"

    def test_test_databroker_script_exists(self):
        assert (self.INT_TEST / "test_databroker.py").exists(), \
            "integration_test/test_databroker.py missing — integration test removed"

    def test_provider_script_exists(self):
        """provider.py feeds test signals into the broker."""
        assert (self.INT_TEST / "provider.py").exists(), \
            "integration_test/provider.py missing — signal provider helper removed"

    def test_requirements_defined(self):
        assert (self.INT_TEST / "requirements.txt").exists(), \
            "integration_test/requirements.txt missing"

    def test_requirements_dev_defined(self):
        assert (self.INT_TEST / "requirements-dev.txt").exists(), \
            "integration_test/requirements-dev.txt missing"
