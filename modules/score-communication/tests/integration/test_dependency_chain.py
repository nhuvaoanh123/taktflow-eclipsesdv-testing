"""Integration tests for score-communication dependency chain (ASIL B).

Verifies that score-communication (LoLa) is correctly consumed by
downstream S-CORE modules and that cross-module interfaces are consistent.

Platform: any (file inspection only, no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
LOLA_DIR = PROJECT_ROOT / "modules" / "score-communication" / "upstream"


# ---------------------------------------------------------------------------
# TestDownstreamModulesReferenceLola
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestDownstreamModulesReferenceLola:
    """Verify downstream modules declare score_communication dependency."""

    @pytest.mark.parametrize("module_name", [
        "score-feo",
        "score-logging",
        "score-scrample",
    ])
    def test_module_references_score_communication(self, module_name):
        module_dir = PROJECT_ROOT / module_name
        if not module_dir.is_dir():
            pytest.skip(f"{module_name} not found locally")
        module_bazel = module_dir / "MODULE.bazel"
        if not module_bazel.exists():
            pytest.skip(f"{module_name}/MODULE.bazel not found")
        content = module_bazel.read_text(encoding="utf-8")
        assert "score_communication" in content, (
            f"{module_name} does not reference score_communication"
        )


# ---------------------------------------------------------------------------
# TestLolaModuleDependencies
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestLolaModuleDependencies:
    """Verify MODULE.bazel declares required dependencies."""

    MODULE_BAZEL = LOLA_DIR / "MODULE.bazel"

    def test_module_bazel_exists(self):
        assert self.MODULE_BAZEL.exists(), "MODULE.bazel missing"

    def test_module_name(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        assert 'name = "score_communication"' in content, (
            "Expected module name 'score_communication'"
        )

    def test_declares_score_baselibs(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        assert re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_baselibs"', content
        ), "MODULE.bazel does not declare score_baselibs"


# ---------------------------------------------------------------------------
# TestCrossModuleHeaders
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestCrossModuleHeaders:
    """Verify public headers accessible for downstream inclusion."""

    def test_mw_com_headers_accessible(self):
        mw_com = LOLA_DIR / "score" / "mw" / "com"
        assert mw_com.is_dir(), "score/mw/com/ not accessible"
        h_files = list(mw_com.rglob("*.h"))
        assert len(h_files) >= 5, (
            f"Only {len(h_files)} headers in mw/com/ -- expected more"
        )

    def test_message_passing_headers_accessible(self):
        mp = LOLA_DIR / "score" / "message_passing"
        assert mp.is_dir(), "score/message_passing/ not accessible"
        h_files = list(mp.rglob("*.h"))
        assert len(h_files) >= 3, (
            f"Only {len(h_files)} headers in message_passing/"
        )
