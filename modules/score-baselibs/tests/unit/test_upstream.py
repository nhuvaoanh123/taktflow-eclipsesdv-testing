"""Unit test wrapper for score-baselibs upstream tests (ASIL B)."""

import subprocess
from pathlib import Path

import pytest

BASELIBS_DIR = Path(__file__).resolve().parents[4] / "modules" / "score-baselibs" / "upstream"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or BASELIBS_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.score_baselibs
class TestUpstreamUnitTests:

    def test_all_unit_tests(self):
        rc, out, err = _run(
            "bazel test //... --build_tests_only --test_output=summary",
            timeout=1800,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        combined = out + err
        failed = [l for l in combined.split("\n") if "FAILED" in l]
        assert rc == 0, f"Tests failed ({len(failed)}):\n" + "\n".join(failed[:20])

    def test_os_abstraction_tests(self):
        rc, _, err = _run(
            "bazel test //score/os/... --test_output=errors", timeout=600,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("OS test targets not found")
        assert rc == 0, f"OS tests failed:\n{err[-1000:]}"

    def test_concurrency_tests(self):
        rc, _, err = _run(
            "bazel test //score/concurrency/... --test_output=errors",
            timeout=600,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("concurrency test targets not found")
        assert rc == 0, f"concurrency tests failed:\n{err[-1000:]}"
