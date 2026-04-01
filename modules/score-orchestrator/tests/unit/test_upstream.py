"""Unit test wrapper for score-orchestrator upstream tests (ASIL B)."""

import subprocess
import os
import re
from pathlib import Path

import pytest

ORCH_DIR = Path(__file__).resolve().parents[4] / "score-orchestrator"
CARGO_ENV = {
    **os.environ,
    "PATH": f"{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""),
}


def _run(cmd, cwd=None, timeout=600, env=None):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or ORCH_DIR,
        capture_output=True, text=True, timeout=timeout,
        env=env or CARGO_ENV,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.score_orchestrator
class TestCargoUnitTests:

    def test_cargo_test_workspace(self):
        rc, out, err = _run("cargo test --workspace 2>&1", timeout=600)
        combined = out + err
        if rc != 0 and "could not find" in combined.lower():
            pytest.skip("Cargo not available")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"

    def test_orchestration_crate(self):
        rc, out, err = _run("cargo test -p orchestration 2>&1", timeout=300)
        combined = out + err
        if rc != 0 and "no such package" in combined.lower():
            pytest.skip("orchestration package not found")
        assert rc == 0, f"orchestration tests failed:\n{combined[-1000:]}"


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.score_orchestrator
class TestBazelUnitTests:

    def test_bazel_test_all(self):
        rc, out, err = _run(
            "bazel test //... --build_tests_only --test_output=summary",
            timeout=1800,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        assert rc == 0, f"Bazel tests failed:\n{(out+err)[-2000:]}"
