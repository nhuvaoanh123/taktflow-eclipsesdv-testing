"""Build and test verification for score-orchestrator.

Run on Linux laptop:
    pytest modules/score-orchestrator/tests/build/test_build.py -v
"""

import subprocess
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "score-orchestrator"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
        capture_output=True, text=True, timeout=timeout,
        env={**__import__("os").environ, "PATH": f"{Path.home()}/.cargo/bin:" + __import__("os").environ.get("PATH", "")},
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"score-orchestrator not found at {MODULE_DIR}"
    assert (MODULE_DIR / "Cargo.toml").exists(), "Cargo.toml missing"
    return MODULE_DIR


class TestEnvironment:

    def test_cargo_installed(self):
        rc, out, _ = _run("cargo --version")
        assert rc == 0, "Cargo not installed"

    def test_rustc_installed(self):
        rc, out, _ = _run("rustc --version")
        assert rc == 0, "Rust compiler not installed"


class TestBuild:

    @pytest.mark.build
    @pytest.mark.score_orchestrator
    def test_cargo_build_workspace(self, module_dir):
        rc, out, err = _run("cargo build --workspace", timeout=600)
        assert rc == 0, f"Build failed:\n{err[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_orchestrator
    def test_cargo_build_release(self, module_dir):
        rc, _, err = _run("cargo build --release --workspace", timeout=600)
        assert rc == 0, f"Release build failed:\n{err[-2000:]}"


class TestUnitTests:

    @pytest.mark.unit
    @pytest.mark.score_orchestrator
    def test_cargo_test_workspace(self, module_dir):
        rc, out, err = _run("cargo test --workspace 2>&1", timeout=600)
        combined = out + err
        print(combined[-3000:])
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"

    @pytest.mark.unit
    @pytest.mark.score_orchestrator
    def test_orchestration_lib(self, module_dir):
        rc, out, err = _run(
            "cargo test -p orchestration 2>&1", timeout=300,
        )
        assert rc == 0, f"orchestration tests failed:\n{(out+err)[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.score_orchestrator
    def test_orchestration_macros(self, module_dir):
        rc, out, err = _run(
            "cargo test -p orchestration_macros --lib 2>&1", timeout=300,
        )
        assert rc == 0, f"macros tests failed:\n{(out+err)[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.score_orchestrator
    def test_component_integration(self, module_dir):
        """Run the test_scenarios binary (multi-scenario CIT)."""
        rc, out, err = _run(
            "cargo test -p test_scenarios 2>&1", timeout=300,
        )
        assert rc == 0, f"CIT scenarios failed:\n{(out+err)[-2000:]}"


class TestCodeQuality:

    @pytest.mark.build
    @pytest.mark.score_orchestrator
    def test_clippy(self, module_dir):
        rc, _, err = _run(
            "cargo clippy --workspace -- -D warnings 2>&1",
            timeout=300,
        )
        assert rc == 0, f"Clippy warnings:\n{err[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_orchestrator
    def test_fmt_check(self, module_dir):
        rc, _, err = _run("cargo fmt --all -- --check 2>&1", timeout=60)
        assert rc == 0, f"Format check failed:\n{err[-1000:]}"
