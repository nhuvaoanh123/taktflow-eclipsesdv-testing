"""
API contract regression tests for score-persistency.

Validates that the expected file structure, public APIs, crate layout,
and build targets remain stable across versions. These tests catch
unintentional breaking changes to the library's public surface.

The score-persistency library is an ASIL-D rated KVS (key-value store)
with dual C++/Rust implementation.
"""

from pathlib import Path

import pytest

PERSISTENCY_DIR = Path(__file__).parent.parent.parent.parent / "score-persistency"

pytestmark = pytest.mark.score_persistency


# ---------------------------------------------------------------------------
# TestModuleIdentity -- MODULE.bazel metadata
# ---------------------------------------------------------------------------


class TestModuleIdentity:
    """Verify Bazel module identity and version."""

    def test_module_bazel_exists(self):
        """MODULE.bazel must exist at repository root."""
        module_file = PERSISTENCY_DIR / "MODULE.bazel"
        assert module_file.exists(), f"MODULE.bazel not found at {module_file}"

    def test_module_name(self):
        """Module must be named score_persistency."""
        module_file = PERSISTENCY_DIR / "MODULE.bazel"
        content = module_file.read_text(encoding="utf-8")
        assert 'name = "score_persistency"' in content or \
               "name = 'score_persistency'" in content, (
            "MODULE.bazel does not declare name = 'score_persistency'"
        )

    def test_module_version(self):
        """Module version must be 0.0.0 (pre-release)."""
        module_file = PERSISTENCY_DIR / "MODULE.bazel"
        content = module_file.read_text(encoding="utf-8")
        assert 'version = "0.0.0"' in content or \
               "version = '0.0.0'" in content, (
            "MODULE.bazel does not declare version = '0.0.0'"
        )


# ---------------------------------------------------------------------------
# TestCppApiContract -- public C++ headers
# ---------------------------------------------------------------------------


class TestCppApiContract:
    """Verify the public C++ API files exist and are well-formed."""

    CPP_SRC = PERSISTENCY_DIR / "src" / "cpp" / "src"
    PUBLIC_HEADERS = ["kvs.hpp", "kvsbuilder.hpp", "kvsvalue.hpp"]

    def test_cpp_src_directory_exists(self):
        """The src/cpp/src/ directory must exist."""
        assert self.CPP_SRC.is_dir(), f"C++ source directory not found: {self.CPP_SRC}"

    @pytest.mark.parametrize("header", PUBLIC_HEADERS)
    def test_public_header_exists(self, header):
        """Each public C++ header must exist."""
        header_path = self.CPP_SRC / header
        assert header_path.exists(), f"Public header missing: {header_path}"

    @pytest.mark.parametrize("header", PUBLIC_HEADERS)
    def test_public_header_has_include_guard(self, header):
        """Public headers should have include guards or #pragma once."""
        header_path = self.CPP_SRC / header
        if not header_path.exists():
            pytest.skip(f"{header} does not exist")
        content = header_path.read_text(encoding="utf-8", errors="replace")
        has_guard = "#pragma once" in content or "#ifndef" in content
        assert has_guard, f"{header} lacks include guard or #pragma once"

    @pytest.mark.parametrize("header", PUBLIC_HEADERS)
    def test_public_header_not_empty(self, header):
        """Public headers must not be empty."""
        header_path = self.CPP_SRC / header
        if not header_path.exists():
            pytest.skip(f"{header} does not exist")
        content = header_path.read_text(encoding="utf-8", errors="replace")
        # Strip comments and whitespace
        meaningful = [
            line for line in content.splitlines()
            if line.strip() and not line.strip().startswith("//")
        ]
        assert len(meaningful) > 5, f"{header} appears to be trivially small"


# ---------------------------------------------------------------------------
# TestCppInternalContract -- internal C++ headers
# ---------------------------------------------------------------------------


class TestCppInternalContract:
    """Verify internal C++ headers exist."""

    INTERNAL_DIR = PERSISTENCY_DIR / "src" / "cpp" / "src" / "internal"
    INTERNAL_HEADERS = ["error.hpp", "kvs_helper.hpp"]

    def test_internal_directory_exists(self):
        """The src/cpp/src/internal/ directory must exist."""
        assert self.INTERNAL_DIR.is_dir(), (
            f"Internal headers directory not found: {self.INTERNAL_DIR}"
        )

    @pytest.mark.parametrize("header", INTERNAL_HEADERS)
    def test_internal_header_exists(self, header):
        """Each internal header must exist."""
        header_path = self.INTERNAL_DIR / header
        assert header_path.exists(), f"Internal header missing: {header_path}"


# ---------------------------------------------------------------------------
# TestRustCrateContract -- Rust crate files
# ---------------------------------------------------------------------------


