"""Build and test verification for score-persistency (ASIL D).

Wraps Bazel build commands into pytest for ASIL D evidence.

Run: pytest modules/score-persistency/tests/build/test_build.py -v
"""

import subprocess
import pytest
from pathlib import Path

PERSISTENCY_DIR = Path(__file__).resolve().parents[4] / "modules" / "score-persistency" / "upstream"
LOCKFILE = "--lockfile_mode=update"
CONFIG = "--config=x86_64-linux"


def _run(cmd, cwd=None, timeout=600):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or PERSISTENCY_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="session")
def module_dir():
    assert PERSISTENCY_DIR.exists(), f"score-persistency not found at {PERSISTENCY_DIR}"
    assert (PERSISTENCY_DIR / "MODULE.bazel").exists(), "MODULE.bazel missing"
    return PERSISTENCY_DIR


class TestEnvironment:

    def test_bazel_installed(self):
        rc, _, _ = _run("bazel --version")
        assert rc == 0, "Bazel not installed"

    def test_bazel_version_matches(self):
        bzl_version = PERSISTENCY_DIR / ".bazelversion"
        if not bzl_version.exists():
            pytest.skip(".bazelversion not found")
        expected = bzl_version.read_text().strip()
        rc, out, _ = _run("bazel --version")
        assert expected in out, f"Expected Bazel {expected}, got: {out}"


class TestBuild:

    @pytest.mark.build
    @pytest.mark.score_persistency
    def test_bazel_build_all(self, module_dir):
        rc, _, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //...", timeout=1200,
        )
        assert rc == 0, f"Build failed:\n{err[-2000:]}"


class TestUnitTests:

    @pytest.mark.unit
    @pytest.mark.score_persistency
    def test_all_unit_tests(self, module_dir):
        rc, out, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //... "
            "--build_tests_only --test_output=summary",
            timeout=1800,
        )
        combined = out + err
        failed = [l for l in combined.split("\n") if "FAILED" in l]
        assert rc == 0, (
            f"Unit tests failed ({len(failed)}):\n"
            + "\n".join(failed[:20])
        )


class TestCodeQuality:

    @pytest.mark.build
    @pytest.mark.score_persistency
    def test_lockfile_present(self, module_dir):
        lock = module_dir / "MODULE.bazel.lock"
        assert lock.exists(), "MODULE.bazel.lock missing"
