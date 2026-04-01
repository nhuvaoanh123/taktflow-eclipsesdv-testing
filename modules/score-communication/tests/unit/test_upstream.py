"""Unit test wrapper for score-communication upstream tests (ASIL B).

Wraps Bazel unit test execution into pytest for unified ASIL B evidence.
Actual test logic lives in the upstream repo; this wrapper captures
pass/fail status and integrates with JUnit XML reporting.

Run: pytest modules/score-communication/tests/unit/ -v
"""

import subprocess
from pathlib import Path

import pytest

LOLA_DIR = Path(__file__).resolve().parents[4] / "modules" / "score-communication" / "upstream"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or LOLA_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.score_communication
class TestUpstreamUnitTests:
    """Execute upstream Bazel unit tests and capture results."""

    def test_message_passing_layer(self):
        """score/message_passing unit tests."""
        rc, _, err = _run(
            "bazel test //score/message_passing/... --test_output=errors",
            timeout=600,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        assert rc == 0, f"message_passing tests failed:\n{err[-1000:]}"

    def test_mw_com_impl(self):
        """score/mw/com/impl unit tests."""
        rc, _, err = _run(
            "bazel test //score/mw/com/impl/... --test_output=errors",
            timeout=600,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        assert rc == 0, f"mw/com/impl tests failed:\n{err[-1000:]}"

    def test_all_unit_tests(self):
        """Full upstream unit test suite."""
        rc, out, err = _run(
            "bazel test //... --build_tests_only --test_output=summary",
            timeout=1800,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        combined = out + err
        failed = [l for l in combined.split("\n") if "FAILED" in l and "//" in l]
        assert rc == 0, (
            f"Unit tests failed ({len(failed)} failures):\n"
            + "\n".join(failed[:20])
        )
