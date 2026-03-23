#!/usr/bin/env bash
# =============================================================================
# score-lifecycle Regression Test
# Verifies build, C++/Rust tests, sanitizers, and code quality checks.
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIFECYCLE_DIR="$(dirname "$SCRIPT_DIR")/score-lifecycle"
PASS=0
FAIL=0
SKIP=0

check() {
    local name="$1" expected="$2" actual="$3"
    if echo "$actual" | grep -q "$expected"; then
        echo "  PASS: $name"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $name (expected '$expected')"
        FAIL=$((FAIL + 1))
    fi
}

skip() {
    local name="$1" reason="$2"
    echo "  SKIP: $name ($reason)"
    SKIP=$((SKIP + 1))
}

echo "=== score-lifecycle Regression Test ==="
echo "Date: $(date)"
echo "Lifecycle dir: $LIFECYCLE_DIR"
echo ""

# ---------------------------------------------------------------------------
# Pre-flight: verify toolchain
# ---------------------------------------------------------------------------
echo "--- Pre-flight ---"

if command -v bazel &>/dev/null; then
    BAZEL_VER=$(bazel --version 2>/dev/null | head -1)
    check "Bazel available" "bazel" "$BAZEL_VER"
else
    echo "  FAIL: bazel not found in PATH"
    FAIL=$((FAIL + 1))
    echo ""
    echo "=== Results ==="
    echo "PASS: $PASS  FAIL: $FAIL  SKIP: $SKIP  TOTAL: $((PASS + FAIL + SKIP))"
    echo "STATUS: ABORT (bazel not available)"
    exit 1
fi

if command -v cargo &>/dev/null; then
    CARGO_VER=$(cargo --version 2>/dev/null | head -1)
    check "Cargo available" "cargo" "$CARGO_VER"
else
    echo "  FAIL: cargo not found in PATH"
    FAIL=$((FAIL + 1))
    echo ""
    echo "=== Results ==="
    echo "PASS: $PASS  FAIL: $FAIL  SKIP: $SKIP  TOTAL: $((PASS + FAIL + SKIP))"
    echo "STATUS: ABORT (cargo not available)"
    exit 1
fi

if [ ! -d "$LIFECYCLE_DIR" ]; then
    echo "  FAIL: score-lifecycle directory not found at $LIFECYCLE_DIR"
    FAIL=$((FAIL + 1))
    echo ""
    echo "=== Results ==="
    echo "PASS: $PASS  FAIL: $FAIL  SKIP: $SKIP  TOTAL: $((PASS + FAIL + SKIP))"
    echo "STATUS: ABORT (source directory missing)"
    exit 1
fi

cd "$LIFECYCLE_DIR" || exit 1
echo ""

# ---------------------------------------------------------------------------
# 1. Build all (Bazel)
# ---------------------------------------------------------------------------
echo "--- Test: Full Build (//src/... //examples/...) ---"
BUILD_OUT=$(bazel build --config=x86_64-linux //src/... //examples/... 2>&1) || true
check "Full build completed" "Build completed" "$BUILD_OUT"
echo ""

# ---------------------------------------------------------------------------
# 2. Run C++ tests (Bazel)
# ---------------------------------------------------------------------------
echo "--- Test: C++ Tests (//src/...) ---"
CPP_OUT=$(bazel test --config=x86_64-linux //src/... 2>&1) || true
check "C++ tests passed" "PASSED" "$CPP_OUT"
echo ""

# ---------------------------------------------------------------------------
# 3. Run Rust tests (Cargo)
# ---------------------------------------------------------------------------
echo "--- Test: Rust Tests ---"
RUST_OUT=$(cargo test --features stub_supervisor_api_client 2>&1) || true
check "Rust tests passed" "test result: ok" "$RUST_OUT"
echo ""

# ---------------------------------------------------------------------------
# 4. Rust clippy
# ---------------------------------------------------------------------------
echo "--- Test: Rust Clippy ---"
if command -v cargo-clippy &>/dev/null || cargo clippy --version &>/dev/null; then
    CLIPPY_OUT=$(cargo clippy --all-features --all-targets -- -D warnings 2>&1) || true
    if echo "$CLIPPY_OUT" | grep -q "error"; then
        check "Clippy clean" "no warnings" "errors found"
    else
        check "Clippy clean" "clean" "clean"
    fi
else
    skip "Clippy" "clippy not installed"
fi
echo ""

# ---------------------------------------------------------------------------
# 5. AddressSanitizer (ASan)
# ---------------------------------------------------------------------------
echo "--- Test: AddressSanitizer (ASan) on //src/... ---"
ASAN_OUT=$(bazel test --config=x86_64-linux --define sanitize=address //src/... 2>&1) || true
if echo "$ASAN_OUT" | grep -q "PASSED"; then
    check "ASan on src" "clean" "clean"
elif echo "$ASAN_OUT" | grep -q "no test targets"; then
    skip "ASan on src" "no test targets found"
else
    check "ASan on src" "clean" "violations detected"
fi
echo ""

# ---------------------------------------------------------------------------
# 6. Format check
# ---------------------------------------------------------------------------
echo "--- Test: Format Check ---"
FORMAT_OUT=$(bazel test //:format.check 2>&1) || true
if echo "$FORMAT_OUT" | grep -q "PASSED"; then
    check "Format check" "clean" "clean"
elif echo "$FORMAT_OUT" | grep -q "no test targets\|does not exist"; then
    skip "Format check" "format.check target not found"
else
    check "Format check" "clean" "format issues detected"
fi
echo ""

# ---------------------------------------------------------------------------
# 7. Copyright check
# ---------------------------------------------------------------------------
echo "--- Test: Copyright Check ---"
COPYRIGHT_OUT=$(bazel run //:copyright.check 2>&1) || true
if echo "$COPYRIGHT_OUT" | grep -q "PASSED\|SUCCESS\|ok\|completed"; then
    check "Copyright check" "clean" "clean"
elif echo "$COPYRIGHT_OUT" | grep -q "does not exist"; then
    skip "Copyright check" "copyright.check target not found"
else
    check "Copyright check" "clean" "copyright issues detected"
fi
echo ""

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo "==========================================="
echo "=== Results ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"
echo "SKIP: $SKIP"
echo "TOTAL: $((PASS + FAIL + SKIP))"
echo "==========================================="

if [ "$FAIL" -eq 0 ]; then
    echo "STATUS: ALL PASS"
    exit 0
else
    echo "STATUS: $FAIL FAILURE(S)"
    exit 1
fi
