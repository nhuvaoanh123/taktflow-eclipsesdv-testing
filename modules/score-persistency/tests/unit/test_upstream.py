"""Unit test wrapper for score-persistency upstream tests (ASIL D)."""

import subprocess
from pathlib import Path

import pytest

PERSISTENCY_DIR = Path(__file__).resolve().parents[4] / "modules" / "score-persistency" / "upstream"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or PERSISTENCY_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.mark.asil_d
@pytest.mark.unit
@pytest.mark.score_persistency
class TestUpstreamUnitTests:

    def test_all_unit_tests(self):
        rc, out, err = _run(
            "bazel test //... --build_tests_only --test_output=summary",
            timeout=1800,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        assert rc == 0, f"Tests failed:\n{(out+err)[-2000:]}"

    def test_kv_store_tests(self):
        rc, _, err = _run(
            "bazel test //score/persistency/... --test_output=errors",
            timeout=600,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("persistency test targets not found")
        assert rc == 0, f"KV store tests failed:\n{err[-1000:]}"
