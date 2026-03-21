"""Bazel build/test utilities for S-CORE modules."""

import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def bazel_build(target, config=None, cwd=None, timeout=600):
    """Run bazel build and return (exit_code, stdout, stderr)."""
    cmd = f"bazel build {target}"
    if config:
        cmd += f" --config={config}"
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or PROJECT_ROOT,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def bazel_test(target, config=None, cwd=None, timeout=1800):
    """Run bazel test and return (exit_code, stdout, stderr)."""
    cmd = f"bazel test {target} --test_output=summary"
    if config:
        cmd += f" --config={config}"
    result = subprocess.run(
        cmd, shell=True, cwd=cwd or PROJECT_ROOT,
        capture_output=True, text=True, timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def parse_test_summary(output):
    """Parse Bazel test output for pass/fail counts."""
    for line in (output or "").split("\n"):
        if "Executed" in line and "tests" in line:
            # "Executed 252 out of 253 tests: 252 tests pass and 1 was skipped."
            parts = line.split()
            return {
                "executed": int(parts[1]) if len(parts) > 1 else 0,
                "total": int(parts[4]) if len(parts) > 4 else 0,
                "passed": int(parts[6]) if "pass" in line else 0,
            }
    return None
