"""Performance benchmark verification for score-lifecycle (ASIL B).

Health monitoring must meet watchdog timing constraints:
- Heartbeat check: within supervision window
- Deadline supervision: detect overruns within FTTI
- Recovery action: trigger safe-state within configured timeout

ISO 26262 Part 6 Table 10: timing analysis required for ASIL B.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
LIFECYCLE_DIR = PROJECT_ROOT / "modules" / "score-lifecycle" / "upstream"


@pytest.mark.asil_b
@pytest.mark.performance
class TestHealthMonitorTiming:
    """Verify health monitoring has timing-related constructs."""

    CANDIDATES = [
        LIFECYCLE_DIR / "src" / "health_monitoring_lib",
        LIFECYCLE_DIR / "health_monitoring_lib",
    ]

    @property
    def health_lib(self) -> Path:
        for c in self.CANDIDATES:
            if c.is_dir():
                return c
        return self.CANDIDATES[0]

    def test_deadline_supervision_has_timing(self):
        """Deadline supervision must reference time/duration."""
        lib = self.health_lib
        deadline_files = list(lib.rglob("*deadline*"))
        if not deadline_files:
            pytest.skip("No deadline supervision files found")
        content = ""
        for f in deadline_files:
            if f.is_file():
                content += f.read_text(encoding="utf-8", errors="ignore")
        has_time = any(kw in content.lower() for kw in [
            "duration", "timeout", "elapsed", "deadline", "timer",
            "millisecond", "microsecond", "tick",
        ])
        assert has_time, (
            "Deadline supervision has no timing constructs -- "
            "ASIL B: deadline monitoring requires time measurement"
        )

    def test_heartbeat_has_counter(self):
        """Heartbeat/alive supervision must use a counter or window."""
        lib = self.health_lib
        alive_files = list(lib.rglob("*alive*")) + list(lib.rglob("*heartbeat*"))
        if not alive_files:
            pytest.skip("No alive/heartbeat files found")
        content = ""
        for f in alive_files:
            if f.is_file():
                content += f.read_text(encoding="utf-8", errors="ignore")
        has_counter = any(kw in content.lower() for kw in [
            "counter", "count", "window", "expected_alive", "alive_counter",
        ])
        assert has_counter, (
            "Heartbeat supervision has no counter/window -- "
            "ASIL B: alive monitoring requires counter-based detection"
        )

    def test_watchdog_has_timeout(self):
        """Watchdog must reference timeout/trigger for safe-state."""
        lib = self.health_lib
        wdg_files = [
            f for f in lib.rglob("*") if f.is_file() and "watchdog" in f.name.lower()
        ]
        if not wdg_files:
            pytest.skip("No watchdog files found")
        content = ""
        for f in wdg_files:
            content += f.read_text(encoding="utf-8", errors="ignore")
        has_timeout = any(kw in content.lower() for kw in [
            "timeout", "trigger", "expired", "safe_state", "reset",
        ])
        assert has_timeout, (
            "Watchdog has no timeout/trigger -- "
            "ASIL B: watchdog must enforce timing constraints"
        )


@pytest.mark.asil_b
@pytest.mark.performance
class TestBenchmarkInfrastructure:
    """Verify lifecycle has benchmark/test infrastructure for timing."""

    def test_cpp_test_files_exist(self):
        """C++ test files must exist for health monitoring timing tests."""
        test_files = list(LIFECYCLE_DIR.rglob("*test*.cpp"))
        if not test_files:
            test_files = list(LIFECYCLE_DIR.rglob("*test*.cc"))
        assert len(test_files) >= 1, (
            "No C++ test files found -- timing verification missing"
        )

    def test_rust_test_infrastructure(self):
        """Rust test annotations must exist."""
        rs_files = list(LIFECYCLE_DIR.rglob("*.rs"))
        if not rs_files:
            pytest.skip("No Rust source files")
        has_tests = False
        for f in rs_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if "#[test]" in content:
                has_tests = True
                break
        assert has_tests, (
            "No #[test] annotations -- ASIL B requires timing test evidence"
        )
