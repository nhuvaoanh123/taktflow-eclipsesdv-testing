"""End-to-end stack integration tests for score-baselibs (ASIL B).

Verifies that score-baselibs provides all interfaces needed for the
full SDV stack (communication, lifecycle, logging, FEO) to function.

Platform: any (file inspection only).
"""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
BASELIBS_DIR = PROJECT_ROOT / "modules" / "score-baselibs" / "upstream"
SCORE_DIR = BASELIBS_DIR / "score"


@pytest.mark.asil_b
@pytest.mark.e2e
class TestFullStackDependencies:
    """Verify baselibs provides all interfaces for the SDV stack."""

    REQUIRED_COMPONENTS = [
        ("os", "OS abstraction for platform independence"),
        ("memory", "Memory management for shared/unique resources"),
        ("concurrency", "Thread-safe primitives for multi-core"),
        ("result", "Error handling without exceptions"),
    ]

    @pytest.mark.parametrize(
        "component, desc",
        REQUIRED_COMPONENTS,
        ids=[c[0] for c in REQUIRED_COMPONENTS],
    )
    def test_component_exists(self, component, desc):
        path = SCORE_DIR / component
        assert path.is_dir(), (
            f"score/{component}/ missing -- {desc}"
        )

    @pytest.mark.parametrize(
        "component, desc",
        REQUIRED_COMPONENTS,
        ids=[c[0] for c in REQUIRED_COMPONENTS],
    )
    def test_component_has_headers(self, component, desc):
        path = SCORE_DIR / component
        if not path.is_dir():
            pytest.skip(f"{component}/ not found")
        h_files = list(path.rglob("*.h"))
        assert len(h_files) >= 1, (
            f"score/{component}/ has no headers -- public API removed"
        )

    def test_language_safecpp_exists(self):
        """SafeC++ patterns (noexcept, safe_math, aborts_upon_exception)."""
        safecpp = SCORE_DIR / "language" / "safecpp"
        assert safecpp.is_dir(), "language/safecpp/ missing -- safety patterns removed"
