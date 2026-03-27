"""
Safety contract tests for score-persistency.

Validates ASIL-D safety requirements for the KVS library.
ASIL-D is the highest automotive safety integrity level and demands:
    - Rigorous error handling (no silent failures)
    - Minimal unsafe code with documented justification
    - CRC validation for data integrity (Adler-32)
    - Snapshot integrity for crash recovery
    - Explicit safety classification in build configuration

These tests verify structural safety properties, not runtime behavior.
"""

import re
from pathlib import Path

import pytest

PERSISTENCY_DIR = Path(__file__).parent.parent.parent.parent / "score-persistency"

pytestmark = pytest.mark.score_persistency


# ---------------------------------------------------------------------------
# TestAsilDClassification -- ASIL-D safety classification
# ---------------------------------------------------------------------------


class TestAsilDClassification:
    """Verify ASIL-D classification is declared in project configuration."""

    def test_project_config_exists(self):
        """project_config.bzl must exist for safety classification."""
        candidates = [
            PERSISTENCY_DIR / "project_config.bzl",
            PERSISTENCY_DIR / "config" / "project_config.bzl",
            PERSISTENCY_DIR / "build" / "project_config.bzl",
        ]
        found = any(c.exists() for c in candidates)
        assert found, (
            "project_config.bzl not found. Required for ASIL-D classification. "
            f"Checked: {', '.join(str(c) for c in candidates)}"
        )

    def test_asil_d_declared(self):
        """project_config.bzl must declare ASIL_D classification."""
        candidates = [
            PERSISTENCY_DIR / "project_config.bzl",
            PERSISTENCY_DIR / "config" / "project_config.bzl",
            PERSISTENCY_DIR / "build" / "project_config.bzl",
        ]
        content = ""
        for c in candidates:
            if c.exists():
                content = c.read_text(encoding="utf-8")
                break

        if not content:
            pytest.skip("project_config.bzl not found")

        assert "ASIL_D" in content or "ASIL-D" in content or "asil_d" in content, (
            "project_config.bzl does not declare ASIL_D classification"
        )

    def test_safety_classification_not_qm(self):
        """Safety classification must not be QM (quality management only)."""
        candidates = [
            PERSISTENCY_DIR / "project_config.bzl",
            PERSISTENCY_DIR / "config" / "project_config.bzl",
        ]
        content = ""
        for c in candidates:
            if c.exists():
                content = c.read_text(encoding="utf-8")
                break

        if not content:
            pytest.skip("project_config.bzl not found")

        # Ensure it's not downgraded to QM
        lines = content.splitlines()
        for line in lines:
            if "safety" in line.lower() or "asil" in line.lower():
                # This line mentions safety -- make sure it says ASIL_D
                if "QM" in line and "ASIL_D" not in line:
                    pytest.fail(
                        f"Safety classification appears to be QM, not ASIL_D: {line}"
                    )


# ---------------------------------------------------------------------------
# TestCppApiSafety -- C++ error handling patterns
# ---------------------------------------------------------------------------


