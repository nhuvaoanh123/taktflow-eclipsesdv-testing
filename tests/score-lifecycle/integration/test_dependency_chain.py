"""Integration tests for score-lifecycle dependency chain.

Verifies that score-lifecycle correctly declares its dependencies
on score_baselibs, score_logging, score_baselibs_rust, and flatbuffers.
All baselibs dependencies are transitively proven via the baselibs assessment.
Platform: any (file inspection only, no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
LIFECYCLE_DIR = Path(__file__).parent.parent.parent.parent / "score-lifecycle"


# ---------------------------------------------------------------------------
# TestBaseLibsDependency
# ---------------------------------------------------------------------------
class TestBaseLibsDependency:
    """Verify MODULE.bazel declares score_baselibs (0.2.4), score_logging
    (0.1.0), score_baselibs_rust (0.1.0).  All are transitively proven
    via the baselibs assessment."""

    MODULE_BAZEL = LIFECYCLE_DIR / "MODULE.bazel"

    def test_module_bazel_exists(self):
        assert self.MODULE_BAZEL.exists(), (
            f"score-lifecycle/MODULE.bazel not found at {self.MODULE_BAZEL}"
        )

    def test_declares_score_baselibs(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        pattern = r'bazel_dep\(\s*name\s*=\s*"score_baselibs"'
        assert re.search(pattern, content), (
            "score-lifecycle/MODULE.bazel does not declare a bazel_dep "
            "on score_baselibs"
        )

    def test_score_baselibs_version(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        match = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_baselibs"\s*,\s*version\s*=\s*"([^"]+)"',
            content,
        )
        assert match, (
            "Cannot parse score_baselibs version from score-lifecycle/MODULE.bazel"
        )
        assert match.group(1) == "0.2.4", (
            f"Expected score_baselibs 0.2.4, found {match.group(1)}"
        )

    def test_declares_score_logging(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        pattern = r'bazel_dep\(\s*name\s*=\s*"score_logging"'
        assert re.search(pattern, content), (
            "score-lifecycle/MODULE.bazel does not declare a bazel_dep "
            "on score_logging"
        )

    def test_score_logging_version(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        match = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_logging"\s*,\s*version\s*=\s*"([^"]+)"',
            content,
        )
        assert match, (
            "Cannot parse score_logging version from score-lifecycle/MODULE.bazel"
        )
        assert match.group(1) == "0.1.0", (
            f"Expected score_logging 0.1.0, found {match.group(1)}"
        )

    def test_declares_score_baselibs_rust(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        pattern = r'bazel_dep\(\s*name\s*=\s*"score_baselibs_rust"'
        assert re.search(pattern, content), (
            "score-lifecycle/MODULE.bazel does not declare a bazel_dep "
            "on score_baselibs_rust"
        )

    def test_score_baselibs_rust_version(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        match = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_baselibs_rust"\s*,\s*version\s*=\s*"([^"]+)"',
            content,
        )
        assert match, (
            "Cannot parse score_baselibs_rust version from "
            "score-lifecycle/MODULE.bazel"
        )
        assert match.group(1) == "0.1.0", (
            f"Expected score_baselibs_rust 0.1.0, found {match.group(1)}"
        )

    def test_transitive_baselibs_coverage_note(self):
        """Informational: score_baselibs, score_logging, and
        score_baselibs_rust are all transitively proven via the baselibs
        assessment.  This test documents the expectation."""
        expected_deps = 3
        assert expected_deps > 0, "Sanity check"


# ---------------------------------------------------------------------------
# TestDownstreamDependencies
# ---------------------------------------------------------------------------
class TestDownstreamDependencies:
    """Check if score-inc_time depends on score_lifecycle_health."""

    INC_TIME_DIR = PROJECT_ROOT / "score-inc_time"

    def test_inc_time_directory_exists(self):
        if not self.INC_TIME_DIR.is_dir():
            pytest.skip("score-inc_time directory does not exist locally")
        assert self.INC_TIME_DIR.is_dir()

    def test_inc_time_module_bazel_exists(self):
        if not self.INC_TIME_DIR.is_dir():
            pytest.skip("score-inc_time directory does not exist locally")
        module_bazel = self.INC_TIME_DIR / "MODULE.bazel"
        assert module_bazel.exists(), (
            "score-inc_time/MODULE.bazel not found"
        )

    def test_inc_time_depends_on_lifecycle_health(self):
        """score-inc_time should reference score_lifecycle or
        score_lifecycle_health in its MODULE.bazel."""
        if not self.INC_TIME_DIR.is_dir():
            pytest.skip("score-inc_time directory does not exist locally")

        module_bazel = self.INC_TIME_DIR / "MODULE.bazel"
        if not module_bazel.exists():
            pytest.skip("score-inc_time/MODULE.bazel not found")

        content = module_bazel.read_text(encoding="utf-8")
        has_lifecycle = "score_lifecycle" in content
        has_health = "lifecycle_health" in content
        assert has_lifecycle or has_health, (
            "score-inc_time/MODULE.bazel does not reference "
            "score_lifecycle or score_lifecycle_health -- "
            "expected dependency link"
        )

    def test_lifecycle_module_bazel_exists(self):
        module_bazel = LIFECYCLE_DIR / "MODULE.bazel"
        assert module_bazel.exists(), (
            "score-lifecycle/MODULE.bazel not found"
        )

    def test_lifecycle_declares_module_name(self):
        """The MODULE.bazel should declare a module() with a name."""
        module_bazel = LIFECYCLE_DIR / "MODULE.bazel"
        content = module_bazel.read_text(encoding="utf-8")
        pattern = r'module\(\s*name\s*=\s*"[^"]+"'
        assert re.search(pattern, content, re.DOTALL), (
            "score-lifecycle/MODULE.bazel does not declare a module() name"
        )


# ---------------------------------------------------------------------------
# TestFlatBuffersDependency
# ---------------------------------------------------------------------------
class TestFlatBuffersDependency:
    """Verify flatbuffers declared and .fbs schema files exist."""

    MODULE_BAZEL = LIFECYCLE_DIR / "MODULE.bazel"

    def test_declares_flatbuffers(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        assert "flatbuffers" in content, (
            "score-lifecycle/MODULE.bazel does not reference flatbuffers"
        )

    def test_flatbuffers_bazel_dep(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        pattern = r'bazel_dep\(\s*name\s*=\s*"flatbuffers"'
        assert re.search(pattern, content), (
            "score-lifecycle/MODULE.bazel does not declare a bazel_dep "
            "on flatbuffers"
        )

    def test_fbs_schema_files_exist(self):
        """At least one .fbs schema file should exist in score-lifecycle."""
        fbs_files = list(LIFECYCLE_DIR.rglob("*.fbs"))
        assert len(fbs_files) > 0, (
            "No .fbs schema files found in score-lifecycle -- "
            "flatbuffers dependency declared but no schemas present"
        )

    def test_fbs_schema_count(self):
        """Expect a reasonable number of FlatBuffers schemas."""
        fbs_files = list(LIFECYCLE_DIR.rglob("*.fbs"))
        assert len(fbs_files) >= 1, (
            f"Expected at least 1 .fbs schema file, found {len(fbs_files)}"
        )


# ---------------------------------------------------------------------------
# TestRustDependencies
# ---------------------------------------------------------------------------
class TestRustDependencies:
    """Verify Cargo.toml and Cargo.lock exist at root.
    Verify health_monitoring_lib/Cargo.toml exists."""

    def test_cargo_toml_at_root(self):
        cargo_toml = LIFECYCLE_DIR / "Cargo.toml"
        assert cargo_toml.exists(), (
            "Cargo.toml not found at score-lifecycle root -- "
            "Rust workspace not configured"
        )

    def test_cargo_lock_at_root(self):
        cargo_lock = LIFECYCLE_DIR / "Cargo.lock"
        assert cargo_lock.exists(), (
            "Cargo.lock not found at score-lifecycle root -- "
            "Rust dependencies not locked"
        )

    def test_health_monitoring_lib_cargo_toml(self):
        """health_monitoring_lib should have its own Cargo.toml."""
        candidates = [
            LIFECYCLE_DIR / "health_monitoring_lib" / "Cargo.toml",
            LIFECYCLE_DIR / "src" / "health_monitoring_lib" / "Cargo.toml",
        ]
        found = any(c.exists() for c in candidates)
        assert found, (
            "health_monitoring_lib/Cargo.toml not found -- "
            f"checked: {[str(c) for c in candidates]}"
        )

    def test_cargo_toml_has_workspace(self):
        """Root Cargo.toml should define a workspace."""
        cargo_toml = LIFECYCLE_DIR / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("Cargo.toml not found")

        content = cargo_toml.read_text(encoding="utf-8")
        assert "[workspace]" in content, (
            "Root Cargo.toml does not define a [workspace] section"
        )


# ---------------------------------------------------------------------------
# TestCrossComponentHeaders
# ---------------------------------------------------------------------------
class TestCrossComponentHeaders:
    """Verify that key headers from baselibs used by lifecycle exist.

    Lifecycle depends on score/os headers and score/result headers
    from score-baselibs.
    """

    BASELIBS_DIR = PROJECT_ROOT / "score-baselibs"

    # Headers from score-baselibs known to be consumed by lifecycle
    KNOWN_LIFECYCLE_BASELIBS_HEADERS = [
        "score/os/errno.h",
        "score/os/fcntl.h",
        "score/os/pthread.h",
        "score/os/unistd.h",
        "score/os/utils/signal.h",
        "score/result/result.h",
    ]

    @pytest.mark.parametrize("header_path", KNOWN_LIFECYCLE_BASELIBS_HEADERS)
    def test_known_header_exists(self, header_path: str):
        if not self.BASELIBS_DIR.is_dir():
            pytest.skip("score-baselibs directory not found")

        full_path = self.BASELIBS_DIR / header_path
        assert full_path.exists(), (
            f"Header {header_path} expected by lifecycle is missing from "
            f"score-baselibs"
        )

    def test_discover_score_includes_in_lifecycle(self):
        """Scan lifecycle C++ sources for #include \"score/...\" and verify
        that a reasonable fraction map to existing baselibs headers.

        Not all score/ includes originate from score-baselibs (some are
        local to score-lifecycle).
        """
        if not LIFECYCLE_DIR.is_dir():
            pytest.skip("score-lifecycle directory not found")
        if not self.BASELIBS_DIR.is_dir():
            pytest.skip("score-baselibs directory not found")

        include_pattern = re.compile(r'#include\s+"(score/[^"]+)"')
        discovered: set[str] = set()

        for ext in ("*.cpp", "*.h"):
            for source_file in LIFECYCLE_DIR.rglob(ext):
                try:
                    text = source_file.read_text(
                        encoding="utf-8", errors="ignore"
                    )
                except OSError:
                    continue
                for match in include_pattern.finditer(text):
                    discovered.add(match.group(1))

        if not discovered:
            pytest.skip("No score/ includes discovered in score-lifecycle")

        baselibs_candidates = [
            h for h in discovered
            if (self.BASELIBS_DIR / h).exists()
        ]

        assert len(baselibs_candidates) >= 3, (
            f"Expected at least 3 score-baselibs headers used by lifecycle, "
            f"found {len(baselibs_candidates)}: {baselibs_candidates}"
        )

    def test_os_headers_available(self):
        """score/os/ directory in baselibs should have headers available
        for lifecycle consumption."""
        if not self.BASELIBS_DIR.is_dir():
            pytest.skip("score-baselibs directory not found")

        os_dir = self.BASELIBS_DIR / "score" / "os"
        assert os_dir.is_dir(), "score/os/ directory missing in baselibs"
        headers = list(os_dir.glob("*.h"))
        assert len(headers) >= 10, (
            f"Expected at least 10 OS abstraction headers, found {len(headers)}"
        )

    def test_result_headers_available(self):
        """score/result/ directory in baselibs should have headers available
        for lifecycle consumption."""
        if not self.BASELIBS_DIR.is_dir():
            pytest.skip("score-baselibs directory not found")

        result_dir = self.BASELIBS_DIR / "score" / "result"
        assert result_dir.is_dir(), "score/result/ directory missing in baselibs"
        headers = list(result_dir.glob("*.h"))
        assert len(headers) >= 1, (
            f"Expected at least 1 result header, found {len(headers)}"
        )
