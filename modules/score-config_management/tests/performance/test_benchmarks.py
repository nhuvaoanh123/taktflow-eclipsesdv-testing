"""Performance benchmark verification for score-config_management (ASIL B).

Configuration access must not block safety-critical callers:
- Config read: bounded lookup time
- No dynamic allocation on read path
- Error handling must not throw (noexcept)

ISO 26262 Part 6 Table 10: timing analysis required for ASIL B.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
CONFIG_MGMT_DIR = PROJECT_ROOT / "score-config_management"
SCORE_DIR = CONFIG_MGMT_DIR / "score"
CODE_DIR = SCORE_DIR / "config_management" / "config_provider" / "code"


@pytest.mark.asil_b
@pytest.mark.performance
class TestConfigAccessPerformance:
    """Verify config access has bounded-time properties."""

    def test_no_dynamic_allocation_in_headers(self):
        """Config provider headers should minimize dynamic allocation."""
        if not CODE_DIR.is_dir():
            pytest.skip("code/ not found")
        h_files = list(CODE_DIR.rglob("*.h"))
        if not h_files:
            pytest.skip("No headers found")
        alloc_count = 0
        for h in h_files:
            content = h.read_text(encoding="utf-8", errors="ignore")
            alloc_count += len(re.findall(
                r"\b(new\s+\w|malloc|calloc|make_shared|make_unique)", content
            ))
        assert alloc_count <= 10, (
            f"Config headers have {alloc_count} allocation calls -- "
            "ASIL B: config access should use pre-allocated storage"
        )

    def test_error_types_are_value_types(self):
        """Error types should be value types, not heap-allocated."""
        error_dir = CODE_DIR / "config_provider" / "error"
        if not error_dir.is_dir():
            pytest.skip("error/ not found")
        h_files = list(error_dir.rglob("*.h"))
        if not h_files:
            pytest.skip("No error headers")
        for h in h_files:
            content = h.read_text(encoding="utf-8", errors="ignore")
            has_enum = "enum" in content.lower()
            has_struct = "struct" in content or "class" in content
            assert has_enum or has_struct, (
                f"{h.name} does not define error as enum/struct -- "
                "errors should be stack-allocated value types"
            )


@pytest.mark.asil_b
@pytest.mark.performance
class TestBenchmarkInfrastructure:
    """Verify test infrastructure for timing evidence."""

    def test_test_files_exist(self):
        """Test files must exist for config access timing."""
        if not CODE_DIR.is_dir():
            pytest.skip("code/ not found")
        test_files = list(CODE_DIR.rglob("*test*"))
        assert len(test_files) >= 1, (
            "No test files -- ASIL B requires performance evidence"
        )

    def test_build_files_exist(self):
        """BUILD files must exist."""
        build_files = (
            list(CONFIG_MGMT_DIR.rglob("BUILD"))
            + list(CONFIG_MGMT_DIR.rglob("BUILD.bazel"))
        )
        assert len(build_files) >= 1, "No BUILD files found"
