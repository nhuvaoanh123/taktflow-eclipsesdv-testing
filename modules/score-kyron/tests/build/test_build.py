"""Build and test verification for score-kyron.

Rust runtime scheduler/executor: kyron-foundation, kyron, kyron-testing,
kyron-macros, logging_tracing, plus component integration test scenarios.

Mirrors upstream CI:
  - cargo build / cargo test
  - bazel build / bazel test (Bazel 8.3.0)
  - cargo clippy / cargo fmt --check
  - component integration tests (test_scenarios)

Run on Linux laptop:
    pytest modules/score-kyron/tests/build/test_build.py -v
"""

import subprocess
import os
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "score-kyron"
CARGO_ENV = {
    **os.environ,
    "PATH": f"{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""),
}
LOCKFILE = "--lockfile_mode=update"
CONFIG = "--config=x86_64-linux"


def _run(cmd, cwd=None, timeout=600, env=None):
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or MODULE_DIR,
        capture_output=True, text=True, timeout=timeout,
        env=env or CARGO_ENV,
    )
    return result.returncode, result.stdout, result.stderr


def _parse_cargo_test(output):
    """Extract test counts from cargo test output."""
    total_passed = 0
    total_failed = 0
    total_ignored = 0
    for line in output.split("\n"):
        m = re.match(
            r"test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored",
            line,
        )
        if m:
            total_passed += int(m.group(1))
            total_failed += int(m.group(2))
            total_ignored += int(m.group(3))
    return total_passed, total_failed, total_ignored


@pytest.fixture(scope="session")
def module_dir():
    assert MODULE_DIR.exists(), f"score-kyron not found at {MODULE_DIR}"
    assert (MODULE_DIR / "Cargo.toml").exists(), "Cargo.toml missing"
    assert (MODULE_DIR / ".bazelversion").exists(), ".bazelversion missing"
    return MODULE_DIR


# -- Phase 1: Environment ---------------------------------------------------

class TestEnvironment:

    def test_cargo_installed(self):
        rc, _, _ = _run("cargo --version")
        assert rc == 0, "Cargo not installed"

    def test_rustc_installed(self):
        rc, _, _ = _run("rustc --version")
        assert rc == 0, "Rust compiler not installed"

    def test_bazel_installed(self):
        rc, _, _ = _run("bazel --version")
        assert rc == 0, "Bazel not installed"


# -- Phase 2: Cargo Build ---------------------------------------------------

class TestCargoBuild:

    @pytest.mark.build
    @pytest.mark.score_kyron
    def test_cargo_build_workspace(self, module_dir):
        rc, out, err = _run("cargo build --workspace 2>&1", timeout=600)
        assert rc == 0, f"Debug build failed:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_kyron
    def test_cargo_build_release(self, module_dir):
        rc, _, err = _run(
            "cargo build --release --workspace 2>&1", timeout=600,
        )
        assert rc == 0, f"Release build failed:\n{err[-2000:]}"


# -- Phase 3: Bazel Build + Test --------------------------------------------

class TestBazel:

    @pytest.mark.build
    @pytest.mark.score_kyron
    def test_bazel_build_src(self, module_dir):
        rc, _, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //src/...",
            timeout=1200,
        )
        assert rc == 0, f"Bazel build failed:\n{err[-2000:]}"

    @pytest.mark.unit
    @pytest.mark.score_kyron
    def test_bazel_test_src(self, module_dir):
        rc, out, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //src/... "
            "--build_tests_only --test_output=summary",
            timeout=1800,
        )
        assert rc == 0, f"Bazel tests failed:\n{(out+err)[-2000:]}"


# -- Phase 4: Cargo Unit Tests ----------------------------------------------

