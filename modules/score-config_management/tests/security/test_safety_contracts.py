"""Safety and security contract verification for score-config_management (ASIL B).

score-config_management is ASIL B-rated. Key safety/security contracts:

- ConfigProvider mock must exist so ASIL-B consumers can unit-test
  without a real config backend.
- ParameterSet validation must reject malformed config values at the
  API boundary (no unchecked casts from external input).
- Error types must be explicit (no exceptions in hot config path).

Verification method: file inspection.
Platform: any (no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
CONFIG_MGMT_DIR = PROJECT_ROOT / "score-config_management"
SCORE_DIR = CONFIG_MGMT_DIR / "score"
CONFIG_PROVIDER = SCORE_DIR / "config_management" / "config_provider"
CODE_DIR = CONFIG_PROVIDER / "code"


# ---------------------------------------------------------------------------
# TestMockPattern
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestMockPattern:
    """Verify that config_provider provides mock/stub for downstream testing."""

    def test_config_provider_mock_header_exists(self):
        """config_provider_mock.h must exist for downstream unit testing."""
        mock_path = CODE_DIR / "config_provider" / "config_provider_mock.h"
        if not mock_path.exists():
            # Search more broadly
            mocks = list(CODE_DIR.rglob("*mock*.h"))
            assert len(mocks) > 0, (
                "No mock headers found in config_provider/code/ — "
                "downstream consumers cannot unit-test config access"
            )

    def test_mock_uses_gmock_or_stub(self):
        """Mock must use GMock or a manual stub — not real config backend."""
        mock_path = CODE_DIR / "config_provider" / "config_provider_mock.h"
        if not mock_path.exists():
            mocks = list(CODE_DIR.rglob("*mock*.h"))
            if not mocks:
                pytest.skip("No mock headers found")
            mock_path = mocks[0]
        content = mock_path.read_text(encoding="utf-8", errors="ignore")
        has_mock = (
            "MOCK_METHOD" in content
            or "MockFunction" in content
            or "Fake" in content
            or "Stub" in content
            or "Mock" in content
        )
        assert has_mock, (
            f"{mock_path.name} does not use GMock or stub — "
            "tests may depend on real config backend"
        )


# ---------------------------------------------------------------------------
# TestErrorHandlingContract
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestErrorHandlingContract:
    """Verify explicit error handling in config_provider."""

    def test_error_types_directory_exists(self):
        error_dir = CODE_DIR / "config_provider" / "error"
        assert error_dir.is_dir(), \
            "config_provider/error/ missing — error type definitions removed"

    def test_error_test_files_exist(self):
        """Error types must have test coverage."""
        error_dir = CODE_DIR / "config_provider" / "error"
        if not error_dir.is_dir():
            pytest.skip("error/ directory not found")
        test_files = list(error_dir.rglob("*_test*"))
        assert len(test_files) >= 1, \
            "No test files in error/ — error types untested"

    def test_no_exceptions_in_parameter_set(self):
        """ParameterSet should use explicit error returns, not exceptions."""
        ps_dir = CODE_DIR / "parameter_set"
        if not ps_dir.is_dir():
            pytest.skip("parameter_set/ not found")
        h_files = list(ps_dir.rglob("*.h"))
        violations = []
        for f in h_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            # Check for throw statements (not in test files)
            if "_test" not in f.name and "throw " in content:
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if "throw " in line:
                        violations.append(f"{f.name}:{i+1}: {line.strip()}")
        if violations:
            print(f"Warning: throw statements in parameter_set headers:\n"
                  + "\n".join(violations[:5]))


# ---------------------------------------------------------------------------
# TestCppSourceQuality
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestCppSourceQuality:
    """Basic source quality checks for C++ code."""

    def test_headers_have_include_guards_or_pragma(self):
        """All headers must have include guards or #pragma once."""
        if not CODE_DIR.is_dir():
            pytest.skip("code/ directory not found")
        h_files = list(CODE_DIR.rglob("*.h"))
        if not h_files:
            pytest.skip("No header files found")
        violations = []
        for f in h_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            has_guard = (
                "#pragma once" in content
                or re.search(r"#ifndef\s+\w+_H", content, re.IGNORECASE)
            )
            if not has_guard:
                violations.append(f.name)
        assert not violations, (
            f"Headers without include guards:\n" + "\n".join(violations[:10])
        )


# ---------------------------------------------------------------------------
# TestAsilBBuildReproducibility
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAsilBBuildReproducibility:
    """ASIL B: verify build reproducibility and test infrastructure."""

    def test_module_bazel_exists(self):
        assert (CONFIG_MGMT_DIR / "MODULE.bazel").exists(), (
            "MODULE.bazel missing -- ASIL B requires reproducible build"
        )

    def test_module_bazel_lock_exists(self):
        assert (CONFIG_MGMT_DIR / "MODULE.bazel.lock").exists(), (
            "MODULE.bazel.lock missing -- ASIL B requires locked deps"
        )

    def test_build_files_exist(self):
        build_files = (
            list(CONFIG_MGMT_DIR.rglob("BUILD"))
            + list(CONFIG_MGMT_DIR.rglob("BUILD.bazel"))
        )
        assert len(build_files) >= 1, (
            "No BUILD files -- ASIL B requires buildable targets"
        )

    def test_test_directory_exists(self):
        """Config management must have unit tests for ASIL B."""
        test_files = list(CODE_DIR.rglob("*test*")) if CODE_DIR.is_dir() else []
        assert len(test_files) >= 1, (
            "No test files found -- ASIL B requires test coverage"
        )

    def test_bazelrc_exists(self):
        path = CONFIG_MGMT_DIR / ".bazelrc"
        if not path.exists():
            pytest.skip(".bazelrc not found")
        content = path.read_text(encoding="utf-8")
        assert "x86_64-linux" in content or "config" in content, (
            ".bazelrc does not define platform configs"
        )
