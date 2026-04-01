"""Regression tests for score-config_management API contract stability.

Verification methods: API contract verification, file existence.
Platform: any (no build required — file inspection only).

score-config_management provides S-CORE configuration middleware:
  - ConfigProvider: typed parameter sets with persistency backend
  - ParameterSet: key-value store with type validation
  - Factory pattern (factory_mw_com) for LoLa/mw_com integration
  - MQTT event subscription for configuration change notification

If expected source files, headers, or BUILD targets are missing, the
upstream module may have broken backwards compatibility.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
CONFIG_MGMT_DIR = PROJECT_ROOT / "score-config_management"
SCORE_DIR = CONFIG_MGMT_DIR / "score"
CONFIG_PROVIDER = SCORE_DIR / "config_management" / "config_provider"


# ---------------------------------------------------------------------------
# TestModuleIdentity
# ---------------------------------------------------------------------------
class TestModuleIdentity:
    """Verify MODULE.bazel with expected name and version."""

    def test_module_bazel_exists(self):
        assert (CONFIG_MGMT_DIR / "MODULE.bazel").exists(), \
            f"MODULE.bazel not found at {CONFIG_MGMT_DIR}"

    def test_module_name_is_score_config_management(self):
        content = (CONFIG_MGMT_DIR / "MODULE.bazel").read_text(encoding="utf-8")
        assert "score_config_management" in content, \
            "Expected module name 'score_config_management' in MODULE.bazel"

    def test_bazelversion_exists(self):
        path = CONFIG_MGMT_DIR / ".bazelversion"
        if not path.exists():
            pytest.skip(".bazelversion not found")
        version = path.read_text().strip()
        assert re.match(r"\d+\.\d+\.\d+", version), \
            f"Invalid version format in .bazelversion: {version}"


# ---------------------------------------------------------------------------
# TestConfigProviderComponent
# ---------------------------------------------------------------------------
class TestConfigProviderComponent:
    """Verify config_provider component structure (core C++ library)."""

    CODE_DIR = CONFIG_PROVIDER / "code"

    def test_config_provider_directory_exists(self):
        assert CONFIG_PROVIDER.is_dir(), \
            "score/config_management/config_provider/ missing"

    def test_code_directory_exists(self):
        assert self.CODE_DIR.is_dir(), \
            "config_provider/code/ missing — source tree removed"

    def test_parameter_set_directory_exists(self):
        path = self.CODE_DIR / "parameter_set"
        assert path.is_dir(), \
            "config_provider/code/parameter_set/ missing — core data model removed"

    def test_parameter_set_has_headers(self):
        path = self.CODE_DIR / "parameter_set"
        if not path.is_dir():
            pytest.skip("parameter_set/ not found")
        h_files = list(path.rglob("*.h"))
        assert len(h_files) >= 1, \
            "No headers in parameter_set/ — public API removed"

    def test_parameter_set_has_test_files(self):
        path = self.CODE_DIR / "parameter_set"
        if not path.is_dir():
            pytest.skip("parameter_set/ not found")
        test_files = list(path.rglob("*_test.cpp")) + list(path.rglob("*_test.cc"))
        assert len(test_files) >= 1, \
            "No test files in parameter_set/ — upstream tests removed"

    def test_config_provider_subdir_exists(self):
        path = self.CODE_DIR / "config_provider"
        assert path.is_dir(), \
            "config_provider/code/config_provider/ missing — core provider removed"

    def test_config_provider_has_headers(self):
        path = self.CODE_DIR / "config_provider"
        if not path.is_dir():
            pytest.skip("config_provider/ subdir not found")
        h_files = list(path.rglob("*.h"))
        assert len(h_files) >= 1, \
            "No headers in config_provider/ — provider API removed"

    def test_config_provider_mock_exists(self):
        """Mock must exist for downstream consumers to unit-test config access."""
        path = self.CODE_DIR / "config_provider"
        if not path.is_dir():
            pytest.skip("config_provider/ subdir not found")
        mocks = list(path.rglob("*mock*"))
        assert len(mocks) >= 1, \
            "No mock files in config_provider/ — test seam removed"

    def test_factory_directory_exists(self):
        """Factory for mw_com integration must exist."""
        path = self.CODE_DIR / "config_provider" / "factory"
        assert path.is_dir(), \
            "config_provider/factory/ missing — factory pattern removed"

    def test_persistency_directory_exists(self):
        """Persistency backend for config storage."""
        path = self.CODE_DIR / "persistency"
        assert path.is_dir(), \
            "config_provider/code/persistency/ missing — storage backend removed"

    def test_error_directory_exists(self):
        """Error type definitions for config operations."""
        path = self.CODE_DIR / "config_provider" / "error"
        assert path.is_dir(), \
            "config_provider/error/ missing — error types removed"


# ---------------------------------------------------------------------------
# TestBuildTargets
# ---------------------------------------------------------------------------
class TestBuildTargets:
    """Verify BUILD files exist for key components."""

    def test_top_level_build_file_exists(self):
        has_build = (
            (CONFIG_MGMT_DIR / "BUILD").exists()
            or (CONFIG_MGMT_DIR / "BUILD.bazel").exists()
        )
        assert has_build, "No top-level BUILD file in score-config_management"

    def test_config_provider_build_file_exists(self):
        if not CONFIG_PROVIDER.is_dir():
            pytest.skip("config_provider/ not found")
        has_build = (
            (CONFIG_PROVIDER / "BUILD").exists()
            or (CONFIG_PROVIDER / "BUILD.bazel").exists()
        )
        if not has_build:
            # Check recursively for any BUILD file
            builds = list(CONFIG_PROVIDER.rglob("BUILD")) + list(
                CONFIG_PROVIDER.rglob("BUILD.bazel")
            )
            assert len(builds) > 0, \
                "No BUILD files found in config_provider/"


# ---------------------------------------------------------------------------
# TestBazelConfiguration
# ---------------------------------------------------------------------------
class TestBazelConfiguration:
    """Verify .bazelrc build configuration."""

    def test_bazelrc_exists(self):
        assert (CONFIG_MGMT_DIR / ".bazelrc").exists(), \
            ".bazelrc not found — build configs missing"

    @pytest.mark.parametrize("config", ["x86_64-linux"])
    def test_bazelrc_has_config(self, config):
        path = CONFIG_MGMT_DIR / ".bazelrc"
        if not path.exists():
            pytest.skip(".bazelrc not found")
        assert config in path.read_text(encoding="utf-8"), \
            f"Config '{config}' not found in .bazelrc"
