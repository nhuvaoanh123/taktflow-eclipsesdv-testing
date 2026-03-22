"""Regression tests for score-baselibs API contract stability.

Verification methods: API contract verification (#7), file existence (#8).
Platform: any (no build required).

These tests verify that the score-baselibs public API surface has not
regressed between versions. If an expected header, test target, or mock
is missing, the upstream module may have broken backwards compatibility.
"""

from pathlib import Path

import pytest

BASELIBS_DIR = Path(__file__).parent.parent.parent.parent / "score-baselibs"


# ---------------------------------------------------------------------------
# TestModuleIdentity
# ---------------------------------------------------------------------------
class TestModuleIdentity:
    """Verify MODULE.bazel exists with expected name and version."""

    def test_module_bazel_exists(self):
        module_path = BASELIBS_DIR / "MODULE.bazel"
        assert module_path.exists(), f"MODULE.bazel not found at {module_path}"

    def test_module_version_is_0_2_4(self):
        module_path = BASELIBS_DIR / "MODULE.bazel"
        content = module_path.read_text(encoding="utf-8")
        assert 'version = "0.2.4"' in content, (
            "Expected version 0.2.4 in MODULE.bazel; upstream may have bumped "
            "the version without updating the test baseline"
        )

    def test_module_name_is_score_baselibs(self):
        module_path = BASELIBS_DIR / "MODULE.bazel"
        content = module_path.read_text(encoding="utf-8")
        assert 'name = "score_baselibs"' in content, (
            "Expected module name 'score_baselibs' in MODULE.bazel"
        )


# ---------------------------------------------------------------------------
# TestOsAbstractionContract
# ---------------------------------------------------------------------------
class TestOsAbstractionContract:
    """Verify score/os/ headers, mocklib, and test directories exist."""

    OS_DIR = BASELIBS_DIR / "score" / "os"

    @pytest.mark.parametrize(
        "header",
        [
            "acl.h",
            "errno.h",
            "fcntl.h",
            "mman.h",
            "pthread.h",
            "socket.h",
            "stat.h",
            "semaphore.h",
            "spawn.h",
            "unistd.h",
            "time.h",
            "sched.h",
            "select.h",
            "dirent.h",
            "grp.h",
            "ioctl.h",
            "stdlib.h",
            "string.h",
        ],
    )
    def test_os_header_exists(self, header: str):
        path = self.OS_DIR / header
        assert path.exists(), (
            f"OS abstraction header {header} missing -- API surface may have regressed"
        )

    def test_object_seam_header_exists(self):
        path = self.OS_DIR / "ObjectSeam.h"
        assert path.exists(), "ObjectSeam.h missing -- Object Seam pattern removed?"

    def test_mocklib_directory_exists(self):
        path = self.OS_DIR / "mocklib"
        assert path.is_dir(), "score/os/mocklib/ directory missing"

    def test_test_directory_exists(self):
        path = self.OS_DIR / "test"
        assert path.is_dir(), "score/os/test/ directory missing"

    def test_utils_fake_directory_exists(self):
        path = self.OS_DIR / "utils" / "fake"
        assert path.is_dir(), "score/os/utils/fake/ directory missing"

    @pytest.mark.parametrize(
        "mock_header",
        [
            "acl_mock.h",
            "errno_mock.h",
            "fcntl_mock.h",
            "socketmock.h",
            "capability_mock.h",
        ],
    )
    def test_mocklib_header_exists(self, mock_header: str):
        path = self.OS_DIR / "mocklib" / mock_header
        assert path.exists(), (
            f"Mock header {mock_header} missing from mocklib -- "
            "Object Seam mocks may have been removed"
        )

    def test_os_build_file_exists(self):
        path = self.OS_DIR / "BUILD"
        assert path.exists(), "score/os/BUILD missing"

    def test_mocklib_build_file_exists(self):
        path = self.OS_DIR / "mocklib" / "BUILD"
        assert path.exists(), "score/os/mocklib/BUILD missing"


