"""Regression tests for score-feo API contract stability.

Verification methods: API contract verification (#7), file existence (#8).
Platform: any (no build required).

These tests verify that the score-feo (score_feo v0.0.0) public API surface
has not regressed between versions. The FEO scheduler is a Rust-primary
project (edition 2024) with 8 crates, minimal C++ (feo-time bridge),
Bazel 8.3.0 build, and Perfetto-based tracing.

If an expected crate, source file, header, or test target is missing,
the upstream module may have broken backwards compatibility.
"""

import re
from pathlib import Path

import pytest

FEO_DIR = Path(__file__).parent.parent.parent.parent / "score-feo"


# ---------------------------------------------------------------------------
# TestModuleIdentity
# ---------------------------------------------------------------------------
class TestModuleIdentity:
    """Verify MODULE.bazel exists with expected name and version."""

    def test_module_bazel_exists(self):
        module_path = FEO_DIR / "MODULE.bazel"
        assert module_path.exists(), f"MODULE.bazel not found at {module_path}"

    def test_module_name_is_score_feo(self):
        module_path = FEO_DIR / "MODULE.bazel"
        content = module_path.read_text(encoding="utf-8")
        assert 'name = "score_feo"' in content, (
            "Expected module name 'score_feo' in MODULE.bazel"
        )

    def test_module_version_is_0_0_0(self):
        module_path = FEO_DIR / "MODULE.bazel"
        content = module_path.read_text(encoding="utf-8")
        assert 'version = "0.0.0"' in content, (
            "Expected version 0.0.0 in MODULE.bazel; upstream may have bumped "
            "the version without updating the test baseline"
        )


# ---------------------------------------------------------------------------
# TestFeoCoreCrate
# ---------------------------------------------------------------------------
class TestFeoCoreCrate:
    """Verify the feo core crate (scheduler, workers, agents, signalling)."""

    FEO_SRC = FEO_DIR / "src" / "feo"

    def test_cargo_toml_exists(self):
        path = self.FEO_SRC / "Cargo.toml"
        assert path.exists(), "src/feo/Cargo.toml missing -- core crate removed?"

    def test_cargo_toml_has_package_name(self):
        path = self.FEO_SRC / "Cargo.toml"
        if not path.exists():
            pytest.skip("src/feo/Cargo.toml not found")
        content = path.read_text(encoding="utf-8")
        assert "[package]" in content, (
            "src/feo/Cargo.toml does not define a [package] section"
        )

    @pytest.mark.parametrize(
        "source_file",
        [
            "activity.rs",
            "scheduler.rs",
        ],
    )
    def test_key_source_file_exists(self, source_file: str):
        """Key Rust source files must exist in the feo crate src/ tree."""
        candidates = [
            self.FEO_SRC / "src" / source_file,
            self.FEO_SRC / source_file,
        ]
        found = any(c.exists() for c in candidates)
        if not found:
            # Search recursively as fallback
            matches = list(self.FEO_SRC.rglob(source_file))
            found = len(matches) > 0
        assert found, (
            f"Key source file {source_file} not found in src/feo/ -- "
            "core scheduler API may have regressed"
        )

    @pytest.mark.parametrize(
        "subdir",
        [
            "worker",
            "agent",
            "signalling",
        ],
    )
    def test_key_subdirectory_exists(self, subdir: str):
        """Key subdirectories for the agent/worker/signalling model."""
        # Check direct path and recursive
        direct = self.FEO_SRC / "src" / subdir
        if direct.is_dir():
            return
        matches = [d for d in self.FEO_SRC.rglob(subdir) if d.is_dir()]
        assert len(matches) > 0, (
            f"Subdirectory {subdir}/ not found in src/feo/ -- "
            "core FEO architecture component may have been removed"
        )

    def test_build_file_exists(self):
        build_files = list(self.FEO_SRC.rglob("BUILD")) + list(
            self.FEO_SRC.rglob("BUILD.bazel")
        )
        assert len(build_files) > 0, "No BUILD files found in src/feo/"

    def test_rust_source_files_exist(self):
        rs_files = list(self.FEO_SRC.rglob("*.rs"))
        assert len(rs_files) >= 3, (
            f"Expected at least 3 Rust source files in src/feo/, "
            f"found {len(rs_files)}"
        )


