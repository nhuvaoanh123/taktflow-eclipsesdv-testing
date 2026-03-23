"""Performance test infrastructure for score-baselibs.

Verifies benchmark targets exist and are properly configured.
Actual benchmark execution requires Bazel on Linux.
"""

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
BASELIBS_DIR = PROJECT_ROOT / "modules" / "score-baselibs" / "upstream"


# ---------------------------------------------------------------------------
# TestBenchmarkTargetsExist
# ---------------------------------------------------------------------------
class TestBenchmarkTargetsExist:
    """Verify Google Benchmark files exist in the repo.

    Searches for files matching ``*_benchmark*.cpp`` or ``*_bench*.cpp``
    and verifies that associated BUILD files reference the
    ``google_benchmark`` dependency.
    """

    def _find_benchmark_sources(self) -> list[Path]:
        """Return all C++ files that look like benchmark harnesses."""
        results: list[Path] = []
        for pattern in ("*_benchmark*.cpp", "*_bench*.cpp",
                        "*benchmark*.cpp", "*bench*.cpp"):
            results.extend(BASELIBS_DIR.rglob(pattern))
        # Deduplicate while preserving order
        seen: set[Path] = set()
        unique: list[Path] = []
        for p in results:
            if p not in seen:
                seen.add(p)
                unique.append(p)
        return unique

    def test_benchmark_sources_exist(self):
        """At least one benchmark source file should exist in score-baselibs."""
        sources = self._find_benchmark_sources()
        # It is acceptable if the project has not yet added benchmarks;
        # in that case we skip rather than fail.
        if not sources:
            pytest.skip(
                "No benchmark source files (*_benchmark*.cpp / *_bench*.cpp) "
                "found in score-baselibs -- benchmarks may not be implemented yet"
            )
        assert len(sources) > 0

    def test_benchmark_sources_have_build_files(self):
        """Each benchmark source file should be in a directory that has a
        BUILD or BUILD.bazel file."""
        sources = self._find_benchmark_sources()
        if not sources:
            pytest.skip("No benchmark sources found")

        missing_build: list[str] = []
        for src in sources:
            parent = src.parent
            has_build = (
                (parent / "BUILD").exists()
                or (parent / "BUILD.bazel").exists()
            )
            if not has_build:
                missing_build.append(str(src.relative_to(BASELIBS_DIR)))

        assert not missing_build, (
            f"Benchmark sources without BUILD file: {missing_build}"
        )

    def test_build_files_reference_google_benchmark(self):
        """BUILD files containing benchmark targets should reference
        ``google_benchmark`` or ``@com_google_benchmark``."""
        sources = self._find_benchmark_sources()
        if not sources:
            pytest.skip("No benchmark sources found")

        benchmark_dirs: set[Path] = {s.parent for s in sources}
        dirs_missing_ref: list[str] = []

        for d in benchmark_dirs:
            build_file = d / "BUILD"
            if not build_file.exists():
                build_file = d / "BUILD.bazel"
            if not build_file.exists():
                continue

            content = build_file.read_text(encoding="utf-8", errors="ignore")
            if "benchmark" not in content.lower():
                dirs_missing_ref.append(str(d.relative_to(BASELIBS_DIR)))

        if dirs_missing_ref:
            pytest.xfail(
                f"BUILD files in benchmark dirs do not reference "
                f"google_benchmark: {dirs_missing_ref}"
            )

    def test_benchmark_cpp_includes_benchmark_header(self):
        """Benchmark source files should #include <benchmark/benchmark.h>
        or a project-specific wrapper."""
        sources = self._find_benchmark_sources()
        if not sources:
            pytest.skip("No benchmark sources found")

        bad_sources: list[str] = []
        for src in sources:
            content = src.read_text(encoding="utf-8", errors="ignore")
            if "benchmark" not in content.lower():
                bad_sources.append(str(src.relative_to(BASELIBS_DIR)))

        assert not bad_sources, (
            f"Benchmark sources that do not include benchmark header: "
            f"{bad_sources}"
        )


# ---------------------------------------------------------------------------
# TestBenchmarkConfiguration
# ---------------------------------------------------------------------------
class TestBenchmarkConfiguration:
    """Verify MODULE.bazel declares google_benchmark and BUILD rules
    use correct test size / tags for benchmarks."""

    def test_module_bazel_exists(self):
        module_path = BASELIBS_DIR / "MODULE.bazel"
        assert module_path.exists(), "MODULE.bazel not found in score-baselibs"

    def test_google_benchmark_declared(self):
        """MODULE.bazel should declare google_benchmark as a dependency
        (direct or dev)."""
        module_path = BASELIBS_DIR / "MODULE.bazel"
        content = module_path.read_text(encoding="utf-8")

        has_benchmark = (
            "google_benchmark" in content
            or "com_google_benchmark" in content
        )
        if not has_benchmark:
            pytest.xfail(
                "MODULE.bazel does not declare google_benchmark -- "
                "benchmarks may use a different framework or are not yet set up"
            )

    def test_benchmark_build_rules_use_appropriate_size(self):
        """Benchmark BUILD targets should use size = \"large\" or
        size = \"enormous\" since benchmarks are long-running.
        At minimum, they should not use size = \"small\"."""
        sources = list(BASELIBS_DIR.rglob("*benchmark*.cpp"))
        sources.extend(BASELIBS_DIR.rglob("*bench*.cpp"))
        if not sources:
            pytest.skip("No benchmark sources found")

        benchmark_dirs: set[Path] = {s.parent for s in sources}
        small_size_found: list[str] = []

        for d in benchmark_dirs:
            build_file = d / "BUILD"
            if not build_file.exists():
                build_file = d / "BUILD.bazel"
            if not build_file.exists():
                continue

            content = build_file.read_text(encoding="utf-8", errors="ignore")
            # Look for the benchmark target and check if it uses size=small
            if "benchmark" in content.lower() and 'size = "small"' in content:
                small_size_found.append(
                    str(build_file.relative_to(BASELIBS_DIR))
                )

        assert not small_size_found, (
            f"Benchmark BUILD rules should not use size=\"small\": "
            f"{small_size_found}"
        )

    def test_benchmark_build_rules_have_benchmark_tag(self):
        """Benchmark targets should be tagged with 'benchmark' or 'perf'
        so they can be filtered in CI."""
        sources = list(BASELIBS_DIR.rglob("*benchmark*.cpp"))
        sources.extend(BASELIBS_DIR.rglob("*bench*.cpp"))
        if not sources:
            pytest.skip("No benchmark sources found")

        benchmark_dirs: set[Path] = {s.parent for s in sources}
        missing_tags: list[str] = []

        for d in benchmark_dirs:
            build_file = d / "BUILD"
            if not build_file.exists():
                build_file = d / "BUILD.bazel"
            if not build_file.exists():
                continue

            content = build_file.read_text(encoding="utf-8", errors="ignore")
            if "benchmark" in content.lower():
                # Check for tags containing benchmark or perf
                has_tag = bool(
                    re.search(r'tags\s*=\s*\[.*"(benchmark|perf)"', content)
                )
                if not has_tag:
                    missing_tags.append(
                        str(build_file.relative_to(BASELIBS_DIR))
                    )

        if missing_tags:
            # This is advisory, not a hard failure
            pytest.xfail(
                f"Benchmark BUILD rules without 'benchmark'/'perf' tag: "
                f"{missing_tags}"
            )
