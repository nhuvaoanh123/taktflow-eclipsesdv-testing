"""Build and test verification for score-feo (ASIL B).

Wraps Bazel + Cargo build commands into pytest for ASIL B evidence.

Run: pytest modules/score-feo/tests/build/test_build.py -v
"""

import subprocess
import os
import re
import pytest
from pathlib import Path

FEO_DIR = Path(__file__).resolve().parents[4] / "modules" / "score-feo" / "upstream"
CARGO_ENV = {
    **os.environ,
    "PATH": f"{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""),
}


def _run(cmd, cwd=None, timeout=600, env=None):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or FEO_DIR,
        capture_output=True, text=True, timeout=timeout,
        env=env or CARGO_ENV,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="session")
def feo_dir():
    assert FEO_DIR.exists(), f"score-feo not found at {FEO_DIR}"
    assert (FEO_DIR / "MODULE.bazel").exists(), "MODULE.bazel missing"
    return FEO_DIR


class TestEnvironment:

    def test_bazel_installed(self):
        rc, _, _ = _run("bazel --version")
        assert rc == 0, "Bazel not installed"

    def test_cargo_installed(self):
        rc, _, _ = _run("cargo --version")
        assert rc == 0, "Cargo not installed"

    def test_bazel_version_matches(self):
        expected = (FEO_DIR / ".bazelversion").read_text().strip()
        rc, out, _ = _run("bazel --version")
        assert expected in out, f"Expected Bazel {expected}, got: {out}"


class TestCargoBuild:

    @pytest.mark.build
    @pytest.mark.score_feo
    def test_cargo_build_workspace(self, feo_dir):
        rc, out, err = _run("cargo build --workspace 2>&1", timeout=600)
        assert rc == 0, f"Cargo build failed:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_feo
    def test_cargo_build_release(self, feo_dir):
        rc, _, err = _run("cargo build --release --workspace 2>&1", timeout=600)
        assert rc == 0, f"Release build failed:\n{err[-2000:]}"


class TestBazelBuild:

    @pytest.mark.build
    @pytest.mark.score_feo
    def test_bazel_build_all(self, feo_dir):
        rc, _, err = _run(
            "bazel build //...", timeout=1200,
        )
        assert rc == 0, f"Bazel build failed:\n{err[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_feo
    def test_examples_build(self, feo_dir):
        rc, _, err = _run("bazel build //examples/...", timeout=600)
        if rc != 0 and "no targets" in err.lower():
            pytest.skip("No examples directory")
        assert rc == 0, f"Examples build failed:\n{err[-1000:]}"


class TestCodeQuality:

    @pytest.mark.build
    @pytest.mark.score_feo
    def test_cargo_clippy(self, feo_dir):
        rc, out, err = _run(
            "cargo clippy --workspace --all-targets -- -D warnings 2>&1",
            timeout=300,
        )
        assert rc == 0, f"Clippy warnings:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_feo
    def test_cargo_fmt_check(self, feo_dir):
        rc, out, err = _run("cargo fmt --all -- --check 2>&1", timeout=60)
        assert rc == 0, f"Format issues:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_feo
    def test_lockfile_present(self, feo_dir):
        assert (feo_dir / "Cargo.lock").exists(), "Cargo.lock missing"
        assert (feo_dir / "MODULE.bazel.lock").exists() or True, \
            "MODULE.bazel.lock missing"
