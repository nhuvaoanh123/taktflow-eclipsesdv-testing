"""Integration tests for score-logging dependency chain.

Verifies that score-logging is correctly declared as a dependency by
downstream S-CORE modules (score-feo, score-persistency, score-lifecycle),
and that the logging frontend headers used by those modules exist.

Platform: any (file inspection only, no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
LOGGING_DIR = PROJECT_ROOT / "score-logging"
SCORE_DIR = LOGGING_DIR / "score"


# ---------------------------------------------------------------------------
# TestDownstreamModulesReferenceLogging
# ---------------------------------------------------------------------------
class TestDownstreamModulesReferenceLogging:
    """Verify that modules which depend on logging declare score_logging
    in their MODULE.bazel."""

    @pytest.mark.parametrize("module_name", [
        "score-feo",
        "score-baselibs",
    ])
    def test_module_references_score_logging(self, module_name):
        """Downstream S-CORE modules must declare score_logging dependency."""
        module_dir = PROJECT_ROOT / module_name
        if not module_dir.is_dir():
            pytest.skip(f"{module_name} directory not found locally")

        module_bazel = module_dir / "MODULE.bazel"
        if not module_bazel.exists():
            pytest.skip(f"{module_name}/MODULE.bazel not found")

        content = module_bazel.read_text(encoding="utf-8")
        assert "score_logging" in content, (
            f"{module_name}/MODULE.bazel does not reference score_logging -- "
            "dependency link broken"
        )


# ---------------------------------------------------------------------------
# TestLoggingHeadersAccessible
# ---------------------------------------------------------------------------
class TestLoggingHeadersAccessible:
    """Verify that logging frontend headers are accessible for include resolution."""

    MW_LOG = SCORE_DIR / "mw" / "log"

    def test_mw_log_directory_accessible(self):
        assert self.MW_LOG.is_dir(), \
            "score/mw/log/ directory not accessible from test runner path"

    @pytest.mark.parametrize("expected_path_fragment", [
        "mw/log",
    ])
    def test_header_path_fragment_reachable(self, expected_path_fragment):
        """Headers under score/mw/log/ should be reachable as score/mw/log/*."""
        h_files = list(self.MW_LOG.rglob("*.h"))
        assert len(h_files) > 0, \
            f"No headers found under score/{expected_path_fragment}/ — path unreachable"


# ---------------------------------------------------------------------------
# TestMwLogToDatarouterIntegration
# ---------------------------------------------------------------------------
class TestMwLogToDatarouterIntegration:
    """Verify integration between mw/log frontend and datarouter backend.

    score/mw/log writes to a circular shared-memory buffer. score/datarouter
    reads that buffer and routes records to DLT. The two components must
    agree on the session handle interface.
    """

    DATAROUTER = SCORE_DIR / "datarouter"
    MW_LOG = SCORE_DIR / "mw" / "log"

    def test_session_handle_interface_exists(self):
        """Session handle interface must exist in datarouter/daemon_communication."""
        iface = self.DATAROUTER / "daemon_communication" / "session_handle_interface.h"
        assert iface.exists(), \
            "session_handle_interface.h missing — mw/log↔datarouter contract broken"

    def test_session_handle_mock_exists(self):
        """Mock for session handle must exist to enable unit testing."""
        mock = self.DATAROUTER / "daemon_communication" / "session_handle_mock.h"
        assert mock.exists(), \
            "session_handle_mock.h missing — cannot unit test mw/log without mock"

    def test_filetransfer_interface_exists(self):
        """File transfer interface must exist in dlt_filetransfer_trigger_lib."""
        iface_dir = self.DATAROUTER / "dlt_filetransfer_trigger_lib" / "include"
        if not iface_dir.is_dir():
            pytest.skip("dlt_filetransfer_trigger_lib/include/ not found")
        h_files = list(iface_dir.rglob("*.h"))
        assert len(h_files) >= 1, \
            "No headers in dlt_filetransfer_trigger_lib/include/ — interface removed"

    def test_datarouter_datarouter_subdir_has_sources(self):
        """datarouter/ subdirectory must contain the daemon implementation."""
        dr_dir = self.DATAROUTER / "datarouter"
        if not dr_dir.is_dir():
            pytest.skip("score/datarouter/datarouter/ not found")
        h_files = list(dr_dir.rglob("*.h"))
        assert len(h_files) >= 1, \
            "No headers in datarouter/datarouter/ — daemon implementation missing"


# ---------------------------------------------------------------------------
# TestBazelRegistryEntry
# ---------------------------------------------------------------------------
class TestBazelRegistryEntry:
    """Verify score-bazel_registry contains an entry for score_logging."""

    REGISTRY_DIR = PROJECT_ROOT / "score-bazel_registry"

    def test_registry_exists(self):
        assert self.REGISTRY_DIR.is_dir(), \
            "score-bazel_registry not found — cannot verify registry entry"

    def test_score_logging_module_dir_exists(self):
        module_dir = self.REGISTRY_DIR / "modules" / "score_logging"
        assert module_dir.is_dir(), \
            "score_logging module directory not found in score-bazel_registry/modules/"

    def test_metadata_json_exists(self):
        metadata = self.REGISTRY_DIR / "modules" / "score_logging" / "metadata.json"
        assert metadata.exists(), \
            "metadata.json not found for score_logging in Bazel registry"

    def test_registry_has_version_entries(self):
        module_dir = self.REGISTRY_DIR / "modules" / "score_logging"
        if not module_dir.is_dir():
            pytest.skip("score_logging registry module dir missing")
        version_dirs = [
            d for d in module_dir.iterdir()
            if d.is_dir() and re.match(r"\d+\.\d+\.\d+", d.name)
        ]
        assert len(version_dirs) > 0, \
            "No version directories found in registry for score_logging"