# ---------------------------------------------------------------------------
# TestSharedMemoryContract
# ---------------------------------------------------------------------------
class TestSharedMemoryContract:
    """Verify score/memory/shared/ headers and mock implementations exist."""

    SHM_DIR = BASELIBS_DIR / "score" / "memory" / "shared"

    def test_shared_memory_directory_exists(self):
        assert self.SHM_DIR.is_dir(), "score/memory/shared/ directory missing"

    @pytest.mark.parametrize(
        "header",
        [
            "shared_memory_factory.h",
            "shared_memory_resource.h",
            "i_shared_memory_factory.h",
            "i_shared_memory_resource.h",
            "shared_memory_error.h",
            "offset_ptr.h",
            "managed_memory_resource.h",
            "memory_resource_proxy.h",
        ],
    )
    def test_shared_memory_header_exists(self, header: str):
        path = self.SHM_DIR / header
        assert path.exists(), (
            f"Shared memory header {header} missing -- API may have regressed"
        )

    @pytest.mark.parametrize(
        "mock_file",
        [
            "shared_memory_factory_mock.h",
            "shared_memory_resource_mock.h",
            "atomic_mock.h",
        ],
    )
    def test_shared_memory_mock_exists(self, mock_file: str):
        path = self.SHM_DIR / mock_file
        assert path.exists(), (
            f"Shared memory mock {mock_file} missing -- test infrastructure broken"
        )

    def test_fake_directory_exists(self):
        path = self.SHM_DIR / "fake"
        assert path.is_dir(), "score/memory/shared/fake/ directory missing"

    def test_build_file_exists(self):
        path = self.SHM_DIR / "BUILD"
        assert path.exists(), "score/memory/shared/BUILD missing"


# ---------------------------------------------------------------------------
# TestConcurrencyContract
# ---------------------------------------------------------------------------
class TestConcurrencyContract:
    """Verify score/concurrency/ directory has expected components."""

    CONC_DIR = BASELIBS_DIR / "score" / "concurrency"

    def test_concurrency_directory_exists(self):
        assert self.CONC_DIR.is_dir(), "score/concurrency/ directory missing"

    @pytest.mark.parametrize(
        "subdir",
        [
            "future",
            "timed_executor",
            "thread_load_tracking",
        ],
    )
    def test_concurrency_subdir_exists(self, subdir: str):
        path = self.CONC_DIR / subdir
        assert path.is_dir(), (
            f"Concurrency subdir {subdir}/ missing -- component may have been removed"
        )

    @pytest.mark.parametrize(
        "header",
        [
            "locked_ptr.h",
            "synchronized_queue.h",
            "notification.h",
            "executor.h",
            "thread_pool.h",
            "synchronized.h",
        ],
    )
    def test_concurrency_header_exists(self, header: str):
        path = self.CONC_DIR / header
        assert path.exists(), (
            f"Concurrency header {header} missing -- API may have regressed"
        )

    def test_executor_mock_exists(self):
        path = self.CONC_DIR / "executor_mock.h"
        assert path.exists(), "executor_mock.h missing -- test seam removed"

    def test_build_file_exists(self):
        path = self.CONC_DIR / "BUILD"
        assert path.exists(), "score/concurrency/BUILD missing"


# ---------------------------------------------------------------------------
# TestResultContract
# ---------------------------------------------------------------------------
class TestResultContract:
    """Verify score/result/ exists with expected headers."""

    RESULT_DIR = BASELIBS_DIR / "score" / "result"

    def test_result_directory_exists(self):
        assert self.RESULT_DIR.is_dir(), "score/result/ directory missing"

    @pytest.mark.parametrize(
        "header",
        [
            "result.h",
            "error.h",
            "error_code.h",
            "error_domain.h",
        ],
    )
    def test_result_header_exists(self, header: str):
        path = self.RESULT_DIR / header
        assert path.exists(), (
            f"Result header {header} missing -- core error handling API regressed"
        )

    def test_build_file_exists(self):
        path = self.RESULT_DIR / "BUILD"
        assert path.exists(), "score/result/BUILD missing"


