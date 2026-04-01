"""Regression tests for score-baselibs_rust API contract stability (ASIL B).

Verification methods: API contract verification, file existence.
Platform: any (no build required — file inspection only).

score-baselibs_rust provides Rust foundation libraries: containers, sync
primitives, elementary types, PAL, threading, logging format macros.

If expected crates, source files, or test targets are missing, the
upstream module may have broken backwards compatibility.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
BASELIBS_RUST_DIR = PROJECT_ROOT / "score-baselibs_rust"
SRC_DIR = BASELIBS_RUST_DIR / "src"


# ---------------------------------------------------------------------------
# TestModuleIdentity
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestModuleIdentity:
    """Verify MODULE.bazel with expected name."""

    def test_module_bazel_exists(self):
        assert (BASELIBS_RUST_DIR / "MODULE.bazel").exists(), (
            "MODULE.bazel missing"
        )

    def test_module_name(self):
        content = (BASELIBS_RUST_DIR / "MODULE.bazel").read_text(encoding="utf-8")
        assert 'name = "score_baselibs_rust"' in content, (
            "Expected module name 'score_baselibs_rust'"
        )


# ---------------------------------------------------------------------------
# TestCoreCrates
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestCoreCrates:
    """Verify core crate directories and Cargo.toml files exist."""

    EXPECTED_CRATES = [
        "containers",
        "sync",
        "elementary",
    ]

    @pytest.mark.parametrize("crate_name", EXPECTED_CRATES)
    def test_crate_directory_exists(self, crate_name):
        path = SRC_DIR / crate_name
        assert path.is_dir(), (
            f"src/{crate_name}/ missing -- core crate removed"
        )

    @pytest.mark.parametrize("crate_name", EXPECTED_CRATES)
    def test_crate_has_cargo_toml(self, crate_name):
        path = SRC_DIR / crate_name / "Cargo.toml"
        assert path.exists(), (
            f"src/{crate_name}/Cargo.toml missing"
        )

    @pytest.mark.parametrize("crate_name", EXPECTED_CRATES)
    def test_crate_has_source_files(self, crate_name):
        crate_dir = SRC_DIR / crate_name
        if not crate_dir.is_dir():
            pytest.skip(f"{crate_name}/ not found")
        rs_files = list(crate_dir.rglob("*.rs"))
        assert len(rs_files) >= 1, (
            f"src/{crate_name}/ has no Rust source files"
        )

    @pytest.mark.parametrize("crate_name", EXPECTED_CRATES)
    def test_crate_has_tests(self, crate_name):
        """Each core crate must have test files or #[test] annotations."""
        crate_dir = SRC_DIR / crate_name
        if not crate_dir.is_dir():
            pytest.skip(f"{crate_name}/ not found")
        has_tests = False
        for f in crate_dir.rglob("*.rs"):
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "#[cfg(test)]" in content or "#[test]" in content:
                has_tests = True
                break
        test_files = [f for f in crate_dir.rglob("*.rs") if "test" in f.name.lower()]
        assert has_tests or len(test_files) > 0, (
            f"src/{crate_name}/ has no test infrastructure -- "
            "ASIL B requires test coverage"
        )


# ---------------------------------------------------------------------------
# TestBuildConfiguration
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestBuildConfiguration:
    """Verify build configuration files exist."""

    def test_cargo_lock_exists(self):
        assert (BASELIBS_RUST_DIR / "Cargo.lock").exists(), (
            "Cargo.lock missing -- deps not locked"
        )

    def test_bazelversion_exists(self):
        path = BASELIBS_RUST_DIR / ".bazelversion"
        assert path.exists(), ".bazelversion missing"

    def test_bazelrc_exists(self):
        path = BASELIBS_RUST_DIR / ".bazelrc"
        if not path.exists():
            pytest.skip(".bazelrc not found")
        content = path.read_text(encoding="utf-8")
        assert "x86_64-linux" in content or "config" in content, (
            ".bazelrc lacks platform configuration"
        )

    def test_build_files_exist(self):
        build_files = (
            list(BASELIBS_RUST_DIR.rglob("BUILD"))
            + list(BASELIBS_RUST_DIR.rglob("BUILD.bazel"))
        )
        assert len(build_files) >= 1, "No BUILD files found"

    def test_module_bazel_lock_exists(self):
        assert (BASELIBS_RUST_DIR / "MODULE.bazel.lock").exists(), (
            "MODULE.bazel.lock missing -- Bazel deps not locked"
        )


# ---------------------------------------------------------------------------
# TestPalCrate
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestPalCrate:
    """Verify Platform Abstraction Layer (PAL) crate."""

    PAL_DIR = SRC_DIR / "pal"

    def test_pal_directory_exists(self):
        assert self.PAL_DIR.is_dir(), "src/pal/ missing -- PAL removed"

    def test_pal_has_cargo_toml(self):
        assert (self.PAL_DIR / "Cargo.toml").exists(), (
            "src/pal/Cargo.toml missing"
        )

    def test_pal_has_source_files(self):
        if not self.PAL_DIR.is_dir():
            pytest.skip("pal/ not found")
        rs_files = list(self.PAL_DIR.rglob("*.rs"))
        assert len(rs_files) >= 1, "src/pal/ has no source files"
