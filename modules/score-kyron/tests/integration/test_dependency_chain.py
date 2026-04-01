"""Integration tests for score-kyron dependency chain.

Verifies that score-kyron workspace crates have correct inter-crate
dependencies and that the iceoryx2 IPC integration is properly wired.

Platform: any (file inspection only, no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
KYRON_DIR = PROJECT_ROOT / "score-kyron"
SRC_DIR = KYRON_DIR / "src"


# ---------------------------------------------------------------------------
# TestInterCrateDependencies
# ---------------------------------------------------------------------------
class TestInterCrateDependencies:
    """Verify that workspace crates reference each other correctly."""

    def _read_cargo_toml(self, crate_name):
        path = SRC_DIR / crate_name / "Cargo.toml"
        if not path.exists():
            pytest.skip(f"{crate_name}/Cargo.toml not found")
        return path.read_text(encoding="utf-8")

    def test_kyron_depends_on_foundation(self):
        """kyron core must depend on kyron-foundation."""
        content = self._read_cargo_toml("kyron")
        assert "kyron-foundation" in content, \
            "kyron does not depend on kyron-foundation"

    def test_kyron_depends_on_macros(self):
        """kyron core should depend on kyron-macros for proc-macros."""
        content = self._read_cargo_toml("kyron")
        assert "kyron-macros" in content, \
            "kyron does not depend on kyron-macros"


# ---------------------------------------------------------------------------
# TestIceoryx2Integration
# ---------------------------------------------------------------------------
class TestIceoryx2Integration:
    """Verify iceoryx2 IPC event integration in kyron."""

    IPC_DIR = SRC_DIR / "kyron" / "src" / "ipc"

    def test_ipc_directory_exists(self):
        if not self.IPC_DIR.is_dir():
            ipc_file = SRC_DIR / "kyron" / "src" / "ipc.rs"
            assert ipc_file.exists(), \
                "No IPC module found in kyron"

    def test_iceoryx2_referenced(self):
        """Kyron must reference iceoryx2 for shared-memory IPC."""
        ipc_dir = self.IPC_DIR
        if not ipc_dir.is_dir():
            ipc_file = SRC_DIR / "kyron" / "src" / "ipc.rs"
            if not ipc_file.exists():
                pytest.skip("IPC module not found")
            content = ipc_file.read_text(encoding="utf-8", errors="ignore")
        else:
            content = ""
            for f in ipc_dir.rglob("*.rs"):
                content += f.read_text(encoding="utf-8", errors="ignore")
        assert "iceoryx2" in content, \
            "iceoryx2 not referenced in IPC module"


# ---------------------------------------------------------------------------
# TestXtaskTooling
# ---------------------------------------------------------------------------
class TestXtaskTooling:
    """Verify xtask helper (license checks, build orchestration)."""

    XTASK = SRC_DIR / "xtask"

    def test_xtask_exists(self):
        assert self.XTASK.is_dir(), \
            "src/xtask/ missing — build tooling removed"

    def test_xtask_has_main(self):
        if not self.XTASK.is_dir():
            pytest.skip("xtask not found")
        main_rs = self.XTASK / "src" / "main.rs"
        assert main_rs.exists(), \
            "xtask/src/main.rs missing — xtask entry point removed"
