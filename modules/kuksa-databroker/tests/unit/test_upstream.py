"""Unit test wrapper for kuksa-databroker upstream tests (ASIL B)."""

import subprocess
import os
import re
from pathlib import Path

import pytest

DATABROKER_DIR = Path(__file__).resolve().parents[4] / "eclipse-kuksa-databroker"
CARGO_ENV = {
    **os.environ,
    "PATH": f"{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""),
}


def _run(cmd, cwd=None, timeout=600, env=None):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or DATABROKER_DIR,
        capture_output=True, text=True, timeout=timeout,
        env=env or CARGO_ENV,
    )
    return result.returncode, result.stdout, result.stderr


def _parse_cargo_test(output):
    total_passed = 0
    total_failed = 0
    for line in output.split("\n"):
        m = re.match(
            r"test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored",
            line,
        )
        if m:
            total_passed += int(m.group(1))
            total_failed += int(m.group(2))
    return total_passed, total_failed


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.kuksa
class TestCargoUnitTests:

    def test_cargo_test_workspace(self):
        rc, out, err = _run("cargo test --workspace 2>&1", timeout=600)
        combined = out + err
        if rc != 0 and "could not find" in combined.lower():
            pytest.skip("Cargo not available")
        passed, failed = _parse_cargo_test(combined)
        print(f"Results: {passed} passed, {failed} failed")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"

    def test_databroker_crate(self):
        rc, out, err = _run("cargo test -p databroker 2>&1", timeout=300)
        combined = out + err
        if rc != 0 and "no such package" in combined.lower():
            pytest.skip("databroker package not found")
        assert rc == 0, f"databroker tests failed:\n{combined[-1000:]}"

    def test_lib_crate(self):
        rc, out, err = _run("cargo test -p lib 2>&1", timeout=300)
        combined = out + err
        if rc != 0 and "no such package" in combined.lower():
            pytest.skip("lib package not found")
        assert rc == 0, f"lib tests failed:\n{combined[-1000:]}"
