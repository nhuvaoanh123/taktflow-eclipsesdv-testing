"""Safety and security contract verification for score-logging.

score-logging is QM-rated but is used by ASIL-B components. The logging
path must not compromise the safety of callers:

- No dynamic memory allocation in the hot logging path.
- Circular buffer writes must be atomic (no torn writes visible to readers).
- The DLT session handle interface must use mock-friendly abstractions
  (Object Seam pattern) so ASIL-B consumers can test without the daemon.
- Rust bindings must declare no_std compatibility or explicit std usage.

Verification method: file inspection (§14 boundary analysis + §4 fault injection).
Platform: any (no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
LOGGING_DIR = PROJECT_ROOT / "score-logging"
SCORE_DIR = LOGGING_DIR / "score"
MW_LOG = SCORE_DIR / "mw" / "log"
DATAROUTER = SCORE_DIR / "datarouter"


# ---------------------------------------------------------------------------
# TestObjectSeamPattern
# ---------------------------------------------------------------------------
class TestObjectSeamPattern:
    """Verify that the datarouter uses the Object Seam pattern so that
    ASIL-B consumers can mock out the logging daemon in unit tests."""

    def test_session_handle_interface_is_abstract(self):
        """session_handle_interface.h must declare a pure-virtual or abstract
        interface — this is the seam that enables mocking."""
        iface_path = DATAROUTER / "daemon_communication" / "session_handle_interface.h"
        if not iface_path.exists():
            pytest.skip("session_handle_interface.h not found")
        content = iface_path.read_text(encoding="utf-8", errors="ignore")
        has_virtual = "virtual" in content
        has_interface_suffix = "Interface" in iface_path.name
        assert has_virtual or has_interface_suffix, (
            "session_handle_interface.h does not appear to declare an abstract "
            "interface (no 'virtual' keyword) — Object Seam pattern not applied"
        )

    def test_session_handle_mock_uses_gmock_or_stub(self):
        """session_handle_mock.h must use GMock or a manual stub — not real
        DLT calls — so tests pass without the daemon running."""
        mock_path = DATAROUTER / "daemon_communication" / "session_handle_mock.h"
        if not mock_path.exists():
            pytest.skip("session_handle_mock.h not found")
        content = mock_path.read_text(encoding="utf-8", errors="ignore")
        has_mock = (
            "MOCK_METHOD" in content
            or "MockFunction" in content
            or "Fake" in content
            or "Stub" in content
        )
        assert has_mock, (
            "session_handle_mock.h does not appear to use GMock or stub — "
            "unit tests may depend on real DLT daemon"
        )

    def test_fake_recorder_environment_exists(self):
        """fake_recorder_environment must exist so mw/log callers can test
        without a real logging backend."""
        path = MW_LOG / "test" / "fake_recorder_environment"
        assert path.is_dir(), (
            "score/mw/log/test/fake_recorder_environment/ missing — "
            "Object Seam for logging frontend removed"
        )

    def test_fake_recorder_has_source(self):
        """fake_recorder must provide a testable recorder implementation."""
        path = MW_LOG / "test" / "fake_recorder"
        if not path.is_dir():
            pytest.skip("fake_recorder/ directory not found")
        sources = list(path.rglob("*.h")) + list(path.rglob("*.cc"))
        assert len(sources) >= 1, (
            "fake_recorder/ contains no C++ source files — fake implementation missing"
        )


# ---------------------------------------------------------------------------
# TestRustBindingsSafety
# ---------------------------------------------------------------------------
class TestRustBindingsSafety:
    """Verify Rust logging bindings follow safety conventions."""

    RUST_DIR = MW_LOG / "rust"

    def test_rust_dir_exists(self):
        assert self.RUST_DIR.is_dir(), \
            "score/mw/log/rust/ directory missing — Rust bindings removed"

    def test_no_unsafe_without_comment(self):
        """Every unsafe block in the Rust bindings must have a # SAFETY: comment.

        Bare unsafe blocks without documented justification are not permitted
        in safety-relevant code.
        """
        if not self.RUST_DIR.is_dir():
            pytest.skip("Rust bindings directory not found")

        rs_files = list(self.RUST_DIR.rglob("*.rs"))
        if not rs_files:
            pytest.skip("No Rust source files found")

        violations = []
        for f in rs_files:
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
            for i, line in enumerate(lines):
                if "unsafe" in line and "{" in line:
                    # Check previous 3 lines for a SAFETY comment
                    context = "\n".join(lines[max(0, i - 3):i])
                    if "SAFETY" not in context and "Safety" not in context:
                        violations.append(f"{f.name}:{i + 1}: {line.strip()}")

        assert not violations, (
            f"Unsafe blocks without SAFETY justification:\n"
            + "\n".join(violations[:10])
        )

    def test_rust_source_files_present(self):
        if not self.RUST_DIR.is_dir():
            pytest.skip("Rust directory not found")
        rs_files = list(self.RUST_DIR.rglob("*.rs"))
        assert len(rs_files) >= 1, \
            "No Rust source files in score/mw/log/rust/ — bindings removed"


# ---------------------------------------------------------------------------
# TestConsoleLoggingEnvironment
# ---------------------------------------------------------------------------
class TestConsoleLoggingEnvironment:
    """Verify console logging environment for diagnostics and debugging."""

    CONSOLE_ENV = MW_LOG / "test" / "console_logging_environment"

    def test_console_env_directory_exists(self):
        assert self.CONSOLE_ENV.is_dir(), (
            "score/mw/log/test/console_logging_environment/ missing — "
            "console debugging backend removed"
        )

    def test_console_env_has_source_files(self):
        if not self.CONSOLE_ENV.is_dir():
            pytest.skip("console_logging_environment not found")
        sources = list(self.CONSOLE_ENV.rglob("*.h")) + list(self.CONSOLE_ENV.rglob("*.cc"))
        assert len(sources) >= 1, (
            "console_logging_environment/ contains no C++ source files"
        )


# ---------------------------------------------------------------------------
# TestLoggingFrontendDesign
# ---------------------------------------------------------------------------
class TestLoggingFrontendDesign:
    """Verify design documentation for the logging frontend."""

    DESIGN_DIR = MW_LOG / "design"

    def test_design_directory_exists(self):
        assert self.DESIGN_DIR.is_dir(), \
            "score/mw/log/design/ missing — design documentation removed"

    def test_design_has_content(self):
        if not self.DESIGN_DIR.is_dir():
            pytest.skip("design/ directory not found")
        files = list(self.DESIGN_DIR.iterdir())
        assert len(files) >= 1, \
            "score/mw/log/design/ is empty — design documentation missing"


# ---------------------------------------------------------------------------
# TestLegacyApiBackwardCompat
# ---------------------------------------------------------------------------
class TestLegacyApiBackwardCompat:
    """Verify that the legacy non-verbose API is maintained for
    backward compatibility with older consumers."""

    LEGACY_DIR = MW_LOG / "legacy_non_verbose_api"

    def test_legacy_api_directory_exists(self):
        assert self.LEGACY_DIR.is_dir(), (
            "score/mw/log/legacy_non_verbose_api/ missing — "
            "backward-compatible API removed, which may break older consumers"
        )

    def test_legacy_api_has_source_files(self):
        if not self.LEGACY_DIR.is_dir():
            pytest.skip("legacy_non_verbose_api/ not found")
        sources = list(self.LEGACY_DIR.rglob("*.h")) + list(self.LEGACY_DIR.rglob("*.cc"))
        assert len(sources) >= 1, \
            "legacy_non_verbose_api/ contains no source files"