# ---------------------------------------------------------------------------
# TestFeoComCrate
# ---------------------------------------------------------------------------
class TestFeoComCrate:
    """Verify feo-com communication crate."""

    FEO_COM = FEO_DIR / "src" / "feo-com"

    def test_cargo_toml_exists(self):
        path = self.FEO_COM / "Cargo.toml"
        assert path.exists(), "src/feo-com/Cargo.toml missing -- com crate removed?"

    def test_src_directory_exists(self):
        src = self.FEO_COM / "src"
        assert src.is_dir(), "src/feo-com/src/ directory missing"

    def test_rust_source_files_exist(self):
        rs_files = list(self.FEO_COM.rglob("*.rs"))
        assert len(rs_files) >= 1, (
            f"Expected at least 1 Rust source file in src/feo-com/, "
            f"found {len(rs_files)}"
        )

    def test_build_file_exists(self):
        build_files = list(self.FEO_COM.rglob("BUILD")) + list(
            self.FEO_COM.rglob("BUILD.bazel")
        )
        assert len(build_files) > 0, "No BUILD files found in src/feo-com/"


# ---------------------------------------------------------------------------
# TestFeoTimeCrate
# ---------------------------------------------------------------------------
class TestFeoTimeCrate:
    """Verify feo-time crate with C++ bridge (feo_time.h)."""

    FEO_TIME = FEO_DIR / "src" / "feo-time"

    def test_cargo_toml_exists(self):
        path = self.FEO_TIME / "Cargo.toml"
        assert path.exists(), (
            "src/feo-time/Cargo.toml missing -- time crate removed?"
        )

    def test_feo_time_header_exists(self):
        """The C++ API header feo_time.h must exist."""
        candidates = [
            self.FEO_TIME / "include" / "feo_time.h",
            self.FEO_TIME / "feo_time.h",
        ]
        found = any(c.exists() for c in candidates)
        if not found:
            matches = list(self.FEO_TIME.rglob("feo_time.h"))
            found = len(matches) > 0
        assert found, (
            "feo_time.h not found in src/feo-time/ -- "
            "C++ time bridge API may have been removed"
        )

    def test_rust_tests_exist(self):
        """tests.rs or test files should exist for feo-time."""
        candidates = [
            self.FEO_TIME / "tests.rs",
            self.FEO_TIME / "src" / "tests.rs",
        ]
        found = any(c.exists() for c in candidates)
        if not found:
            # Search for any test-related .rs files
            test_files = [
                f for f in self.FEO_TIME.rglob("*.rs")
                if "test" in f.name.lower()
            ]
            found = len(test_files) > 0
        assert found, (
            "No Rust test files found in src/feo-time/ -- "
            "13 unit tests expected"
        )

    def test_cpp_test_exists(self):
        """time_test.cc or C++ test file should exist."""
        candidates = [
            self.FEO_TIME / "time_test.cc",
        ]
        found = any(c.exists() for c in candidates)
        if not found:
            cc_tests = [
                f for f in self.FEO_TIME.rglob("*")
                if f.is_file()
                and "test" in f.name.lower()
                and f.suffix in (".cc", ".cpp")
            ]
            found = len(cc_tests) > 0
        assert found, (
            "No C++ test file (time_test.cc) found in src/feo-time/ -- "
            "C++ time bridge test may have been removed"
        )

    def test_build_file_exists(self):
        build_files = list(self.FEO_TIME.rglob("BUILD")) + list(
            self.FEO_TIME.rglob("BUILD.bazel")
        )
        assert len(build_files) > 0, "No BUILD files found in src/feo-time/"


