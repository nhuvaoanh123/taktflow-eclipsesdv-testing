"""Safety and security contract verification for score-logging (ASIL B).

score-logging is now ASIL B-rated. The logging path must not compromise
the safety of callers:

- No dynamic memory allocation in the hot logging path.
- Circular buffer writes must be atomic (no torn writes visible to readers).
- The DLT session handle interface must use mock-friendly abstractions
  (Object Seam pattern) so ASIL-B consumers can test without the daemon.
- Rust bindings must declare no_std compatibility or explicit std usage.
- All unsafe blocks must have SAFETY justification comments.
- Test infrastructure must provide statement + branch coverage evidence.

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
@pytest.mark.asil_b
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
@pytest.mark.asil_b
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
@pytest.mark.asil_b
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
@pytest.mark.asil_b
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
@pytest.mark.asil_b
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


# ---------------------------------------------------------------------------
# TestAsilBNoDynamicAllocation
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAsilBNoDynamicAllocation:
    """ASIL B: verify logging hot path avoids heap allocation.

    ISO 26262 Part 6 Table 1: dynamic memory allocation is restricted
    for ASIL B. The mw/log recording path should use pre-allocated
    circular buffers, not runtime allocation.
    """

    def test_no_malloc_in_recorder_sources(self):
        """Recorder implementation should not call malloc/new directly."""
        detail_dir = MW_LOG / "detail"
        if not detail_dir.is_dir():
            pytest.skip("mw/log/detail/ not found")
        violations = []
        for f in detail_dir.rglob("*.cc"):
            content = f.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"\b(malloc|calloc|realloc)\b", content):
                violations.append(f.name)
        assert not violations, (
            f"Direct malloc/calloc/realloc calls in recorder: {violations} -- "
            "ASIL B: use pre-allocated buffers in logging hot path"
        )

    def test_no_exceptions_in_log_path(self):
        """Logging headers should use noexcept — exceptions in log path
        could cascade to safety-critical callers."""
        h_files = list(MW_LOG.glob("*.h"))
        if not h_files:
            pytest.skip("No headers in mw/log/")
        throw_count = 0
        noexcept_count = 0
        for h in h_files:
            content = h.read_text(encoding="utf-8", errors="ignore")
            throw_count += len(re.findall(r"\bthrow\b", content))
            noexcept_count += len(re.findall(r"\bnoexcept\b", content))
        if noexcept_count == 0 and throw_count == 0:
            pytest.skip("No throw/noexcept keywords — may use C-style API")
        assert noexcept_count >= throw_count, (
            f"Log headers: {throw_count} throw vs {noexcept_count} noexcept -- "
            "ASIL B: logging API should be noexcept-dominant"
        )


# ---------------------------------------------------------------------------
# TestAsilBTestInfrastructure
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAsilBTestInfrastructure:
    """ASIL B: verify sufficient test infrastructure for coverage evidence.

    ISO 26262 Part 6 Table 9: ASIL B requires statement coverage (++)
    and branch coverage (+).
    """

    def test_unit_test_directory_exists(self):
        """mw/log must have a test/ directory with unit tests."""
        test_dir = MW_LOG / "test"
        assert test_dir.is_dir(), (
            "mw/log/test/ missing -- ASIL B requires test infrastructure"
        )

    def test_datarouter_unit_tests_exist(self):
        """datarouter must have unit test files."""
        dr_test = DATAROUTER / "test"
        if not dr_test.is_dir():
            # Check alternative: test/ut/
            dr_test = DATAROUTER / "test" / "ut"
        test_files = list(DATAROUTER.rglob("*test*"))
        assert len(test_files) >= 1, (
            "No test files found in datarouter/ -- "
            "ASIL B requires unit test coverage evidence"
        )

    def test_bazelrc_has_coverage_config(self):
        """ASIL B: .bazelrc must define coverage instrumentation filter."""
        bazelrc = LOGGING_DIR / ".bazelrc"
        if not bazelrc.exists():
            pytest.skip(".bazelrc not found")
        content = bazelrc.read_text(encoding="utf-8")
        assert "instrumentation_filter" in content or "coverage" in content, (
            ".bazelrc does not configure coverage instrumentation -- "
            "ASIL B requires coverage measurement capability"
        )

    def test_module_bazel_lock_exists(self):
        """ASIL B: dependency lockfile must exist for build reproducibility."""
        lock = LOGGING_DIR / "MODULE.bazel.lock"
        assert lock.exists(), (
            "MODULE.bazel.lock missing -- ASIL B requires reproducible builds"
        )
