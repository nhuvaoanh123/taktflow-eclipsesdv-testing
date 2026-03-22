"""Regression tests for score-lifecycle API contract stability.

Verification methods: API contract verification (#7), file existence (#8).
Platform: any (no build required).

These tests verify that the score-lifecycle (score_lifecycle_health v0.0.0)
public API surface has not regressed between versions. If an expected header,
test target, mock, or schema is missing, the upstream module may have broken
backwards compatibility.
"""

from pathlib import Path

import pytest

LIFECYCLE_DIR = Path(__file__).parent.parent.parent.parent / "score-lifecycle"


# ---------------------------------------------------------------------------
# TestModuleIdentity
# ---------------------------------------------------------------------------
class TestModuleIdentity:
    """Verify MODULE.bazel exists with expected name and version."""

    def test_module_bazel_exists(self):
        module_path = LIFECYCLE_DIR / "MODULE.bazel"
        assert module_path.exists(), f"MODULE.bazel not found at {module_path}"

    def test_module_name_is_score_lifecycle_health(self):
        module_path = LIFECYCLE_DIR / "MODULE.bazel"
        content = module_path.read_text(encoding="utf-8")
        assert 'name = "score_lifecycle_health"' in content, (
            "Expected module name 'score_lifecycle_health' in MODULE.bazel"
        )

    def test_module_version_is_0_0_0(self):
        module_path = LIFECYCLE_DIR / "MODULE.bazel"
        content = module_path.read_text(encoding="utf-8")
        assert 'version = "0.0.0"' in content, (
            "Expected version 0.0.0 in MODULE.bazel; upstream may have bumped "
            "the version without updating the test baseline"
        )


# ---------------------------------------------------------------------------
# TestControlClientContract
# ---------------------------------------------------------------------------
class TestControlClientContract:
    """Verify control_client_lib public headers exist."""

    CONTROL_DIR = (
        LIFECYCLE_DIR
        / "src"
        / "control_client_lib"
        / "include"
        / "score"
        / "lcm"
    )

    @pytest.mark.parametrize(
        "header",
        [
            "control_client.h",
            "execution_error_event.h",
        ],
    )
    def test_control_client_header_exists(self, header: str):
        path = self.CONTROL_DIR / header
        assert path.exists(), (
            f"Control client header {header} missing -- API surface may have regressed"
        )

    def test_control_client_build_file_exists(self):
        path = LIFECYCLE_DIR / "src" / "control_client_lib" / "BUILD"
        assert path.exists(), "src/control_client_lib/BUILD missing"


# ---------------------------------------------------------------------------
# TestHealthMonitoringContract
# ---------------------------------------------------------------------------
class TestHealthMonitoringContract:
    """Verify health_monitoring_lib C++ public headers exist."""

    HM_CPP_DIR = (
        LIFECYCLE_DIR
        / "src"
        / "health_monitoring_lib"
        / "cpp"
        / "include"
        / "score"
        / "hm"
    )

    @pytest.mark.parametrize(
        "header",
        [
            "health_monitor.h",
            "heartbeat/heartbeat_monitor.h",
            "deadline/deadline_monitor.h",
            "logic/logic_monitor.h",
            "common.h",
            "tag.h",
        ],
    )
    def test_health_monitoring_header_exists(self, header: str):
        path = self.HM_CPP_DIR / header
        assert path.exists(), (
            f"Health monitoring header {header} missing -- "
            "C++ health monitoring API may have regressed"
        )

    def test_health_monitoring_build_file_exists(self):
        path = LIFECYCLE_DIR / "src" / "health_monitoring_lib" / "BUILD"
        assert path.exists(), "src/health_monitoring_lib/BUILD missing"


# ---------------------------------------------------------------------------
# TestLaunchManagerContract
# ---------------------------------------------------------------------------
class TestLaunchManagerContract:
    """Verify launch_manager_daemon public headers exist."""

    LMD_DIR = LIFECYCLE_DIR / "src" / "launch_manager_daemon"

    @pytest.mark.parametrize(
        "header",
        [
            "common/include/score/lcm/exec_error_domain.h",
            "common/include/score/lcm/identifier_hash.hpp",
        ],
    )
    def test_common_header_exists(self, header: str):
        path = self.LMD_DIR / header
        assert path.exists(), (
            f"Launch manager common header {header} missing -- "
            "API surface may have regressed"
        )

    def test_monitor_header_exists(self):
        path = (
            self.LMD_DIR
            / "health_monitor_lib"
            / "include"
            / "score"
            / "lcm"
            / "Monitor.h"
        )
        assert path.exists(), "Monitor.h missing from health_monitor_lib"

    def test_monitor_impl_wrapper_header_exists(self):
        path = (
            self.LMD_DIR
            / "health_monitor_lib"
            / "include"
            / "score"
            / "lcm"
            / "MonitorImplWrapper.h"
        )
        assert path.exists(), "MonitorImplWrapper.h missing from health_monitor_lib"

    def test_lifecycle_client_header_exists(self):
        path = (
            self.LMD_DIR
            / "lifecycle_client_lib"
            / "include"
            / "score"
            / "lcm"
            / "lifecycle_client.h"
        )
        assert path.exists(), "lifecycle_client.h missing from launch_manager_daemon"

    def test_irecovery_client_header_exists(self):
        path = (
            self.LMD_DIR
            / "recovery_client_lib"
            / "include"
            / "score"
            / "lcm"
            / "irecovery_client.h"
        )
        assert path.exists(), "irecovery_client.h missing from recovery_client_lib"

    @pytest.mark.parametrize(
        "build_subpath",
        [
            "BUILD",
            "common/BUILD",
            "health_monitor_lib/BUILD",
            "lifecycle_client_lib/BUILD",
            "process_state_client_lib/BUILD",
            "recovery_client_lib/BUILD",
        ],
    )
    def test_launch_manager_build_file_exists(self, build_subpath: str):
        path = self.LMD_DIR / build_subpath
        assert path.exists(), (
            f"BUILD file missing at launch_manager_daemon/{build_subpath}"
        )


