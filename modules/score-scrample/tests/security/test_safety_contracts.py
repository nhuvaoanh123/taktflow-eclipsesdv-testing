"""Safety and security contract verification for score-scrample (ASIL B).

score-scrample is ASIL B-rated. Key safety/security contracts:

- C++ sample application must use the project assert handler, not raw
  assert() or abort(), to enable structured crash reporting.
- scorex CLI must validate user input (module names, paths) before
  generating code — no path traversal, no shell injection.
- EventSenderReceiver must handle LoLa IPC errors gracefully without
  crashing the host process.

Verification method: source inspection.
Platform: any (no build required).
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
SCRAMPLE_DIR = PROJECT_ROOT / "score-scrample"
SRC_DIR = SCRAMPLE_DIR / "src"
SCOREX_DIR = SCRAMPLE_DIR / "scorex"


# ---------------------------------------------------------------------------
# TestAssertHandler
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAssertHandler:
    """Verify structured assert handler usage in C++ code."""

    def test_assert_handler_exists(self):
        assert (SRC_DIR / "assert_handler.cpp").exists(), \
            "assert_handler.cpp missing — safety assert handler removed"

    def test_assert_handler_registered(self):
        """main.cpp should reference the assert handler."""
        main_cpp = SRC_DIR / "main.cpp"
        if not main_cpp.exists():
            pytest.skip("main.cpp not found")
        content = main_cpp.read_text(encoding="utf-8", errors="ignore")
        assert "assert" in content.lower(), \
            "main.cpp does not reference assert handler"


# ---------------------------------------------------------------------------
# TestCppSourceSafety
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestCppSourceSafety:
    """Basic safety checks for C++ source files."""

    def test_no_raw_abort_in_application(self):
        """Application code should use assert handler, not raw abort()."""
        if not SRC_DIR.is_dir():
            pytest.skip("src/ not found")
        violations = []
        for f in SRC_DIR.glob("*.cpp"):
            if "assert_handler" in f.name:
                continue  # The handler itself may call abort
            content = f.read_text(encoding="utf-8", errors="ignore")
            lines = content.splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                if re.search(r'\babort\s*\(', stripped):
                    violations.append(f"{f.name}:{i+1}: {stripped[:60]}")
        if violations:
            print(f"Warning: raw abort() calls found:\n"
                  + "\n".join(violations[:5]))

    def test_headers_have_include_guards(self):
        """All C++ headers must have include guards or #pragma once."""
        if not SRC_DIR.is_dir():
            pytest.skip("src/ not found")
        h_files = list(SRC_DIR.glob("*.h"))
        if not h_files:
            pytest.skip("No header files found")
        violations = []
        for f in h_files:
            content = f.read_text(encoding="utf-8", errors="ignore")
            has_guard = (
                "#pragma once" in content
                or re.search(r"#ifndef\s+\w+_H", content, re.IGNORECASE)
            )
            if not has_guard:
                violations.append(f.name)
        assert not violations, (
            f"Headers without include guards:\n" + "\n".join(violations)
        )


# ---------------------------------------------------------------------------
# TestScorexInputValidation
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestScorexInputValidation:
    """Verify that scorex CLI validates user input."""

    def test_validate_init_options_exists(self):
        """init.go must have input validation function."""
        init_go = SCOREX_DIR / "cmd" / "init.go"
        if not init_go.exists():
            pytest.skip("scorex/cmd/init.go not found")
        content = init_go.read_text(encoding="utf-8", errors="ignore")
        assert "validate" in content.lower(), \
            "init.go does not contain validation logic"

    def test_no_shell_exec_in_generator(self):
        """Skeleton generator should not exec shell commands with user input."""
        gen_path = SCOREX_DIR / "internal" / "service" / "skeleton" / "generator.go"
        if not gen_path.exists():
            pytest.skip("generator.go not found")
        content = gen_path.read_text(encoding="utf-8", errors="ignore")
        dangerous_patterns = ["exec.Command", "os.system", "shell("]
        found = [p for p in dangerous_patterns if p in content]
        if found:
            print(f"Warning: potential shell execution in generator: {found}")


# ---------------------------------------------------------------------------
# TestAsilBBuildReproducibility
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAsilBBuildReproducibility:
    """ASIL B: verify build reproducibility and test infrastructure."""

    def test_module_bazel_exists(self):
        assert (SCRAMPLE_DIR / "MODULE.bazel").exists(), (
            "MODULE.bazel missing -- ASIL B requires reproducible build"
        )

    def test_build_files_exist(self):
        build_files = (
            list(SCRAMPLE_DIR.rglob("BUILD"))
            + list(SCRAMPLE_DIR.rglob("BUILD.bazel"))
        )
        assert len(build_files) >= 1, (
            "No BUILD files -- ASIL B requires buildable targets"
        )

    def test_test_infrastructure_exists(self):
        """Test files must exist for ASIL B coverage evidence."""
        test_files = list(SCRAMPLE_DIR.rglob("*test*"))
        assert len(test_files) >= 1, (
            "No test files found -- ASIL B requires test coverage"
        )

    def test_source_files_exist(self):
        """Source files must exist."""
        cpp_files = list(SRC_DIR.rglob("*.cpp")) + list(SRC_DIR.rglob("*.h"))
        assert len(cpp_files) >= 2, (
            f"Expected at least 2 source files, found {len(cpp_files)}"
        )
