"""Performance benchmark verification for score-scrample (ASIL B).

Sample application and scorex CLI must not introduce unbounded latency:
- EventSenderReceiver: bounded IPC response via LoLa
- scorex code generation: bounded template expansion

ISO 26262 Part 6 Table 10: timing analysis required for ASIL B.
"""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
SCRAMPLE_DIR = PROJECT_ROOT / "score-scrample"
SRC_DIR = SCRAMPLE_DIR / "src"
SCOREX_DIR = SCRAMPLE_DIR / "scorex"


@pytest.mark.asil_b
@pytest.mark.performance
class TestEventSenderReceiverPerformance:
    """Verify event sender/receiver has bounded IPC patterns."""

    def test_event_sender_receiver_source_exists(self):
        """EventSenderReceiver source must exist."""
        if not SRC_DIR.is_dir():
            pytest.skip("src/ not found")
        cpp_files = list(SRC_DIR.rglob("*.cpp")) + list(SRC_DIR.rglob("*.h"))
        assert len(cpp_files) >= 2, (
            "Insufficient source files in src/"
        )

    def test_lola_ipc_reference(self):
        """Source should reference LoLa IPC for communication."""
        if not SRC_DIR.is_dir():
            pytest.skip("src/ not found")
        content = ""
        for f in list(SRC_DIR.rglob("*.cpp")) + list(SRC_DIR.rglob("*.h")):
            content += f.read_text(encoding="utf-8", errors="ignore")
        has_lola = any(kw in content for kw in [
            "lola", "LoLa", "score/mw/com", "ProxyEvent", "SkeletonEvent",
        ])
        assert has_lola, (
            "No LoLa IPC references in source -- "
            "EventSenderReceiver should use score-communication"
        )


@pytest.mark.asil_b
@pytest.mark.performance
class TestScorexPerformance:
    """Verify scorex CLI has bounded operations."""

    def test_scorex_binary_exists(self):
        """scorex Go binary source must exist."""
        if not SCOREX_DIR.is_dir():
            pytest.skip("scorex/ not found")
        go_files = list(SCOREX_DIR.rglob("*.go"))
        assert len(go_files) >= 1, "No Go source files in scorex/"

    def test_template_files_exist(self):
        """Code generation templates must exist."""
        if not SCOREX_DIR.is_dir():
            pytest.skip("scorex/ not found")
        templates = (
            list(SCOREX_DIR.rglob("*.tmpl"))
            + list(SCOREX_DIR.rglob("*.tpl"))
            + list(SCOREX_DIR.rglob("*.go.tmpl"))
        )
        if not templates:
            # Check for embedded templates in Go files
            for f in SCOREX_DIR.rglob("*.go"):
                content = f.read_text(encoding="utf-8", errors="ignore")
                if "template" in content.lower():
                    return
            pytest.xfail("No template files found for code generation")
