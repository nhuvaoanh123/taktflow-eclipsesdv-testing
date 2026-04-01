"""Unit test wrapper for score-scrample upstream tests (ASIL B)."""

import subprocess
from pathlib import Path

import pytest

MODULE_DIR = Path(__file__).resolve().parents[4] / "score-scrample"
LOCKFILE = "--lockfile_mode=update"
CONFIG = "--config=x86_64-linux"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.score_scrample
class TestUpstreamUnitTests:

    def test_bazel_test_all(self):
        rc, out, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //... "
            "--build_tests_only --test_output=summary",
            timeout=1800,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        assert rc == 0, f"Tests failed:\n{(out+err)[-2000:]}"

    def test_scorex_go_tests(self):
        """Run scorex Go tests."""
        scorex = MODULE_DIR / "scorex"
        if not scorex.is_dir():
            pytest.skip("scorex/ not found")
        rc, out, err = _run("go test ./...", cwd=scorex, timeout=300)
        if rc != 0 and "not found" in (out + err).lower():
            pytest.skip("Go not available")
        assert rc == 0, f"scorex tests failed:\n{(out+err)[-1000:]}"
