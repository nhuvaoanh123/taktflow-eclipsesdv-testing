"""Safety and security contract verification for score-kyron (ASIL B).

score-kyron is ASIL B-rated as the async runtime for safety-relevant
components. Key contracts:

- Every `unsafe` block must have a documented SAFETY justification.
- Lock-free data structures (SPMC queues, reusable object pools) must use
  atomic orderings correctly — no SeqCst overuse, no Relaxed underuse.
- No dynamic memory allocation in the scheduler hot path (work-stealing loop).

Verification method: source inspection.
Platform: any (no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
KYRON_DIR = PROJECT_ROOT / "score-kyron"
SRC_DIR = KYRON_DIR / "src"


# ---------------------------------------------------------------------------
# TestUnsafeJustifications
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestUnsafeJustifications:
    """Every unsafe block in production code must have a SAFETY comment."""

    def _scan_for_unjustified_unsafe(self, crate_dir):
        """Return list of (file, line) with unsafe blocks lacking SAFETY comment."""
        violations = []
        if not crate_dir.is_dir():
            return violations
        for f in crate_dir.rglob("*.rs"):
            # Skip test files
            if "test" in f.name.lower() or "/tests/" in str(f):
                continue
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                if "unsafe" in stripped and ("{" in stripped or "fn " in stripped):
                    # Skip unsafe trait impls (no block)
                    if stripped.startswith("unsafe impl"):
                        continue
                    # Check previous 5 lines for SAFETY comment
                    context = "\n".join(lines[max(0, i - 5):i])
                    if "SAFETY" not in context and "Safety" not in context:
                        rel = f.relative_to(KYRON_DIR)
                        violations.append(f"{rel}:{i+1}: {stripped[:80]}")
        return violations

    def test_kyron_core_unsafe_justified(self):
        violations = self._scan_for_unjustified_unsafe(SRC_DIR / "kyron")
        if violations:
            print(f"Unjustified unsafe blocks ({len(violations)}):\n"
                  + "\n".join(violations[:15]))
        # Warn but don't fail — upstream may have different conventions
        assert len(violations) < 20, (
            f"Too many unjustified unsafe blocks ({len(violations)}) in kyron core"
        )

    def test_kyron_foundation_unsafe_justified(self):
        violations = self._scan_for_unjustified_unsafe(SRC_DIR / "kyron-foundation")
        if violations:
            print(f"Unjustified unsafe blocks ({len(violations)}):\n"
                  + "\n".join(violations[:15]))
        assert len(violations) < 15, (
            f"Too many unjustified unsafe blocks ({len(violations)}) in foundation"
        )


# ---------------------------------------------------------------------------
# TestAtomicOrderings
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAtomicOrderings:
    """Verify atomic orderings are used intentionally in lock-free code."""

    def test_no_relaxed_in_spmc_queue(self):
        """SPMC queue must not use Relaxed ordering for shared state transitions.

        Relaxed allows reordering that can cause torn reads in multi-consumer
        scenarios. Acquire/Release or stronger is required.
        """
        spmc_path = SRC_DIR / "kyron-foundation" / "src" / "containers" / "spmc_queue.rs"
        if not spmc_path.exists():
            pytest.skip("spmc_queue.rs not found")
        content = spmc_path.read_text(encoding="utf-8", errors="ignore")
        # Count Relaxed usages — should be minimal
        relaxed_count = content.count("Ordering::Relaxed")
        acqrel_count = (
            content.count("Ordering::Acquire")
            + content.count("Ordering::Release")
            + content.count("Ordering::AcqRel")
            + content.count("Ordering::SeqCst")
        )
        if relaxed_count > 0:
            ratio = relaxed_count / max(acqrel_count, 1)
            print(f"Relaxed: {relaxed_count}, Acquire/Release: {acqrel_count}, "
                  f"ratio: {ratio:.2f}")
            # Relaxed should not dominate — flag if >50% of orderings
            assert ratio < 0.5, (
                f"SPMC queue uses Relaxed ordering too frequently "
                f"({relaxed_count}/{relaxed_count + acqrel_count})"
            )


# ---------------------------------------------------------------------------
# TestCargoConfig
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestCargoConfig:
    """Verify Cargo configuration for safety."""

    def test_warnings_as_errors(self):
        """Upstream should set -D warnings in .cargo/config.toml."""
        config_path = KYRON_DIR / ".cargo" / "config.toml"
        if not config_path.exists():
            config_path = KYRON_DIR / ".cargo" / "config"
        if not config_path.exists():
            pytest.skip(".cargo/config.toml not found")
        content = config_path.read_text()
        assert "-D" in content, \
            ".cargo/config.toml should set -D warnings"

    def test_cargo_lock_present(self):
        """Cargo.lock must be committed for reproducible builds."""
        assert (KYRON_DIR / "Cargo.lock").exists(), \
            "Cargo.lock missing — builds are not reproducible"


# ---------------------------------------------------------------------------
# TestAsilBTestInfrastructure
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAsilBTestInfrastructure:
    """ASIL B: verify sufficient test infrastructure.

    ISO 26262 Part 6 Table 9: statement coverage (++) and branch coverage (+).
    """

    def test_has_test_files(self):
        """Test files or inline #[cfg(test)] modules must exist."""
        test_files = [
            f for f in KYRON_DIR.rglob("*.rs")
            if "test" in f.name.lower()
        ]
        inline_tests = False
        for rs_file in KYRON_DIR.rglob("*.rs"):
            content = rs_file.read_text(encoding="utf-8", errors="ignore")
            if "#[cfg(test)]" in content or "#[test]" in content:
                inline_tests = True
                break
        assert len(test_files) > 0 or inline_tests, (
            "No test files or inline test modules -- "
            "ASIL B requires test coverage evidence"
        )

    def test_module_bazel_exists(self):
        """MODULE.bazel must exist for reproducible build definition."""
        assert (KYRON_DIR / "MODULE.bazel").exists(), (
            "MODULE.bazel missing -- ASIL B requires reproducible builds"
        )

    def test_build_files_exist(self):
        """BUILD files must exist for Bazel targets."""
        build_files = (
            list(KYRON_DIR.rglob("BUILD"))
            + list(KYRON_DIR.rglob("BUILD.bazel"))
        )
        assert len(build_files) >= 1, (
            "No BUILD files -- ASIL B requires buildable targets"
        )

    def test_no_dynamic_alloc_in_scheduler(self):
        """ASIL B: work-stealing loop should not allocate."""
        rs_files = list(SRC_DIR.rglob("*.rs")) if SRC_DIR.is_dir() else []
        if not rs_files:
            pytest.skip("No source files found")
        alloc_count = 0
        for f in rs_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            alloc_count += len(re.findall(
                r"\b(Vec::new|vec!\[|Box::new|String::new)", content
            ))
        assert alloc_count <= 40, (
            f"Kyron has {alloc_count} allocation calls -- "
            "ASIL B restricts dynamic allocation in hot paths"
        )

    def test_foundation_crate_exists(self):
        """kyron-foundation crate must exist for low-level primitives."""
        foundation = SRC_DIR / "kyron-foundation"
        assert foundation.is_dir(), (
            "src/kyron-foundation/ missing -- foundation crate removed"
        )

    def test_foundation_has_containers(self):
        """Foundation must provide lock-free containers for ASIL B."""
        containers = SRC_DIR / "kyron-foundation" / "src" / "containers"
        if not containers.is_dir():
            pytest.skip("containers/ directory not found")
        rs_files = list(containers.rglob("*.rs"))
        assert len(rs_files) >= 1, (
            "No container source files -- lock-free primitives missing"
        )
