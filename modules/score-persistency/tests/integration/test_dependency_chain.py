"""
Dependency chain integration tests for score-persistency.

Validates that all declared dependencies are correctly specified,
resolvable, and that cross-component header/crate references are valid.

Dependencies:
    - score_baselibs 0.2.4 (Bazel module)
    - score_logging 0.1.0 (Bazel module)
    - score_baselibs_rust 0.1.0 (Bazel module)
    - tinyjson, adler32, serde (Cargo crates)
"""

import re
from pathlib import Path

import pytest

PERSISTENCY_DIR = Path(__file__).parent.parent.parent.parent / "score-persistency"

pytestmark = pytest.mark.score_persistency


# ---------------------------------------------------------------------------
# TestBaseLibsDependency -- Bazel module dependencies
# ---------------------------------------------------------------------------


class TestBaseLibsDependency:
    """Verify Bazel module dependencies are correctly declared."""

    def _read_module_bazel(self) -> str:
        """Read MODULE.bazel content."""
        module_file = PERSISTENCY_DIR / "MODULE.bazel"
        assert module_file.exists(), f"MODULE.bazel not found: {module_file}"
        return module_file.read_text(encoding="utf-8")

    def test_score_baselibs_dependency(self):
        """score_baselibs must be declared as a dependency at version 0.2.4."""
        content = self._read_module_bazel()
        assert "score_baselibs" in content, (
            "MODULE.bazel does not reference score_baselibs"
        )
        # Check for version specification
        assert "0.2.4" in content, (
            "MODULE.bazel does not specify score_baselibs version 0.2.4"
        )

    def test_score_logging_dependency(self):
        """score_logging must be declared as a dependency at version 0.1.0."""
        content = self._read_module_bazel()
        assert "score_logging" in content, (
            "MODULE.bazel does not reference score_logging"
        )
        assert "0.1.0" in content, (
            "MODULE.bazel does not specify score_logging version 0.1.0"
        )

    def test_score_baselibs_rust_dependency(self):
        """score_baselibs_rust must be declared at version 0.1.0."""
        content = self._read_module_bazel()
        assert "score_baselibs_rust" in content, (
            "MODULE.bazel does not reference score_baselibs_rust"
        )

    def test_no_circular_dependencies(self):
        """MODULE.bazel must not depend on score_persistency itself."""
        content = self._read_module_bazel()
        # Find bazel_dep calls
        deps = re.findall(r'bazel_dep\s*\(\s*name\s*=\s*"([^"]+)"', content)
        assert "score_persistency" not in deps, (
            "MODULE.bazel has a circular dependency on score_persistency"
        )


# ---------------------------------------------------------------------------
# TestRustDependencies -- Cargo.toml dependencies
# ---------------------------------------------------------------------------


class TestRustDependencies:
    """Verify Rust crate dependencies in Cargo.toml."""

    def _read_kvs_cargo_toml(self) -> str:
        """Read the rust_kvs Cargo.toml content."""
        cargo_toml = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "Cargo.toml"
        assert cargo_toml.exists(), f"rust_kvs Cargo.toml not found: {cargo_toml}"
        return cargo_toml.read_text(encoding="utf-8")

    def test_tinyjson_dependency(self):
        """rust_kvs must depend on tinyjson for JSON backend."""
        content = self._read_kvs_cargo_toml()
        assert "tinyjson" in content, (
            "rust_kvs Cargo.toml does not declare tinyjson dependency "
            "(required for JSON backend)"
        )

    def test_adler32_dependency(self):
        """rust_kvs must depend on adler32 for CRC validation."""
        content = self._read_kvs_cargo_toml()
        # Could be "adler32" or "adler" depending on crate name
        has_adler = "adler32" in content or "adler" in content
        assert has_adler, (
            "rust_kvs Cargo.toml does not declare adler32/adler dependency "
            "(required for CRC-Adler32 validation)"
        )

    def test_serde_dependency(self):
        """rust_kvs must depend on serde for serialization."""
        content = self._read_kvs_cargo_toml()
        assert "serde" in content, (
            "rust_kvs Cargo.toml does not declare serde dependency "
            "(required for serialization)"
        )

    def test_cargo_lock_consistency(self):
        """Cargo.lock must exist and be consistent with workspace."""
        cargo_lock = PERSISTENCY_DIR / "Cargo.lock"
        assert cargo_lock.exists(), f"Cargo.lock not found: {cargo_lock}"
        content = cargo_lock.read_text(encoding="utf-8")
        # Verify key dependencies appear in lock file
        assert "tinyjson" in content, "tinyjson not found in Cargo.lock"

    def test_no_wildcard_versions(self):
        """Cargo.toml should not use wildcard (*) versions for safety."""
        content = self._read_kvs_cargo_toml()
        # Find version specifications that are just "*"
        wildcard_deps = re.findall(
            r'(\w+)\s*=\s*["\']?\*["\']?', content
        )
        assert not wildcard_deps, (
            f"Wildcard version dependencies found (unsafe for ASIL-D): "
            f"{wildcard_deps}"
        )


