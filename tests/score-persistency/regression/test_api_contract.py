"""Regression tests for score-persistency API contract stability."""

import pytest
from pathlib import Path

PERSISTENCY_DIR = Path(__file__).parent.parent.parent.parent / "score-persistency"


class TestModuleIdentity:
    def test_module_bazel_exists(self):
        assert (PERSISTENCY_DIR / "MODULE.bazel").exists()

    def test_module_name(self):
        content = (PERSISTENCY_DIR / "MODULE.bazel").read_text()
        assert "score_persistency" in content

    def test_module_version(self):
        content = (PERSISTENCY_DIR / "MODULE.bazel").read_text()
        assert 'version = "0.0.0"' in content


class TestCppApiContract:
    @pytest.mark.parametrize("header", ["kvs.hpp", "kvsbuilder.hpp", "kvsvalue.hpp"])
    def test_cpp_header_exists(self, header):
        assert (PERSISTENCY_DIR / "src" / "cpp" / "src" / header).exists()

    def test_cpp_build_file(self):
        assert (PERSISTENCY_DIR / "src" / "cpp" / "src" / "BUILD").exists()


class TestCppInternalContract:
    @pytest.mark.parametrize("header", ["error.hpp", "kvs_helper.hpp"])
    def test_internal_header_exists(self, header):
        assert (PERSISTENCY_DIR / "src" / "cpp" / "src" / "internal" / header).exists()


class TestRustCrateContract:
    def test_rust_kvs_cargo_toml(self):
        assert (PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "Cargo.toml").exists()

    @pytest.mark.parametrize("module", [
        "kvs.rs", "kvs_api.rs", "kvs_builder.rs", "kvs_value.rs",
        "kvs_backend.rs", "kvs_mock.rs", "json_backend.rs",
        "kvs_serialize.rs", "error_code.rs",
    ])
    def test_rust_module_exists(self, module):
        src = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "src"
        assert (src / module).exists(), f"{module} not found in {src}"


class TestRustToolContract:
    def test_kvs_tool_exists(self):
        tool = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs_tool"
        assert tool.is_dir()
        rs_files = list(tool.rglob("*.rs"))
        assert len(rs_files) > 0


class TestCppTestFiles:
    @pytest.mark.parametrize("test_file", [
        "test_kvs.cpp", "test_kvs_builder.cpp", "test_kvs_error.cpp",
        "test_kvs_general.cpp", "test_kvs_helper.cpp", "bm_kvs.cpp",
    ])
    def test_cpp_test_file_exists(self, test_file):
        assert (PERSISTENCY_DIR / "src" / "cpp" / "tests" / test_file).exists()


class TestRustExamples:
    @pytest.mark.parametrize("example", [
        "basic.rs", "snapshots.rs", "defaults.rs",
        "custom_types.rs", "migration.rs",
    ])
    def test_example_exists(self, example):
        examples_dir = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "examples"
        assert (examples_dir / example).exists()


class TestCargoWorkspace:
    def test_root_cargo_toml(self):
        assert (PERSISTENCY_DIR / "Cargo.toml").exists()

    def test_cargo_lock(self):
        assert (PERSISTENCY_DIR / "Cargo.lock").exists()

    def test_workspace_has_members(self):
        content = (PERSISTENCY_DIR / "Cargo.toml").read_text()
        assert "members" in content


class TestBuildTargets:
    @pytest.mark.parametrize("build_path", [
        "BUILD", "src/cpp/src/BUILD", "src/rust/rust_kvs/BUILD",
    ])
    def test_build_file_exists(self, build_path):
        assert (PERSISTENCY_DIR / build_path).exists()
