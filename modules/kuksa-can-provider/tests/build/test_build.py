"""Build and test verification for kuksa-can-provider (DBC feeder).

Python-based CAN→Kuksa databroker bridge. Reads DBC files, decodes CAN
frames, feeds signals to the databroker via gRPC.

Upstream tests in test/ directory.

Run on Linux laptop:
    pytest modules/kuksa-can-provider/tests/build/test_build.py -v
"""

import subprocess
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "kuksa-kuksa-can-provider"


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
    assert MODULE_DIR.exists(), f"kuksa-can-provider not found at {MODULE_DIR}"
    assert (MODULE_DIR / "dbcfeeder.py").exists(), "dbcfeeder.py missing"
    return MODULE_DIR


# -- Phase 1: Environment ---------------------------------------------------

class TestEnvironment:

    def test_python3_installed(self):
        rc, _, _ = _run("python3 --version")
        assert rc == 0

    def test_can_utils_available(self):
        """vcan0 setup script exists."""
        assert (MODULE_DIR / "createvcan.sh").exists()

    def test_dbc_file_present(self):
        """At least one DBC file for testing."""
        dbcs = list(MODULE_DIR.glob("*.dbc"))
        assert len(dbcs) > 0, "No DBC files found"


# -- Phase 2: Install -------------------------------------------------------

class TestInstall:

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_pip_install_deps(self, module_dir):
        """Install runtime + dev dependencies."""
        reqs = module_dir / "requirements.txt"
        reqs_dev = module_dir / "requirements-dev.txt"
        cmd = "python3 -m pip install --quiet"
        if reqs.exists():
            cmd += f" -r requirements.txt"
        if reqs_dev.exists():
            cmd += f" -r requirements-dev.txt"
        rc, out, err = _run(f"{cmd} 2>&1", timeout=120)
        assert rc == 0, f"pip install failed:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_import_dbcfeederlib(self, module_dir):
        rc, _, err = _run(
            "python3 -c 'import dbcfeederlib; print(\"OK\")' 2>&1",
        )
        assert rc == 0, f"Import failed:\n{err[-500:]}"


# -- Phase 3: Unit Tests ----------------------------------------------------

class TestUnitTests:

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_upstream_tests(self, module_dir):
        """Run upstream test suite."""
        rc, out, err = _run(
            "python3 -m pytest test/ -v --tb=short 2>&1",
            timeout=300,
        )
        combined = out + err
        passed, failed = _parse_pytest(combined)
        print(f"Results: {passed} passed, {failed} failed")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"
        assert passed > 0, "No tests found"

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_dbc_parser(self, module_dir):
        """DBC parsing tests."""
        rc, out, err = _run(
            "python3 -m pytest test/test_dbc/ -v --tb=short 2>&1",
            timeout=60,
        )
        combined = out + err
        passed, _ = _parse_pytest(combined)
        print(f"DBC parser: {passed} passed")
        assert rc == 0, f"DBC tests failed:\n{combined[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_mapping(self, module_dir):
        """Signal mapping tests."""
        rc, out, err = _run(
            "python3 -m pytest test/test_example_mapping/ -v --tb=short 2>&1",
            timeout=60,
        )
        combined = out + err
        passed, _ = _parse_pytest(combined)
        print(f"Mapping: {passed} passed")
        assert rc == 0, f"Mapping tests failed:\n{combined[-1000:]}"
