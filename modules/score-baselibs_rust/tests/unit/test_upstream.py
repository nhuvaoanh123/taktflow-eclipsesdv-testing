"""Unit test wrapper for score-baselibs_rust upstream tests (ASIL B).

Wraps Cargo + Bazel test execution into pytest for ASIL B evidence.
"""

import subprocess
import os
import re
from pathlib import Path

import pytest

MODULE_DIR = Path(__file__).resolve().parents[4] / "score-baselibs_rust"
CARGO_ENV = {
    **os.environ,
    "PATH": f"{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""),
}


def _run(cmd, cwd=None, timeout=600, env=None):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
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
@pytest.mark.score_baselibs_rust
class TestCargoUnitTests:
    """Execute upstream Cargo unit tests."""

    def test_cargo_test_workspace(self):
        rc, out, err = _run("cargo test --workspace 2>&1", timeout=600)
        combined = out + err
        if rc != 0 and "could not find" in combined.lower():
            pytest.skip("Cargo not available")
        passed, failed = _parse_cargo_test(combined)
        print(f"Results: {passed} passed, {failed} failed")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"
        assert passed > 0, "No tests found"

    def test_containers_tests(self):
        rc, out, err = _run("cargo test -p containers 2>&1", timeout=300)
        combined = out + err
        if rc != 0 and "no such package" in combined.lower():
            pytest.skip("containers package not found")
        assert rc == 0, f"containers tests failed:\n{combined[-1000:]}"

    def test_sync_tests(self):
        rc, out, err = _run("cargo test -p sync 2>&1", timeout=300)
        combined = out + err
        if rc != 0 and "no such package" in combined.lower():
            pytest.skip("sync package not found")
        assert rc == 0, f"sync tests failed:\n{combined[-1000:]}"


@pytest.mark.asil_b
@pytest.mark.unit
@pytest.mark.score_baselibs_rust
class TestBazelUnitTests:
    """Execute upstream Bazel unit tests."""

    def test_bazel_test_all(self):
        rc, out, err = _run(
            "bazel test --lockfile_mode=update --config=x86_64-linux "
            "//src/... --build_tests_only --test_output=summary",
            timeout=1800,
        )
        if rc != 0 and "not found" in err.lower():
            pytest.skip("Bazel not available")
        assert rc == 0, f"Bazel tests failed:\n{(out+err)[-2000:]}"
