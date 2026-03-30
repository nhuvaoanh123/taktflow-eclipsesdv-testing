"""Build and test verification for kuksa.val.services.

Vehicle services: HVAC service, seat service, mock service.
Python + C++ (seat controller). Integration tests require databroker running.

Run on Linux laptop:
    pytest modules/kuksa-val-services/tests/build/test_build.py -v
"""

import subprocess
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "kuksa-kuksa.val.services"


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
    assert MODULE_DIR.exists(), f"kuksa.val.services not found at {MODULE_DIR}"
    return MODULE_DIR


# -- Phase 1: Environment ---------------------------------------------------

class TestEnvironment:

    def test_python3_installed(self):
        rc, _, _ = _run("python3 --version")
        assert rc == 0

    def test_proto_files_present(self):
        """Proto definitions for gRPC services."""
        protos = list((MODULE_DIR / "proto").glob("**/*.proto"))
        if not protos:
            pytest.skip("No proto/ directory")
        assert len(protos) > 0

    def test_mock_service_exists(self):
        assert (MODULE_DIR / "mock_service").is_dir()

    def test_hvac_service_exists(self):
        assert (MODULE_DIR / "hvac_service").is_dir()


# -- Phase 2: Install -------------------------------------------------------

class TestInstall:

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_install_mock_service(self, module_dir):
        """Install mock service dependencies."""
        reqs = module_dir / "mock_service" / "requirements.txt"
        if not reqs.exists():
            pytest.skip("No requirements.txt for mock_service")
        rc, out, err = _run(
            f"python3 -m pip install --quiet -r {reqs} 2>&1",
            timeout=120,
        )
        assert rc == 0, f"Install failed:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.kuksa
    def test_install_hvac_service(self, module_dir):
        """Install HVAC service dependencies."""
        reqs = module_dir / "hvac_service" / "requirements.txt"
        if not reqs.exists():
            pytest.skip("No requirements.txt for hvac_service")
        rc, out, err = _run(
            f"python3 -m pip install --quiet -r {reqs} 2>&1",
            timeout=120,
        )
        assert rc == 0, f"Install failed:\n{(out+err)[-2000:]}"


# -- Phase 3: Unit Tests ----------------------------------------------------

class TestUnitTests:

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_mock_service_tests(self, module_dir):
        """Mock service unit tests."""
        test_dir = module_dir / "mock_service" / "test"
        if not test_dir.exists():
            pytest.skip("No mock_service/test/ directory")
        rc, out, err = _run(
            f"python3 -m pytest {test_dir} -v --tb=short 2>&1",
            timeout=120, cwd=module_dir / "mock_service",
        )
        combined = out + err
        passed, failed = _parse_pytest(combined)
        print(f"Mock service: {passed} passed, {failed} failed")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"

    @pytest.mark.unit
    @pytest.mark.kuksa
    def test_seat_controller_build(self, module_dir):
        """Build seat controller C++ component."""
        seat_src = module_dir / "seat_service" / "src"
        cmake = seat_src / "CMakeLists.txt" if seat_src.exists() else None
        if not cmake or not cmake.exists():
            pytest.skip("No CMakeLists.txt for seat_service")
        build_dir = seat_src / "build"
        build_dir.mkdir(exist_ok=True)
        rc, _, err = _run(
            f"cmake -B build -S . && cmake --build build 2>&1",
            cwd=seat_src, timeout=300,
        )
        if rc != 0 and "Could NOT find" in err:
            pytest.skip(f"Missing C++ dependency:\n{err[-500:]}")
        assert rc == 0, f"Build failed:\n{err[-1000:]}"


# -- Phase 4: Integration (requires running databroker) ----------------------

class TestIntegration:

    @pytest.mark.integration
    @pytest.mark.kuksa
    def test_integration_tests_exist(self, module_dir):
        """Verify integration test files are present."""
        int_dir = module_dir / "integration_test"
        assert int_dir.exists(), "integration_test/ directory missing"
        tests = list(int_dir.glob("test_*.py"))
        print(f"Integration tests available: {len(tests)} files")
        assert len(tests) > 0, "No test_*.py in integration_test/"
        # Note: actual integration tests require a running databroker instance
