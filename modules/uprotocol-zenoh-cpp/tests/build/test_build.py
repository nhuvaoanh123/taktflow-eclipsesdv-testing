"""Build and test verification for uProtocol Zenoh C++ transport.

CMake build, depends on up-cpp and zenoh-c.

Run on Linux laptop:
    pytest modules/uprotocol-zenoh-cpp/tests/build/test_build.py -v
"""

import subprocess
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "uprotocol-up-transport-zenoh-cpp"


def _run(cmd, cwd=None, timeout=300):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"zenoh-cpp not found at {MODULE_DIR}"
    assert (MODULE_DIR / "CMakeLists.txt").exists()
    return MODULE_DIR


class TestEnvironment:
    def test_cmake_installed(self):
        rc, _, _ = _run("cmake --version")
        assert rc == 0
    def test_gcc_installed(self):
        rc, _, _ = _run("g++ --version")
        assert rc == 0

class TestBuild:
    @pytest.mark.build
    @pytest.mark.uprotocol
    def test_cmake_configure(self, module_dir):
        build_dir = module_dir / "build"
        build_dir.mkdir(exist_ok=True)
        rc, out, err = _run(
            "cmake -B build -S . -DCMAKE_BUILD_TYPE=Release 2>&1", timeout=120)
        if rc != 0 and "Could NOT find" in err:
            missing = [l for l in err.split("\n") if "Could NOT find" in l]
            pytest.skip(f"Missing deps: {missing[0] if missing else 'unknown'}")
        assert rc == 0, f"Configure failed:\n{err[-2000:]}"

    @pytest.mark.build
    @pytest.mark.uprotocol
    def test_cmake_build(self, module_dir):
        rc, _, err = _run("cmake --build build -j$(nproc) 2>&1", timeout=300)
        if rc != 0 and "No such file or directory" in err:
            pytest.skip("Build dir missing — configure failed")
        assert rc == 0, f"Build failed:\n{err[-2000:]}"