class TestRustCrateContract:
    """Verify the Rust KVS crate structure is intact."""

    RUST_KVS = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs"
    EXPECTED_RS_FILES = [
        "kvs.rs",
        "kvs_api.rs",
        "kvs_builder.rs",
        "kvs_value.rs",
        "kvs_backend.rs",
        "kvs_mock.rs",
        "json_backend.rs",
        "kvs_serialize.rs",
        "error_code.rs",
    ]

    def test_rust_kvs_cargo_toml_exists(self):
        """rust_kvs/Cargo.toml must exist."""
        cargo_toml = self.RUST_KVS / "Cargo.toml"
        assert cargo_toml.exists(), f"Cargo.toml not found: {cargo_toml}"

    def test_rust_kvs_src_directory(self):
        """rust_kvs must have a src/ directory or lib.rs/main.rs."""
        src_dir = self.RUST_KVS / "src"
        lib_rs = self.RUST_KVS / "src" / "lib.rs"
        # Some crates put .rs files directly in the crate root
        has_src = src_dir.is_dir() or lib_rs.exists()
        # Also check for .rs files in the crate root
        root_rs = list(self.RUST_KVS.glob("*.rs"))
        assert has_src or len(root_rs) > 0, (
            f"No Rust source files found in {self.RUST_KVS}"
        )

    @pytest.mark.parametrize("rs_file", EXPECTED_RS_FILES)
    def test_rs_file_exists(self, rs_file):
        """Each expected .rs source file must exist somewhere in the crate."""
        # Check both src/ subdirectory and crate root
        candidates = [
            self.RUST_KVS / "src" / rs_file,
            self.RUST_KVS / rs_file,
        ]
        found = any(c.exists() for c in candidates)
        assert found, (
            f"Rust source file {rs_file} not found. "
            f"Checked: {', '.join(str(c) for c in candidates)}"
        )


# ---------------------------------------------------------------------------
# TestRustToolContract -- CLI tool crate
# ---------------------------------------------------------------------------


class TestRustToolContract:
    """Verify the Rust KVS CLI tool crate exists."""

    RUST_TOOL = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs_tool"

    def test_tool_crate_exists(self):
        """rust_kvs_tool directory must exist."""
        assert self.RUST_TOOL.is_dir(), (
            f"rust_kvs_tool directory not found: {self.RUST_TOOL}"
        )

    def test_kvs_tool_rs_exists(self):
        """kvs_tool.rs must exist in the tool crate."""
        candidates = [
            self.RUST_TOOL / "kvs_tool.rs",
            self.RUST_TOOL / "src" / "kvs_tool.rs",
            self.RUST_TOOL / "src" / "main.rs",
        ]
        found = any(c.exists() for c in candidates)
        assert found, (
            f"kvs_tool.rs not found. Checked: {', '.join(str(c) for c in candidates)}"
        )


# ---------------------------------------------------------------------------
# TestCppTestFiles -- C++ test files
# ---------------------------------------------------------------------------


class TestCppTestFiles:
    """Verify C++ test file structure."""

    CPP_TESTS = PERSISTENCY_DIR / "src" / "cpp" / "tests"

    def test_cpp_tests_directory_exists(self):
        """src/cpp/tests/ directory must exist."""
        assert self.CPP_TESTS.is_dir(), (
            f"C++ tests directory not found: {self.CPP_TESTS}"
        )

    def test_six_test_files_exist(self):
        """There should be at least 6 test source files."""
        test_files = list(self.CPP_TESTS.glob("test_*.cpp")) + \
                     list(self.CPP_TESTS.glob("*_test.cpp"))
        assert len(test_files) >= 6, (
            f"Expected at least 6 C++ test files, found {len(test_files)}: "
            f"{[f.name for f in test_files]}"
        )

    def test_benchmark_file_exists(self):
        """bm_kvs.cpp benchmark file must exist."""
        bm_file = self.CPP_TESTS / "bm_kvs.cpp"
        assert bm_file.exists(), f"Benchmark file not found: {bm_file}"


# ---------------------------------------------------------------------------
# TestPythonIntegration -- Python test infrastructure
# ---------------------------------------------------------------------------


class TestPythonIntegration:
    """Verify Python integration test infrastructure."""

    TEST_CASES = PERSISTENCY_DIR / "tests" / "test_cases"

    def test_test_cases_directory_exists(self):
        """tests/test_cases/ directory must exist."""
        assert self.TEST_CASES.is_dir(), (
            f"Python test_cases directory not found: {self.TEST_CASES}"
        )

    def test_python_test_files_exist(self):
        """At least one Python test file must exist in test_cases/."""
        py_files = list(self.TEST_CASES.glob("test_*.py")) + \
                   list(self.TEST_CASES.glob("*_test.py"))
        assert len(py_files) > 0, (
            f"No Python test files found in {self.TEST_CASES}"
        )

    def test_pytest_config_exists(self):
        """A pytest configuration file should exist (pyproject.toml, pytest.ini, etc.)."""
        config_candidates = [
            PERSISTENCY_DIR / "pyproject.toml",
            PERSISTENCY_DIR / "pytest.ini",
            PERSISTENCY_DIR / "setup.cfg",
            PERSISTENCY_DIR / "tox.ini",
        ]
        found = any(c.exists() for c in config_candidates)
        assert found, (
            "No pytest configuration file found. "
            f"Checked: {', '.join(c.name for c in config_candidates)}"
        )


