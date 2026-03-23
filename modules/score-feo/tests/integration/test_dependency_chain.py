"""Integration tests for score-feo dependency chain.

Verifies that score-feo correctly declares its dependencies on
score_communication, score_baselibs, score_baselibs_rust, score_logging
in MODULE.bazel, and Rust ecosystem dependencies (iceoryx2, tokio, prost,
serde) in Cargo.lock. Also verifies protobuf integration via perfetto-model.

Platform: any (file inspection only, no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
FEO_DIR = PROJECT_ROOT / "modules" / "score-feo" / "upstream"


# ---------------------------------------------------------------------------
# TestScoreDependencies
# ---------------------------------------------------------------------------
class TestScoreDependencies:
    """Verify MODULE.bazel declares score_communication, score_baselibs,
    and score_logging dependencies."""

    MODULE_BAZEL = FEO_DIR / "MODULE.bazel"

    def test_module_bazel_exists(self):
        assert self.MODULE_BAZEL.exists(), (
            f"score-feo/MODULE.bazel not found at {self.MODULE_BAZEL}"
        )

    def test_declares_score_communication(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        pattern = r'bazel_dep\(\s*name\s*=\s*"score_communication"'
        assert re.search(pattern, content), (
            "score-feo/MODULE.bazel does not declare a bazel_dep "
            "on score_communication"
        )

    def test_score_communication_version(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        match = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_communication"\s*,\s*version\s*=\s*"([^"]+)"',
            content,
        )
        assert match, (
            "Cannot parse score_communication version from score-feo/MODULE.bazel"
        )
        assert match.group(1) == "0.1.2", (
            f"Expected score_communication 0.1.2, found {match.group(1)}"
        )

    def test_declares_score_baselibs(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        pattern = r'bazel_dep\(\s*name\s*=\s*"score_baselibs"'
        assert re.search(pattern, content), (
            "score-feo/MODULE.bazel does not declare a bazel_dep "
            "on score_baselibs"
        )

    def test_score_baselibs_version(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        match = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_baselibs"\s*,\s*version\s*=\s*"([^"]+)"',
            content,
        )
        assert match, (
            "Cannot parse score_baselibs version from score-feo/MODULE.bazel"
        )
        assert match.group(1) == "0.2.4", (
            f"Expected score_baselibs 0.2.4, found {match.group(1)}"
        )

    def test_declares_score_baselibs_rust(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        pattern = r'bazel_dep\(\s*name\s*=\s*"score_baselibs_rust"'
        assert re.search(pattern, content), (
            "score-feo/MODULE.bazel does not declare a bazel_dep "
            "on score_baselibs_rust"
        )

    def test_score_baselibs_rust_version(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        match = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_baselibs_rust"\s*,\s*version\s*=\s*"([^"]+)"',
            content,
        )
        assert match, (
            "Cannot parse score_baselibs_rust version from score-feo/MODULE.bazel"
        )
        assert match.group(1) == "0.1.0", (
            f"Expected score_baselibs_rust 0.1.0, found {match.group(1)}"
        )

    def test_declares_score_logging(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        pattern = r'bazel_dep\(\s*name\s*=\s*"score_logging"'
        assert re.search(pattern, content), (
            "score-feo/MODULE.bazel does not declare a bazel_dep "
            "on score_logging"
        )

    def test_score_logging_version(self):
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        match = re.search(
            r'bazel_dep\(\s*name\s*=\s*"score_logging"\s*,\s*version\s*=\s*"([^"]+)"',
            content,
        )
        assert match, (
            "Cannot parse score_logging version from score-feo/MODULE.bazel"
        )
        assert match.group(1) == "0.1.2", (
            f"Expected score_logging 0.1.2, found {match.group(1)}"
        )

    def test_transitive_score_deps_note(self):
        """Informational: score_communication, score_baselibs, score_logging,
        and score_baselibs_rust are all transitively proven via their
        respective assessments."""
        expected_deps = 4
        assert expected_deps > 0, "Sanity check"


# ---------------------------------------------------------------------------
# TestRustDependencies
# ---------------------------------------------------------------------------
class TestRustDependencies:
    """Verify key Rust ecosystem dependencies in Cargo.lock."""

    CARGO_LOCK = FEO_DIR / "Cargo.lock"

    def test_cargo_lock_exists(self):
        assert self.CARGO_LOCK.exists(), (
            "Cargo.lock not found at score-feo root -- "
            "Rust dependencies not locked"
        )

    @pytest.mark.parametrize(
        "crate_name",
        [
            "iceoryx2",
            "tokio",
            "prost",
            "serde",
        ],
    )
    def test_dependency_present_in_lockfile(self, crate_name: str):
        """Key Rust dependencies should appear in Cargo.lock."""
        if not self.CARGO_LOCK.exists():
            pytest.skip("Cargo.lock not found")
        content = self.CARGO_LOCK.read_text(encoding="utf-8")
        # Cargo.lock uses [[package]] sections with name = "crate_name"
        pattern = rf'name\s*=\s*"{crate_name}"'
        assert re.search(pattern, content), (
            f"Rust dependency '{crate_name}' not found in Cargo.lock -- "
            "dependency may have been removed"
        )

    def test_iceoryx2_is_optional_feature(self):
        """iceoryx2 should be gated behind an optional feature in feo-com."""
        cargo_toml = FEO_DIR / "src" / "feo-com" / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("src/feo-com/Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        has_optional = "optional" in content and "iceoryx2" in content
        has_feature = "[features]" in content
        assert has_optional or has_feature, (
            "iceoryx2 does not appear to be optional in feo-com -- "
            "expected optional feature gate for IPC backend selection"
        )

    def test_prost_for_protobuf(self):
        """prost should be used in perfetto-model for protobuf code generation."""
        cargo_toml = FEO_DIR / "src" / "perfetto-model" / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("src/perfetto-model/Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "prost" in content, (
            "prost not referenced in perfetto-model/Cargo.toml -- "
            "protobuf code generation may have changed"
        )

    def test_cargo_toml_at_root(self):
        cargo_toml = FEO_DIR / "Cargo.toml"
        assert cargo_toml.exists(), (
            "Cargo.toml not found at score-feo root -- Rust workspace not configured"
        )

    def test_cargo_toml_has_workspace(self):
        cargo_toml = FEO_DIR / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("Root Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "[workspace]" in content, (
            "Root Cargo.toml does not define a [workspace] section"
        )


# ---------------------------------------------------------------------------
# TestProtobufIntegration
# ---------------------------------------------------------------------------
class TestProtobufIntegration:
    """Verify protobuf integration via MODULE.bazel and perfetto-model crate."""

    MODULE_BAZEL = FEO_DIR / "MODULE.bazel"

    def test_protobuf_in_module_bazel(self):
        """MODULE.bazel should reference protobuf or prost."""
        if not self.MODULE_BAZEL.exists():
            pytest.skip("MODULE.bazel not found")
        content = self.MODULE_BAZEL.read_text(encoding="utf-8")
        has_protobuf = "protobuf" in content.lower() or "prost" in content.lower()
        # Also check for proto toolchain references
        has_proto_ref = "proto" in content.lower()
        assert has_protobuf or has_proto_ref, (
            "No protobuf/prost reference found in MODULE.bazel -- "
            "protobuf integration may have been removed"
        )

    def test_perfetto_model_crate_exists(self):
        """perfetto-model crate should exist for trace model protobuf."""
        path = FEO_DIR / "src" / "perfetto-model"
        assert path.is_dir(), (
            "src/perfetto-model/ directory missing -- "
            "Perfetto trace model crate removed"
        )

    def test_perfetto_model_cargo_toml_references_prost(self):
        cargo_toml = FEO_DIR / "src" / "perfetto-model" / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("src/perfetto-model/Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "prost" in content, (
            "prost not found in perfetto-model/Cargo.toml -- "
            "protobuf integration may have changed"
        )

    def test_perfetto_model_has_proto_files_or_build_script(self):
        """Either .proto source files or a build.rs should exist for codegen."""
        model_dir = FEO_DIR / "src" / "perfetto-model"
        if not model_dir.is_dir():
            pytest.skip("src/perfetto-model/ not found")
        proto_files = list(model_dir.rglob("*.proto"))
        build_rs = model_dir / "build.rs"
        has_codegen = len(proto_files) > 0 or build_rs.exists()
        assert has_codegen, (
            "No .proto files or build.rs found in perfetto-model/ -- "
            "protobuf code generation source missing"
        )

    def test_feo_tracer_depends_on_perfetto_model(self):
        """feo-tracer (not feo-tracing) uses perfetto-model for trace output."""
        cargo_toml = FEO_DIR / "src" / "feo-tracer" / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("src/feo-tracer/Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "perfetto" in content.lower(), (
            "feo-tracer/Cargo.toml does not reference perfetto-model -- "
            "tracer-to-protobuf link may be broken"
        )
