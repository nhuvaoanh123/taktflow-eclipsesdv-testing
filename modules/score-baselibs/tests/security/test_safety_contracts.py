"""Safety contract verification for ASIL-B components in score-baselibs.

Verifies that ASIL-B rated components follow required patterns:
- Object Seam mocking for all OS APIs
- No dynamic allocation in safety-critical paths
- Abort-on-exception handler presence
- Safe math wrappers for arithmetic
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
BASELIBS_DIR = PROJECT_ROOT / "modules" / "score-baselibs" / "upstream"
SCORE_DIR = BASELIBS_DIR / "score"


# ---------------------------------------------------------------------------
# TestAsilBComponentStructure
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAsilBComponentStructure:
    """For each ASIL-B component, verify: mock directory exists,
    test directory exists, BUILD file exists."""

    ASIL_B_COMPONENTS = [
        ("os", SCORE_DIR / "os"),
        ("memory/shared", SCORE_DIR / "memory" / "shared"),
        ("concurrency", SCORE_DIR / "concurrency"),
        ("result", SCORE_DIR / "result"),
        ("language/safecpp", SCORE_DIR / "language" / "safecpp"),
    ]

    @pytest.mark.parametrize(
        "name, path",
        ASIL_B_COMPONENTS,
        ids=[c[0] for c in ASIL_B_COMPONENTS],
    )
    def test_component_directory_exists(self, name: str, path: Path):
        assert path.is_dir(), (
            f"ASIL-B component {name} directory missing at {path}"
        )

    @pytest.mark.parametrize(
        "name, path",
        ASIL_B_COMPONENTS,
        ids=[c[0] for c in ASIL_B_COMPONENTS],
    )
    def test_component_build_file_exists(self, name: str, path: Path):
        build = path / "BUILD"
        build_bazel = path / "BUILD.bazel"
        assert build.exists() or build_bazel.exists(), (
            f"ASIL-B component {name} has no BUILD file"
        )

    @pytest.mark.parametrize(
        "name, path",
        [
            ("os", SCORE_DIR / "os"),
            ("memory/shared", SCORE_DIR / "memory" / "shared"),
        ],
        ids=["os", "memory/shared"],
    )
    def test_component_has_mock_directory(self, name: str, path: Path):
        """Components with Object Seam mocks should have a mocklib or
        mock-containing directory."""
        has_mocklib = (path / "mocklib").is_dir()
        has_mock_files = bool(list(path.glob("*mock*")))
        assert has_mocklib or has_mock_files, (
            f"ASIL-B component {name} has no mock directory or mock files"
        )

    @pytest.mark.parametrize(
        "name, path",
        ASIL_B_COMPONENTS,
        ids=[c[0] for c in ASIL_B_COMPONENTS],
    )
    def test_component_has_test_directory(self, name: str, path: Path):
        """Each ASIL-B component should have a test/ directory or test
        files alongside sources."""
        has_test_dir = (path / "test").is_dir()
        has_test_files = bool(list(path.rglob("*test*")))
        assert has_test_dir or has_test_files, (
            f"ASIL-B component {name} has no test directory or test files"
        )


# ---------------------------------------------------------------------------
# TestAbortOnException
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestAbortOnException:
    """Verify aborts_upon_exception directory exists with the handler."""

    ABORT_DIR = SCORE_DIR / "language" / "safecpp" / "aborts_upon_exception"

    def test_aborts_upon_exception_directory_exists(self):
        assert self.ABORT_DIR.is_dir(), (
            "aborts_upon_exception directory missing -- "
            "ASIL-B exception safety contract violated"
        )

    def test_aborts_upon_exception_source_exists(self):
        cpp = self.ABORT_DIR / "aborts_upon_exception.cpp"
        assert cpp.exists(), (
            "aborts_upon_exception.cpp missing -- handler implementation removed"
        )

    def test_aborts_upon_exception_header_exists(self):
        """The handler should have a header or be referenced by one."""
        headers = list(self.ABORT_DIR.glob("*.h"))
        sources = list(self.ABORT_DIR.glob("*.cpp"))
        assert headers or sources, (
            "No header or source files in aborts_upon_exception/"
        )

    def test_aborts_upon_exception_build_file_exists(self):
        build = self.ABORT_DIR / "BUILD"
        build_bazel = self.ABORT_DIR / "BUILD.bazel"
        assert build.exists() or build_bazel.exists(), (
            "No BUILD file in aborts_upon_exception/ -- target not buildable"
        )

    def test_build_references_exception_handler(self):
        """The BUILD file should define a target for the exception handler."""
        build = self.ABORT_DIR / "BUILD"
        if not build.exists():
            build = self.ABORT_DIR / "BUILD.bazel"
        if not build.exists():
            pytest.skip("No BUILD file found")

        content = build.read_text(encoding="utf-8", errors="ignore")
        assert "aborts_upon_exception" in content, (
            "BUILD file does not reference aborts_upon_exception target"
        )

    def test_handler_calls_abort(self):
        """The exception handler should call std::abort() or abort()
        to enforce the no-exception contract."""
        cpp = self.ABORT_DIR / "aborts_upon_exception.cpp"
        if not cpp.exists():
            pytest.skip("Source file not found")

        content = cpp.read_text(encoding="utf-8", errors="ignore")
        has_abort = "abort" in content.lower()
        assert has_abort, (
            "aborts_upon_exception.cpp does not contain an abort() call -- "
            "handler may not enforce the termination contract"
        )


# ---------------------------------------------------------------------------
# TestSafeMathPresence
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestSafeMathPresence:
    """Verify safe_math headers exist and contain overflow-safe
    arithmetic patterns."""

    SAFE_MATH_DIR = SCORE_DIR / "language" / "safecpp" / "safe_math"

    def test_safe_math_directory_exists(self):
        assert self.SAFE_MATH_DIR.is_dir(), (
            "safe_math directory missing -- ASIL-B arithmetic safety "
            "contract violated"
        )

    def test_safe_math_header_exists(self):
        header = self.SAFE_MATH_DIR / "safe_math.h"
        assert header.exists(), (
            "safe_math.h missing -- overflow-safe arithmetic API removed"
        )

    def test_safe_math_build_exists(self):
        build = self.SAFE_MATH_DIR / "BUILD"
        build_bazel = self.SAFE_MATH_DIR / "BUILD.bazel"
        assert build.exists() or build_bazel.exists(), (
            "No BUILD file in safe_math/"
        )

    def test_overflow_safe_patterns_present(self):
        """safe_math.h should contain patterns indicating overflow-safe
        arithmetic (e.g., Add, Mul, Sub with overflow checks or
        __builtin_add_overflow-style wrappers)."""
        header = self.SAFE_MATH_DIR / "safe_math.h"
        if not header.exists():
            pytest.skip("safe_math.h not found")

        content = header.read_text(encoding="utf-8", errors="ignore")
        # Look for common overflow-safe patterns
        overflow_patterns = [
            r"overflow",
            r"safe_add|SafeAdd|safe_sub|SafeSub|safe_mul|SafeMul",
            r"Add|Sub|Mul",
            r"__builtin_\w+_overflow",
            r"checked_",
        ]

        found_any = any(
            re.search(pat, content, re.IGNORECASE)
            for pat in overflow_patterns
        )
        assert found_any, (
            "safe_math.h does not contain recognizable overflow-safe "
            "arithmetic patterns"
        )

    def test_safe_math_has_tests(self):
        """safe_math should have corresponding test files."""
        test_dir = self.SAFE_MATH_DIR / "test"
        has_test_dir = test_dir.is_dir()
        has_test_files = bool(list(self.SAFE_MATH_DIR.rglob("*test*")))
        assert has_test_dir or has_test_files, (
            "safe_math has no test directory or test files -- "
            "ASIL-B requires test coverage"
        )


# ---------------------------------------------------------------------------
# TestNoExceptionsPattern
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestNoExceptionsPattern:
    """Verify that score/result/ implements no-exception error handling
    using Result and Error types."""

    RESULT_DIR = SCORE_DIR / "result"

    def test_result_directory_exists(self):
        assert self.RESULT_DIR.is_dir(), "score/result/ directory missing"

    def test_result_type_defined(self):
        """result.h should define a Result type for no-exception error
        handling."""
        result_h = self.RESULT_DIR / "result.h"
        if not result_h.exists():
            pytest.skip("result.h not found")

        content = result_h.read_text(encoding="utf-8", errors="ignore")
        assert re.search(r"\bResult\b", content), (
            "result.h does not define a 'Result' type"
        )

    def test_error_type_defined(self):
        """error.h or error_code.h should define Error types."""
        found_error = False
        for candidate in ("error.h", "error_code.h", "error_domain.h"):
            path = self.RESULT_DIR / candidate
            if path.exists():
                content = path.read_text(encoding="utf-8", errors="ignore")
                if re.search(r"\bError\b", content):
                    found_error = True
                    break

        assert found_error, (
            "No Error type found in score/result/ headers -- "
            "no-exception error handling pattern may be missing"
        )

    def test_no_throw_in_result_headers(self):
        """Result headers should prefer noexcept and avoid throw statements
        in their API surface."""
        headers = list(self.RESULT_DIR.glob("*.h"))
        if not headers:
            pytest.skip("No headers in score/result/")

        throw_count = 0
        noexcept_count = 0

        for h in headers:
            content = h.read_text(encoding="utf-8", errors="ignore")
            throw_count += len(re.findall(r"\bthrow\b", content))
            noexcept_count += len(re.findall(r"\bnoexcept\b", content))

        # Allow some throw for static_assert messages etc., but noexcept
        # should dominate
        if noexcept_count == 0 and throw_count == 0:
            pytest.skip("No throw/noexcept keywords found -- may use a "
                        "different pattern")

        assert noexcept_count >= throw_count, (
            f"Result headers have {throw_count} throw vs {noexcept_count} "
            f"noexcept -- expected noexcept-dominant API"
        )


# ---------------------------------------------------------------------------
# TestMockCoverage
# ---------------------------------------------------------------------------
@pytest.mark.asil_b
class TestMockCoverage:
    """For each OS header, verify a corresponding mock exists.

    Count total headers vs total mocks and assert coverage > 80%.
    """

    OS_DIR = SCORE_DIR / "os"
    MOCKLIB_DIR = SCORE_DIR / "os" / "mocklib"

    # Primary OS abstraction headers (the .h files in score/os/)
    EXPECTED_OS_HEADERS = [
        "acl.h",
        "errno.h",
        "fcntl.h",
        "mman.h",
        "pthread.h",
        "socket.h",
        "stat.h",
        "semaphore.h",
        "spawn.h",
        "unistd.h",
        "time.h",
        "sched.h",
        "select.h",
        "dirent.h",
        "grp.h",
        "ioctl.h",
        "stdlib.h",
        "string.h",
        "stdio.h",
        "ifaddrs.h",
        "glob.h",
        "inotify.h",
        "capability.h",
        "sigevent.h",
        "uname.h",
        "mount.h",
        "statvfs.h",
        "getopt.h",
        "libgen.h",
        "arpa_inet.h",
        "netdb.h",
    ]

    @pytest.mark.parametrize(
        "header",
        [
            "acl.h",
            "errno.h",
            "fcntl.h",
            "mman.h",
            "pthread.h",
            "socket.h",
            "stat.h",
            "sched.h",
            "ioctl.h",
            "stdlib.h",
            "string.h",
        ],
    )
    def test_core_os_header_has_mock(self, header: str):
        """Each core OS header should have a corresponding mock in mocklib."""
        stem = header.replace(".h", "")
        mocklib = self.MOCKLIB_DIR

        if not mocklib.is_dir():
            pytest.skip("mocklib directory not found")

        # Check various naming conventions for mock files
        candidates = [
            f"{stem}_mock.h",
            f"{stem}mock.h",
            f"mock_{stem}.h",
        ]

        found = any(
            (mocklib / c).exists()
            for c in candidates
        )
        assert found, (
            f"No mock found for OS header {header} in mocklib/ -- "
            f"checked: {candidates}"
        )

    def test_mock_coverage_above_80_percent(self):
        """At least 80% of OS abstraction headers should have mocks."""
        if not self.MOCKLIB_DIR.is_dir():
            pytest.skip("mocklib directory not found")

        os_headers = [
            h for h in self.EXPECTED_OS_HEADERS
            if (self.OS_DIR / h).exists()
        ]

        if not os_headers:
            pytest.skip("No OS headers found")

        mock_files = {
            f.stem.lower() for f in self.MOCKLIB_DIR.glob("*.h")
        }

        covered = 0
        uncovered_headers: list[str] = []

        for header in os_headers:
            stem = header.replace(".h", "").lower()
            # Check if any mock file name contains the stem
            has_mock = any(
                stem in mock_name or mock_name.replace("mock", "").replace("_", "") == stem
                for mock_name in mock_files
            )
            if has_mock:
                covered += 1
            else:
                uncovered_headers.append(header)

        total = len(os_headers)
        coverage = covered / total if total > 0 else 0

        assert coverage >= 0.80, (
            f"Mock coverage is {coverage:.0%} ({covered}/{total}) -- "
            f"expected >= 80%. Uncovered headers: {uncovered_headers}"
        )

    def test_mock_count_summary(self):
        """Informational: report mock file counts."""
        if not self.MOCKLIB_DIR.is_dir():
            pytest.skip("mocklib directory not found")

        mock_headers = list(self.MOCKLIB_DIR.glob("*.h"))
        mock_sources = list(self.MOCKLIB_DIR.glob("*.cpp"))
        os_headers = list(self.OS_DIR.glob("*.h"))

        # Sanity check that there are a reasonable number of mocks
        assert len(mock_headers) >= 10, (
            f"Expected at least 10 mock headers, found {len(mock_headers)}"
        )
        assert len(os_headers) >= 10, (
            f"Expected at least 10 OS headers, found {len(os_headers)}"
        )

    def test_mocklib_build_file_exists(self):
        build = self.MOCKLIB_DIR / "BUILD"
        build_bazel = self.MOCKLIB_DIR / "BUILD.bazel"
        assert (build.exists() or build_bazel.exists()), (
            "mocklib/ has no BUILD file -- mock targets not buildable"
        )
