"""Integration tests for score-scrample dependency chain.

Verifies that score-scrample correctly integrates with upstream S-CORE
modules (score-communication for LoLa IPC, score-feo for execution order).

Platform: any (file inspection only, no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
SCRAMPLE_DIR = PROJECT_ROOT / "score-scrample"


# ---------------------------------------------------------------------------
# TestScoreCommunicationIntegration
# ---------------------------------------------------------------------------
class TestScoreCommunicationIntegration:
    """Verify integration with score-communication (LoLa IPC)."""

    def test_module_bazel_references_communication(self):
        """MODULE.bazel should declare score_communication dependency."""
        module_bazel = SCRAMPLE_DIR / "MODULE.bazel"
        if not module_bazel.exists():
            pytest.skip("MODULE.bazel not found")
        content = module_bazel.read_text(encoding="utf-8")
        assert "score_communication" in content or "score_com" in content, \
            "MODULE.bazel does not reference score-communication"

    def test_sender_receiver_uses_lola_api(self):
        """Sample sender/receiver must use LoLa (mw/com) API."""
        sr_h = SCRAMPLE_DIR / "src" / "sample_sender_receiver.h"
        sr_cpp = SCRAMPLE_DIR / "src" / "sample_sender_receiver.cpp"
        content = ""
        for f in [sr_h, sr_cpp]:
            if f.exists():
                content += f.read_text(encoding="utf-8", errors="ignore")
        if not content:
            pytest.skip("sample_sender_receiver source not found")
        # Should reference score/mw/com or similar LoLa API
        has_com_ref = (
            "mw/com" in content
            or "com::" in content
            or "EventSenderReceiver" in content
            or "LoLa" in content.lower()
        )
        assert has_com_ref, \
            "sample_sender_receiver does not reference LoLa/mw_com API"


# ---------------------------------------------------------------------------
# TestBazelRegistryEntry
# ---------------------------------------------------------------------------
class TestBazelRegistryEntry:
    """Verify score-bazel_registry contains an entry for score_scrample."""

    REGISTRY_DIR = PROJECT_ROOT / "score-bazel_registry"

    def test_registry_exists(self):
        assert self.REGISTRY_DIR.is_dir(), \
            "score-bazel_registry not found"

    def test_scrample_module_dir_exists(self):
        module_dir = self.REGISTRY_DIR / "modules" / "score_scrample"
        if not module_dir.is_dir():
            # May be registered under a different name
            modules_dir = self.REGISTRY_DIR / "modules"
            if modules_dir.is_dir():
                scrample_dirs = [
                    d for d in modules_dir.iterdir()
                    if d.is_dir() and "scrample" in d.name.lower()
                ]
                assert len(scrample_dirs) > 0, \
                    "No scrample entry found in score-bazel_registry/modules/"


# ---------------------------------------------------------------------------
# TestScorexModulePresets
# ---------------------------------------------------------------------------
class TestScorexModulePresets:
    """Verify scorex CLI module presets reference real S-CORE modules."""

    PRESETS_DIR = SCRAMPLE_DIR / "scorex" / "internal" / "config"

    def test_module_presets_file_exists(self):
        if not self.PRESETS_DIR.is_dir():
            pytest.skip("scorex/internal/config/ not found")
        go_files = list(self.PRESETS_DIR.glob("*preset*"))
        assert len(go_files) >= 1, \
            "No module preset files found in scorex config"

    def test_known_good_loader_exists(self):
        """Known-good configuration loader for validated module combinations."""
        loader_dir = (
            SCRAMPLE_DIR / "scorex" / "internal" / "service" / "knowngood"
        )
        if not loader_dir.is_dir():
            pytest.skip("knowngood/ service not found")
        go_files = list(loader_dir.glob("*.go"))
        assert len(go_files) >= 1, \
            "No Go files in knowngood/ — configuration loader removed"
