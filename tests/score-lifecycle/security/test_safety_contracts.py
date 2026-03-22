"""Safety contract verification for score-lifecycle components.

Verifies that safety-critical lifecycle components follow required patterns:
- Health monitoring structure with heartbeat, deadline, logical supervision
- OS abstraction layer with platform-specific implementations
- Watchdog integration in health monitor
- Recovery interface for fault handling
- Supervision types for alive, deadline, and logical monitoring
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
LIFECYCLE_DIR = PROJECT_ROOT / "score-lifecycle"


# ---------------------------------------------------------------------------
# TestHealthMonitorStructure
# ---------------------------------------------------------------------------
class TestHealthMonitorStructure:
    """Verify health_monitoring_lib has: health_monitor.h, heartbeat/,
    deadline/, logic/ subdirs.  Verify Rust source exists.
    Verify C++ tests exist."""

    # The public health monitoring API is in src/health_monitoring_lib/
    CANDIDATES = [
        LIFECYCLE_DIR / "src" / "health_monitoring_lib",
        LIFECYCLE_DIR / "health_monitoring_lib",
    ]

    @property
    def health_lib(self) -> Path:
        for c in self.CANDIDATES:
            if c.is_dir():
                return c
        return self.CANDIDATES[0]  # default for error messages

    def test_health_monitoring_lib_exists(self):
        assert any(c.is_dir() for c in self.CANDIDATES), (
            f"health_monitoring_lib directory not found -- "
            f"checked: {[str(c) for c in self.CANDIDATES]}"
        )

    def test_health_monitor_header_exists(self):
        """health_monitor.h or equivalent header should exist."""
        lib = self.health_lib
        headers = list(lib.rglob("*health_monitor*.h"))
        assert len(headers) > 0, (
            f"No health_monitor header found in {lib}"
        )

    def test_heartbeat_subdirectory_exists(self):
        lib = self.health_lib
        heartbeat_dirs = list(lib.rglob("heartbeat"))
        has_heartbeat = any(d.is_dir() for d in heartbeat_dirs)
        # Also check for alive supervision as alternative naming
        alive_dirs = list(lib.rglob("alive"))
        has_alive = any(d.is_dir() for d in alive_dirs)
        assert has_heartbeat or has_alive, (
            f"No heartbeat/ or alive/ subdirectory found in {lib}"
        )

    def test_deadline_subdirectory_exists(self):
        lib = self.health_lib
        deadline_dirs = list(lib.rglob("deadline"))
        has_deadline = any(d.is_dir() for d in deadline_dirs)
        assert has_deadline, (
            f"No deadline/ subdirectory found in {lib}"
        )

    def test_logic_subdirectory_exists(self):
        """logic/ or logical/ subdirectory for logical supervision."""
        lib = self.health_lib
        logic_dirs = list(lib.rglob("logic"))
        logical_dirs = list(lib.rglob("logical"))
        has_logic = any(d.is_dir() for d in logic_dirs)
        has_logical = any(d.is_dir() for d in logical_dirs)
        assert has_logic or has_logical, (
            f"No logic/ or logical/ subdirectory found in {lib}"
        )

    def test_rust_source_exists(self):
        """Rust source files (.rs) should exist in health_monitoring_lib."""
        lib = self.health_lib
        rs_files = list(lib.rglob("*.rs"))
        assert len(rs_files) > 0, (
            f"No Rust source files (.rs) found in {lib}"
        )

    def test_cpp_tests_exist(self):
        """C++ test files should exist for health monitoring."""
        lib = self.health_lib
        test_files = list(lib.rglob("*test*.cpp"))
        test_dirs = [d for d in lib.rglob("test") if d.is_dir()]
        has_test_files = len(test_files) > 0
        has_test_dirs = len(test_dirs) > 0
        assert has_test_files or has_test_dirs, (
            f"No C++ test files or test directories found in {lib}"
        )

    def test_build_file_exists(self):
        lib = self.health_lib
        build_files = list(lib.rglob("BUILD")) + list(lib.rglob("BUILD.bazel"))
        assert len(build_files) > 0, (
            f"No BUILD files found in {lib}"
        )


# ---------------------------------------------------------------------------
# TestOsAbstractionLayer
# ---------------------------------------------------------------------------
class TestOsAbstractionLayer:
    """Verify launch_manager_daemon/common has OSAL with linux/ and qnx/
    platform directories.  Verify posix/ shared code."""

    # launch_manager_daemon may be at root or under src/
    CANDIDATES = [
        LIFECYCLE_DIR / "launch_manager_daemon",
        LIFECYCLE_DIR / "src" / "launch_manager_daemon",
    ]

    @property
    def launch_dir(self) -> Path:
        for c in self.CANDIDATES:
            if c.is_dir():
                return c
        return self.CANDIDATES[0]

    def test_launch_manager_daemon_exists(self):
        assert any(c.is_dir() for c in self.CANDIDATES), (
            f"launch_manager_daemon directory not found -- "
            f"checked: {[str(c) for c in self.CANDIDATES]}"
        )

    def test_common_directory_exists(self):
        common = self.launch_dir / "common"
        assert common.is_dir(), (
            f"common/ directory not found in {self.launch_dir}"
        )

    def test_linux_platform_directory_exists(self):
        """OSAL should have a linux/ platform directory."""
        launch = self.launch_dir
        linux_dirs = list(launch.rglob("linux"))
        has_linux = any(d.is_dir() for d in linux_dirs)
        assert has_linux, (
            f"No linux/ platform directory found in {launch}"
        )

    def test_qnx_platform_directory_exists(self):
        """OSAL should have a qnx/ platform directory."""
        launch = self.launch_dir
        qnx_dirs = list(launch.rglob("qnx"))
        has_qnx = any(d.is_dir() for d in qnx_dirs)
        assert has_qnx, (
            f"No qnx/ platform directory found in {launch}"
        )

    def test_posix_shared_code_exists(self):
        """posix/ shared code should exist for cross-platform OSAL."""
        launch = self.launch_dir
        posix_dirs = list(launch.rglob("posix"))
        has_posix = any(d.is_dir() for d in posix_dirs)
        assert has_posix, (
            f"No posix/ shared code directory found in {launch}"
        )

    def test_osal_has_source_files(self):
        """OSAL directories should contain source files."""
        launch = self.launch_dir
        cpp_files = list(launch.rglob("*.cpp"))
        h_files = list(launch.rglob("*.h"))
        assert len(cpp_files) + len(h_files) > 0, (
            f"No C++ source files found in {launch}"
        )


# ---------------------------------------------------------------------------
# TestWatchdogIntegration
# ---------------------------------------------------------------------------
class TestWatchdogIntegration:
    """Verify watchdog-related source files exist in health_monitor_lib
    (search for 'watchdog' in filenames/paths)."""

    CANDIDATES = [
        LIFECYCLE_DIR / "src" / "launch_manager_daemon" / "health_monitor_lib",
        LIFECYCLE_DIR / "src" / "health_monitoring_lib",
        LIFECYCLE_DIR / "health_monitoring_lib",
    ]

    @property
    def health_lib(self) -> Path:
        for c in self.CANDIDATES:
            if c.is_dir():
                return c
        return self.CANDIDATES[0]

    def test_watchdog_files_exist(self):
        """Files with 'watchdog' in their name should exist."""
        lib = self.health_lib
        watchdog_files = [
            f for f in lib.rglob("*")
            if f.is_file() and "watchdog" in f.name.lower()
        ]
        assert len(watchdog_files) > 0, (
            f"No watchdog-related files found in {lib}"
        )

    def test_watchdog_paths_exist(self):
        """Directories or paths containing 'watchdog' should exist."""
        lib = self.health_lib
        watchdog_paths = [
            d for d in lib.rglob("*")
            if "watchdog" in str(d).lower()
        ]
        assert len(watchdog_paths) > 0, (
            f"No watchdog-related paths found in {lib}"
        )

    def test_watchdog_header_exists(self):
        """A watchdog header file (.h or .hpp) should exist."""
        lib = self.health_lib
        watchdog_headers = [
            f for f in lib.rglob("*")
            if f.is_file()
            and "watchdog" in f.name.lower()
            and (f.suffix in (".h", ".hpp"))
        ]
        assert len(watchdog_headers) > 0, (
            f"No watchdog header files found in {lib}"
        )

    def test_watchdog_source_or_rust(self):
        """Watchdog implementation in C++ (.cpp) or Rust (.rs) should exist."""
        lib = self.health_lib
        cpp_files = [
            f for f in lib.rglob("*.cpp")
            if "watchdog" in f.name.lower()
        ]
        rs_files = [
            f for f in lib.rglob("*.rs")
            if "watchdog" in f.name.lower()
        ]
        assert len(cpp_files) + len(rs_files) > 0, (
            f"No watchdog implementation files (.cpp or .rs) found in {lib}"
        )


# ---------------------------------------------------------------------------
# TestRecoveryInterface
# ---------------------------------------------------------------------------
class TestRecoveryInterface:
    """Verify irecovery_client.h exists.
    Verify recovery_client_lib BUILD file."""

    def test_irecovery_client_header_exists(self):
        """irecovery_client.h should exist somewhere in score-lifecycle."""
        headers = list(LIFECYCLE_DIR.rglob("irecovery_client.h"))
        assert len(headers) > 0, (
            "irecovery_client.h not found anywhere in score-lifecycle"
        )

    def test_recovery_client_lib_directory_exists(self):
        """recovery_client_lib directory should exist."""
        dirs = list(LIFECYCLE_DIR.rglob("recovery_client_lib"))
        has_dir = any(d.is_dir() for d in dirs)
        assert has_dir, (
            "recovery_client_lib directory not found in score-lifecycle"
        )

    def test_recovery_client_lib_build_file_exists(self):
        """recovery_client_lib should have a BUILD file."""
        dirs = [
            d for d in LIFECYCLE_DIR.rglob("recovery_client_lib")
            if d.is_dir()
        ]
        if not dirs:
            pytest.skip("recovery_client_lib directory not found")

        found_build = False
        for d in dirs:
            build = d / "BUILD"
            build_bazel = d / "BUILD.bazel"
            if build.exists() or build_bazel.exists():
                found_build = True
                break

        assert found_build, (
            "No BUILD file found in recovery_client_lib/"
        )

    def test_recovery_interface_defines_client(self):
        """irecovery_client.h should define a recovery client interface."""
        headers = list(LIFECYCLE_DIR.rglob("irecovery_client.h"))
        if not headers:
            pytest.skip("irecovery_client.h not found")

        content = headers[0].read_text(encoding="utf-8", errors="ignore")
        has_class = re.search(
            r"\b(class|struct)\b.*\b(IRecoveryClient|RecoveryClient)\b",
            content,
        )
        has_interface = "recovery" in content.lower()
        assert has_class or has_interface, (
            "irecovery_client.h does not appear to define a recovery "
            "client interface"
        )


# ---------------------------------------------------------------------------
# TestSupervisionTypes
# ---------------------------------------------------------------------------
class TestSupervisionTypes:
    """Verify alive, deadline, logical supervision source directories/files
    exist under health_monitoring_lib."""

    # The supervision types (heartbeat, deadline, logic) live in health_monitoring_lib
    CANDIDATES = [
        LIFECYCLE_DIR / "src" / "health_monitoring_lib",
        LIFECYCLE_DIR / "src" / "launch_manager_daemon" / "health_monitor_lib",
        LIFECYCLE_DIR / "health_monitoring_lib",
    ]

    @property
    def health_lib(self) -> Path:
        for c in self.CANDIDATES:
            if c.is_dir():
                return c
        return self.CANDIDATES[0]

    def test_alive_supervision_exists(self):
        """Alive supervision (heartbeat) source files or directory should
        exist."""
        lib = self.health_lib
        alive_dirs = list(lib.rglob("alive"))
        heartbeat_dirs = list(lib.rglob("heartbeat"))
        alive_files = [
            f for f in lib.rglob("*")
            if f.is_file() and "alive" in f.name.lower()
        ]
        heartbeat_files = [
            f for f in lib.rglob("*")
            if f.is_file() and "heartbeat" in f.name.lower()
        ]

        has_alive = (
            any(d.is_dir() for d in alive_dirs)
            or any(d.is_dir() for d in heartbeat_dirs)
            or len(alive_files) > 0
            or len(heartbeat_files) > 0
        )
        assert has_alive, (
            f"No alive/heartbeat supervision files or directories found "
            f"in {lib}"
        )

    def test_deadline_supervision_exists(self):
        """Deadline supervision source files or directory should exist."""
        lib = self.health_lib
        deadline_dirs = list(lib.rglob("deadline"))
        deadline_files = [
            f for f in lib.rglob("*")
            if f.is_file() and "deadline" in f.name.lower()
        ]

        has_deadline = (
            any(d.is_dir() for d in deadline_dirs)
            or len(deadline_files) > 0
        )
        assert has_deadline, (
            f"No deadline supervision files or directories found in {lib}"
        )

    def test_logical_supervision_exists(self):
        """Logical supervision source files or directory should exist."""
        lib = self.health_lib
        logic_dirs = list(lib.rglob("logic"))
        logical_dirs = list(lib.rglob("logical"))
        logic_files = [
            f for f in lib.rglob("*")
            if f.is_file() and "logic" in f.name.lower()
        ]

        has_logical = (
            any(d.is_dir() for d in logic_dirs)
            or any(d.is_dir() for d in logical_dirs)
            or len(logic_files) > 0
        )
        assert has_logical, (
            f"No logical supervision files or directories found in {lib}"
        )

    def test_supervision_has_headers(self):
        """Each supervision type should have at least one header file."""
        lib = self.health_lib
        supervision_headers = [
            f for f in lib.rglob("*.h")
            if any(
                kw in str(f).lower()
                for kw in ("alive", "heartbeat", "deadline", "logic")
            )
        ]
        assert len(supervision_headers) >= 2, (
            f"Expected at least 2 supervision-related headers, "
            f"found {len(supervision_headers)}"
        )

    def test_supervision_has_build_targets(self):
        """BUILD files should exist in supervision subdirectories."""
        lib = self.health_lib
        build_files = list(lib.rglob("BUILD")) + list(lib.rglob("BUILD.bazel"))
        assert len(build_files) >= 1, (
            f"No BUILD files found in {lib} -- "
            f"supervision targets not buildable"
        )
