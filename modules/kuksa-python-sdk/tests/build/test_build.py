"""Build and test verification for eclipse-kuksa-python-sdk.

Python client library for Kuksa.val databroker (gRPC + WebSocket).
Upstream tests in kuksa-client/tests/.

Run on Linux laptop:
    pytest modules/kuksa-python-sdk/tests/build/test_build.py -v
"""

import subprocess
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "eclipse-kuksa-python-sdk"
CLIENT_DIR = MODULE_DIR / "kuksa-client"


def _run(cmd, cwd=None, timeout=120):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or CLIENT_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def _parse_pytest(output):
    """Extract counts from pytest output."""
    m = re.search(r"(\d+) passed", output)
    passed = int(m.group(1)) if m else 0
    m = re.search(r"(\d+) failed", output)
    failed = int(m.group(1)) if m else 0
    m = re.search(r"(\d+) error", output)
    errors = int(m.group(1)) if m else 0
    return passed, failed, errors


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"kuksa-python-sdk not found at {MODULE_DIR}"
    assert CLIENT_DIR.exists(), "kuksa-client/ subdirectory missing"
    return MODULE_DIR


# -- Phase 1: Environment ---------------------------------------------------

class TestEnvironment:

    def test_python3_installed(self):
        rc, out, _ = _run("python3 --version")
        assert rc == 0, "Python3 not installed"

    def test_pip_installed(self):
        rc, _, _ = _run("python3 -m pip --version")
        assert rc == 0, "pip not installed"

    def test_pytest_installed(self):
        rc, _, _ = _run("python3 -m pytest --version")
        assert rc == 0, "pytest not installed"


# -- Phase 2: Install -------------------------------------------------------

class TestInstall:

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_pip_install_client(self, module_dir):
        """Install kuksa-client in editable mode."""
        rc, out, err = _run(
            "python3 -m pip install --user --break-system-packages -e '.[test]' --quiet 2>&1",
            timeout=120,
        )
        if rc != 0:
            # Try without [test] extras
            rc, out, err = _run(
                "python3 -m pip install --user --break-system-packages -e . --quiet 2>&1",
                timeout=120,
            )
        assert rc == 0, f"pip install failed:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_import_kuksa_client(self, module_dir):
        """Verify kuksa-client is importable."""
        rc, _, err = _run(
            "python3 -c 'import kuksa_client; print(kuksa_client.__name__)' 2>&1",
            cwd=MODULE_DIR,
        )
        assert rc == 0, f"Import failed:\n{err[-500:]}"


# -- Phase 3: Unit Tests ----------------------------------------------------

class TestUnitTests:

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_upstream_tests(self, module_dir):
        """Run upstream pytest suite in kuksa-client/tests/."""
        rc, out, err = _run(
            "python3 -m pytest tests/ -v --tb=short 2>&1",
            timeout=300,
        )
        combined = out + err
        passed, failed, errors = _parse_pytest(combined)
        print(f"Results: {passed} passed, {failed} failed, {errors} errors")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"
        assert passed > 0, "No tests found"

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_grpc_client(self, module_dir):
        """gRPC client tests."""
        rc, out, err = _run(
            "python3 -m pytest tests/test_grpc.py -v --tb=short 2>&1",
            timeout=120,
        )
        combined = out + err
        passed, _, _ = _parse_pytest(combined)
        print(f"gRPC tests: {passed} passed")
        assert rc == 0, f"gRPC tests failed:\n{combined[-1000:]}"


# -- Phase 4: Code Quality --------------------------------------------------

class TestCodeQuality:

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_pylint(self, module_dir):
        """Run pylint on kuksa_client package."""
        rc, out, err = _run(
            "python3 -m pylint kuksa_client --disable=all --enable=E 2>&1",
            timeout=60,
        )
        combined = out + err
        if rc != 0 and "No module named" in combined:
            pytest.skip("pylint not installed or module not found")
        # Report only — upstream style
        errors = [l for l in combined.split("\n") if ": E" in l]
        print(f"Pylint errors: {len(errors)}")
