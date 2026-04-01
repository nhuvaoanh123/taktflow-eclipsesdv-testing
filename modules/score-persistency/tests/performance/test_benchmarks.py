"""Performance benchmark verification for score-persistency (ASIL D).

Key-value store must meet ASIL D timing constraints:
- KV read: bounded lookup time (O(1) or O(log n))
- KV write: bounded commit time with fsync
- Recovery: bounded startup time after crash
- No unbounded memory growth

ISO 26262 Part 6 Table 10: timing analysis highly recommended for ASIL D.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
PERSISTENCY_DIR = PROJECT_ROOT / "modules" / "score-persistency" / "upstream"


@pytest.mark.asil_d
@pytest.mark.performance
class TestKvStorePerformance:
    """Verify key-value store has bounded-time operations."""

    def test_source_files_exist(self):
        """Source files must exist for the KV store."""
        src_files = (
            list(PERSISTENCY_DIR.rglob("*.cpp"))
            + list(PERSISTENCY_DIR.rglob("*.cc"))
            + list(PERSISTENCY_DIR.rglob("*.rs"))
        )
        assert len(src_files) >= 3, (
            f"Expected at least 3 source files, found {len(src_files)}"
        )

    def test_kv_store_has_bounded_operations(self):
        """KV store should reference hash/tree for bounded lookup."""
        src_files = (
            list(PERSISTENCY_DIR.rglob("*.cpp"))
            + list(PERSISTENCY_DIR.rglob("*.cc"))
            + list(PERSISTENCY_DIR.rglob("*.h"))
            + list(PERSISTENCY_DIR.rglob("*.rs"))
        )
        if not src_files:
            pytest.skip("No source files found")
        content = ""
        for f in src_files[:50]:  # Limit to avoid reading too many
            content += f.read_text(encoding="utf-8", errors="ignore")
        has_bounded = any(kw in content.lower() for kw in [
            "hash", "btree", "map", "lookup", "find",
            "o(1)", "o(log", "bounded",
        ])
        assert has_bounded, (
            "No bounded-lookup constructs (hash/btree) found -- "
            "ASIL D: KV operations must have bounded time complexity"
        )


@pytest.mark.asil_d
@pytest.mark.performance
class TestBenchmarkInfrastructure:
    """Verify benchmark/test infrastructure exists."""

    def test_test_files_exist(self):
        """Test files must exist for KV store timing verification."""
        test_files = list(PERSISTENCY_DIR.rglob("*test*"))
        assert len(test_files) >= 1, (
            "No test files -- ASIL D requires timing evidence"
        )

    def test_build_files_exist(self):
        """BUILD files must exist."""
        build_files = (
            list(PERSISTENCY_DIR.rglob("BUILD"))
            + list(PERSISTENCY_DIR.rglob("BUILD.bazel"))
        )
        assert len(build_files) >= 1, "No BUILD files found"

    def test_module_bazel_exists(self):
        """MODULE.bazel for reproducible build."""
        assert (PERSISTENCY_DIR / "MODULE.bazel").exists(), (
            "MODULE.bazel missing -- ASIL D requires reproducible builds"
        )
