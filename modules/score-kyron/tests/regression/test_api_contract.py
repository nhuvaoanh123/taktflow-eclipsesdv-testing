"""Regression tests for score-kyron API contract stability.

Verification methods: API contract verification, file existence.
Platform: any (no build required — file inspection only).

score-kyron provides a Rust async runtime scheduler for S-CORE:
  - kyron: async execution engine with work-stealing scheduler
  - kyron-foundation: lock-free containers (SPMC queues, trigger queues,
    reusable object pools, thread wait barriers)
  - kyron-macros: proc-macros for task/main definitions
  - logging_tracing: DLT-compatible tracing layer
  - mio: I/O event loop with epoll/kqueue selectors
  - IPC: iceoryx2 event integration

If expected source files or Cargo packages are missing, the upstream
module may have broken backwards compatibility.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
KYRON_DIR = PROJECT_ROOT / "score-kyron"
SRC_DIR = KYRON_DIR / "src"


# ---------------------------------------------------------------------------
# TestModuleIdentity
# ---------------------------------------------------------------------------
class TestModuleIdentity:
    """Verify Cargo.toml workspace and Bazel module presence."""

    def test_cargo_toml_exists(self):
        assert (KYRON_DIR / "Cargo.toml").exists(), \
            f"Cargo.toml not found at {KYRON_DIR}"

    def test_cargo_toml_is_workspace(self):
        content = (KYRON_DIR / "Cargo.toml").read_text(encoding="utf-8")
        assert "[workspace]" in content, \
            "Cargo.toml is not a workspace — expected multi-crate layout"

    def test_module_bazel_exists(self):
        path = KYRON_DIR / "MODULE.bazel"
        if not path.exists():
            pytest.skip("MODULE.bazel not found (Cargo-primary project)")
        content = path.read_text(encoding="utf-8")
        assert "score_kyron" in content or "kyron" in content, \
            "MODULE.bazel does not reference kyron"

    def test_bazelversion_exists(self):
        path = KYRON_DIR / ".bazelversion"
        if not path.exists():
            pytest.skip(".bazelversion not found")
        version = path.read_text().strip()
        assert re.match(r"\d+\.\d+\.\d+", version), \
            f"Invalid version in .bazelversion: {version}"


# ---------------------------------------------------------------------------
# TestKyronCoreComponent
# ---------------------------------------------------------------------------
class TestKyronCoreComponent:
    """Verify the kyron core runtime crate structure."""

    KYRON_CORE = SRC_DIR / "kyron"

    def test_kyron_directory_exists(self):
        assert self.KYRON_CORE.is_dir(), \
            "src/kyron/ missing — core runtime removed"

    def test_cargo_toml_exists(self):
        assert (self.KYRON_CORE / "Cargo.toml").exists(), \
            "src/kyron/Cargo.toml missing"

    def test_scheduler_module_exists(self):
        path = self.KYRON_CORE / "src" / "scheduler"
        assert path.is_dir(), \
            "src/kyron/src/scheduler/ missing — work-stealing scheduler removed"

    def test_channels_module_exists(self):
        path = self.KYRON_CORE / "src" / "channels"
        assert path.is_dir(), \
            "src/kyron/src/channels/ missing — async channel implementations removed"

    def test_futures_module_exists(self):
        path = self.KYRON_CORE / "src" / "futures"
        assert path.is_dir(), \
            "src/kyron/src/futures/ missing — future combinators removed"

    def test_time_module_exists(self):
        path = self.KYRON_CORE / "src" / "time"
        if not path.is_dir():
            # May be a single file module
            path = self.KYRON_CORE / "src" / "time.rs"
        assert path.exists(), \
            "src/kyron/src/time/ missing — timer wheel removed"

    def test_io_module_exists(self):
        path = self.KYRON_CORE / "src" / "io"
        if not path.is_dir():
            path = self.KYRON_CORE / "src" / "io.rs"
        assert path.exists(), \
            "src/kyron/src/io/ missing — async I/O removed"

    def test_ipc_module_exists(self):
        """IPC module with iceoryx2 event integration."""
        path = self.KYRON_CORE / "src" / "ipc"
        if not path.is_dir():
            path = self.KYRON_CORE / "src" / "ipc.rs"
        assert path.exists(), \
            "src/kyron/src/ipc/ missing — iceoryx2 IPC integration removed"

    def test_mio_module_exists(self):
        """Internal mio I/O event loop."""
        path = self.KYRON_CORE / "src" / "mio"
        if not path.is_dir():
            path = self.KYRON_CORE / "src" / "mio.rs"
        assert path.exists(), \
            "src/kyron/src/mio/ missing — I/O event loop removed"

    def test_has_rust_source_files(self):
        if not self.KYRON_CORE.is_dir():
            pytest.skip("kyron core not found")
        rs_files = list(self.KYRON_CORE.rglob("*.rs"))
        assert len(rs_files) >= 10, \
            f"Expected at least 10 Rust sources in kyron core, found {len(rs_files)}"


# ---------------------------------------------------------------------------
# TestKyronFoundationComponent
# ---------------------------------------------------------------------------
class TestKyronFoundationComponent:
    """Verify kyron-foundation crate (lock-free containers)."""

    FOUNDATION = SRC_DIR / "kyron-foundation"

    def test_foundation_directory_exists(self):
        assert self.FOUNDATION.is_dir(), \
            "src/kyron-foundation/ missing — foundation library removed"

    def test_cargo_toml_exists(self):
        assert (self.FOUNDATION / "Cargo.toml").exists(), \
            "kyron-foundation/Cargo.toml missing"

    def test_containers_module_exists(self):
        path = self.FOUNDATION / "src" / "containers"
        if not path.is_dir():
            path = self.FOUNDATION / "src" / "containers.rs"
        assert path.exists(), \
            "kyron-foundation containers module missing — SPMC queues removed"

    def test_threading_module_exists(self):
        path = self.FOUNDATION / "src" / "threading"
        if not path.is_dir():
            path = self.FOUNDATION / "src" / "threading.rs"
        assert path.exists(), \
            "kyron-foundation threading module missing"


# ---------------------------------------------------------------------------
# TestKyronMacrosComponent
# ---------------------------------------------------------------------------
class TestKyronMacrosComponent:
    """Verify kyron-macros crate (proc-macros)."""

    MACROS = SRC_DIR / "kyron-macros"

    def test_macros_directory_exists(self):
        assert self.MACROS.is_dir(), \
            "src/kyron-macros/ missing — proc-macro crate removed"

    def test_cargo_toml_exists(self):
        assert (self.MACROS / "Cargo.toml").exists(), \
            "kyron-macros/Cargo.toml missing"

    def test_lib_rs_exists(self):
        assert (self.MACROS / "src" / "lib.rs").exists(), \
            "kyron-macros/src/lib.rs missing — proc-macro entry point removed"


# ---------------------------------------------------------------------------
# TestLoggingTracingComponent
# ---------------------------------------------------------------------------
class TestLoggingTracingComponent:
    """Verify logging_tracing crate (DLT integration)."""

    TRACING = SRC_DIR / "logging_tracing"

    def test_tracing_directory_exists(self):
        assert self.TRACING.is_dir(), \
            "src/logging_tracing/ missing — DLT tracing integration removed"

    def test_has_source_files(self):
        if not self.TRACING.is_dir():
            pytest.skip("logging_tracing not found")
        rs_files = list(self.TRACING.rglob("*.rs"))
        assert len(rs_files) >= 1, \
            "No Rust sources in logging_tracing/"


# ---------------------------------------------------------------------------
# TestExamplesExist
# ---------------------------------------------------------------------------
class TestExamplesExist:
    """Verify example programs exist for documentation/testing."""

    EXAMPLES = KYRON_DIR / "src" / "kyron" / "examples"

    def test_examples_directory_exists(self):
        if not self.EXAMPLES.is_dir():
            pytest.skip("examples/ directory not found")
        rs_files = list(self.EXAMPLES.glob("*.rs"))
        assert len(rs_files) >= 1, \
            "No example programs found in kyron/examples/"
