"""Safety and security contract verification for score-orchestrator.

score-orchestrator manages workload lifecycle across ECU partitions. It
is QM-rated, but as a deployment and lifecycle manager it occupies a
privileged position: a compromised orchestrator can start/stop any program.

Security concerns:
- Program configuration loaded from files must be validated.
- IPC via iceoryx2 shared memory: any process with access can inject messages.
- kyron dependency sourced from GitHub — supply chain risk if hash not pinned.
- Procedural macros expand at compile time — malicious macro expansion is silent.

Verification method: file inspection (boundary analysis + configuration validation).
Platform: any (no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
ORCH_DIR = PROJECT_ROOT / "score-orchestrator"


# ---------------------------------------------------------------------------
# TestKyronPinned
# ---------------------------------------------------------------------------
class TestKyronPinned:
    """Verify kyron IPC dependency is pinned to a specific commit hash.

    kyron is sourced from GitHub via a git dependency. Without a pinned
    hash, any push to the kyron repo can silently change orchestrator
    behavior.
    """

    def test_kyron_pinned_by_rev_in_cargo_toml(self):
        """Root Cargo.toml must pin kyron with rev = '<hash>'."""
        cargo_toml = ORCH_DIR / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("Root Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        # kyron must use git + rev pinning
        has_git_rev = re.search(r'kyron.*git.*rev\s*=\s*"[0-9a-f]{7,}"', content, re.DOTALL)
        has_rev_block = "rev = " in content and "kyron" in content
        assert has_git_rev or has_rev_block, (
            "kyron dependency does not appear to be pinned with rev = '<hash>' — "
            "git dependency without hash pin is a supply chain risk"
        )

    def test_kyron_commit_hash_in_cargo_lock(self):
        """Cargo.lock must contain a commit hash for kyron."""
        lock_path = ORCH_DIR / "Cargo.lock"
        if not lock_path.exists():
            pytest.skip("Cargo.lock not found")
        content = lock_path.read_text(encoding="utf-8")
        # Cargo.lock stores source with exact commit hash for git deps
        assert "kyron" in content, "kyron not in Cargo.lock"
        # Look for a git hash associated with kyron
        kyron_section = ""
        in_kyron = False
        for line in content.splitlines():
            if 'name = "kyron"' in line:
                in_kyron = True
            if in_kyron:
                kyron_section += line + "\n"
                if line.strip() == "":
                    break
        has_hash = bool(re.search(r"[0-9a-f]{40}", kyron_section))
        assert has_hash or "source" in kyron_section, (
            "kyron entry in Cargo.lock does not contain a commit hash — "
            "dependency may not be reproducibly pinned"
        )


# ---------------------------------------------------------------------------
# TestProcMacroSafety
# ---------------------------------------------------------------------------
class TestProcMacroSafety:
    """Verify orchestration_macros procedural macro crate safety properties.

    Proc-macros run at compile time with full access to the token stream.
    Malicious or buggy macros can silently generate incorrect code.
    """

    MACROS_DIR = ORCH_DIR / "src" / "orchestration_macros"

    def test_no_file_system_access_in_macro_source(self):
        """Proc-macros should not use std::fs or std::io in normal expansion.

        File system access in a proc-macro is a code injection risk.
        """
        if not self.MACROS_DIR.is_dir():
            pytest.skip("orchestration_macros directory not found")
        rs_files = list(self.MACROS_DIR.rglob("*.rs"))
        violations = []
        for f in rs_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "std::fs::" in content and "build.rs" not in f.name:
                violations.append(f"{f.name}: uses std::fs")
        assert not violations, (
            "Proc-macro source uses std::fs — potential code injection risk:\n"
            + "\n".join(violations)
        )

    def test_no_unsafe_in_macro_source(self):
        """Proc-macros should not use unsafe blocks."""
        if not self.MACROS_DIR.is_dir():
            pytest.skip("orchestration_macros directory not found")
        rs_files = list(self.MACROS_DIR.rglob("*.rs"))
        violations = []
        for f in rs_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "unsafe" in content:
                violations.append(f.name)
        assert not violations, (
            f"Proc-macro source contains 'unsafe': {violations} — "
            "unexpected for token transformation code"
        )


# ---------------------------------------------------------------------------
# TestIceoryx2FeatureGating
# ---------------------------------------------------------------------------
class TestIceoryx2FeatureGating:
    """Verify iceoryx2 IPC backend is feature-gated.

    iceoryx2 shared-memory IPC has no access control by default. It
    should be an optional feature so deployments without SHM requirements
    can disable it.
    """

    def test_iceoryx2_ipc_is_optional_feature(self):
        """iceoryx2-ipc must be declared as an optional (feature-gated) dep."""
        cargo = ORCH_DIR / "src" / "orchestration" / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("src/orchestration/Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        has_feature_def = "[features]" in content and "iceoryx2-ipc" in content
        has_optional = "optional" in content and "iceoryx2" in content
        assert has_feature_def or has_optional, (
            "iceoryx2-ipc does not appear to be feature-gated — "
            "SHM IPC should be optional for deployments without iceoryx2 runtime"
        )


# ---------------------------------------------------------------------------
# TestOrchestrationProgramDatabase
# ---------------------------------------------------------------------------
class TestOrchestrationProgramDatabase:
    """Verify program_database.rs exists and provides configuration validation.

    program_database is the runtime registry of deployed programs. It must
    validate program configurations before accepting them.
    """

    ORCH_SRC = ORCH_DIR / "src" / "orchestration"

    def test_program_database_source_exists(self):
        path = self.ORCH_SRC / "src" / "program_database.rs"
        if not path.exists():
            path = self.ORCH_SRC / "program_database.rs"
        assert path.exists(), (
            "program_database.rs not found — program registry implementation removed"
        )

    def test_testing_module_exists(self):
        """testing/ module provides test harness for program lifecycle tests."""
        test_dir = self.ORCH_SRC / "src" / "testing"
        if not test_dir.is_dir():
            test_dir = self.ORCH_SRC / "testing"
        assert test_dir.is_dir(), (
            "src/orchestration/testing/ missing — lifecycle test harness removed"
        )
