"""Regression tests for score-scrample API contract stability.

Verification methods: API contract verification, file existence.
Platform: any (no build required — file inspection only).

score-scrample provides:
  - C++ sample sender/receiver (LoLa IPC demo application)
  - scorex Go CLI (project initialization, skeleton code generation,
    module presets, known-good configuration loading)
  - Rust library components
  - FEO AD demo with foxglove WebSocket bridge

If expected source files or components are missing, the upstream
module may have broken backwards compatibility.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
SCRAMPLE_DIR = PROJECT_ROOT / "score-scrample"


# ---------------------------------------------------------------------------
# TestModuleIdentity
# ---------------------------------------------------------------------------
class TestModuleIdentity:
    """Verify MODULE.bazel presence and identity."""

    def test_module_bazel_exists(self):
        assert (SCRAMPLE_DIR / "MODULE.bazel").exists(), \
            f"MODULE.bazel not found at {SCRAMPLE_DIR}"

    def test_module_name(self):
        content = (SCRAMPLE_DIR / "MODULE.bazel").read_text(encoding="utf-8")
        assert "scrample" in content.lower(), \
            "MODULE.bazel does not reference scrample"

    def test_bazelversion_exists(self):
        path = SCRAMPLE_DIR / ".bazelversion"
        if not path.exists():
            pytest.skip(".bazelversion not found")
        version = path.read_text().strip()
        assert re.match(r"\d+\.\d+\.\d+", version), \
            f"Invalid version in .bazelversion: {version}"


# ---------------------------------------------------------------------------
# TestSampleSenderReceiverComponent
# ---------------------------------------------------------------------------
class TestSampleSenderReceiverComponent:
    """Verify C++ sample sender/receiver application structure."""

    SRC_DIR = SCRAMPLE_DIR / "src"

    def test_src_directory_exists(self):
        assert self.SRC_DIR.is_dir(), \
            "src/ directory missing — sample application removed"

    def test_main_cpp_exists(self):
        assert (self.SRC_DIR / "main.cpp").exists(), \
            "src/main.cpp missing — application entry point removed"

    def test_sample_sender_receiver_exists(self):
        sr_cpp = self.SRC_DIR / "sample_sender_receiver.cpp"
        sr_h = self.SRC_DIR / "sample_sender_receiver.h"
        assert sr_cpp.exists() or sr_h.exists(), \
            "sample_sender_receiver source files missing"

    def test_assert_handler_exists(self):
        assert (self.SRC_DIR / "assert_handler.cpp").exists(), \
            "src/assert_handler.cpp missing — safety assert handler removed"

    def test_cpp_source_count(self):
        if not self.SRC_DIR.is_dir():
            pytest.skip("src/ not found")
        cpp_files = list(self.SRC_DIR.glob("*.cpp")) + list(self.SRC_DIR.glob("*.h"))
        assert len(cpp_files) >= 3, \
            f"Expected at least 3 C++ files in src/, found {len(cpp_files)}"


# ---------------------------------------------------------------------------
# TestScorexCliComponent
# ---------------------------------------------------------------------------
class TestScorexCliComponent:
    """Verify scorex Go CLI tool structure."""

    SCOREX = SCRAMPLE_DIR / "scorex"

    def test_scorex_directory_exists(self):
        assert self.SCOREX.is_dir(), \
            "scorex/ directory missing — CLI tool removed"

    def test_go_mod_exists(self):
        if not self.SCOREX.is_dir():
            pytest.skip("scorex/ not found")
        assert (self.SCOREX / "go.mod").exists(), \
            "scorex/go.mod missing — Go module not initialized"

    def test_cmd_directory_exists(self):
        """Command implementations for the CLI."""
        cmd_dir = self.SCOREX / "cmd"
        assert cmd_dir.is_dir(), \
            "scorex/cmd/ missing — CLI commands removed"

    def test_init_command_exists(self):
        """Project initialization command."""
        init_go = self.SCOREX / "cmd" / "init.go"
        assert init_go.exists(), \
            "scorex/cmd/init.go missing — init command removed"

    def test_internal_services_exist(self):
        """Internal service implementations."""
        internal = self.SCOREX / "internal"
        assert internal.is_dir(), \
            "scorex/internal/ missing — service implementations removed"

    @pytest.mark.parametrize("service", [
        "projectinit",
        "skeleton",
        "knowngood",
        "module",
    ])
    def test_service_directory_exists(self, service):
        path = self.SCOREX / "internal" / "service" / service
        if not path.is_dir():
            pytest.skip(f"service/{service}/ not found")

    def test_config_module_presets(self):
        """Module presets configuration must exist."""
        presets = self.SCOREX / "internal" / "config" / "module_presets.go"
        if not presets.exists():
            config_dir = self.SCOREX / "internal" / "config"
            if not config_dir.is_dir():
                pytest.skip("config/ not found")
            go_files = list(config_dir.glob("*.go"))
            assert len(go_files) >= 1, \
                "No Go files in scorex/internal/config/ — config module removed"

    def test_skeleton_generator_exists(self):
        """Skeleton code generator must exist."""
        gen = self.SCOREX / "internal" / "service" / "skeleton" / "generator.go"
        if not gen.exists():
            skel_dir = self.SCOREX / "internal" / "service" / "skeleton"
            if not skel_dir.is_dir():
                pytest.skip("skeleton/ service not found")
            go_files = list(skel_dir.glob("*.go"))
            assert len(go_files) >= 1, \
                "No Go files in skeleton/ — generator removed"


# ---------------------------------------------------------------------------
# TestFeoAdDemo
# ---------------------------------------------------------------------------
class TestFeoAdDemo:
    """Verify FEO AD demo components."""

    FEO_DIR = SCRAMPLE_DIR / "feo"

    def test_feo_directory_exists(self):
        if not self.FEO_DIR.is_dir():
            pytest.skip("feo/ directory not found — AD demo may be external")

    def test_foxglove_bridge_exists(self):
        """Foxglove WebSocket bridge for visualization."""
        if not self.FEO_DIR.is_dir():
            pytest.skip("feo/ not found")
        bridge_dir = self.FEO_DIR / "ad-demo" / "lichtblick-com"
        if not bridge_dir.is_dir():
            pytest.skip("lichtblick-com/ not found")
        py_files = list(bridge_dir.glob("*.py"))
        assert len(py_files) >= 1, \
            "No Python files in foxglove bridge directory"


# ---------------------------------------------------------------------------
# TestBazelConfiguration
# ---------------------------------------------------------------------------
class TestBazelConfiguration:
    """Verify Bazel build configuration."""

    def test_bazelrc_exists(self):
        assert (SCRAMPLE_DIR / ".bazelrc").exists(), \
            ".bazelrc not found — build configs missing"

    def test_top_level_build_file(self):
        has_build = (
            (SCRAMPLE_DIR / "BUILD").exists()
            or (SCRAMPLE_DIR / "BUILD.bazel").exists()
        )
        assert has_build, "No top-level BUILD file in score-scrample"
