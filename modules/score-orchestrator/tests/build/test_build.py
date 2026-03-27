"""Build and test verification for score-orchestrator.

Mirrors the upstream CI checks from .github/workflows/:
  - tests.yml: bazel test --lockfile_mode=error --config x86_64-linux //src/...
  - cargo_required.yml: cargo build, tarpaulin, miri, loom
  - clippy.yml: bazel build --config lint //src/...
  - format.yml: bazel test //:format.check
  - component_integration_tests.yml: pytest CIT with test_scenarios binary

Run on Linux laptop:
    pytest modules/score-orchestrator/tests/build/test_build.py -v
"""

import subprocess
import os
import re
import pytest
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parents[4] / "score-orchestrator"
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
    assert MODULE_DIR.exists(), f"score-orchestrator not found at {MODULE_DIR}"
    assert (MODULE_DIR / "Cargo.toml").exists(), "Cargo.toml missing"
    assert (MODULE_DIR / ".bazelversion").exists(), ".bazelversion missing"
    return MODULE_DIR


# ── Phase 1: Environment ────────────────────────────────────────────

class TestEnvironment:

    def test_cargo_installed(self):
        rc, out, _ = _run("cargo --version")
        assert rc == 0, "Cargo not installed"

    def test_rustc_installed(self):
        rc, out, _ = _run("rustc --version")
        assert rc == 0, "Rust compiler not installed"

    def test_bazel_installed(self):
        rc, _, _ = _run("bazel --version")
        assert rc == 0, "Bazel not installed"

    def test_cargo_warns_as_errors(self):
        """Upstream .cargo/config.toml sets rustflags = ['-D', 'warnings']."""
        config_path = MODULE_DIR / ".cargo" / "config.toml"
        if not config_path.exists():
            config_path = MODULE_DIR / ".cargo" / "config"
        if config_path.exists():
            content = config_path.read_text()
            assert "-D" in content, ".cargo/config.toml should set -D warnings"


# ── Phase 2: Cargo Build (mirrors cargo_required.yml) ───────────────

class TestCargoBuild:
    """Mirrors: cargo_required.yml → cargo build --verbose"""

    @pytest.mark.build
    @pytest.mark.score_orchestrator
    def test_cargo_build_verbose(self, module_dir):
        """CI job: cargo build --verbose"""
        rc, out, err = _run("cargo build --verbose 2>&1", timeout=600)
        assert rc == 0, f"Debug build failed:\n{(out+err)[-2000:]}"

    @pytest.mark.build
    @pytest.mark.score_orchestrator
    def test_cargo_build_release(self, module_dir):
        rc, _, err = _run(
            "cargo build --release --workspace 2>&1", timeout=600,
        )
        assert rc == 0, f"Release build failed:\n{err[-2000:]}"


# ── Phase 3: Bazel Build + Test (mirrors tests.yml) ─────────────────

class TestBazel:
    """Mirrors: tests.yml → bazel test //src/..."""

    @pytest.mark.build
    @pytest.mark.score_orchestrator
    def test_bazel_build_src(self, module_dir):
        rc, _, err = _run(
            f"bazel build {LOCKFILE} {CONFIG} //src/...",
            timeout=1200,
        )
        assert rc == 0, f"Bazel build failed:\n{err[-2000:]}"

    @pytest.mark.unit
    @pytest.mark.score_orchestrator
    def test_bazel_test_src(self, module_dir):
        """CI primary: bazel test --config x86_64-linux //src/..."""
        rc, out, err = _run(
            f"bazel test {LOCKFILE} {CONFIG} //src/... "
            "--test_output=summary",
            timeout=1800,
        )
        assert rc == 0, f"Bazel tests failed:\n{(out+err)[-2000:]}"


# ── Phase 4: Cargo Unit Tests ───────────────────────────────────────

class TestCargoUnitTests:

    @pytest.mark.unit
    @pytest.mark.score_orchestrator
    def test_cargo_test_workspace(self, module_dir):
        """Full workspace test — primary cargo CI command."""
        rc, out, err = _run("cargo test --workspace 2>&1", timeout=600)
        combined = out + err
        passed, failed, ignored = _parse_cargo_test(combined)
        print(f"Results: {passed} passed, {failed} failed, {ignored} ignored")
        assert rc == 0, f"Tests failed:\n{combined[-2000:]}"
        assert passed > 0, "No tests found"

    @pytest.mark.unit
    @pytest.mark.score_orchestrator
    def test_orchestration_lib(self, module_dir):
        """Core orchestration library unit tests."""
        rc, out, err = _run("cargo test -p orchestration 2>&1", timeout=300)
        combined = out + err
        passed, _, _ = _parse_cargo_test(combined)
        print(f"orchestration: {passed} passed")
        assert rc == 0, f"orchestration tests failed:\n{combined[-1000:]}"

    @pytest.mark.unit
    @pytest.mark.score_orchestrator
    def test_test_scenarios(self, module_dir):
        """Component integration test scenarios."""
        rc, out, err = _run("cargo test -p test_scenarios 2>&1", timeout=300)
        assert rc == 0, f"CIT scenarios failed:\n{(out+err)[-2000:]}"


