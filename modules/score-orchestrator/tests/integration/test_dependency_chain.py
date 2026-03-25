"""Integration tests for score-orchestrator dependency chain.

Verifies that score-orchestrator correctly declares its dependencies on
kyron, iceoryx2, and orchestration_macros, and that the MODULE.bazel
declares score infrastructure dependencies.

Platform: any (file inspection only, no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
ORCH_DIR = PROJECT_ROOT / "score-orchestrator"


# ---------------------------------------------------------------------------
# TestModuleBazelDependencies
# ---------------------------------------------------------------------------
class TestModuleBazelDependencies:
    """Verify MODULE.bazel declares S-CORE infrastructure dependencies."""

    MODULE_BAZEL = ORCH_DIR / "MODULE.bazel"

    def _content(self):
        return self.MODULE_BAZEL.read_text(encoding="utf-8")

    def test_module_bazel_exists(self):
        assert self.MODULE_BAZEL.exists(), \
            f"MODULE.bazel not found at {ORCH_DIR}"

    def test_declares_rules_rust(self):
        assert re.search(r'bazel_dep\(\s*name\s*=\s*"rules_rust"', self._content()), \
            "MODULE.bazel does not declare rules_rust — Rust build support missing"

    def test_declares_score_rust_policies(self):
        assert "score_rust_policies" in self._content(), \
            "MODULE.bazel does not reference score_rust_policies — Clippy policy missing"

    def test_declares_bazel_skylib(self):
        assert re.search(r'bazel_dep\(\s*name\s*=\s*"bazel_skylib"', self._content()), \
            "MODULE.bazel does not declare bazel_skylib"


# ---------------------------------------------------------------------------
# TestWorkspaceDependencyChain
# ---------------------------------------------------------------------------
class TestWorkspaceDependencyChain:
    """Verify the Cargo workspace dependency chain is intact."""

    CARGO_TOML = ORCH_DIR / "Cargo.toml"

    def _content(self):
        return self.CARGO_TOML.read_text(encoding="utf-8")

    def test_workspace_dependency_section_exists(self):
        assert "[workspace.dependencies]" in self._content(), \
            "Root Cargo.toml has no [workspace.dependencies] section"

    @pytest.mark.parametrize("dep", ["kyron", "iceoryx2", "orchestration"])
    def test_workspace_dep_declared(self, dep):
        assert dep in self._content(), \
            f"'{dep}' not found in workspace dependencies"

    def test_orchestration_crate_depends_on_kyron(self):
        cargo = ORCH_DIR / "src" / "orchestration" / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("src/orchestration/Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        assert "kyron" in content, \
            "src/orchestration/Cargo.toml does not depend on kyron"

    def test_orchestration_crate_depends_on_iceoryx2(self):
        cargo = ORCH_DIR / "src" / "orchestration" / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("src/orchestration/Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        assert "iceoryx2" in content, \
            "src/orchestration/Cargo.toml does not reference iceoryx2"

    def test_orchestration_dev_depends_on_kyron_testing(self):
        """Dev dependencies must include kyron-testing for CIT."""
        cargo = ORCH_DIR / "src" / "orchestration" / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("src/orchestration/Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        assert "kyron-testing" in content, \
            "Dev dependencies missing kyron-testing — CIT may not work"


# ---------------------------------------------------------------------------
# TestCrossModuleIntegration
# ---------------------------------------------------------------------------
class TestCrossModuleIntegration:
    """Verify score-orchestrator works with score-logging and score-feo.

    The orchestrator manages program lifecycle and uses DLT logging
    (score-logging) for diagnostics. score-feo integrates as an activity
    executor under the orchestrator's supervision.
    """

    def test_orchestration_has_logging_feature(self):
        """Orchestration crate should support score-log or log feature."""
        cargo = ORCH_DIR / "src" / "orchestration" / "Cargo.toml"
        if not cargo.exists():
            pytest.skip("src/orchestration/Cargo.toml not found")
        content = cargo.read_text(encoding="utf-8")
        has_score_log = "score-log" in content
        has_log = "logging" in content.lower() or '"log"' in content
        assert has_score_log or has_log, (
            "src/orchestration/Cargo.toml has no logging feature — "
            "integration with score-logging may be missing"
        )

    def test_flags_directory_exists(self):
        """score-orchestrator/src/flags/ provides Bazel build flags."""
        path = ORCH_DIR / "src" / "flags"
        assert path.is_dir(), \
            "src/flags/ missing — Bazel feature flag configuration removed"

    def test_docs_directory_exists(self):
        """Documentation should exist for integration guidance."""
        path = ORCH_DIR / "src" / "orchestration" / "doc"
        has_doc = path.is_dir() or (ORCH_DIR / "docs").is_dir()
        assert has_doc, \
            "No docs/ or doc/ directory found — integration documentation missing"


# ---------------------------------------------------------------------------
# TestBazelRegistry
# ---------------------------------------------------------------------------
class TestBazelRegistry:
    """Verify score-bazel_registry contains score_orchestrator entry."""

    REGISTRY_DIR = PROJECT_ROOT / "score-bazel_registry"

    def test_registry_exists(self):
        assert self.REGISTRY_DIR.is_dir(), \
            "score-bazel_registry not found"

    def test_score_orchestrator_module_dir(self):
        module_dir = self.REGISTRY_DIR / "modules" / "score_orchestrator"
        assert module_dir.is_dir(), \
            "score_orchestrator not found in score-bazel_registry/modules/"

    def test_metadata_json_exists(self):
        metadata = self.REGISTRY_DIR / "modules" / "score_orchestrator" / "metadata.json"
        assert metadata.exists(), \
            "metadata.json missing for score_orchestrator in Bazel registry"