# ---------------------------------------------------------------------------
# TestProcessStateContract
# ---------------------------------------------------------------------------
class TestProcessStateContract:
    """Verify process_state_client_lib public headers exist."""

    PS_DIR = (
        LIFECYCLE_DIR
        / "src"
        / "launch_manager_daemon"
        / "process_state_client_lib"
        / "include"
        / "score"
        / "lcm"
    )

    @pytest.mark.parametrize(
        "header",
        [
            "iprocessstatenotifier.hpp",
            "iprocessstatereceiver.hpp",
            "posixprocess.hpp",
            "processstatenotifier.hpp",
            "processstatereceiver.hpp",
        ],
    )
    def test_process_state_header_exists(self, header: str):
        path = self.PS_DIR / header
        assert path.exists(), (
            f"Process state header {header} missing -- API surface may have regressed"
        )


# ---------------------------------------------------------------------------
# TestLegacyLifecycleContract
# ---------------------------------------------------------------------------
class TestLegacyLifecycleContract:
    """Verify legacy lifecycle_client_lib public headers exist."""

    LEGACY_DIR = LIFECYCLE_DIR / "src" / "lifecycle_client_lib" / "include"

    @pytest.mark.parametrize(
        "header",
        [
            "lifecyclemanager.h",
            "application.h",
            "applicationcontext.h",
            "aasapplicationcontainer.h",
            "runapplication.h",
        ],
    )
    def test_legacy_lifecycle_header_exists(self, header: str):
        path = self.LEGACY_DIR / header
        assert path.exists(), (
            f"Legacy lifecycle header {header} missing -- "
            "backwards-compatible API may have been removed"
        )

    def test_legacy_lifecycle_build_file_exists(self):
        path = LIFECYCLE_DIR / "src" / "lifecycle_client_lib" / "BUILD"
        assert path.exists(), "src/lifecycle_client_lib/BUILD missing"


# ---------------------------------------------------------------------------
# TestMockAvailability
# ---------------------------------------------------------------------------
class TestMockAvailability:
    """Verify test mocks are available for downstream consumers."""

    MOCKS_DIR = (
        LIFECYCLE_DIR
        / "src"
        / "lifecycle_client_lib"
        / "test"
        / "ut"
        / "mocks"
    )

    def test_mocks_directory_exists(self):
        assert self.MOCKS_DIR.is_dir(), (
            "Mocks directory missing at src/lifecycle_client_lib/test/ut/mocks/"
        )

    @pytest.mark.parametrize(
        "mock_header",
        [
            "applicationcontextmock.h",
            "lifecyclemanagermock.h",
        ],
    )
    def test_mock_header_exists(self, mock_header: str):
        path = self.MOCKS_DIR / mock_header
        assert path.exists(), (
            f"Mock header {mock_header} missing -- test infrastructure may be broken"
        )

    @pytest.mark.parametrize(
        "mock_source",
        [
            "applicationcontextmock.cpp",
            "lifecyclemanagermock.cpp",
        ],
    )
    def test_mock_source_exists(self, mock_source: str):
        path = self.MOCKS_DIR / mock_source
        assert path.exists(), (
            f"Mock source {mock_source} missing -- mock implementations removed"
        )


# ---------------------------------------------------------------------------
# TestFlatBuffersSchemas
# ---------------------------------------------------------------------------
class TestFlatBuffersSchemas:
    """Verify FlatBuffers schema files and generated headers exist."""

    LMD_DIR = LIFECYCLE_DIR / "src" / "launch_manager_daemon"

    @pytest.mark.parametrize(
        "schema_path",
        [
            "config/lm_flatcfg.fbs",
            "health_monitor_lib/config/hm_flatcfg.fbs",
            "health_monitor_lib/config/hmcore_flatcfg.fbs",
        ],
    )
    def test_fbs_schema_exists(self, schema_path: str):
        path = self.LMD_DIR / schema_path
        assert path.exists(), (
            f"FlatBuffers schema {schema_path} missing -- "
            "configuration format may have changed"
        )

    @pytest.mark.parametrize(
        "generated_header",
        [
            "config/lm_flatcfg_generated.h",
            "health_monitor_lib/config/hm_flatcfg_generated.h",
            "health_monitor_lib/config/hmcore_flatcfg_generated.h",
        ],
    )
    def test_fbs_generated_header_exists(self, generated_header: str):
        path = self.LMD_DIR / generated_header
        assert path.exists(), (
            f"FlatBuffers generated header {generated_header} missing -- "
            "generated code may need to be regenerated"
        )


