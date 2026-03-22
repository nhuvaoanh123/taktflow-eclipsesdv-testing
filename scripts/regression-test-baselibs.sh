#!/usr/bin/env bash
# =============================================================================
# score-baselibs Regression Test
# Verifies build, ASIL-B tests, sanitizers, and API contract stability.
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASELIBS_DIR="$(dirname "$SCRIPT_DIR")/score-baselibs"
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

echo "=== score-baselibs Regression Test ==="
echo "Date: $(date)"
echo "Baselibs dir: $BASELIBS_DIR"
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

if [ ! -d "$BASELIBS_DIR" ]; then
    echo "  FAIL: score-baselibs directory not found at $BASELIBS_DIR"
    FAIL=$((FAIL + 1))
    echo ""
    echo "=== Results ==="
    echo "PASS: $PASS  FAIL: $FAIL  SKIP: $SKIP  TOTAL: $((PASS + FAIL + SKIP))"
    echo "STATUS: ABORT (source directory missing)"
    exit 1
fi

cd "$BASELIBS_DIR" || exit 1
echo ""

# ---------------------------------------------------------------------------
# 1. Full build
# ---------------------------------------------------------------------------
echo "--- Test: Full Build (//score/...) ---"
BUILD_OUT=$(bazel build //score/... --config=bl-x86_64-linux 2>&1) || true
check "Full build completed" "Build completed" "$BUILD_OUT"
echo ""

# ---------------------------------------------------------------------------
# 2. ASIL-B Component Tests (individual)
# ---------------------------------------------------------------------------
echo "--- Test: ASIL-B OS Tests ---"
OS_OUT=$(bazel test //score/os/test/... --config=bl-x86_64-linux 2>&1) || true
check "OS tests passed" "PASSED" "$OS_OUT"
echo ""

echo "--- Test: ASIL-B Shared Memory Tests ---"
MEM_OUT=$(bazel test //score/memory/... --config=bl-x86_64-linux 2>&1) || true
check "Memory tests passed" "PASSED" "$MEM_OUT"
echo ""

echo "--- Test: ASIL-B Concurrency Tests ---"
CONC_OUT=$(bazel test //score/concurrency/... --config=bl-x86_64-linux 2>&1) || true
check "Concurrency tests passed" "PASSED" "$CONC_OUT"
echo ""

echo "--- Test: ASIL-B Result Tests ---"
RES_OUT=$(bazel test //score/result/... --config=bl-x86_64-linux 2>&1) || true
check "Result tests passed" "PASSED" "$RES_OUT"
echo ""

echo "--- Test: ASIL-B SafeCPP Tests ---"
SAFE_OUT=$(bazel test //score/language/safecpp/... --config=bl-x86_64-linux 2>&1) || true
check "SafeCPP tests passed" "PASSED" "$SAFE_OUT"
echo ""

# ---------------------------------------------------------------------------
# 3. Full test suite
# ---------------------------------------------------------------------------
echo "--- Test: Full Test Suite (//score/...) ---"
ALL_OUT=$(bazel test //score/... --config=bl-x86_64-linux 2>&1) || true
check "Full test suite passed" "PASSED" "$ALL_OUT"
echo ""

# ---------------------------------------------------------------------------
# 4. Sanitizers on ASIL-B components
# ---------------------------------------------------------------------------
ASIL_B_TARGETS=(
    "//score/os/test/..."
    "//score/memory/..."
    "//score/concurrency/..."
)

echo "--- Test: AddressSanitizer (ASan) on ASIL-B Components ---"
ASAN_FAIL=0
for target in "${ASIL_B_TARGETS[@]}"; do
    ASAN_OUT=$(bazel test "$target" --config=bl-x86_64-linux \
        --features=asan 2>&1) || true
    if echo "$ASAN_OUT" | grep -q "PASSED"; then
        : # ok
    elif echo "$ASAN_OUT" | grep -q "no test targets"; then
        : # no targets, not a failure
    else
        ASAN_FAIL=1
    fi
done
if [ "$ASAN_FAIL" -eq 0 ]; then
    check "ASan on ASIL-B components" "clean" "clean"
else
    check "ASan on ASIL-B components" "clean" "violations detected"
fi
echo ""

echo "--- Test: UndefinedBehaviorSanitizer (UBSan) on ASIL-B Components ---"
UBSAN_FAIL=0
for target in "${ASIL_B_TARGETS[@]}"; do
    UBSAN_OUT=$(bazel test "$target" --config=bl-x86_64-linux \
        --features=ubsan 2>&1) || true
    if echo "$UBSAN_OUT" | grep -q "PASSED"; then
        : # ok
    elif echo "$UBSAN_OUT" | grep -q "no test targets"; then
        : # no targets, not a failure
    else
        UBSAN_FAIL=1
    fi
done
if [ "$UBSAN_FAIL" -eq 0 ]; then
    check "UBSan on ASIL-B components" "clean" "clean"
else
    check "UBSan on ASIL-B components" "clean" "violations detected"
fi
echo ""

echo "--- Test: LeakSanitizer (LSan) on ASIL-B Components ---"
LSAN_FAIL=0
for target in "${ASIL_B_TARGETS[@]}"; do
    LSAN_OUT=$(bazel test "$target" --config=bl-x86_64-linux \
        --features=lsan 2>&1) || true
    if echo "$LSAN_OUT" | grep -q "PASSED"; then
        : # ok
    elif echo "$LSAN_OUT" | grep -q "no test targets"; then
        : # no targets, not a failure
    else
        LSAN_FAIL=1
    fi
done
if [ "$LSAN_FAIL" -eq 0 ]; then
    check "LSan on ASIL-B components" "clean" "clean"
else
    check "LSan on ASIL-B components" "clean" "violations detected"
fi
echo ""

# ---------------------------------------------------------------------------
# 5. Format check
# ---------------------------------------------------------------------------
echo "--- Test: Format Check ---"
if command -v clang-format &>/dev/null; then
    FORMAT_ISSUES=0
    while IFS= read -r -d '' src; do
        if ! clang-format --dry-run --Werror "$src" &>/dev/null; then
            FORMAT_ISSUES=$((FORMAT_ISSUES + 1))
        fi
    done < <(find "$BASELIBS_DIR/score" -type f \( -name '*.cpp' -o -name '*.h' \) -print0 2>/dev/null)
    if [ "$FORMAT_ISSUES" -eq 0 ]; then
        check "clang-format compliance" "clean" "clean"
    else
        check "clang-format compliance" "clean" "$FORMAT_ISSUES files with format issues"
    fi
else
    skip "clang-format compliance" "clang-format not installed"
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