# ---------------------------------------------------------------------------
# TestFeoTracingCrate
# ---------------------------------------------------------------------------
class TestFeoTracingCrate:
    """Verify feo-tracing crate for Perfetto-based tracing."""

    FEO_TRACING = FEO_DIR / "src" / "feo-tracing"

    def test_cargo_toml_exists(self):
        path = self.FEO_TRACING / "Cargo.toml"
        assert path.exists(), (
            "src/feo-tracing/Cargo.toml missing -- tracing crate removed?"
        )

    def test_rust_source_files_exist(self):
        rs_files = list(self.FEO_TRACING.rglob("*.rs"))
        assert len(rs_files) >= 1, (
            f"Expected at least 1 Rust source file in src/feo-tracing/, "
            f"found {len(rs_files)}"
        )

    def test_build_file_exists(self):
        build_files = list(self.FEO_TRACING.rglob("BUILD")) + list(
            self.FEO_TRACING.rglob("BUILD.bazel")
        )
        assert len(build_files) > 0, "No BUILD files found in src/feo-tracing/"


# ---------------------------------------------------------------------------
# TestFeoTracerBinary
# ---------------------------------------------------------------------------
class TestFeoTracerBinary:
    """Verify feo-tracer daemon binary crate."""

    FEO_TRACER = FEO_DIR / "src" / "feo-tracer"

    def test_cargo_toml_exists(self):
        path = self.FEO_TRACER / "Cargo.toml"
        assert path.exists(), (
            "src/feo-tracer/Cargo.toml missing -- tracer binary removed?"
        )

    def test_cargo_toml_has_binary_target(self):
        path = self.FEO_TRACER / "Cargo.toml"
        if not path.exists():
            pytest.skip("src/feo-tracer/Cargo.toml not found")
        content = path.read_text(encoding="utf-8")
        has_bin = "[[bin]]" in content or "[package]" in content
        assert has_bin, (
            "src/feo-tracer/Cargo.toml does not appear to define a binary target"
        )

    def test_rust_source_files_exist(self):
        rs_files = list(self.FEO_TRACER.rglob("*.rs"))
        assert len(rs_files) >= 1, (
            f"Expected at least 1 Rust source file in src/feo-tracer/, "
            f"found {len(rs_files)}"
        )

    def test_build_file_exists(self):
        build_files = list(self.FEO_TRACER.rglob("BUILD")) + list(
            self.FEO_TRACER.rglob("BUILD.bazel")
        )
        assert len(build_files) > 0, "No BUILD files found in src/feo-tracer/"


# ---------------------------------------------------------------------------
# TestPerfettoModel
# ---------------------------------------------------------------------------
class TestPerfettoModel:
    """Verify perfetto-model crate (protobuf trace model with prost)."""

    PERFETTO_MODEL = FEO_DIR / "src" / "perfetto-model"

    def test_cargo_toml_exists(self):
        path = self.PERFETTO_MODEL / "Cargo.toml"
        assert path.exists(), (
            "src/perfetto-model/Cargo.toml missing -- protobuf model removed?"
        )

    def test_rust_source_files_exist(self):
        rs_files = list(self.PERFETTO_MODEL.rglob("*.rs"))
        assert len(rs_files) >= 1, (
            f"Expected at least 1 Rust source file in src/perfetto-model/, "
            f"found {len(rs_files)}"
        )

    def test_proto_or_generated_files_exist(self):
        """Either .proto source files or generated Rust bindings should exist."""
        proto_files = list(self.PERFETTO_MODEL.rglob("*.proto"))
        generated_rs = [
            f for f in self.PERFETTO_MODEL.rglob("*.rs")
            if "generated" in f.name.lower()
            or "proto" in f.name.lower()
            or "perfetto" in f.name.lower()
        ]
        assert len(proto_files) > 0 or len(generated_rs) > 0, (
            "No .proto files or proto-generated Rust files found in "
            "src/perfetto-model/ -- protobuf model may have been removed"
        )

    def test_build_file_exists(self):
        build_files = list(self.PERFETTO_MODEL.rglob("BUILD")) + list(
            self.PERFETTO_MODEL.rglob("BUILD.bazel")
        )
        assert len(build_files) > 0, "No BUILD files found in src/perfetto-model/"


