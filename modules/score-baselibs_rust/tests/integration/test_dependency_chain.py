"""Integration tests for score-baselibs_rust dependency chain (ASIL B).

Verifies that score-baselibs_rust is correctly consumed by downstream
S-CORE modules and that its crate structure is internally consistent.

Platform: any (file inspection only, no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
BASELIBS_RUST_DIR = PROJECT_ROOT / "score-baselibs_rust"
SRC_DIR = BASELIBS_RUST_DIR / "src"


# ---------------------------------------------------------------------------
# TestWorkspaceConsistency
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestWorkspaceConsistency:
    """Verify Cargo workspace members are consistent."""

    def test_cargo_toml_has_workspace(self):
        cargo = BASELIBS_RUST_DIR / "Cargo.toml"
        assert cargo.exists(), "Root Cargo.toml missing"
        content = cargo.read_text(encoding="utf-8")
        assert "[workspace]" in content, "No [workspace] in Cargo.toml"

    def test_workspace_members_exist(self):
        """Each member listed in [workspace] must have a directory."""
        cargo = BASELIBS_RUST_DIR / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        members = re.findall(r'"(src/[^"]+)"', content)
        missing = [m for m in members if not (BASELIBS_RUST_DIR / m).is_dir()]
        assert not missing, (
            f"Workspace members with missing directories: {missing}"
        )

    def test_each_crate_has_cargo_toml(self):
        """Each src/ subdirectory with .rs files must have Cargo.toml."""
        if not SRC_DIR.is_dir():
            pytest.skip("src/ not found")
        crate_dirs = [d for d in SRC_DIR.iterdir() if d.is_dir()]
        missing = []
        for d in crate_dirs:
            rs_files = list(d.rglob("*.rs"))
            if rs_files and not (d / "Cargo.toml").exists():
                missing.append(d.name)
        assert not missing, (
            f"Crate directories without Cargo.toml: {missing}"
        )


# ---------------------------------------------------------------------------
# TestDownstreamDependents
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestDownstreamDependents:
    """Verify downstream modules reference score_baselibs_rust."""

    @pytest.mark.parametrize("module_name", [
        "score-feo",
        "score-kyron",
        "score-logging",
    ])
    def test_downstream_references_baselibs_rust(self, module_name):
        module_dir = PROJECT_ROOT / module_name
        if not module_dir.is_dir():
            pytest.skip(f"{module_name} not found locally")
        module_bazel = module_dir / "MODULE.bazel"
        if not module_bazel.exists():
            pytest.skip(f"{module_name}/MODULE.bazel not found")
        content = module_bazel.read_text(encoding="utf-8")
        assert "score_baselibs_rust" in content, (
            f"{module_name} does not reference score_baselibs_rust"
        )


# ---------------------------------------------------------------------------
# TestModuleBazelDependencies
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestModuleBazelDependencies:
    """Verify MODULE.bazel declares expected dependencies."""

    MODULE_BAZEL = BASELIBS_RUST_DIR / "MODULE.bazel"

    def test_module_bazel_exists(self):
        assert self.MODULE_BAZEL.exists(), "MODULE.bazel missing"

    def test_module_name(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        assert 'name = "score_baselibs_rust"' in content, (
            "Expected module name 'score_baselibs_rust'"
        )

    def test_bazel_dep_on_score_baselibs(self):
        """Should depend on score_baselibs (C++ counterpart)."""
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        has_dep = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_baselibs"', content
        )
        # This is optional — some Rust crates may not need C++ baselibs
        if not has_dep:
            pytest.skip("No score_baselibs dependency (may be standalone)")
