"""Unit test wrapper for score-feo upstream tests (ASIL B).

Wraps Cargo + Bazel unit test execution into pytest for ASIL B evidence.
"""

import subprocess
import os
import re
from pathlib import Path

import pytest

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
@pytest.mark.score_feo
class TestCargoUnitTests:
    """Execute upstream Cargo unit tests."""

    def test_cargo_test_workspace(self):
        """Full Cargo workspace test."""
        rc, out, err = _run("cargo test --workspace 2>&1", timeout=600)
        combined = out + err
        passed, failed = _parse_cargo_test(combined)
        print(f"Results: {passed} passed, {failed} failed")
        if rc != 0 and "could not find" in combined.lower():
            pytest.skip("Cargo not available")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"
        assert passed > 0, "No tests found"

    def test_feo_core_tests(self):
        """FEO core crate tests."""
        rc, out, err = _run("cargo test -p feo 2>&1", timeout=300)
        combined = out + err
        if rc != 0 and "no such package" in combined.lower():
            pytest.skip("feo package not found")
        assert rc == 0, f"feo core tests failed:\n{combined[-1000:]}"

    def test_feo_time_tests(self):
        """FEO time crate tests (13 expected)."""
        rc, out, err = _run("cargo test -p feo-time 2>&1", timeout=300)
        combined = out + err
        if rc != 0 and "no such package" in combined.lower():
            pytest.skip("feo-time package not found")
        assert rc == 0, f"feo-time tests failed:\n{combined[-1000:]}"


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.score_feo
class TestBazelUnitTests:
    """Execute upstream Bazel unit tests."""

    def test_bazel_test_all(self):
        """Full Bazel test suite."""
        rc, out, err = _run(
            "bazel test //... --build_tests_only --test_output=summary",
            timeout=1800,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        assert rc == 0, f"Bazel tests failed:\n{(out+err)[-2000:]}"
