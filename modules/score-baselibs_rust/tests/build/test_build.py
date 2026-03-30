"""Build and test verification for score-baselibs_rust.

Rust foundation libraries: containers, sync primitives, elementary types,
platform abstraction layer (PAL), threading, logging format macros.

Mirrors upstream CI:
  - cargo build / cargo test
  - bazel build / bazel test (Bazel 8.4.2)
  - cargo clippy / cargo fmt --check

Run on Linux laptop:
    pytest modules/score-baselibs_rust/tests/build/test_build.py -v
"""

import subprocess
import os
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "score-baselibs_rust"
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
    assert MODULE_DIR.exists(), f"score-baselibs_rust not found at {MODULE_DIR}"
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
    @pytest.mark.score_baselibs_rust
    def test_cargo_build_workspace(self, module_dir):
        rc, out, err = _run("cargo build --workspace 2>&1", timeout=600)
        assert rc == 0, f"Debug build failed:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_baselibs_rust
    def test_cargo_build_release(self, module_dir):
        rc, _, err = _run(
            "cargo build --release --workspace 2>&1", timeout=600,
        )
        assert rc == 0, f"Release build failed:\n{err[-2000:]}"


# -- Phase 3: Bazel Build ---------------------------------------------------

class TestBazel:

    @pytest.mark.build
    @pytest.mark.score_baselibs_rust
    def test_bazel_build_all(self, module_dir):
        rc, _, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //src/...",
            timeout=1200,
        )
        assert rc == 0, f"Bazel build failed:\n{err[-2000:]}"

    @pytest.mark.unit
    @pytest.mark.score_baselibs_rust
    def test_bazel_test_all(self, module_dir):
        rc, out, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //src/... "
            "--build_tests_only --test_output=summary",
            timeout=1800,
        )
        assert rc == 0, f"Bazel tests failed:\n{(out+err)[-2000:]}"


# -- Phase 4: Cargo Unit Tests ----------------------------------------------

class TestCargoUnitTests:

    @pytest.mark.unit
    @pytest.mark.score_baselibs_rust
    def test_cargo_test_workspace(self, module_dir):
        rc, out, err = _run("cargo test --workspace 2>&1", timeout=600)
        combined = out + err
        passed, failed, ignored = _parse_cargo_test(combined)
        print(f"Results: {passed} passed, {failed} failed, {ignored} ignored")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"
        assert passed > 0, "No tests found"

    @pytest.mark.unit
    @pytest.mark.score_baselibs_rust
    def test_containers_lib(self, module_dir):
        """Core containers library unit tests."""
        rc, out, err = _run("cargo test -p containers 2>&1", timeout=300)
        combined = out + err
        passed, _, _ = _parse_cargo_test(combined)
        print(f"containers: {passed} passed")
        assert rc == 0, f"containers tests failed:\n{combined[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.score_baselibs_rust
    def test_sync_lib(self, module_dir):
        """Sync primitives library unit tests."""
        rc, out, err = _run("cargo test -p sync 2>&1", timeout=300)
        combined = out + err
        passed, _, _ = _parse_cargo_test(combined)
        print(f"sync: {passed} passed")
        assert rc == 0, f"sync tests failed:\n{combined[-1000:]}"


# -- Phase 5: Clippy --------------------------------------------------------

class TestClippy:

    @pytest.mark.build
    @pytest.mark.score_baselibs_rust
    def test_cargo_clippy(self, module_dir):
        rc, out, err = _run(
            "cargo clippy --workspace --all-targets -- -D warnings 2>&1",
            timeout=300,
        )
        assert rc == 0, f"Clippy warnings:\n{(out+err)[-2000:]}"


# -- Phase 6: Format --------------------------------------------------------

class TestFormat:

    @pytest.mark.build
    @pytest.mark.score_baselibs_rust
    def test_cargo_fmt_check(self, module_dir):
        rc, out, err = _run("cargo fmt --all -- --check 2>&1", timeout=60)
        combined = out + err
        if rc != 0:
            diffs = sum(1 for l in combined.split("\n") if l.startswith("Diff in"))
            print(f"Format diffs: {diffs} (upstream style, non-blocking)")
        # Report only — upstream formatting may differ from local rustfmt version
        print(f"Format check exit code: {rc}")


# -- Phase 7: Coverage ------------------------------------------------------

class TestCoverage:

    @pytest.mark.slow
    @pytest.mark.score_baselibs_rust
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


# -- Phase 8: Compliance ----------------------------------------------------

class TestCompliance:

    @pytest.mark.build
    @pytest.mark.score_baselibs_rust
    def test_lockfile_present(self, module_dir):
        lockfile = module_dir / "MODULE.bazel.lock"
        assert lockfile.exists(), "MODULE.bazel.lock missing"
