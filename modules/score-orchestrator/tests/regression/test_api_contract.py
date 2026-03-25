"""Regression tests for score-orchestrator API contract stability.

Verification methods: API contract verification, file existence.
Platform: any (no build required — file inspection only).

score-orchestrator provides a Rust workload orchestration framework.
Public API surface:

  Rust  : src/orchestration/src/  (programs, actions, events, api/, core/)
  Macros: src/orchestration_macros/ (proc-macro crate, proc-macro = true)
  CIT   : tests/test_scenarios/rust/ (component integration test scenarios)

If expected crates, source files, or workspace members are missing,
upstream may have broken backwards compatibility.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
ORCH_DIR = PROJECT_ROOT / "score-orchestrator"


# ---------------------------------------------------------------------------
# TestModuleIdentity
# ---------------------------------------------------------------------------
class TestModuleIdentity:
    """Verify MODULE.bazel and Cargo.toml identity."""

    def test_module_bazel_exists(self):
        assert (ORCH_DIR / "MODULE.bazel").exists(), \
            f"MODULE.bazel not found at {ORCH_DIR}"

    def test_module_name_is_score_orchestrator(self):
        content = (ORCH_DIR / "MODULE.bazel").read_text(encoding="utf-8")
        assert 'name = "score_orchestrator"' in content, \
            "Expected module name 'score_orchestrator' in MODULE.bazel"

    def test_cargo_workspace_version(self):
        """Workspace package version must be 0.0.3."""
        path = ORCH_DIR / "Cargo.toml"
        if not path.exists():
            pytest.skip("Cargo.toml not found")
        content = path.read_text(encoding="utf-8")
        assert 'version = "0.0.3"' in content, \
            "Expected workspace.package.version = '0.0.3' in Cargo.toml"

    def test_rust_toolchain_pinned(self):
        """Rust toolchain must be pinned to 1.85.0 via rust-toolchain.toml."""
        path = ORCH_DIR / "rust-toolchain.toml"
        if not path.exists():
            pytest.skip("rust-toolchain.toml not found")
        content = path.read_text(encoding="utf-8")
        assert "1.85" in content, \
            "Expected Rust 1.85.x pinned in rust-toolchain.toml"

    def test_bazel_version_is_8_3_0(self):
        path = ORCH_DIR / ".bazelversion"
        if not path.exists():
            pytest.skip(".bazelversion not found")
        assert path.read_text().strip() == "8.3.0", \
            "Expected Bazel 8.3.0 pinned in .bazelversion"


# ---------------------------------------------------------------------------
# TestCargoWorkspace
# ---------------------------------------------------------------------------
class TestCargoWorkspace:
    """Verify Cargo workspace structure with expected members."""

    def test_root_cargo_toml_exists(self):
        assert (ORCH_DIR / "Cargo.toml").exists(), \
            "Root Cargo.toml missing — Rust workspace removed"

    def test_cargo_lock_exists(self):
        assert (ORCH_DIR / "Cargo.lock").exists(), \
            "Cargo.lock not found — dependencies not locked"

    def test_workspace_defines_members(self):
        content = (ORCH_DIR / "Cargo.toml").read_text(encoding="utf-8")
        assert "[workspace]" in content, "Root Cargo.toml missing [workspace]"
        assert "members" in content, "Workspace does not declare members"

    @pytest.mark.parametrize("member_path", [
        "src/orchestration",
        "src/orchestration_macros",
        "src/xtask",
    ])
    def test_workspace_member_exists(self, member_path):
        """Required workspace members must exist as directories."""
        path = ORCH_DIR / member_path
        assert path.is_dir(), \
            f"Workspace member {member_path}/ missing — crate removed"

    def test_tests_test_scenarios_rust_exists(self):
        """Component integration tests directory must be present."""
        path = ORCH_DIR / "tests" / "test_scenarios" / "rust"
        assert path.is_dir(), \
            "tests/test_scenarios/rust/ missing — CIT harness removed"


# ---------------------------------------------------------------------------
# TestOrchestrationCrate
# ---------------------------------------------------------------------------
class TestOrchestrationCrate:
    """Verify core orchestration library structure."""

    ORCH_SRC = ORCH_DIR / "src" / "orchestration"

    def test_cargo_toml_exists(self):
        assert (self.ORCH_SRC / "Cargo.toml").exists(), \
            "src/orchestration/Cargo.toml missing"

    @pytest.mark.parametrize("subdir", [
        "actions",
        "api",
        "common",
        "core",
        "events",
        "testing",
    ])
    def test_key_subdir_exists(self, subdir):
        """Key architectural components must exist as directories."""
        candidates = [
            self.ORCH_SRC / "src" / subdir,
            self.ORCH_SRC / subdir,
        ]
        found = any(c.is_dir() for c in candidates)
        if not found:
            matches = [d for d in self.ORCH_SRC.rglob(subdir) if d.is_dir()]
            found = len(matches) > 0
        assert found, \
            f"src/orchestration/{subdir}/ missing — component removed"

    @pytest.mark.parametrize("source_file", [
        "lib.rs",
        "program.rs",
        "program_database.rs",
        "prelude.rs",
    ])
    def test_key_source_file_exists(self, source_file):
        """Key source files must exist in the orchestration crate."""
        path = self.ORCH_SRC / "src" / source_file
        if not path.exists():
            path = self.ORCH_SRC / source_file
        assert path.exists(), \
            f"{source_file} not found in src/orchestration/ — API may have regressed"

    def test_rust_source_count(self):
        rs_files = list(self.ORCH_SRC.rglob("*.rs"))
        assert len(rs_files) >= 10, \
            f"Expected at least 10 Rust source files in src/orchestration/, found {len(rs_files)}"

    def test_examples_directory_exists(self):
        assert (self.ORCH_SRC / "examples").is_dir(), \
            "src/orchestration/examples/ missing — reference examples removed"

    def test_camera_drv_example_exists(self):
        """camera_drv_object_det example demonstrates real-world usage."""
        path = self.ORCH_SRC / "examples" / "camera_drv_object_det"
        assert path.is_dir(), \
            "src/orchestration/examples/camera_drv_object_det/ missing"


# ---------------------------------------------------------------------------
# TestOrchestrationMacrosCrate
# ---------------------------------------------------------------------------
class TestOrchestrationMacrosCrate:
    """Verify procedural macros crate."""

    MACROS_DIR = ORCH_DIR / "src" / "orchestration_macros"

    def test_cargo_toml_exists(self):
        assert (self.MACROS_DIR / "Cargo.toml").exists(), \
            "src/orchestration_macros/Cargo.toml missing"

    def test_is_proc_macro(self):
        """Crate must be declared as proc-macro = true."""
        path = self.MACROS_DIR / "Cargo.toml"
        if not path.exists():
            pytest.skip("Cargo.toml not found")
        content = path.read_text(encoding="utf-8")
        assert "proc-macro = true" in content, \
            "orchestration_macros is not declared as proc-macro = true"

    def test_depends_on_syn_and_quote(self):
        """syn + quote are the standard proc-macro dependencies."""
        path = self.MACROS_DIR / "Cargo.toml"
        if not path.exists():
            pytest.skip("Cargo.toml not found")
        content = path.read_text(encoding="utf-8")
        assert "syn" in content, "syn dependency missing from orchestration_macros"
        assert "quote" in content, "quote dependency missing from orchestration_macros"

    def test_rust_source_exists(self):
        rs_files = list(self.MACROS_DIR.rglob("*.rs"))
        assert len(rs_files) >= 1, \
            "No Rust source in orchestration_macros/ — macro implementations removed"

    def test_cpp_bridge_exists(self):
        """C++ bridge for non-Rust callers."""
        cpp_dir = self.MACROS_DIR / "cpp"
        assert cpp_dir.is_dir(), \
            "src/orchestration_macros/cpp/ missing — C++ bridge removed"


# ---------------------------------------------------------------------------
# TestKyronDependency
# ---------------------------------------------------------------------------
class TestKyronDependency:
    """Verify kyron IPC runtime dependency (the core of orchestration)."""

    def test_kyron_in_cargo_lock(self):
        """kyron must be present in Cargo.lock."""
        lock_path = ORCH_DIR / "Cargo.lock"
        if not lock_path.exists():
            pytest.skip("Cargo.lock not found")
        content = lock_path.read_text(encoding="utf-8")
        assert "kyron" in content, \
            "kyron not found in Cargo.lock — IPC runtime may have been removed"

    def test_iceoryx2_in_cargo_lock(self):
        """iceoryx2 shared-memory IPC must be present in Cargo.lock."""
        lock_path = ORCH_DIR / "Cargo.lock"
        if not lock_path.exists():
            pytest.skip("Cargo.lock not found")
        content = lock_path.read_text(encoding="utf-8")
        assert "iceoryx2" in content, \
            "iceoryx2 not found in Cargo.lock — SHM IPC backend removed"

    def test_kyron_referenced_in_workspace_cargo_toml(self):
        """Root Cargo.toml must declare kyron as a workspace dependency."""
        cargo_toml = ORCH_DIR / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("Root Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "kyron" in content, \
            "kyron not referenced in root Cargo.toml workspace dependencies"

    def test_orchestration_features_include_iceoryx2(self):
        """Orchestration crate must declare iceoryx2-ipc as a feature."""
        cargo_toml = ORCH_DIR / "src" / "orchestration" / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("src/orchestration/Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "iceoryx2-ipc" in content, \
            "iceoryx2-ipc feature not declared in orchestration Cargo.toml"


# ---------------------------------------------------------------------------
# TestComponentIntegrationTests
# ---------------------------------------------------------------------------
class TestComponentIntegrationTests:
    """Verify test scenario infrastructure."""

    SCENARIOS = ORCH_DIR / "tests" / "test_scenarios" / "rust"

    def test_scenarios_dir_exists(self):
        assert self.SCENARIOS.is_dir(), \
            "tests/test_scenarios/rust/ missing — CIT infrastructure removed"

    def test_scenarios_has_rust_source(self):
        if not self.SCENARIOS.is_dir():
            pytest.skip("test_scenarios/rust/ not found")
        rs_files = list(self.SCENARIOS.rglob("*.rs"))
        assert len(rs_files) >= 1, \
            "No Rust source files in test_scenarios/rust/ — CIT removed"

    def test_scenarios_has_cargo_toml(self):
        if not self.SCENARIOS.is_dir():
            pytest.skip("test_scenarios/rust/ not found")
        cargo_files = list(self.SCENARIOS.rglob("Cargo.toml"))
        assert len(cargo_files) >= 1, \
            "No Cargo.toml in test_scenarios/rust/ — CIT workspace not configured"