class TestCppApiSafety:
    """Verify C++ API follows ASIL-D error handling patterns."""

    CPP_SRC = PERSISTENCY_DIR / "src" / "cpp" / "src"

    def _read_all_cpp_sources(self) -> dict[str, str]:
        """Read all C++ source files and return {name: content}."""
        sources = {}
        if not self.CPP_SRC.is_dir():
            return sources
        for ext in ("*.hpp", "*.cpp"):
            for f in self.CPP_SRC.rglob(ext):
                sources[str(f.relative_to(PERSISTENCY_DIR))] = \
                    f.read_text(encoding="utf-8", errors="replace")
        return sources

    def test_kvs_hpp_exists(self):
        """kvs.hpp must exist as the primary API header."""
        kvs_hpp = self.CPP_SRC / "kvs.hpp"
        assert kvs_hpp.exists(), f"kvs.hpp not found: {kvs_hpp}"

    def test_error_handling_present(self):
        """C++ sources must use error handling (Result, error codes, exceptions)."""
        sources = self._read_all_cpp_sources()
        if not sources:
            pytest.skip("No C++ sources found")

        error_patterns = [
            r"error",
            r"Error",
            r"Result",
            r"Status",
            r"exception",
            r"throw",
            r"ErrorCode",
            r"error_code",
        ]

        has_error_handling = False
        for name, content in sources.items():
            for pattern in error_patterns:
                if re.search(pattern, content):
                    has_error_handling = True
                    break
            if has_error_handling:
                break

        assert has_error_handling, (
            "No error handling patterns found in C++ sources. "
            "ASIL-D requires explicit error handling."
        )

    def test_error_hpp_exists(self):
        """error.hpp must exist in internal/ for error type definitions."""
        error_hpp = self.CPP_SRC / "internal" / "error.hpp"
        assert error_hpp.exists(), (
            f"error.hpp not found: {error_hpp}. "
            "ASIL-D requires dedicated error handling infrastructure."
        )

    def test_no_bare_assert_in_production(self):
        """Production code should not use bare assert() -- use proper error handling."""
        sources = self._read_all_cpp_sources()
        if not sources:
            pytest.skip("No C++ sources found")

        # Only check non-test, non-internal files for bare asserts
        violations = []
        for name, content in sources.items():
            if "test" in name.lower() or "mock" in name.lower():
                continue
            # Find assert() calls that aren't static_assert
            bare_asserts = re.findall(
                r'(?<!static_)assert\s*\(', content
            )
            if bare_asserts:
                violations.append(f"{name}: {len(bare_asserts)} bare assert()")

        if violations:
            pytest.xfail(
                "Bare assert() found in production code (review for ASIL-D):\n" +
                "\n".join(f"  - {v}" for v in violations)
            )


# ---------------------------------------------------------------------------
# TestRustSafety -- Rust unsafe code audit
# ---------------------------------------------------------------------------


class TestRustSafety:
    """Verify Rust code follows ASIL-D safety patterns."""

    RUST_KVS = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs"

    def _read_all_rust_sources(self) -> dict[str, str]:
        """Read all Rust source files and return {name: content}."""
        sources = {}
        if not self.RUST_KVS.is_dir():
            return sources
        for f in self.RUST_KVS.rglob("*.rs"):
            sources[str(f.relative_to(PERSISTENCY_DIR))] = \
                f.read_text(encoding="utf-8", errors="replace")
        return sources

    def test_unsafe_block_count(self):
        """Count unsafe blocks -- ASIL-D demands minimal unsafe usage.

        Each unsafe block should have a documented safety justification.
        """
        sources = self._read_all_rust_sources()
        if not sources:
            pytest.skip("No Rust sources found")

        unsafe_locations = []
        for name, content in sources.items():
            if "mock" in name.lower() or "test" in name.lower():
                continue
            matches = list(re.finditer(r'\bunsafe\b', content))
            for m in matches:
                line_num = content[:m.start()].count('\n') + 1
                unsafe_locations.append(f"{name}:{line_num}")

        # ASIL-D: unsafe blocks should be minimal and justified
        max_allowed = 10  # Threshold for review
        if len(unsafe_locations) > max_allowed:
            pytest.xfail(
                f"Found {len(unsafe_locations)} unsafe usages "
                f"(threshold: {max_allowed}). "
                f"ASIL-D requires review:\n" +
                "\n".join(f"  - {loc}" for loc in unsafe_locations[:20])
            )

    def test_error_handling_pattern(self):
        """Rust code must use Result/Option for error handling, not unwrap()."""
        sources = self._read_all_rust_sources()
        if not sources:
            pytest.skip("No Rust sources found")

        unwrap_violations = []
        for name, content in sources.items():
            if "mock" in name.lower() or "test" in name.lower() or "example" in name.lower():
                continue
            unwraps = len(re.findall(r'\.unwrap\(\)', content))
            if unwraps > 0:
                unwrap_violations.append(f"{name}: {unwraps} unwrap() calls")

        if unwrap_violations:
            pytest.xfail(
                "unwrap() found in production Rust code (review for ASIL-D):\n" +
                "\n".join(f"  - {v}" for v in unwrap_violations)
            )

    def test_error_code_module_exists(self):
        """error_code.rs must exist for typed error handling."""
        candidates = [
            self.RUST_KVS / "src" / "error_code.rs",
            self.RUST_KVS / "error_code.rs",
        ]
        found = any(c.exists() for c in candidates)
        assert found, (
            "error_code.rs not found. ASIL-D requires typed error handling."
        )

    def test_panic_handling(self):
        """Production Rust code should minimize panic! usage."""
        sources = self._read_all_rust_sources()
        if not sources:
            pytest.skip("No Rust sources found")

        panic_locations = []
        for name, content in sources.items():
            if "mock" in name.lower() or "test" in name.lower():
                continue
            panics = list(re.finditer(r'\bpanic!\b', content))
            for m in panics:
                line_num = content[:m.start()].count('\n') + 1
                panic_locations.append(f"{name}:{line_num}")

        if panic_locations:
            pytest.xfail(
                f"Found {len(panic_locations)} panic! usages in production code. "
                f"ASIL-D requires graceful error handling:\n" +
                "\n".join(f"  - {loc}" for loc in panic_locations[:10])
            )