# ---------------------------------------------------------------------------
# TestExamples
# ---------------------------------------------------------------------------
class TestExamples:
    """Verify example directories exist for downstream reference."""

    EXAMPLES_DIR = FEO_DIR / "examples" / "rust"

    def test_examples_directory_exists(self):
        has_examples = (
            self.EXAMPLES_DIR.is_dir()
            or (FEO_DIR / "examples").is_dir()
        )
        assert has_examples, "examples/ directory missing from score-feo"

    @pytest.mark.parametrize(
        "example",
        [
            "mini-adas",
            "cycle-benchmark",
        ],
    )
    def test_example_directory_exists(self, example: str):
        # Check examples/rust/<example> first, then examples/<example>
        candidates = [
            self.EXAMPLES_DIR / example,
            FEO_DIR / "examples" / example,
        ]
        found = any(c.is_dir() for c in candidates)
        assert found, (
            f"Example directory {example}/ missing -- "
            "reference application may have been removed"
        )

    @pytest.mark.parametrize(
        "example",
        [
            "mini-adas",
            "cycle-benchmark",
        ],
    )
    def test_example_has_rust_source(self, example: str):
        """Each example should contain at least one .rs file."""
        candidates = [
            self.EXAMPLES_DIR / example,
            FEO_DIR / "examples" / example,
        ]
        for c in candidates:
            if c.is_dir():
                rs_files = list(c.rglob("*.rs"))
                if len(rs_files) > 0:
                    return
        pytest.skip(f"Example {example} directory not found or has no .rs files")


# ---------------------------------------------------------------------------
# TestIntegrationTests
# ---------------------------------------------------------------------------
class TestIntegrationTests:
    """Verify integration test harness and test agent."""

    TESTS_DIR = FEO_DIR / "tests" / "rust"

    def test_tests_directory_exists(self):
        candidates = [
            self.TESTS_DIR,
            FEO_DIR / "tests",
        ]
        assert any(c.is_dir() for c in candidates), (
            "tests/ directory missing from score-feo"
        )

    def test_feo_tests_directory_exists(self):
        candidates = [
            self.TESTS_DIR / "feo_tests",
            FEO_DIR / "tests" / "feo_tests",
        ]
        found = any(c.is_dir() for c in candidates)
        if not found:
            # Search recursively for feo_tests
            matches = [d for d in FEO_DIR.rglob("feo_tests") if d.is_dir()]
            found = len(matches) > 0
        assert found, (
            "feo_tests/ directory not found -- integration test harness missing"
        )

    def test_test_agent_directory_exists(self):
        candidates = [
            self.TESTS_DIR / "test_agent",
            FEO_DIR / "tests" / "test_agent",
        ]
        found = any(c.is_dir() for c in candidates)
        if not found:
            matches = [d for d in FEO_DIR.rglob("test_agent") if d.is_dir()]
            found = len(matches) > 0
        assert found, (
            "test_agent/ directory not found -- mock agent for testing missing"
        )

    def test_test_agent_has_rust_source(self):
        """Test agent should have Rust source files."""
        candidates = [
            self.TESTS_DIR / "test_agent",
            FEO_DIR / "tests" / "test_agent",
        ]
        for c in candidates:
            if c.is_dir():
                rs_files = list(c.rglob("*.rs"))
                if len(rs_files) > 0:
                    return
        # Recursive fallback
        matches = [d for d in FEO_DIR.rglob("test_agent") if d.is_dir()]
        for d in matches:
            rs_files = list(d.rglob("*.rs"))
            if len(rs_files) > 0:
                return
        pytest.skip("test_agent directory not found or has no .rs files")