# ---------------------------------------------------------------------------
# TestRustComponents
# ---------------------------------------------------------------------------
class TestRustComponents:
    """Verify Rust component manifests exist."""

    def test_root_cargo_toml_exists(self):
        path = LIFECYCLE_DIR / "Cargo.toml"
        assert path.exists(), "Root Cargo.toml missing -- Rust workspace removed?"

    def test_health_monitoring_cargo_toml_exists(self):
        path = LIFECYCLE_DIR / "src" / "health_monitoring_lib" / "Cargo.toml"
        assert path.exists(), (
            "health_monitoring_lib/Cargo.toml missing -- Rust health monitoring removed"
        )

    @pytest.mark.parametrize(
        "rust_binding_path",
        [
            "src/launch_manager_daemon/health_monitor_lib/rust_bindings/Cargo.toml",
            "src/launch_manager_daemon/lifecycle_client_lib/rust_bindings/Cargo.toml",
        ],
    )
    def test_rust_bindings_cargo_toml_exists(self, rust_binding_path: str):
        path = LIFECYCLE_DIR / rust_binding_path
        assert path.exists(), (
            f"Rust bindings {rust_binding_path} missing -- "
            "Rust FFI bindings may have been removed"
        )

    @pytest.mark.parametrize(
        "rust_binding_build",
        [
            "src/launch_manager_daemon/health_monitor_lib/rust_bindings/BUILD",
            "src/launch_manager_daemon/lifecycle_client_lib/rust_bindings/BUILD",
        ],
    )
    def test_rust_bindings_build_file_exists(self, rust_binding_build: str):
        path = LIFECYCLE_DIR / rust_binding_build
        assert path.exists(), (
            f"Rust bindings BUILD file missing at {rust_binding_build}"
        )


# ---------------------------------------------------------------------------
# TestBuildTargets
# ---------------------------------------------------------------------------
class TestBuildTargets:
    """Verify key BUILD files exist for each component."""

    @pytest.mark.parametrize(
        "build_path",
        [
            "BUILD",
            "src/BUILD",
            "src/control_client_lib/BUILD",
            "src/health_monitoring_lib/BUILD",
            "src/lifecycle_client_lib/BUILD",
            "src/launch_manager_daemon/BUILD",
            "src/launch_manager_daemon/common/BUILD",
            "src/launch_manager_daemon/health_monitor_lib/BUILD",
            "src/launch_manager_daemon/lifecycle_client_lib/BUILD",
            "src/launch_manager_daemon/process_state_client_lib/BUILD",
            "src/launch_manager_daemon/recovery_client_lib/BUILD",
        ],
    )
    def test_build_file_exists(self, build_path: str):
        path = LIFECYCLE_DIR / build_path
        assert path.exists(), (
            f"BUILD file missing at {build_path} -- Bazel target may have been removed"
        )

    def test_top_level_build_file_exists(self):
        """The repository root must have a BUILD or BUILD.bazel file."""
        has_build = (LIFECYCLE_DIR / "BUILD").exists() or (
            LIFECYCLE_DIR / "BUILD.bazel"
        ).exists()
        assert has_build, "No top-level BUILD or BUILD.bazel in score-lifecycle"


# ---------------------------------------------------------------------------
# TestExamples
# ---------------------------------------------------------------------------
class TestExamples:
    """Verify example directories exist for downstream reference."""

    EXAMPLES_DIR = LIFECYCLE_DIR / "examples"

    def test_examples_directory_exists(self):
        assert self.EXAMPLES_DIR.is_dir(), "examples/ directory missing"

    @pytest.mark.parametrize(
        "example",
        [
            "control_application",
            "cpp_lifecycle_app",
            "cpp_supervised_app",
            "rust_supervised_app",
        ],
    )
    def test_example_directory_exists(self, example: str):
        path = self.EXAMPLES_DIR / example
        assert path.is_dir(), (
            f"Example directory {example}/ missing -- "
            "reference application may have been removed"
        )


# ---------------------------------------------------------------------------
# TestPlatformSupport
# ---------------------------------------------------------------------------
class TestPlatformSupport:
    """Verify OSAL platform directories exist under launch_manager_daemon common."""

    OSAL_DIR = (
        LIFECYCLE_DIR
        / "src"
        / "launch_manager_daemon"
        / "common"
        / "src"
        / "internal"
        / "osal"
    )

    @pytest.mark.parametrize(
        "platform",
        [
            "linux",
            "qnx",
            "posix",
        ],
    )
    def test_osal_platform_directory_exists(self, platform: str):
        path = self.OSAL_DIR / platform
        assert path.is_dir(), (
            f"OSAL platform directory {platform}/ missing -- "
            "platform support may have been dropped"
        )