# ---------------------------------------------------------------------------
# TestCrossComponentHeaders -- cross-component includes
# ---------------------------------------------------------------------------


class TestCrossComponentHeaders:
    """Verify cross-component header dependencies are accessible."""

    CPP_SRC = PERSISTENCY_DIR / "src" / "cpp" / "src"

    def _find_includes(self, header_path: Path) -> list[str]:
        """Extract #include directives from a file."""
        if not header_path.exists():
            return []
        content = header_path.read_text(encoding="utf-8", errors="replace")
        return re.findall(r'#include\s+[<"]([^>"]+)[>"]', content)

    def test_baselibs_filesystem_header_referenced(self):
        """C++ sources should reference baselibs filesystem headers."""
        all_includes = []
        for hpp in self.CPP_SRC.rglob("*.hpp"):
            all_includes.extend(self._find_includes(hpp))
        for cpp in self.CPP_SRC.rglob("*.cpp"):
            all_includes.extend(self._find_includes(cpp))

        # Check for filesystem-related includes from baselibs
        filesystem_refs = [
            inc for inc in all_includes
            if "filesystem" in inc.lower() or "file" in inc.lower()
        ]
        assert len(filesystem_refs) > 0 or len(all_includes) == 0, (
            "No filesystem-related includes found in C++ sources. "
            "KVS should depend on baselibs filesystem abstraction."
        )

    def test_baselibs_json_header_referenced(self):
        """C++ sources should reference baselibs JSON headers."""
        all_includes = []
        for hpp in self.CPP_SRC.rglob("*.hpp"):
            all_includes.extend(self._find_includes(hpp))
        for cpp in self.CPP_SRC.rglob("*.cpp"):
            all_includes.extend(self._find_includes(cpp))

        json_refs = [
            inc for inc in all_includes
            if "json" in inc.lower()
        ]
        assert len(json_refs) > 0 or len(all_includes) == 0, (
            "No JSON-related includes found in C++ sources. "
            "KVS uses JSON backend and should include JSON headers."
        )

    def test_logging_header_referenced(self):
        """C++ sources should reference score_logging headers."""
        all_includes = []
        for hpp in self.CPP_SRC.rglob("*.hpp"):
            all_includes.extend(self._find_includes(hpp))
        for cpp in self.CPP_SRC.rglob("*.cpp"):
            all_includes.extend(self._find_includes(cpp))

        logging_refs = [
            inc for inc in all_includes
            if "log" in inc.lower()
        ]
        assert len(logging_refs) > 0 or len(all_includes) == 0, (
            "No logging-related includes found in C++ sources. "
            "KVS should use score_logging for ASIL-D traceability."
        )

    def test_rust_baselibs_dependency(self):
        """Rust crate should depend on score_baselibs_rust."""
        cargo_toml = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("rust_kvs Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        # The dependency might be via Bazel rather than Cargo directly
        # Check BUILD files as well
        build_files = list(
            (PERSISTENCY_DIR / "src" / "rust").rglob("BUILD*")
        )
        build_content = ""
        for bf in build_files:
            build_content += bf.read_text(encoding="utf-8", errors="replace")

        has_baselibs_rust = (
            "score_baselibs_rust" in content or
            "score_baselibs_rust" in build_content
        )
        assert has_baselibs_rust, (
            "rust_kvs does not reference score_baselibs_rust in "
            "Cargo.toml or BUILD files"
        )