# ---------------------------------------------------------------------------
# TestSafeCppContract
# ---------------------------------------------------------------------------
class TestSafeCppContract:
    """Verify score/language/safecpp/ exists with safe math, abort handler."""

    SAFECPP_DIR = BASELIBS_DIR / "score" / "language" / "safecpp"

    def test_safecpp_directory_exists(self):
        assert self.SAFECPP_DIR.is_dir(), "score/language/safecpp/ directory missing"

    @pytest.mark.parametrize(
        "subdir",
        [
            "safe_math",
            "aborts_upon_exception",
            "safe_atomics",
            "scoped_function",
            "string_view",
        ],
    )
    def test_safecpp_subdir_exists(self, subdir: str):
        path = self.SAFECPP_DIR / subdir
        assert path.is_dir(), (
            f"SafeCpp subdir {subdir}/ missing -- safety component removed"
        )

    def test_safe_math_header_exists(self):
        path = self.SAFECPP_DIR / "safe_math" / "safe_math.h"
        assert path.exists(), "safe_math.h missing -- ASIL-B safe math API removed"

    def test_aborts_upon_exception_source_exists(self):
        path = self.SAFECPP_DIR / "aborts_upon_exception" / "aborts_upon_exception.cpp"
        assert path.exists(), "aborts_upon_exception.cpp missing"

    def test_build_file_exists(self):
        path = self.SAFECPP_DIR / "BUILD"
        assert path.exists(), "score/language/safecpp/BUILD missing"


# ---------------------------------------------------------------------------
# TestLoggingContract
# ---------------------------------------------------------------------------
class TestLoggingContract:
    """Verify score/mw/log/ exists with frontend headers."""

    LOG_DIR = BASELIBS_DIR / "score" / "mw" / "log"

    def test_log_directory_exists(self):
        assert self.LOG_DIR.is_dir(), "score/mw/log/ directory missing"

    @pytest.mark.parametrize(
        "header",
        [
            "logging.h",
            "logger.h",
            "log_stream.h",
            "log_stream_factory.h",
            "log_level.h",
            "log_common.h",
            "recorder.h",
            "runtime.h",
            "slot_handle.h",
        ],
    )
    def test_log_header_exists(self, header: str):
        path = self.LOG_DIR / header
        assert path.exists(), (
            f"Logging header {header} missing -- logging frontend API regressed"
        )

    def test_recorder_mock_exists(self):
        path = self.LOG_DIR / "recorder_mock.h"
        assert path.exists(), "recorder_mock.h missing -- logging test seam removed"

    def test_build_file_exists(self):
        path = self.LOG_DIR / "BUILD"
        assert path.exists(), "score/mw/log/BUILD missing"

    def test_log_test_directory_exists(self):
        path = self.LOG_DIR / "test"
        assert path.is_dir(), "score/mw/log/test/ directory missing"


# ---------------------------------------------------------------------------
# TestBuildTargets
# ---------------------------------------------------------------------------
class TestBuildTargets:
    """Verify key BUILD files exist for each component."""

    @pytest.mark.parametrize(
        "build_path",
        [
            "score/os/BUILD",
            "score/os/mocklib/BUILD",
            "score/memory/shared/BUILD",
            "score/concurrency/BUILD",
            "score/concurrency/future/BUILD",
            "score/concurrency/timed_executor/BUILD",
            "score/result/BUILD",
            "score/language/safecpp/BUILD",
            "score/language/safecpp/safe_math/BUILD",
            "score/language/safecpp/aborts_upon_exception/BUILD",
            "score/mw/log/BUILD",
            "score/json/BUILD",
            "score/filesystem/BUILD",
            "score/containers/BUILD",
            "score/bitmanipulation/BUILD",
        ],
    )
    def test_build_file_exists(self, build_path: str):
        path = BASELIBS_DIR / build_path
        assert path.exists(), (
            f"BUILD file missing at {build_path} -- Bazel target may have been removed"
        )

    def test_top_level_build_file_exists(self):
        """The repository root must have a BUILD or BUILD.bazel file."""
        has_build = (BASELIBS_DIR / "BUILD").exists() or (
            BASELIBS_DIR / "BUILD.bazel"
        ).exists()
        assert has_build, "No top-level BUILD or BUILD.bazel in score-baselibs"
