"""Build and test verification for eclipse-kuksa-databroker.

Run on Linux laptop:
    pytest modules/kuksa-databroker/tests/build/test_build.py -v
"""

import subprocess
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "eclipse-kuksa-databroker"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
        capture_output=True, text=True, timeout=timeout,
        env={**__import__("os").environ, "PATH": f"{Path.home()}/.cargo/bin:" + __import__("os").environ.get("PATH", "")},
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"kuksa-databroker not found at {MODULE_DIR}"
    assert (MODULE_DIR / "Cargo.toml").exists(), "Cargo.toml missing"
    return MODULE_DIR


class TestEnvironment:

    def test_cargo_installed(self):
        rc, out, _ = _run("cargo --version")
        assert rc == 0, "Cargo not installed"

    def test_protoc_available(self):
        rc, _, _ = _run("protoc --version")
        if rc != 0:
            pytest.skip("protoc not installed — proto compilation uses bundled version")


class TestBuild:

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_cargo_build_workspace(self, module_dir):
        rc, out, err = _run("cargo build --workspace", timeout=600)
        assert rc == 0, f"Build failed:\n{err[-2000:]}"

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_databroker_binary(self, module_dir):
        rc, _, err = _run("cargo build -p databroker", timeout=600)
        assert rc == 0, f"databroker build failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_databroker_cli(self, module_dir):
        rc, _, err = _run("cargo build -p databroker-cli", timeout=300)
        assert rc == 0, f"CLI build failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_proto_compilation(self, module_dir):
        rc, _, err = _run("cargo build -p databroker-proto", timeout=300)
        assert rc == 0, f"Proto build failed:\n{err[-1000:]}"


class TestUnitTests:

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_cargo_test_workspace(self, module_dir):
        rc, out, err = _run("cargo test --workspace 2>&1", timeout=600)
        combined = out + err
        print(combined[-3000:])
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_databroker_tests(self, module_dir):
        rc, out, err = _run("cargo test -p databroker 2>&1", timeout=300)
        assert rc == 0, f"databroker tests failed:\n{(out+err)[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_proto_tests(self, module_dir):
        rc, out, err = _run(
            "cargo test -p databroker-proto 2>&1", timeout=300,
        )
        assert rc == 0, f"proto tests failed:\n{(out+err)[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_glob_matching(self, module_dir):
        """Verify VSS glob/wildcard path matching logic."""
        rc, out, err = _run(
            "cargo test -p databroker --lib glob 2>&1", timeout=120,
        )
        assert rc == 0, f"glob tests failed:\n{(out+err)[-500:]}"

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_authorization(self, module_dir):
        """Verify JWT auth and scope handling."""
        rc, out, err = _run(
            "cargo test -p databroker --lib authorization 2>&1", timeout=120,
        )
        assert rc == 0, f"auth tests failed:\n{(out+err)[-500:]}"

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_query_executor(self, module_dir):
        """Verify SQL-like query execution on VSS tree."""
        rc, out, err = _run(
            "cargo test -p databroker --lib query 2>&1", timeout=120,
        )
        assert rc == 0, f"query tests failed:\n{(out+err)[-500:]}"


class TestCodeQuality:

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_clippy(self, module_dir):
        rc, _, err = _run(
            "cargo clippy --workspace -- -D warnings 2>&1",
            timeout=300,
        )
        assert rc == 0, f"Clippy warnings:\n{err[-2000:]}"

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_fmt_check(self, module_dir):
        rc, _, err = _run("cargo fmt --all -- --check 2>&1", timeout=60)
        assert rc == 0, f"Format check failed:\n{err[-1000:]}"


class TestVSSData:

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_vss_json_exists(self, module_dir):
        """Verify VSS 4.0 metadata file is present."""
        vss = module_dir / "data" / "vss-core" / "vss_release_4.0.json"
        assert vss.exists(), f"VSS JSON not found at {vss}"

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_vss_json_valid(self, module_dir):
        """Verify VSS JSON parses correctly."""
        import json
        vss = module_dir / "data" / "vss-core" / "vss_release_4.0.json"
        if not vss.exists():
            pytest.skip("VSS JSON not found")
        with open(vss) as f:
            data = json.load(f)
        assert len(data) > 0, "VSS JSON is empty"