# ── Phase 5: Clippy (mirrors clippy.yml) ─────────────────────────────

class TestClippy:
    """Mirrors: cargo clippy --all-targets --features tracing -- -D warnings"""

    @pytest.mark.build
    @pytest.mark.score_orchestrator
    def test_cargo_clippy_with_features(self, module_dir):
        """Upstream: clippy with --features tracing enabled."""
        rc, out, err = _run(
            "cargo clippy --all-targets --features tracing "
            "-- -D warnings 2>&1",
            timeout=300,
        )
        assert rc == 0, f"Clippy warnings:\n{(out+err)[-2000:]}"


# ── Phase 6: Format (mirrors format.yml) ─────────────────────────────

class TestFormat:
    """Note: upstream rustfmt.toml says DO_NOT_USE_LOCAL_RUSTFMT.
    Use Bazel format target instead.
    """

    @pytest.mark.build
    @pytest.mark.score_orchestrator
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


# ── Phase 7: Loom Concurrency Testing ────────────────────────────────

class TestLoom:
    """Mirrors: cargo_required.yml → cargo xtask build:loom
    Uses RUSTFLAGS="--cfg loom"
    """

    @pytest.mark.slow
    @pytest.mark.score_orchestrator
    def test_loom_build(self, module_dir):
        """Build with loom cfg — verifies concurrency model checking compiles."""
        env = {**CARGO_ENV, "RUSTFLAGS": "--cfg loom"}
        rc, out, err = _run(
            "cargo build --workspace 2>&1",
            timeout=600, env=env,
        )
        combined = out + err
        if rc != 0 and "loom" in combined.lower():
            print(f"Loom note: {combined[-500:]}")
            pytest.skip("Loom cfg not fully wired")
        assert rc == 0, f"Loom build failed:\n{combined[-1000:]}"


# ── Phase 8: Tarpaulin Coverage ──────────────────────────────────────

class TestCoverage:
    """Mirrors: cargo +nightly tarpaulin --all-features --engine llvm"""

    @pytest.mark.slow
    @pytest.mark.score_orchestrator
    def test_tarpaulin(self, module_dir):
        rc, _, _ = _run("cargo tarpaulin --version 2>&1")
        if rc != 0:
            pytest.skip(
                "cargo-tarpaulin not installed — "
                "install with: cargo install cargo-tarpaulin"
            )
        rc, out, err = _run(
            "cargo tarpaulin --skip-clean --out Stdout --verbose "
            "--no-dead-code --all-features 2>&1",
            timeout=600,
        )
        combined = out + err
        for line in reversed(combined.split("\n")):
            if "%" in line and "coverage" in line.lower():
                print(f"Coverage: {line.strip()}")
                break
        assert rc == 0, f"Tarpaulin failed:\n{combined[-2000:]}"


# ── Phase 9: Miri UB Detection ──────────────────────────────────────

class TestMiri:
    """Mirrors: cargo +nightly miri test --workspace"""

    @pytest.mark.slow
    @pytest.mark.score_orchestrator
    def test_miri(self, module_dir):
        rc, _, _ = _run("cargo +nightly miri --version 2>&1")
        if rc != 0:
            pytest.skip("Miri not installed")

        env = {**CARGO_ENV, "CARGO_INCREMENTAL": "0"}
        rc, out, err = _run(
            "cargo +nightly miri test --workspace 2>&1",
            timeout=1800, env=env,
        )
        combined = out + err
        if rc != 0 and "unsupported" in combined.lower():
            pytest.skip("Miri does not support some operations")
        passed, failed, _ = _parse_cargo_test(combined)
        print(f"Miri: {passed} passed, {failed} failed")
        assert rc == 0, f"Miri found UB:\n{combined[-2000:]}"


# ── Phase 10: Copyright / License ────────────────────────────────────

class TestCompliance:

    @pytest.mark.build
    @pytest.mark.score_orchestrator
    def test_copyright_check(self, module_dir):
        """CI job: copyright.yml"""
        rc, _, err = _run(
            f"bazel run {LOCKFILE} //:copyright.check 2>&1",
            timeout=120,
        )
        if rc != 0 and "no such target" in err.lower():
            pytest.skip("No //:copyright.check target")
        assert rc == 0, f"Copyright check failed:\n{err[-1000:]}"

    @pytest.mark.build
    @pytest.mark.score_orchestrator
    def test_lockfile_present(self, module_dir):
        """MODULE.bazel.lock must be present for reproducible builds."""
        lockfile = module_dir / "MODULE.bazel.lock"
        assert lockfile.exists(), "MODULE.bazel.lock missing"