# ---------------------------------------------------------------------------
# TestBuildTargets -- BUILD files for key packages
# ---------------------------------------------------------------------------


class TestBuildTargets:
    """Verify BUILD files exist for key packages."""

    BUILD_FILE_NAMES = ["BUILD", "BUILD.bazel"]

    def _has_build_file(self, directory: Path) -> bool:
        """Check if a directory contains a BUILD or BUILD.bazel file."""
        return any((directory / name).exists() for name in self.BUILD_FILE_NAMES)

    def test_root_build_file(self):
        """Root BUILD file must exist (defines //:unit_tests etc.)."""
        assert self._has_build_file(PERSISTENCY_DIR), (
            "No BUILD file at repository root"
        )

    def test_cpp_src_build_file(self):
        """src/cpp/ must have a BUILD file."""
        cpp_dir = PERSISTENCY_DIR / "src" / "cpp"
        assert self._has_build_file(cpp_dir) or \
               self._has_build_file(cpp_dir / "src"), (
            f"No BUILD file in {cpp_dir} or {cpp_dir / 'src'}"
        )

    def test_rust_src_build_file(self):
        """src/rust/ must have a BUILD file."""
        rust_dir = PERSISTENCY_DIR / "src" / "rust"
        assert self._has_build_file(rust_dir) or \
               self._has_build_file(rust_dir / "rust_kvs"), (
            f"No BUILD file in {rust_dir} or {rust_dir / 'rust_kvs'}"
        )

    def test_tests_build_file(self):
        """tests/ must have a BUILD file."""
        tests_dir = PERSISTENCY_DIR / "tests"
        assert self._has_build_file(tests_dir), (
            f"No BUILD file in {tests_dir}"
        )


# ---------------------------------------------------------------------------
# TestExamples -- Rust example files
# ---------------------------------------------------------------------------


class TestExamples:
    """Verify Rust example files exist."""

    EXAMPLES_DIR = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "examples"
    EXPECTED_EXAMPLES = [
        "basic.rs",
        "snapshots.rs",
        "defaults.rs",
        "custom_types.rs",
        "migration.rs",
    ]

    def test_examples_directory_exists(self):
        """An examples directory must exist."""
        # Examples might be at different levels
        candidates = [
            self.EXAMPLES_DIR,
            PERSISTENCY_DIR / "examples",
            PERSISTENCY_DIR / "src" / "rust" / "examples",
        ]
        found = any(c.is_dir() for c in candidates)
        assert found, (
            f"No examples directory found. "
            f"Checked: {', '.join(str(c) for c in candidates)}"
        )

    @pytest.mark.parametrize("example", EXPECTED_EXAMPLES)
    def test_example_exists(self, example):
        """Each expected example file must exist."""
        candidates = [
            self.EXAMPLES_DIR / example,
            PERSISTENCY_DIR / "examples" / example,
            PERSISTENCY_DIR / "src" / "rust" / "examples" / example,
        ]
        found = any(c.exists() for c in candidates)
        assert found, (
            f"Example {example} not found. "
            f"Checked: {', '.join(str(c) for c in candidates)}"
        )


# ---------------------------------------------------------------------------
# TestCargoWorkspace -- Cargo workspace configuration
# ---------------------------------------------------------------------------


class TestCargoWorkspace:
    """Verify Cargo workspace configuration."""

    def test_root_cargo_toml_exists(self):
        """Cargo.toml must exist at the repository root."""
        cargo_toml = PERSISTENCY_DIR / "Cargo.toml"
        assert cargo_toml.exists(), f"Root Cargo.toml not found: {cargo_toml}"

    def test_cargo_lock_exists(self):
        """Cargo.lock must exist (pinned dependencies for reproducibility)."""
        cargo_lock = PERSISTENCY_DIR / "Cargo.lock"
        assert cargo_lock.exists(), f"Cargo.lock not found: {cargo_lock}"

    def test_workspace_members(self):
        """Root Cargo.toml must define workspace members."""
        cargo_toml = PERSISTENCY_DIR / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("Cargo.toml does not exist")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "[workspace]" in content, (
            "Root Cargo.toml does not define a [workspace] section"
        )
        assert "members" in content, (
            "Root Cargo.toml workspace section does not define members"
        )

    def test_workspace_includes_rust_kvs(self):
        """Workspace must include the rust_kvs crate."""
        cargo_toml = PERSISTENCY_DIR / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("Cargo.toml does not exist")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "rust_kvs" in content, (
            "Workspace does not include rust_kvs crate"
        )

    def test_workspace_includes_rust_kvs_tool(self):
        """Workspace must include the rust_kvs_tool crate."""
        cargo_toml = PERSISTENCY_DIR / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("Cargo.toml does not exist")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "rust_kvs_tool" in content, (
            "Workspace does not include rust_kvs_tool crate"
        )

    def test_workspace_includes_test_scenarios(self):
        """Workspace must include the test_scenarios crate."""
        cargo_toml = PERSISTENCY_DIR / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("Cargo.toml does not exist")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "test_scenarios" in content, (
            "Workspace does not include test_scenarios crate"
        )
