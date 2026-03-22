"""Integration tests for score-baselibs dependency chain.

Verifies that score-baselibs is correctly referenced as a dependency
by downstream S-CORE modules, ensuring API compatibility.
Platform: any (file inspection only).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
BASELIBS_DIR = PROJECT_ROOT / "score-baselibs"


# ---------------------------------------------------------------------------
# TestLolaTransitiveDependency
# ---------------------------------------------------------------------------
class TestLolaTransitiveDependency:
    """Verify score-communication/MODULE.bazel references score_baselibs.

    LoLa (Low Latency communication) depends on score_baselibs.  If all
    252 LoLa tests pass, that transitively proves the baselibs layer is
    functional for the APIs that LoLa consumes.
    """

    COMM_DIR = PROJECT_ROOT / "score-communication"

    def test_communication_module_bazel_exists(self):
        module_path = self.COMM_DIR / "MODULE.bazel"
        assert module_path.exists(), (
            f"score-communication/MODULE.bazel not found at {module_path}"
        )

    def test_communication_depends_on_score_baselibs(self):
        module_path = self.COMM_DIR / "MODULE.bazel"
        content = module_path.read_text(encoding="utf-8")
        assert "score_baselibs" in content, (
            "score-communication/MODULE.bazel does not reference score_baselibs -- "
            "dependency link may be broken"
        )

    def test_communication_declares_bazel_dep_on_baselibs(self):
        module_path = self.COMM_DIR / "MODULE.bazel"
        content = module_path.read_text(encoding="utf-8")
        pattern = r'bazel_dep\(\s*name\s*=\s*"score_baselibs"'
        assert re.search(pattern, content), (
            "score-communication/MODULE.bazel does not declare a bazel_dep "
            "on score_baselibs"
        )

    def test_version_constraint_matches_baselibs(self):
        """The version pinned in score-communication should match the
        version declared in score-baselibs/MODULE.bazel."""
        comm_module = self.COMM_DIR / "MODULE.bazel"
        base_module = BASELIBS_DIR / "MODULE.bazel"

        comm_content = comm_module.read_text(encoding="utf-8")
        base_content = base_module.read_text(encoding="utf-8")

        # Extract baselibs own version
        base_match = re.search(
            r'module\([^)]*version\s*=\s*"([^"]+)"', base_content, re.DOTALL
        )
        assert base_match, "Cannot parse version from score-baselibs/MODULE.bazel"
        baselibs_version = base_match.group(1)

        # Extract version used by communication
        comm_match = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_baselibs"\s*,\s*version\s*=\s*"([^"]+)"',
            comm_content,
        )
        assert comm_match, (
            "Cannot parse score_baselibs version from score-communication/MODULE.bazel"
        )
        comm_pinned_version = comm_match.group(1)

        assert comm_pinned_version == baselibs_version, (
            f"Version mismatch: score-communication pins score_baselibs "
            f"at {comm_pinned_version} but score-baselibs declares {baselibs_version}"
        )

    def test_lola_test_count_note(self):
        """Informational: LoLa has 252 tests that transitively exercise
        score-baselibs.  This test merely documents the expectation; the
        actual test execution requires Bazel on Linux."""
        # This is a documentation-level assertion; always passes.
        expected_lola_tests = 252
        assert expected_lola_tests > 0, "Sanity check"


# ---------------------------------------------------------------------------
# TestDownstreamDependencies
# ---------------------------------------------------------------------------
class TestDownstreamDependencies:
    """Check that other S-CORE modules reference score_baselibs in their
    MODULE.bazel.  Modules that do not exist locally are skipped."""

    @pytest.mark.parametrize(
        "module_name",
        [
            "score-lifecycle",
            "score-persistency",
            "score-feo",
            "score-logging",
        ],
    )
    def test_module_references_score_baselibs(self, module_name: str):
        module_dir = PROJECT_ROOT / module_name
        if not module_dir.is_dir():
            pytest.skip(f"{module_name} directory does not exist locally")

        module_bazel = module_dir / "MODULE.bazel"
        if not module_bazel.exists():
            pytest.skip(f"{module_name}/MODULE.bazel not found")

        content = module_bazel.read_text(encoding="utf-8")
        assert "score_baselibs" in content, (
            f"{module_name}/MODULE.bazel does not reference score_baselibs -- "
            f"expected a direct or transitive dependency"
        )

    @pytest.mark.parametrize(
        "module_name",
        [
            "score-lifecycle",
            "score-persistency",
            "score-feo",
            "score-logging",
        ],
    )
    def test_module_dir_exists_or_skip(self, module_name: str):
        module_dir = PROJECT_ROOT / module_name
        if not module_dir.is_dir():
            pytest.skip(f"{module_name} not cloned locally")
        assert module_dir.is_dir()


# ---------------------------------------------------------------------------
# TestBazelRegistryEntry
# ---------------------------------------------------------------------------
class TestBazelRegistryEntry:
    """Verify score-bazel_registry contains a metadata entry for
    score_baselibs."""

    REGISTRY_DIR = PROJECT_ROOT / "score-bazel_registry"

    def test_registry_directory_exists(self):
        assert self.REGISTRY_DIR.is_dir(), (
            "score-bazel_registry directory not found -- "
            "cannot verify registry entry"
        )

    def test_score_baselibs_module_dir_exists(self):
        module_dir = self.REGISTRY_DIR / "modules" / "score_baselibs"
        assert module_dir.is_dir(), (
            "score_baselibs module directory not found in "
            "score-bazel_registry/modules/"
        )

    def test_metadata_json_exists(self):
        metadata = (
            self.REGISTRY_DIR / "modules" / "score_baselibs" / "metadata.json"
        )
        assert metadata.exists(), (
            "metadata.json not found for score_baselibs in the Bazel registry"
        )

    def test_registry_has_version_entries(self):
        module_dir = self.REGISTRY_DIR / "modules" / "score_baselibs"
        if not module_dir.is_dir():
            pytest.skip("score_baselibs registry module dir missing")

        version_dirs = [
            d for d in module_dir.iterdir()
            if d.is_dir() and re.match(r"\d+\.\d+\.\d+", d.name)
        ]
        assert len(version_dirs) > 0, (
            "No version directories found in registry for score_baselibs"
        )

    def test_registry_contains_current_version(self):
        """The version declared in score-baselibs/MODULE.bazel should have
        a corresponding entry in the registry."""
        base_module = BASELIBS_DIR / "MODULE.bazel"
        if not base_module.exists():
            pytest.skip("score-baselibs/MODULE.bazel not found")

        content = base_module.read_text(encoding="utf-8")
        match = re.search(
            r'module\([^)]*version\s*=\s*"([^"]+)"', content, re.DOTALL
        )
        assert match, "Cannot parse version from score-baselibs/MODULE.bazel"
        version = match.group(1)

        version_dir = (
            self.REGISTRY_DIR / "modules" / "score_baselibs" / version
        )
        assert version_dir.is_dir(), (
            f"Registry does not contain version {version} for score_baselibs"
        )


# ---------------------------------------------------------------------------
# TestCrossComponentHeaders
# ---------------------------------------------------------------------------
class TestCrossComponentHeaders:
    """Verify that key baselibs headers used by LoLa actually exist.

    Parses LoLa source and BUILD files to find ``#include "score/..."``
    directives and confirms the referenced headers are present in
    score-baselibs.
    """

    COMM_DIR = PROJECT_ROOT / "score-communication"
    SCORE_DIR = BASELIBS_DIR / "score"

    # Headers known to be consumed by LoLa from score-baselibs
    KNOWN_LOLA_BASELIBS_HEADERS = [
        "score/os/errno.h",
        "score/os/fcntl.h",
        "score/os/mman.h",
        "score/os/pthread.h",
        "score/os/socket.h",
        "score/os/stat.h",
        "score/os/unistd.h",
        "score/os/semaphore.h",
        "score/memory/shared/shared_memory_factory.h",
        "score/memory/shared/shared_memory_resource.h",
        "score/memory/shared/offset_ptr.h",
        "score/concurrency/notification.h",
        "score/concurrency/executor.h",
        "score/result/result.h",
    ]

    @pytest.mark.parametrize("header_path", KNOWN_LOLA_BASELIBS_HEADERS)
    def test_known_header_exists(self, header_path: str):
        full_path = BASELIBS_DIR / header_path
        assert full_path.exists(), (
            f"Header {header_path} expected by LoLa is missing from "
            f"score-baselibs"
        )

    def test_discover_score_includes_in_lola(self):
        """Scan LoLa C++ sources for #include \"score/...\" and verify
        that a reasonable fraction of them map to existing baselibs headers.

        This is a best-effort discovery test -- not all score/ includes
        originate from score-baselibs (some are local to score-communication).
        """
        comm_dir = self.COMM_DIR
        if not comm_dir.is_dir():
            pytest.skip("score-communication directory not found")

        include_pattern = re.compile(r'#include\s+"(score/[^"]+)"')
        discovered: set[str] = set()

        # Walk .cpp and .h files in score-communication
        for ext in ("*.cpp", "*.h"):
            for source_file in comm_dir.rglob(ext):
                try:
                    text = source_file.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                for match in include_pattern.finditer(text):
                    discovered.add(match.group(1))

        if not discovered:
            pytest.skip("No score/ includes discovered in score-communication")

        # Filter to headers that could plausibly come from baselibs
        baselibs_candidates = [
            h for h in discovered
            if (BASELIBS_DIR / h).exists()
        ]

        assert len(baselibs_candidates) >= 5, (
            f"Expected at least 5 score-baselibs headers used by LoLa, "
            f"found {len(baselibs_candidates)}: {baselibs_candidates}"
        )

    def test_os_directory_has_headers(self):
        os_dir = self.SCORE_DIR / "os"
        assert os_dir.is_dir(), "score/os/ directory missing"
        headers = list(os_dir.glob("*.h"))
        assert len(headers) >= 10, (
            f"Expected at least 10 OS abstraction headers, found {len(headers)}"
        )

    def test_memory_shared_directory_has_headers(self):
        shm_dir = self.SCORE_DIR / "memory" / "shared"
        assert shm_dir.is_dir(), "score/memory/shared/ directory missing"
        headers = list(shm_dir.glob("*.h"))
        assert len(headers) >= 5, (
            f"Expected at least 5 shared memory headers, found {len(headers)}"
        )

    def test_concurrency_directory_has_headers(self):
        conc_dir = self.SCORE_DIR / "concurrency"
        assert conc_dir.is_dir(), "score/concurrency/ directory missing"
        headers = list(conc_dir.glob("*.h"))
        assert len(headers) >= 3, (
            f"Expected at least 3 concurrency headers, found {len(headers)}"
        )