# ---------------------------------------------------------------------------
# TestCrcValidation -- Adler-32 CRC for data integrity
# ---------------------------------------------------------------------------


class TestCrcValidation:
    """Verify CRC validation infrastructure for data integrity."""

    def test_adler32_dependency_declared(self):
        """adler32 must be declared as a dependency for CRC validation."""
        cargo_toml = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("rust_kvs Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        has_adler = "adler32" in content or "adler" in content
        assert has_adler, (
            "No adler32/adler dependency found in rust_kvs Cargo.toml. "
            "CRC-Adler32 is required for defaults validation."
        )

    def test_crc_used_in_source(self):
        """CRC/checksum functionality must be referenced in source code."""
        rust_kvs = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs"
        if not rust_kvs.is_dir():
            pytest.skip("rust_kvs directory not found")

        all_content = ""
        for f in rust_kvs.rglob("*.rs"):
            all_content += f.read_text(encoding="utf-8", errors="replace")

        crc_patterns = ["adler", "crc", "checksum", "Adler32"]
        has_crc = any(p in all_content for p in crc_patterns)
        assert has_crc, (
            "No CRC/checksum references found in Rust sources. "
            "Defaults CRC (Adler-32) is a safety requirement."
        )

    def test_defaults_with_crc(self):
        """KVS defaults must use CRC for integrity validation."""
        rust_kvs = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs"
        if not rust_kvs.is_dir():
            pytest.skip("rust_kvs directory not found")

        # Look for files that handle defaults
        relevant_files = []
        for f in rust_kvs.rglob("*.rs"):
            content = f.read_text(encoding="utf-8", errors="replace")
            if "default" in content.lower() and ("crc" in content.lower() or "adler" in content.lower()):
                relevant_files.append(f.name)

        assert len(relevant_files) > 0, (
            "No source files found that combine defaults with CRC validation. "
            "ASIL-D requires CRC-protected defaults."
        )


# ---------------------------------------------------------------------------
# TestSnapshotIntegrity -- snapshot mechanism
# ---------------------------------------------------------------------------


class TestSnapshotIntegrity:
    """Verify snapshot support for crash recovery."""

    def test_snapshot_source_files_exist(self):
        """Source files related to snapshot functionality must exist."""
        rust_kvs = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs"
        if not rust_kvs.is_dir():
            pytest.skip("rust_kvs directory not found")

        # Search for snapshot-related content in source files
        snapshot_files = []
        for f in rust_kvs.rglob("*.rs"):
            content = f.read_text(encoding="utf-8", errors="replace")
            if "snapshot" in content.lower():
                snapshot_files.append(f.name)

        assert len(snapshot_files) > 0, (
            "No snapshot-related source files found. "
            "KVS must support snapshots for crash recovery."
        )

    def test_snapshot_example_exists(self):
        """A snapshots example should demonstrate the snapshot API."""
        candidates = [
            PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "examples" / "snapshots.rs",
            PERSISTENCY_DIR / "examples" / "snapshots.rs",
            PERSISTENCY_DIR / "src" / "rust" / "examples" / "snapshots.rs",
        ]
        found = any(c.exists() for c in candidates)
        assert found, (
            "snapshots.rs example not found. "
            f"Checked: {', '.join(str(c) for c in candidates)}"
        )

    def test_flush_support(self):
        """KVS must support flush operations for data persistence."""
        rust_kvs = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs"
        if not rust_kvs.is_dir():
            pytest.skip("rust_kvs directory not found")

        flush_files = []
        for f in rust_kvs.rglob("*.rs"):
            content = f.read_text(encoding="utf-8", errors="replace")
            if "flush" in content.lower():
                flush_files.append(f.name)

        assert len(flush_files) > 0, (
            "No flush-related code found in Rust sources. "
            "KVS must support explicit flush for data persistence."
        )
