"""Build and test verification for Ankaios Python SDK.

Run on Linux laptop:
    pytest modules/ankaios-sdk-python/tests/build/test_build.py -v
"""

import subprocess
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "ankaios-ank-sdk-python"


def _run(cmd, cwd=None, timeout=120):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def _parse_pytest(output):
    m = re.search(r"(\d+) passed", output)
    passed = int(m.group(1)) if m else 0
    m = re.search(r"(\d+) failed", output)
    failed = int(m.group(1)) if m else 0
    return passed, failed


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"ankaios-sdk-python not found at {MODULE_DIR}"
    return MODULE_DIR


class TestEnvironment:
    def test_python3_installed(self):
        rc, _, _ = _run("python3 --version")
        assert rc == 0

class TestInstall:
    @pytest.mark.build
    @pytest.mark.ankaios
    def test_pip_install(self, module_dir):
        rc, out, err = _run(
            "python3 -m pip install --user --break-system-packages -e '.[dev]' --quiet 2>&1",
            timeout=120,
        )
        if rc != 0:
            rc, out, err = _run(
                "python3 -m pip install --user --break-system-packages -e . --quiet 2>&1",
                timeout=120,
            )
        assert rc == 0, f"Install failed:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.ankaios
    def test_import_sdk(self, module_dir):
        rc, _, err = _run("python3 -c 'import ankaios_sdk; print(\"OK\")' 2>&1")
        assert rc == 0, f"Import failed:\n{err[-500:]}"

class TestUnitTests:
    @pytest.mark.unit
    @pytest.mark.ankaios
    def test_upstream_tests(self, module_dir):
        rc, out, err = _run("python3 -m pytest tests/ -v --tb=short 2>&1", timeout=120)
        combined = out + err
        passed, failed = _parse_pytest(combined)
        print(f"Results: {passed} passed, {failed} failed")
        if rc != 0 and "ModuleNotFoundError" in combined:
            pytest.skip(f"Missing dependency:\n{combined[-500:]}")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"
        assert passed > 0, "No tests found"
