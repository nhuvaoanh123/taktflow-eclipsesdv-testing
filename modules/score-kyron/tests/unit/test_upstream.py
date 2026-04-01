"""Unit test wrapper for score-kyron upstream tests (ASIL B).

Wraps Cargo + Bazel unit test execution into pytest for ASIL B evidence.
"""

import subprocess
import os
import re
from pathlib import Path

import pytest

KYRON_DIR = Path(__file__).resolve().parents[4] / "score-kyron"
CARGO_ENV = {
    **os.environ,
    "PATH": f"{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""),
}


def _run(cmd, cwd=None, timeout=600, env=None):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or KYRON_DIR,
        capture_output=True, text=True, timeout=timeout,
        env=env or CARGO_ENV,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.score_kyron
class TestCargoUnitTests:
    """Execute upstream Cargo unit tests."""

    def test_cargo_test_workspace(self):
        rc, out, err = _run("cargo test --workspace 2>&1", timeout=600)
        combined = out + err
        if rc != 0 and "could not find" in combined.lower():
            pytest.skip("Cargo not available")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"

    def test_kyron_core_tests(self):
        rc, out, err = _run("cargo test -p kyron 2>&1", timeout=300)
        combined = out + err
        if rc != 0 and "no such package" in combined.lower():
            pytest.skip("kyron package not found")
        assert rc == 0, f"kyron core tests failed:\n{combined[-1000:]}"

    def test_kyron_foundation_tests(self):
        rc, out, err = _run("cargo test -p kyron-foundation 2>&1", timeout=300)
        combined = out + err
        if rc != 0 and "no such package" in combined.lower():
            pytest.skip("kyron-foundation not found")
        assert rc == 0, f"kyron-foundation tests failed:\n{combined[-1000:]}"


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.score_kyron
class TestBazelUnitTests:
    """Execute upstream Bazel unit tests."""

    def test_bazel_test_all(self):
        rc, out, err = _run(
            "bazel test //src/... --build_tests_only --test_output=summary",
            timeout=1800,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        assert rc == 0, f"Bazel tests failed:\n{(out+err)[-2000:]}"
