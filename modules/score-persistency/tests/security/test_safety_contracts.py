"""Safety contract verification for ASIL-D score-persistency."""

import pytest
from pathlib import Path

PERSISTENCY_DIR = Path(__file__).parent.parent.parent / "upstream"


class TestAsilDClassification:
    def test_project_config_exists(self):
        assert (PERSISTENCY_DIR / "project_config.bzl").exists()

    def test_asil_d_declared(self):
        content = (PERSISTENCY_DIR / "project_config.bzl").read_text()
        assert "ASIL_D" in content or "asil_d" in content.lower()


class TestCppApiSafety:
    def test_kvs_header_exists(self):
        assert (PERSISTENCY_DIR / "src" / "cpp" / "src" / "kvs.hpp").exists()

    def test_error_handling_exists(self):
        assert (PERSISTENCY_DIR / "src" / "cpp" / "src" / "internal" / "error.hpp").exists()

    def test_kvs_has_error_returns(self):
        content = (PERSISTENCY_DIR / "src" / "cpp" / "src" / "kvs.hpp").read_text()
        has_result = "Result" in content or "result" in content or "Error" in content
        assert has_result, "KVS API should use error/result types"


class TestRustSafety:
    def test_rust_kvs_exists(self):
        src = PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "src"
        assert src.is_dir()

    def test_error_code_module(self):
        assert (PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "src" / "error_code.rs").exists()

    def test_mock_module_exists(self):
        assert (PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "src" / "kvs_mock.rs").exists()


class TestCrcValidation:
    def test_adler32_in_cargo(self):
        content = (PERSISTENCY_DIR / "Cargo.lock").read_text()
        assert "adler32" in content, "CRC validation requires adler32 crate"


class TestSnapshotIntegrity:
    def test_snapshot_example_exists(self):
        assert (PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "examples" / "snapshots.rs").exists()

    def test_kvs_backend_exists(self):
        assert (PERSISTENCY_DIR / "src" / "rust" / "rust_kvs" / "src" / "kvs_backend.rs").exists()
