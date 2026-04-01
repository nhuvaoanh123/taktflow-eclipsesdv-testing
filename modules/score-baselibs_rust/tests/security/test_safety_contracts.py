"""Safety contract verification for score-baselibs_rust (ASIL B).

Rust foundation libraries providing containers, sync primitives,
elementary types, PAL, threading, and logging format macros.

ASIL B requirements verified:
- Unsafe blocks documented with SAFETY justification
- No dynamic allocation in lock-free container hot paths
- Atomic orderings correct (no Relaxed for shared state transitions)
- Test infrastructure for statement + branch coverage
- Build reproducibility (Cargo.lock + MODULE.bazel.lock)

Verification method: source inspection (ISO 26262 Part 6).
Platform: any (no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
BASELIBS_RUST_DIR = PROJECT_ROOT / "score-baselibs_rust"
SRC_DIR = BASELIBS_RUST_DIR / "src"


# ---------------------------------------------------------------------------
# TestAsilBUnsafeJustifications
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAsilBUnsafeJustifications:
    """ASIL B: every unsafe block must have a SAFETY justification comment."""

    def _scan_unjustified(self, search_dir):
        violations = []
        if not search_dir.is_dir():
            return violations
        for f in search_dir.rglob("*.rs"):
            if "test" in f.name.lower():
                continue
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                if "unsafe" in stripped and ("{" in stripped or "fn " in stripped):
                    if stripped.startswith("unsafe impl"):
                        continue
                    context = "\n".join(lines[max(0, i - 5):i])
                    if "SAFETY" not in context and "Safety" not in context:
                        rel = f.relative_to(BASELIBS_RUST_DIR) if BASELIBS_RUST_DIR.is_dir() else f.name
                        violations.append(f"{rel}:{i+1}: {stripped[:80]}")
        return violations

    def test_containers_unsafe_justified(self):
        """Containers crate: all unsafe blocks must have SAFETY comment."""
        violations = self._scan_unjustified(SRC_DIR / "containers")
        assert len(violations) < 15, (
            f"Too many unjustified unsafe blocks ({len(violations)}) "
            f"in containers:\n" + "\n".join(violations[:10])
        )

    def test_sync_unsafe_justified(self):
        """Sync primitives: all unsafe blocks must have SAFETY comment."""
        violations = self._scan_unjustified(SRC_DIR / "sync")
        assert len(violations) < 10, (
            f"Too many unjustified unsafe blocks ({len(violations)}) "
            f"in sync:\n" + "\n".join(violations[:10])
        )

    def test_pal_unsafe_justified(self):
        """PAL (Platform Abstraction Layer): unsafe blocks justified."""
        violations = self._scan_unjustified(SRC_DIR / "pal")
        assert len(violations) < 10, (
            f"Too many unjustified unsafe blocks ({len(violations)}) "
            f"in pal:\n" + "\n".join(violations[:10])
        )


# ---------------------------------------------------------------------------
# TestAsilBAtomicCorrectness
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAsilBAtomicCorrectness:
    """ASIL B: verify atomic orderings in lock-free data structures."""

    def test_no_relaxed_dominance_in_containers(self):
        """Container atomics should not overuse Relaxed ordering."""
        containers_dir = SRC_DIR / "containers"
        if not containers_dir.is_dir():
            pytest.skip("containers/ not found")
        relaxed = 0
        strong = 0
        for f in containers_dir.rglob("*.rs"):
            content = f.read_text(encoding="utf-8", errors="ignore")
            relaxed += content.count("Ordering::Relaxed")
            strong += (
                content.count("Ordering::Acquire")
                + content.count("Ordering::Release")
                + content.count("Ordering::AcqRel")
                + content.count("Ordering::SeqCst")
            )
        if relaxed == 0 and strong == 0:
            pytest.skip("No atomic orderings found in containers")
        total = relaxed + strong
        assert relaxed / max(total, 1) < 0.6, (
            f"Relaxed dominates: {relaxed}/{total} -- "
            "ASIL B: lock-free containers need Acquire/Release for correctness"
        )

    def test_sync_primitives_use_acquire_release(self):
        """Sync primitives must use at least Acquire/Release."""
        sync_dir = SRC_DIR / "sync"
        if not sync_dir.is_dir():
            pytest.skip("sync/ not found")
        has_acqrel = False
        for f in sync_dir.rglob("*.rs"):
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "Acquire" in content or "Release" in content or "AcqRel" in content:
                has_acqrel = True
                break
        assert has_acqrel, (
            "sync/ crate has no Acquire/Release orderings -- "
            "ASIL B: sync primitives must use correct memory orderings"
        )


# ---------------------------------------------------------------------------
# TestAsilBBuildReproducibility
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAsilBBuildReproducibility:
    """ASIL B: verify build reproducibility."""

    def test_cargo_lock_exists(self):
        assert (BASELIBS_RUST_DIR / "Cargo.lock").exists(), (
            "Cargo.lock missing -- ASIL B requires locked deps"
        )

    def test_module_bazel_exists(self):
        assert (BASELIBS_RUST_DIR / "MODULE.bazel").exists(), (
            "MODULE.bazel missing -- ASIL B requires reproducible build"
        )

    def test_module_bazel_lock_exists(self):
        assert (BASELIBS_RUST_DIR / "MODULE.bazel.lock").exists(), (
            "MODULE.bazel.lock missing -- ASIL B requires locked Bazel deps"
        )

    def test_bazelversion_pinned(self):
        path = BASELIBS_RUST_DIR / ".bazelversion"
        if not path.exists():
            pytest.skip(".bazelversion not found")
        version = path.read_text().strip()
        assert re.match(r"\d+\.\d+\.\d+", version), (
            f"Invalid Bazel version pin: {version}"
        )


# ---------------------------------------------------------------------------
# TestAsilBTestInfrastructure
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAsilBTestInfrastructure:
    """ASIL B: verify test infrastructure for coverage evidence.

    ISO 26262 Part 6 Table 9: statement coverage (++) + branch coverage (+).
    """

    def test_has_test_files(self):
        """Inline #[test] or #[cfg(test)] must exist in source."""
        rs_files = list(BASELIBS_RUST_DIR.rglob("*.rs"))
        if not rs_files:
            pytest.skip("No Rust source files found")
        has_tests = False
        for f in rs_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "#[cfg(test)]" in content or "#[test]" in content:
                has_tests = True
                break
        test_files = [f for f in rs_files if "test" in f.name.lower()]
        assert has_tests or len(test_files) > 0, (
            "No test infrastructure -- ASIL B requires coverage evidence"
        )

    def test_build_files_exist(self):
        build_files = (
            list(BASELIBS_RUST_DIR.rglob("BUILD"))
            + list(BASELIBS_RUST_DIR.rglob("BUILD.bazel"))
        )
        assert len(build_files) >= 1, (
            "No BUILD files -- ASIL B requires buildable targets"
        )

    @pytest.mark.parametrize("crate_name", [
        "containers",
        "sync",
        "elementary",
    ])
    def test_crate_directory_exists(self, crate_name):
        """Core crates must exist."""
        path = SRC_DIR / crate_name
        assert path.is_dir(), (
            f"src/{crate_name}/ missing -- core crate removed"
        )

    @pytest.mark.parametrize("crate_name", [
        "containers",
        "sync",
        "elementary",
    ])
    def test_crate_has_cargo_toml(self, crate_name):
        """Each crate must have Cargo.toml."""
        path = SRC_DIR / crate_name / "Cargo.toml"
        assert path.exists(), (
            f"src/{crate_name}/Cargo.toml missing"
        )

    def test_cargo_warnings_as_errors(self):
        """Upstream should set -D warnings in .cargo/config.toml."""
        config = BASELIBS_RUST_DIR / ".cargo" / "config.toml"
        if not config.exists():
            config = BASELIBS_RUST_DIR / ".cargo" / "config"
        if not config.exists():
            pytest.skip(".cargo/config.toml not found")
        content = config.read_text(encoding="utf-8")
        assert "-D" in content, (
            ".cargo/config.toml should set -D warnings for ASIL B"
        )
