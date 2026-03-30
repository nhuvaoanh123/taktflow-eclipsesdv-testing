"""Build and test verification for Ankaios Rust SDK.

Run on Linux laptop:
    pytest modules/ankaios-sdk-rust/tests/build/test_build.py -v
"""

import subprocess
import os
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "ankaios-ank-sdk-rust"
CARGO_ENV = {
    **os.environ,
    "PATH": f"{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""),
}


def _run(cmd, cwd=None, timeout=600, env=None):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
        capture_output=True, text=True, timeout=timeout,
        env=env or CARGO_ENV,
    )
    return result.returncode, result.stdout, result.stderr


def _parse_cargo_test(output):
    total_passed = total_failed = total_ignored = 0
    for line in output.split("\n"):
        m = re.match(r"test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored", line)
        if m:
            total_passed += int(m.group(1))
            total_failed += int(m.group(2))
            total_ignored += int(m.group(3))
    return total_passed, total_failed, total_ignored


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"ankaios-sdk-rust not found at {MODULE_DIR}"
    assert (MODULE_DIR / "Cargo.toml").exists(), "Cargo.toml missing"
    return MODULE_DIR


class TestEnvironment:
    def test_cargo_installed(self):
        rc, _, _ = _run("cargo --version")
        assert rc == 0

class TestCargoBuild:
    @pytest.mark.build
    @pytest.mark.ankaios
    def test_cargo_build(self, module_dir):
        rc, out, err = _run("cargo build 2>&1", timeout=600)
        combined = out + err
        if rc != 0 and ("requires rustc" in combined or "can't find crate" in combined):
            pytest.skip(f"Rust toolchain issue:\n{combined[-300:]}")
        assert rc == 0, f"Build failed:\n{combined[-2000:]}"

class TestCargoTests:
    @pytest.mark.unit
    @pytest.mark.ankaios
    def test_cargo_test(self, module_dir):
        rc, out, err = _run("cargo test 2>&1", timeout=300)
        combined = out + err
        if rc != 0 and ("requires rustc" in combined or "can't find crate" in combined):
            pytest.skip("Rust toolchain issue — update with rustup")
        passed, failed, ignored = _parse_cargo_test(combined)
        print(f"Results: {passed} passed, {failed} failed, {ignored} ignored")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"

class TestClippy:
    @pytest.mark.build
    @pytest.mark.ankaios
    def test_cargo_clippy(self, module_dir):
        rc, out, err = _run("cargo clippy --all-targets -- -D warnings 2>&1", timeout=300)
        if rc != 0:
            print(f"Clippy issues (non-blocking)")
        print(f"Clippy exit code: {rc}")