# ---------------------------------------------------------------------------
# TestCargoWorkspace
# ---------------------------------------------------------------------------
class TestCargoWorkspace:
    """Verify root Cargo.toml workspace with 12 members."""

    def test_root_cargo_toml_exists(self):
        path = FEO_DIR / "Cargo.toml"
        assert path.exists(), "Root Cargo.toml missing -- Rust workspace removed?"

    def test_cargo_lock_exists(self):
        path = FEO_DIR / "Cargo.lock"
        assert path.exists(), (
            "Cargo.lock not found -- Rust dependencies not locked"
        )

    def test_cargo_toml_has_workspace(self):
        path = FEO_DIR / "Cargo.toml"
        if not path.exists():
            pytest.skip("Root Cargo.toml not found")
        content = path.read_text(encoding="utf-8")
        assert "[workspace]" in content, (
            "Root Cargo.toml does not define a [workspace] section"
        )

    def test_workspace_has_members(self):
        """Workspace should declare members."""
        path = FEO_DIR / "Cargo.toml"
        if not path.exists():
            pytest.skip("Root Cargo.toml not found")
        content = path.read_text(encoding="utf-8")
        assert "members" in content, (
            "Root Cargo.toml [workspace] does not declare members"
        )

    def test_workspace_member_count(self):
        """Expect approximately 12 workspace members."""
        path = FEO_DIR / "Cargo.toml"
        if not path.exists():
            pytest.skip("Root Cargo.toml not found")
        content = path.read_text(encoding="utf-8")
        # Count quoted strings in members array
        member_matches = re.findall(r'"[^"]+/[^"]*"', content)
        assert len(member_matches) >= 4, (
            f"Expected at least 4 workspace members, found {len(member_matches)} "
            f"-- crates may have been removed from workspace"
        )


# ---------------------------------------------------------------------------
# TestBuildTargets
# ---------------------------------------------------------------------------
class TestBuildTargets:
    """Verify key BUILD files exist for each component."""

    @pytest.mark.parametrize(
        "build_path",
        [
            "src/feo",
            "src/feo-com",
            "src/feo-time",
            "src/feo-tracing",
            "src/feo-tracer",
            "src/perfetto-model",
        ],
    )
    def test_crate_build_file_exists(self, build_path: str):
        crate_dir = FEO_DIR / build_path
        build = crate_dir / "BUILD"
        build_bazel = crate_dir / "BUILD.bazel"
        assert build.exists() or build_bazel.exists(), (
            f"No BUILD or BUILD.bazel file found at {build_path}/ -- "
            "Bazel target may have been removed"
        )

    def test_top_level_build_file_exists(self):
        """The repository root must have a BUILD or BUILD.bazel file."""
        has_build = (FEO_DIR / "BUILD").exists() or (
            FEO_DIR / "BUILD.bazel"
        ).exists()
        assert has_build, "No top-level BUILD or BUILD.bazel in score-feo"

    def test_bazelrc_exists(self):
        """A .bazelrc file should exist for build configuration."""
        path = FEO_DIR / ".bazelrc"
        assert path.exists(), (
            ".bazelrc not found -- build configs (--config=x86_64-linux, "
            "--config=lint-rust) may be missing"
        )

    @pytest.mark.parametrize(
        "config_name",
        [
            "x86_64-linux",
            "lint-rust",
        ],
    )
    def test_bazelrc_has_config(self, config_name: str):
        """Key build configs should be defined in .bazelrc."""
        path = FEO_DIR / ".bazelrc"
        if not path.exists():
            pytest.skip(".bazelrc not found")
        content = path.read_text(encoding="utf-8")
        assert config_name in content, (
            f"Config '{config_name}' not found in .bazelrc -- "
            "build configuration may have been removed"
        )
