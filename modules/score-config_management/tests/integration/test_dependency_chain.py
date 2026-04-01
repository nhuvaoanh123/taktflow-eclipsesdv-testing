"""Integration tests for score-config_management dependency chain.

Verifies that score-config_management correctly declares its dependencies
and that key integration points (mw_com factory, persistency backend)
exist as expected.

Platform: any (file inspection only, no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
CONFIG_MGMT_DIR = PROJECT_ROOT / "score-config_management"
SCORE_DIR = CONFIG_MGMT_DIR / "score"
CONFIG_PROVIDER = SCORE_DIR / "config_management" / "config_provider"


# ---------------------------------------------------------------------------
# TestMwComFactoryIntegration
# ---------------------------------------------------------------------------
class TestMwComFactoryIntegration:
    """Verify integration between config_provider and score-communication (mw_com).

    The factory_mw_com pattern creates ConfigProvider instances that use
    score-communication (LoLa) for event subscription/notification.
    """

    FACTORY_DIR = CONFIG_PROVIDER / "code" / "config_provider" / "factory"

    def test_factory_directory_exists(self):
        assert self.FACTORY_DIR.is_dir(), \
            "config_provider/factory/ missing — mw_com integration removed"

    def test_factory_mw_com_header_exists(self):
        if not self.FACTORY_DIR.is_dir():
            pytest.skip("factory/ not found")
        h_files = list(self.FACTORY_DIR.rglob("*mw_com*"))
        assert len(h_files) >= 1, \
            "No factory_mw_com files — score-communication integration broken"

    def test_factory_has_source_files(self):
        if not self.FACTORY_DIR.is_dir():
            pytest.skip("factory/ not found")
        sources = list(self.FACTORY_DIR.rglob("*.h")) + list(
            self.FACTORY_DIR.rglob("*.cpp")
        ) + list(self.FACTORY_DIR.rglob("*.cc"))
        assert len(sources) >= 1, \
            "No source files in factory/ — implementation removed"


# ---------------------------------------------------------------------------
# TestPersistencyIntegration
# ---------------------------------------------------------------------------
class TestPersistencyIntegration:
    """Verify persistency backend integration for config storage."""

    PERSISTENCY_DIR = CONFIG_PROVIDER / "code" / "persistency"

    def test_persistency_directory_exists(self):
        assert self.PERSISTENCY_DIR.is_dir(), \
            "config_provider/code/persistency/ missing — storage backend removed"

    def test_persistency_has_headers(self):
        if not self.PERSISTENCY_DIR.is_dir():
            pytest.skip("persistency/ not found")
        h_files = list(self.PERSISTENCY_DIR.rglob("*.h"))
        assert len(h_files) >= 1, \
            "No headers in persistency/ — interface removed"


# ---------------------------------------------------------------------------
# TestBazelRegistryEntry
# ---------------------------------------------------------------------------
class TestBazelRegistryEntry:
    """Verify score-bazel_registry contains an entry for score_config_management."""

    REGISTRY_DIR = PROJECT_ROOT / "score-bazel_registry"

    def test_registry_exists(self):
        assert self.REGISTRY_DIR.is_dir(), \
            "score-bazel_registry not found"

    def test_config_management_module_dir_exists(self):
        module_dir = self.REGISTRY_DIR / "modules" / "score_config_management"
        assert module_dir.is_dir(), \
            "score_config_management not found in score-bazel_registry/modules/"

    def test_metadata_json_exists(self):
        metadata = (
            self.REGISTRY_DIR / "modules" / "score_config_management" / "metadata.json"
        )
        assert metadata.exists(), \
            "metadata.json not found for score_config_management in Bazel registry"

    def test_registry_has_version_entries(self):
        module_dir = self.REGISTRY_DIR / "modules" / "score_config_management"
        if not module_dir.is_dir():
            pytest.skip("Registry module dir missing")
        version_dirs = [
            d for d in module_dir.iterdir()
            if d.is_dir() and re.match(r"\d+\.\d+\.\d+", d.name)
        ]
        assert len(version_dirs) > 0, \
            "No version directories found in registry for score_config_management"
