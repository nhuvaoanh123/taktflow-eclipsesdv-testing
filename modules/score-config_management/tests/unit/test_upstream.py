"""Unit test wrapper for score-config_management upstream tests (ASIL B)."""

import subprocess
from pathlib import Path

import pytest

MODULE_DIR = Path(__file__).resolve().parents[4] / "score-config_management"
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
@pytest.mark.score_config_management
class TestUpstreamUnitTests:

    def test_all_unit_tests(self):
        rc, out, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //... "
            "--build_tests_only --test_output=summary",
            timeout=1800,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        assert rc == 0, f"Tests failed:\n{(out+err)[-2000:]}"

    def test_config_provider_tests(self):
        rc, _, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} "
            "//score/config_management/config_provider/... "
            "--test_output=errors",
            timeout=600,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("config_provider test targets not found")
        assert rc == 0, f"config_provider tests failed:\n{err[-1000:]}"