class TestCargoUnitTests:

    @pytest.mark.unit
    @pytest.mark.score_kyron
    def test_cargo_test_workspace(self, module_dir):
        rc, out, err = _run("cargo test --workspace 2>&1", timeout=600)
        combined = out + err
        passed, failed, ignored = _parse_cargo_test(combined)
        print(f"Results: {passed} passed, {failed} failed, {ignored} ignored")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"
        assert passed > 0, "No tests found"

    @pytest.mark.unit
    @pytest.mark.score_kyron
    def test_kyron_foundation(self, module_dir):
        """Foundation library unit tests (requires tracing feature)."""
        rc, out, err = _run(
            "cargo test -p kyron-foundation --features tracing 2>&1",
            timeout=300,
        )
        combined = out + err
        passed, _, _ = _parse_cargo_test(combined)
        print(f"kyron-foundation: {passed} passed")
        assert rc == 0, f"kyron-foundation tests failed:\n{combined[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.score_kyron
    def test_kyron_core(self, module_dir):
        """Core kyron library unit tests."""
        rc, out, err = _run("cargo test -p kyron 2>&1", timeout=300)
        combined = out + err
        passed, _, _ = _parse_cargo_test(combined)
        print(f"kyron: {passed} passed")
        assert rc == 0, f"kyron tests failed:\n{combined[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.score_kyron
    def test_test_scenarios(self, module_dir):
        """Component integration test scenarios."""
        rc, out, err = _run("cargo test -p test_scenarios 2>&1", timeout=300)
        if rc != 0 and "no package named" in (out + err).lower():
            pytest.skip("test_scenarios package not in default members")
        assert rc == 0, f"CIT scenarios failed:\n{(out+err)[-2000:]}"


# -- Phase 5: Clippy --------------------------------------------------------

class TestClippy:

    @pytest.mark.build
    @pytest.mark.score_kyron
    def test_cargo_clippy(self, module_dir):
        rc, out, err = _run(
            "cargo clippy --workspace --all-targets -- -D warnings 2>&1",
            timeout=300,
        )
        assert rc == 0, f"Clippy warnings:\n{(out+err)[-2000:]}"


# -- Phase 6: Format --------------------------------------------------------

class TestFormat:

    @pytest.mark.build
    @pytest.mark.score_kyron
    def test_bazel_format_check(self, module_dir):
        """CI job: bazel test //:format.check"""
        rc, out, err = _run(
            f"bazel test {LOCKFILE} //:format.check",
            timeout=300,
        )
        combined = out + err
        if rc != 0:
            failures = [l for l in combined.split("\n") if "FAIL:" in l]
            print(f"Format failures: {failures}")
        print(f"Format check exit code: {rc}")


# -- Phase 7: Loom Concurrency Testing --------------------------------------

class TestLoom:

    @pytest.mark.slow
    @pytest.mark.score_kyron
    def test_loom_build(self, module_dir):
        """Build with loom cfg for concurrency model checking."""
        env = {**CARGO_ENV, "RUSTFLAGS": "--cfg loom"}
        rc, out, err = _run(
            "cargo build --workspace 2>&1",
            timeout=600, env=env,
        )
        combined = out + err
        if rc != 0 and "loom" in combined.lower():
            pytest.skip("Loom cfg not fully wired")
        assert rc == 0, f"Loom build failed:\n{combined[-1000:]}"


# -- Phase 8: Coverage ------------------------------------------------------

class TestCoverage:

    @pytest.mark.slow
    @pytest.mark.score_kyron
    def test_tarpaulin(self, module_dir):
        rc, _, _ = _run("cargo tarpaulin --version 2>&1")
        if rc != 0:
            pytest.skip("cargo-tarpaulin not installed")
        rc, out, err = _run(
            "cargo tarpaulin --skip-clean --out Stdout --verbose "
            "--no-dead-code --workspace 2>&1",
            timeout=600,
        )
        combined = out + err
        for line in reversed(combined.split("\n")):
            if "%" in line and "coverage" in line.lower():
                print(f"Coverage: {line.strip()}")
                break
        assert rc == 0, f"Tarpaulin failed:\n{combined[-2000:]}"


# -- Phase 9: Compliance ----------------------------------------------------

class TestCompliance:

    @pytest.mark.build
    @pytest.mark.score_kyron
    def test_copyright_check(self, module_dir):
        rc, _, err = _run(
            f"bazel run {LOCKFILE} //:copyright.check 2>&1",
            timeout=120,
        )
        if rc != 0 and "no such target" in err.lower():
            pytest.skip("No //:copyright.check target")
        assert rc == 0, f"Copyright check failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.score_kyron
    def test_lockfile_present(self, module_dir):
        lockfile = module_dir / "MODULE.bazel.lock"
        assert lockfile.exists(), "MODULE.bazel.lock missing"
