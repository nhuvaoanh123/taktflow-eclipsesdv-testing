"""Regression tests for score-logging API contract stability.

Verification methods: API contract verification, file existence.
Platform: any (no build required — file inspection only).

score-logging v0.0.0 provides DLT-compatible structured logging for the
S-CORE ecosystem. Public API surface:

  C++  : score/mw/log/log.h (frontend)
  Rust : score/mw/log/rust/ (Rust bindings)
  DLT  : score/datarouter/ (daemon bridge — standalone binary)

If expected source files, headers, or BUILD targets are missing, the
upstream module may have broken backwards compatibility.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
LOGGING_DIR = PROJECT_ROOT / "score-logging"
SCORE_DIR = LOGGING_DIR / "score"


# ---------------------------------------------------------------------------
# TestModuleIdentity
# ---------------------------------------------------------------------------
class TestModuleIdentity:
    """Verify MODULE.bazel with expected name and version."""

    def test_module_bazel_exists(self):
        assert (LOGGING_DIR / "MODULE.bazel").exists(), \
            f"MODULE.bazel not found at {LOGGING_DIR}"

    def test_module_name_is_score_logging(self):
        content = (LOGGING_DIR / "MODULE.bazel").read_text(encoding="utf-8")
        assert 'name = "score_logging"' in content, \
            "Expected module name 'score_logging' in MODULE.bazel"

    def test_module_version_is_0_0_0(self):
        content = (LOGGING_DIR / "MODULE.bazel").read_text(encoding="utf-8")
        assert 'version = "0.0.0"' in content, \
            "Expected version 0.0.0 in MODULE.bazel"

    def test_bazel_version_is_8_3_0(self):
        path = LOGGING_DIR / ".bazelversion"
        if not path.exists():
            pytest.skip(".bazelversion not found")
        assert path.read_text().strip() == "8.3.0", \
            "Expected Bazel 8.3.0 pinned in .bazelversion"


# ---------------------------------------------------------------------------
# TestMwLogComponent
# ---------------------------------------------------------------------------
class TestMwLogComponent:
    """Verify score/mw/log logging frontend structure."""

    MW_LOG = SCORE_DIR / "mw" / "log"

    def test_mw_log_directory_exists(self):
        assert self.MW_LOG.is_dir(), \
            "score/mw/log/ directory missing — logging frontend removed"

    def test_build_file_exists(self):
        build = self.MW_LOG / "BUILD"
        build_bazel = self.MW_LOG / "BUILD.bazel"
        assert build.exists() or build_bazel.exists(), \
            "No BUILD file in score/mw/log/"

    def test_detail_directory_exists(self):
        assert (self.MW_LOG / "detail").is_dir(), \
            "score/mw/log/detail/ missing — recorder implementations removed"

    def test_test_directory_exists(self):
        assert (self.MW_LOG / "test").is_dir(), \
            "score/mw/log/test/ missing — unit test suite removed"

    @pytest.mark.parametrize("subdir", [
        "console_logging_environment",
        "fake_recorder",
        "fake_recorder_environment",
    ])
    def test_test_environment_exists(self, subdir):
        """Test environment helpers must exist for downstream consumers."""
        path = self.MW_LOG / "test" / subdir
        assert path.is_dir(), \
            f"score/mw/log/test/{subdir}/ missing — test helper removed"

    def test_rust_bindings_directory_exists(self):
        assert (self.MW_LOG / "rust").is_dir(), \
            "score/mw/log/rust/ missing — Rust logging bindings removed"

    def test_rust_source_files_exist(self):
        rs_files = list((self.MW_LOG / "rust").rglob("*.rs"))
        assert len(rs_files) >= 1, \
            f"Expected at least 1 Rust source in mw/log/rust/, found {len(rs_files)}"

    def test_flags_directory_exists(self):
        assert (self.MW_LOG / "flags").is_dir(), \
            "score/mw/log/flags/ missing — feature flag configuration removed"

    def test_design_directory_exists(self):
        assert (self.MW_LOG / "design").is_dir(), \
            "score/mw/log/design/ missing — design documentation removed"

    def test_cpp_header_files_exist(self):
        h_files = list(self.MW_LOG.rglob("*.h"))
        assert len(h_files) >= 3, \
            f"Expected at least 3 C++ headers in mw/log/, found {len(h_files)}"

    def test_cpp_source_files_exist(self):
        cc_files = list(self.MW_LOG.rglob("*.cc")) + list(self.MW_LOG.rglob("*.cpp"))
        assert len(cc_files) >= 1, \
            f"Expected at least 1 C++ source file in mw/log/, found {len(cc_files)}"


# ---------------------------------------------------------------------------
# TestDataRouterComponent
# ---------------------------------------------------------------------------
class TestDataRouterComponent:
    """Verify score/datarouter DLT daemon bridge structure."""

    DATAROUTER = SCORE_DIR / "datarouter"

    def test_datarouter_directory_exists(self):
        assert self.DATAROUTER.is_dir(), \
            "score/datarouter/ directory missing — DLT bridge removed"

    def test_build_file_exists(self):
        build = self.DATAROUTER / "BUILD"
        build_bazel = self.DATAROUTER / "BUILD.bazel"
        assert build.exists() or build_bazel.exists(), \
            "No BUILD file in score/datarouter/"

    def test_include_directory_exists(self):
        assert (self.DATAROUTER / "include").is_dir(), \
            "score/datarouter/include/ missing — public API removed"

    def test_datarouter_subdir_exists(self):
        assert (self.DATAROUTER / "datarouter").is_dir(), \
            "score/datarouter/datarouter/ missing — daemon implementation removed"

    def test_dlt_filetransfer_trigger_exists(self):
        assert (self.DATAROUTER / "dlt_filetransfer_trigger_lib").is_dir(), \
            "score/datarouter/dlt_filetransfer_trigger_lib/ missing"

    def test_daemon_communication_directory_exists(self):
        assert (self.DATAROUTER / "daemon_communication").is_dir(), \
            "score/datarouter/daemon_communication/ missing"

    def test_error_directory_exists(self):
        assert (self.DATAROUTER / "error").is_dir(), \
            "score/datarouter/error/ missing — error type definitions removed"

    def test_datarouter_has_headers(self):
        h_files = list(self.DATAROUTER.rglob("*.h"))
        assert len(h_files) >= 5, \
            f"Expected at least 5 headers in datarouter/, found {len(h_files)}"

    @pytest.mark.parametrize("header", [
        "data_router.h",
        "file_transfer.h",
    ])
    def test_key_public_header_exists(self, header):
        """Key public headers must exist for downstream consumers."""
        matches = list(self.DATAROUTER.rglob(header))
        assert len(matches) > 0, \
            f"Public header {header} not found in score/datarouter/"


# ---------------------------------------------------------------------------
# TestScoreDependencies
# ---------------------------------------------------------------------------
class TestScoreDependencies:
    """Verify MODULE.bazel declares required S-CORE dependencies."""

    MODULE_BAZEL = LOGGING_DIR / "MODULE.bazel"

    def _content(self):
        return self.MODULE_BAZEL.read_text(encoding="utf-8")

    def test_declares_score_baselibs(self):
        assert re.search(r'bazel_dep\(\s*name\s*=\s*"score_baselibs"', self._content()), \
            "MODULE.bazel does not declare score_baselibs dependency"

    def test_score_baselibs_version(self):
        m = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_baselibs"\s*,\s*version\s*=\s*"([^"]+)"',
            self._content(),
        )
        assert m, "Cannot parse score_baselibs version"
        assert m.group(1) == "0.2.4", \
            f"Expected score_baselibs 0.2.4, found {m.group(1)}"

    def test_declares_score_communication(self):
        assert re.search(r'bazel_dep\(\s*name\s*=\s*"score_communication"', self._content()), \
            "MODULE.bazel does not declare score_communication dependency"

    def test_score_communication_version(self):
        m = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_communication"\s*,\s*version\s*=\s*"([^"]+)"',
            self._content(),
        )
        assert m, "Cannot parse score_communication version"
        assert m.group(1) == "0.1.2", \
            f"Expected score_communication 0.1.2, found {m.group(1)}"

    def test_declares_score_baselibs_rust(self):
        assert re.search(r'bazel_dep\(\s*name\s*=\s*"score_baselibs_rust"', self._content()), \
            "MODULE.bazel does not declare score_baselibs_rust — Rust bindings may break"

    def test_declares_score_bazel_platforms(self):
        assert re.search(r'bazel_dep\(\s*name\s*=\s*"score_bazel_platforms"', self._content()), \
            "MODULE.bazel does not declare score_bazel_platforms"

    def test_trlc_configured(self):
        """TRLC requirements traceability should be declared."""
        assert "trlc" in self._content().lower(), \
            "TRLC not referenced in MODULE.bazel — requirements traceability may be missing"


# ---------------------------------------------------------------------------
# TestBazelConfiguration
# ---------------------------------------------------------------------------
class TestBazelConfiguration:
    """Verify .bazelrc build configuration."""

    def test_bazelrc_exists(self):
        assert (LOGGING_DIR / ".bazelrc").exists(), \
            ".bazelrc not found — build configs missing"

    @pytest.mark.parametrize("config", ["x86_64-linux"])
    def test_bazelrc_has_config(self, config):
        path = LOGGING_DIR / ".bazelrc"
        if not path.exists():
            pytest.skip(".bazelrc not found")
        assert config in path.read_text(encoding="utf-8"), \
            f"Config '{config}' not found in .bazelrc"

    def test_top_level_build_file_exists(self):
        has_build = (LOGGING_DIR / "BUILD").exists() or (LOGGING_DIR / "BUILD.bazel").exists()
        assert has_build, "No top-level BUILD or BUILD.bazel in score-logging"

    def test_module_bazel_lock_exists(self):
        assert (LOGGING_DIR / "MODULE.bazel.lock").exists(), \
            "MODULE.bazel.lock not found — Bazel module dependencies not locked"
