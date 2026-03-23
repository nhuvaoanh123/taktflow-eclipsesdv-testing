"""Safety contract verification for score-feo components.

Verifies that the Fixed Execution Order (FEO) scheduler follows required
patterns for deterministic scheduling:
- QM classification (not ASIL-rated)
- Deterministic scheduler with worker pool
- IPC safety via feo-com with optional iceoryx2 backend
- Tracing infrastructure for observability (feo-tracing, perfetto-model, feo-tracer)
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
FEO_DIR = PROJECT_ROOT / "score-feo"


# ---------------------------------------------------------------------------
# TestQmClassification
# ---------------------------------------------------------------------------
class TestQmClassification:
    """Verify FEO is QM-rated (not ASIL) in project configuration."""

    def test_project_config_exists(self):
        """project_config.bzl or equivalent should exist."""
        candidates = [
            FEO_DIR / "project_config.bzl",
            FEO_DIR / "project_config.json",
            FEO_DIR / "MODULE.bazel",
        ]
        assert any(c.exists() for c in candidates), (
            "No project configuration file found -- "
            "cannot determine safety classification"
        )

    def test_qm_classification(self):
        """FEO should be classified as QM (Quality Management),
        not ASIL-rated."""
        # Check project_config.bzl first
        config_bzl = FEO_DIR / "project_config.bzl"
        if config_bzl.exists():
            content = config_bzl.read_text(encoding="utf-8")
            has_qm = "qm" in content.lower() or "QM" in content
            has_asil = re.search(r"asil[_-]?[abcd]", content, re.IGNORECASE)
            if has_qm:
                assert True
                return
            if has_asil:
                pytest.fail(
                    "FEO appears to claim ASIL rating in project_config.bzl -- "
                    "expected QM classification"
                )
                return

        # If no project_config.bzl, check MODULE.bazel for safety annotations
        module_bazel = FEO_DIR / "MODULE.bazel"
        if module_bazel.exists():
            content = module_bazel.read_text(encoding="utf-8")
            has_asil = re.search(r"asil[_-]?[abcd]", content, re.IGNORECASE)
            if has_asil:
                pytest.fail(
                    "FEO appears to claim ASIL rating in MODULE.bazel -- "
                    "expected QM classification"
                )

        # No explicit ASIL claim found -- consistent with QM
        assert True

    def test_no_asil_in_cargo_workspace(self):
        """Root Cargo.toml should not claim ASIL classification."""
        cargo_toml = FEO_DIR / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("Root Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        has_asil = re.search(r"asil[_-]?[abcd]", content, re.IGNORECASE)
        assert not has_asil, (
            "Root Cargo.toml contains ASIL reference -- "
            "FEO is expected to be QM-rated"
        )


# ---------------------------------------------------------------------------
# TestDeterministicScheduler
# ---------------------------------------------------------------------------
class TestDeterministicScheduler:
    """Verify deterministic scheduler components exist:
    scheduler.rs, worker/ directory, agent/ directory."""

    FEO_SRC = FEO_DIR / "src" / "feo"

    def test_scheduler_source_exists(self):
        """scheduler.rs must exist as the core scheduling engine."""
        candidates = [
            self.FEO_SRC / "src" / "scheduler.rs",
            self.FEO_SRC / "scheduler.rs",
        ]
        found = any(c.exists() for c in candidates)
        if not found:
            matches = list(self.FEO_SRC.rglob("scheduler.rs"))
            found = len(matches) > 0
        assert found, (
            "scheduler.rs not found in src/feo/ -- "
            "deterministic scheduler implementation missing"
        )

    def test_worker_directory_exists(self):
        """worker/ directory must exist for the worker pool model."""
        direct = self.FEO_SRC / "src" / "worker"
        if direct.is_dir():
            return
        matches = [d for d in self.FEO_SRC.rglob("worker") if d.is_dir()]
        assert len(matches) > 0, (
            "worker/ directory not found in src/feo/ -- "
            "worker pool for deterministic execution missing"
        )

    def test_activity_source_exists(self):
        """activity.rs must exist as the schedulable unit abstraction."""
        candidates = [
            self.FEO_SRC / "src" / "activity.rs",
            self.FEO_SRC / "activity.rs",
        ]
        found = any(c.exists() for c in candidates)
        if not found:
            matches = list(self.FEO_SRC.rglob("activity.rs"))
            found = len(matches) > 0
        assert found, (
            "activity.rs not found in src/feo/ -- "
            "activity abstraction for scheduling missing"
        )

    def test_signalling_exists(self):
        """Signalling infrastructure for deterministic execution ordering."""
        candidates = [
            self.FEO_SRC / "src" / "signalling",
            self.FEO_SRC / "signalling",
        ]
        found = any(c.is_dir() for c in candidates)
        if not found:
            matches = [d for d in self.FEO_SRC.rglob("signalling") if d.is_dir()]
            found = len(matches) > 0
        if not found:
            # Also check for signal-related .rs files
            signal_files = [
                f for f in self.FEO_SRC.rglob("*.rs")
                if "signal" in f.name.lower()
            ]
            found = len(signal_files) > 0
        assert found, (
            "signalling/ directory or signal source files not found in src/feo/ -- "
            "execution order signalling infrastructure missing"
        )

    def test_scheduler_has_tests(self):
        """Scheduler should have associated test files or test modules."""
        test_files = [
            f for f in self.FEO_SRC.rglob("*.rs")
            if "test" in f.name.lower() or "test" in str(f.parent).lower()
        ]
        # Also check for #[cfg(test)] in scheduler.rs
        scheduler_files = list(self.FEO_SRC.rglob("scheduler.rs"))
        has_test_mod = False
        for sf in scheduler_files:
            content = sf.read_text(encoding="utf-8", errors="ignore")
            if "#[cfg(test)]" in content or "#[test]" in content:
                has_test_mod = True
                break
        assert len(test_files) > 0 or has_test_mod, (
            "No test files or test modules found for the scheduler -- "
            "deterministic scheduling behavior not tested"
        )


# ---------------------------------------------------------------------------
# TestIpcSafety
# ---------------------------------------------------------------------------
class TestIpcSafety:
    """Verify IPC safety: feo-com directory, iceoryx2 optional feature,
    Linux SHM default backend."""

    FEO_COM = FEO_DIR / "src" / "feo-com"

    def test_feo_com_directory_exists(self):
        assert self.FEO_COM.is_dir(), (
            "src/feo-com/ directory missing -- IPC communication crate removed"
        )

    def test_feo_com_has_cargo_toml(self):
        path = self.FEO_COM / "Cargo.toml"
        assert path.exists(), "src/feo-com/Cargo.toml missing"

    def test_iceoryx2_optional_feature(self):
        """iceoryx2 should be available as an optional IPC backend."""
        cargo_toml = self.FEO_COM / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("src/feo-com/Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        has_iceoryx2 = "iceoryx2" in content
        assert has_iceoryx2, (
            "iceoryx2 not referenced in feo-com/Cargo.toml -- "
            "optional IPC backend may have been removed"
        )

    def test_default_ipc_is_linux_shm(self):
        """Default IPC should be Linux SHM (iceoryx2 is optional).
        Check that default-features or default feature does not include iceoryx2."""
        cargo_toml = self.FEO_COM / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("src/feo-com/Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        # If iceoryx2 is in default features, that's unexpected
        default_match = re.search(
            r'default\s*=\s*\[([^\]]*)\]', content
        )
        if default_match:
            default_features = default_match.group(1)
            if "iceoryx2" in default_features:
                pytest.fail(
                    "iceoryx2 appears to be a default feature -- "
                    "expected Linux SHM as default IPC backend"
                )

    def test_feo_com_has_source_files(self):
        """feo-com should have Rust source files implementing IPC."""
        rs_files = list(self.FEO_COM.rglob("*.rs"))
        assert len(rs_files) >= 1, (
            f"Expected at least 1 Rust source file in src/feo-com/, "
            f"found {len(rs_files)}"
        )

    def test_feo_com_build_file_exists(self):
        build_files = list(self.FEO_COM.rglob("BUILD")) + list(
            self.FEO_COM.rglob("BUILD.bazel")
        )
        assert len(build_files) > 0, "No BUILD files found in src/feo-com/"


# ---------------------------------------------------------------------------
# TestTracingInfrastructure
# ---------------------------------------------------------------------------
class TestTracingInfrastructure:
    """Verify tracing infrastructure: feo-tracing crate, perfetto-model crate,
    feo-tracer binary daemon."""

    def test_feo_tracing_exists(self):
        path = FEO_DIR / "src" / "feo-tracing"
        assert path.is_dir(), (
            "src/feo-tracing/ directory missing -- tracing crate removed"
        )

    def test_feo_tracing_cargo_toml(self):
        path = FEO_DIR / "src" / "feo-tracing" / "Cargo.toml"
        assert path.exists(), "src/feo-tracing/Cargo.toml missing"

    def test_perfetto_model_exists(self):
        path = FEO_DIR / "src" / "perfetto-model"
        assert path.is_dir(), (
            "src/perfetto-model/ directory missing -- "
            "Perfetto trace model crate removed"
        )

    def test_perfetto_model_cargo_toml(self):
        path = FEO_DIR / "src" / "perfetto-model" / "Cargo.toml"
        assert path.exists(), "src/perfetto-model/Cargo.toml missing"

    def test_feo_tracer_exists(self):
        path = FEO_DIR / "src" / "feo-tracer"
        assert path.is_dir(), (
            "src/feo-tracer/ directory missing -- tracer daemon removed"
        )

    def test_feo_tracer_cargo_toml(self):
        path = FEO_DIR / "src" / "feo-tracer" / "Cargo.toml"
        assert path.exists(), "src/feo-tracer/Cargo.toml missing"

    def test_tracing_chain_complete(self):
        """All three tracing components must exist: feo-tracing (lib),
        perfetto-model (protobuf), feo-tracer (binary)."""
        components = [
            FEO_DIR / "src" / "feo-tracing",
            FEO_DIR / "src" / "perfetto-model",
            FEO_DIR / "src" / "feo-tracer",
        ]
        missing = [str(c) for c in components if not c.is_dir()]
        assert len(missing) == 0, (
            f"Tracing chain incomplete -- missing components: {missing}"
        )

    def test_feo_tracer_references_perfetto(self):
        """feo-tracer (the daemon) uses perfetto-model for trace output."""
        cargo_toml = FEO_DIR / "src" / "feo-tracer" / "Cargo.toml"
        if not cargo_toml.exists():
            pytest.skip("src/feo-tracer/Cargo.toml not found")
        content = cargo_toml.read_text(encoding="utf-8")
        assert "perfetto" in content.lower(), (
            "feo-tracer does not reference perfetto-model -- "
            "tracer to protobuf link may be broken"
        )

    def test_feo_tracer_is_binary(self):
        """feo-tracer should produce a binary (has main.rs or [[bin]])."""
        tracer_dir = FEO_DIR / "src" / "feo-tracer"
        if not tracer_dir.is_dir():
            pytest.skip("src/feo-tracer/ not found")
        main_rs = tracer_dir / "src" / "main.rs"
        if main_rs.exists():
            return
        # Check for [[bin]] in Cargo.toml
        cargo_toml = tracer_dir / "Cargo.toml"
        if cargo_toml.exists():
            content = cargo_toml.read_text(encoding="utf-8")
            if "[[bin]]" in content:
                return
        # Search for main.rs anywhere
        main_files = list(tracer_dir.rglob("main.rs"))
        assert len(main_files) > 0, (
            "No main.rs found in src/feo-tracer/ -- "
            "tracer daemon may not produce a binary"
        )
