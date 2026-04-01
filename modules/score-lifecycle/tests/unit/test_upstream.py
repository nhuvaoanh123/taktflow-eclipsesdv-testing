"""Unit test wrapper for score-lifecycle upstream tests (ASIL B).

Wraps Bazel unit test execution into pytest for ASIL B evidence.
"""

import subprocess
from pathlib import Path

import pytest

LIFECYCLE_DIR = Path(__file__).resolve().parents[4] / "modules" / "score-lifecycle" / "upstream"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or LIFECYCLE_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.score_lifecycle
class TestUpstreamUnitTests:
    """Execute upstream unit tests."""

    def test_all_unit_tests(self):
        """Full upstream unit test suite."""
        rc, out, err = _run(
            "bazel test //... --build_tests_only --test_output=summary",
            timeout=1800,
        )
        if rc != 0 and ("not found" in err.lower() or "no targets" in err.lower()):
            pytest.skip("Bazel not available or no test targets")
        combined = out + err
        failed = [l for l in combined.split("\n") if "FAILED" in l]
        assert rc == 0, f"Unit tests failed:\n" + "\n".join(failed[:20])

    def test_health_monitoring_tests(self):
        """Health monitoring library tests."""
        rc, _, err = _run(
            "bazel test //src/health_monitoring_lib/... --test_output=errors",
            timeout=600,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("health_monitoring_lib test targets not found")
        assert rc == 0, f"Health monitoring tests failed:\n{err[-1000:]}"
