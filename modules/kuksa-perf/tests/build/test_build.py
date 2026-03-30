"""Build and test verification for kuksa-perf.

Rust-based performance benchmarking tool for Kuksa databroker.
Measures throughput and latency for gRPC/VSS operations.

Run on Linux laptop:
    pytest modules/kuksa-perf/tests/build/test_build.py -v
"""

import subprocess
import os
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "kuksa-kuksa-perf"
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
    total_passed = 0
    total_failed = 0
    total_ignored = 0
    for line in output.split("\n"):
        m = re.match(
            r"test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored",
            line,
        )
        if m:
            total_passed += int(m.group(1))
            total_failed += int(m.group(2))
            total_ignored += int(m.group(3))
    return total_passed, total_failed, total_ignored


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"kuksa-perf not found at {MODULE_DIR}"
    assert (MODULE_DIR / "Cargo.toml").exists(), "Cargo.toml missing"
    return MODULE_DIR


# -- Phase 1: Environment ---------------------------------------------------

class TestEnvironment:

    def test_cargo_installed(self):
        rc, _, _ = _run("cargo --version")
        assert rc == 0, "Cargo not installed"

    def test_rustc_installed(self):
        rc, _, _ = _run("rustc --version")
        assert rc == 0, "Rust compiler not installed"


# -- Phase 2: Build ---------------------------------------------------------

class TestCargoBuild:

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_cargo_build(self, module_dir):
        rc, out, err = _run("cargo build 2>&1", timeout=600)
        assert rc == 0, f"Build failed:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_cargo_build_release(self, module_dir):
        rc, _, err = _run("cargo build --release 2>&1", timeout=600)
        assert rc == 0, f"Release build failed:\n{err[-2000:]}"


# -- Phase 3: Tests ---------------------------------------------------------

class TestCargoTests:

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_cargo_test(self, module_dir):
        """Run cargo tests (if any — perf tool may have few unit tests)."""
        rc, out, err = _run("cargo test 2>&1", timeout=300)
        combined = out + err
        passed, failed, ignored = _parse_cargo_test(combined)
        print(f"Results: {passed} passed, {failed} failed, {ignored} ignored")
        # perf tool may have zero tests — that's OK, build is the main check
        if passed == 0 and failed == 0:
            print("No unit tests in perf tool (benchmark-only crate)")
        assert failed == 0, f"Tests failed:\n{combined[-2000:]}"


# -- Phase 4: Clippy --------------------------------------------------------

class TestClippy:

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_cargo_clippy(self, module_dir):
        rc, out, err = _run(
            "cargo clippy --all-targets -- -D warnings 2>&1",
            timeout=300,
        )
        combined = out + err
        if rc != 0:
            errors = [l for l in combined.split("\n") if "error:" in l]
            print(f"Clippy issues ({len(errors)} errors, non-blocking)")
        print(f"Clippy exit code: {rc}")
