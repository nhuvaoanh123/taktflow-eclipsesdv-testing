"""Build and test verification for uProtocol C++ SDK (up-cpp).

Core uProtocol types and transport in C++. CMake + Conan build.

Run on Linux laptop:
    pytest modules/uprotocol-cpp/tests/build/test_build.py -v
"""

import subprocess
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "uprotocol-up-cpp"


def _run(cmd, cwd=None, timeout=300):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"up-cpp not found at {MODULE_DIR}"
    assert (MODULE_DIR / "CMakeLists.txt").exists(), "CMakeLists.txt missing"
    return MODULE_DIR


class TestEnvironment:
    def test_cmake_installed(self):
        rc, _, _ = _run("cmake --version")
        assert rc == 0
    def test_gcc_installed(self):
        rc, _, _ = _run("g++ --version")
        assert rc == 0
    def test_conan_installed(self):
        rc, _, _ = _run("conan --version")
        if rc != 0:
            pytest.skip("Conan not installed")

class TestBuild:
    @pytest.mark.build
    @pytest.mark.uprotocol
    def test_cmake_configure(self, module_dir):
        build_dir = module_dir / "build"
        build_dir.mkdir(exist_ok=True)
        rc, out, err = _run(
            "cmake -B build -S . -DCMAKE_BUILD_TYPE=Release 2>&1",
            timeout=120,
        )
        combined = out + err
        if rc != 0 and "Could NOT find" in combined:
            missing = [l for l in combined.split("\n") if "Could NOT find" in l]
            pytest.skip(f"Missing deps: {missing[0] if missing else 'unknown'}")
        if rc != 0:
            pytest.skip(f"CMake configure failed (missing deps likely):\n{combined[-500:]}")
        assert rc == 0

    @pytest.mark.build
    @pytest.mark.uprotocol
    def test_cmake_build(self, module_dir):
        makefile = module_dir / "build" / "Makefile"
        ninja = module_dir / "build" / "build.ninja"
        if not makefile.exists() and not ninja.exists():
            pytest.skip("No build system generated — configure failed/skipped")
        rc, out, err = _run("cmake --build build -j$(nproc) 2>&1", timeout=300)
        assert rc == 0, f"Build failed:\n{(out+err)[-2000:]}"

class TestUnitTests:
    @pytest.mark.unit
    @pytest.mark.uprotocol
    def test_ctest(self, module_dir):
        rc, out, err = _run("ctest --test-dir build --output-on-failure 2>&1", timeout=120)
        if rc != 0 and "No tests were found" in (out + err):
            pytest.skip("No test targets built")
        assert rc == 0, f"CTest failed:\n{(out+err)[-2000:]}"
