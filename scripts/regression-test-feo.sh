#!/usr/bin/env bash
# =============================================================================
# FEO (Fixed Execution Order) Regression Test
# Builds, tests, lints, and formats score-feo, then summarizes results.
# Requires: Bazel 8.3.0, Rust toolchain (edition 2024), Linux x86_64
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FEO_DIR="$(dirname "$SCRIPT_DIR")/score-feo"
RESULTS_DIR="$(dirname "$SCRIPT_DIR")/taktflow-eclipsesdv-testing/results/feo"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
LOG_DIR="$RESULTS_DIR/test-reports"

PASS=0
FAIL=0
SKIP=0

mkdir -p "$LOG_DIR"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
section() {
    echo ""
    echo "================================================================="
    echo "  $1"
    echo "================================================================="
    echo ""
}

check() {
    local name="$1" exit_code="$2"
    if [ "$exit_code" -eq 0 ]; then
        echo "  PASS: $name"
        PASS=$((PASS + 1))
    elif [ "$exit_code" -eq 77 ]; then
        echo "  SKIP: $name"
        SKIP=$((SKIP + 1))
    else
        echo "  FAIL: $name (exit code: $exit_code)"
        FAIL=$((FAIL + 1))
    fi
}

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
section "Pre-flight Checks"

if [ ! -d "$FEO_DIR" ]; then
    echo "ERROR: score-feo directory not found at $FEO_DIR"
    exit 1
fi

echo "  FEO_DIR: $FEO_DIR"
echo "  Date: $(date)"
echo "  Host: $(hostname)"

if [ -f "$FEO_DIR/MODULE.bazel" ]; then
    echo "  MODULE.bazel: found"
    check "MODULE.bazel exists" 0
else
    echo "  MODULE.bazel: NOT FOUND"
    check "MODULE.bazel exists" 1
fi

if [ -f "$FEO_DIR/Cargo.toml" ]; then
    echo "  Cargo.toml: found"
    check "Cargo.toml exists" 0
else
    echo "  Cargo.toml: NOT FOUND"
    check "Cargo.toml exists" 1
fi

# Check Bazel version
if command -v bazel &> /dev/null; then
    BAZEL_VERSION=$(bazel --version 2>/dev/null | head -1)
    echo "  Bazel: $BAZEL_VERSION"
    check "Bazel available" 0
else
    echo "  Bazel: NOT FOUND"
    check "Bazel available" 1
    echo "SKIP: Cannot proceed without Bazel"
    SKIP=$((SKIP + 4))
    # Jump to summary
    section "Summary"
    echo "PASS: $PASS"
    echo "FAIL: $FAIL"
    echo "SKIP: $SKIP"
    echo "TOTAL: $((PASS + FAIL + SKIP))"
    exit 1
fi

# ---------------------------------------------------------------------------
# Step 1: Build
# ---------------------------------------------------------------------------
section "Step 1: Bazel Build (--config=x86_64-linux)"

BUILD_LOG="$LOG_DIR/build-$TIMESTAMP.log"
echo "  Log: $BUILD_LOG"

cd "$FEO_DIR"
bazel build --config=x86_64-linux //... 2>&1 | tee "$BUILD_LOG"
BUILD_EXIT=${PIPESTATUS[0]}

check "bazel build //..." $BUILD_EXIT

if [ $BUILD_EXIT -eq 0 ]; then
    ACTION_COUNT=$(grep -c "action" "$BUILD_LOG" 2>/dev/null || echo "unknown")
    echo "  Actions: $ACTION_COUNT"
fi

# ---------------------------------------------------------------------------
# Step 2: Test
# ---------------------------------------------------------------------------
section "Step 2: Bazel Test (--config=x86_64-linux)"

TEST_LOG="$LOG_DIR/test-$TIMESTAMP.log"
echo "  Log: $TEST_LOG"

bazel test --config=x86_64-linux //... 2>&1 | tee "$TEST_LOG"
TEST_EXIT=${PIPESTATUS[0]}

check "bazel test //..." $TEST_EXIT

# Extract test counts from Bazel output
TESTS_PASSED=$(grep -oP '\d+ test\(s\) passed' "$TEST_LOG" 2>/dev/null || echo "")
TESTS_FAILED=$(grep -oP '\d+ test\(s\) failed' "$TEST_LOG" 2>/dev/null || echo "")
echo "  Passed: ${TESTS_PASSED:-unknown}"
echo "  Failed: ${TESTS_FAILED:-none}"

# ---------------------------------------------------------------------------
# Step 3: Lint (Rust)
# ---------------------------------------------------------------------------
section "Step 3: Rust Lint (--config=lint-rust)"

LINT_LOG="$LOG_DIR/lint-$TIMESTAMP.log"
echo "  Log: $LINT_LOG"

bazel build --config=lint-rust //... 2>&1 | tee "$LINT_LOG"
LINT_EXIT=${PIPESTATUS[0]}

check "bazel build --config=lint-rust //..." $LINT_EXIT

if [ $LINT_EXIT -eq 0 ]; then
    WARNING_COUNT=$(grep -ciE "warning|clippy" "$LINT_LOG" 2>/dev/null || echo "0")
    echo "  Warnings: $WARNING_COUNT"
fi

# ---------------------------------------------------------------------------
# Step 4: Format check (optional -- may not have rustfmt config)
# ---------------------------------------------------------------------------
section "Step 4: Format Check"

if command -v cargo &> /dev/null; then
    FMT_LOG="$LOG_DIR/fmt-$TIMESTAMP.log"
    echo "  Log: $FMT_LOG"

    cd "$FEO_DIR"
    cargo fmt --check 2>&1 | tee "$FMT_LOG"
    FMT_EXIT=${PIPESTATUS[0]}

    check "cargo fmt --check" $FMT_EXIT
else
    echo "  SKIP: cargo not available"
    check "cargo fmt --check" 77
fi

# ---------------------------------------------------------------------------
# Step 5: Workspace verification
# ---------------------------------------------------------------------------
section "Step 5: Workspace Verification"

# Count workspace members
if [ -f "$FEO_DIR/Cargo.toml" ]; then
    MEMBER_COUNT=$(grep -c '"' "$FEO_DIR/Cargo.toml" 2>/dev/null || echo "0")
    echo "  Cargo.toml member lines: $MEMBER_COUNT"
fi

# Count crate directories
CRATE_DIRS=0
for crate in feo feo-com feo-time feo-tracing feo-tracer feo-cpp-build feo-cpp-macros perfetto-model; do
    if [ -d "$FEO_DIR/src/$crate" ]; then
        CRATE_DIRS=$((CRATE_DIRS + 1))
    fi
done
echo "  Crate directories found: $CRATE_DIRS / 8"
if [ $CRATE_DIRS -ge 8 ]; then
    check "All 8 crate directories exist" 0
else
    check "All 8 crate directories exist" 1
fi

# Check examples
for example in mini-adas cycle-benchmark; do
    if [ -d "$FEO_DIR/examples/rust/$example" ] || [ -d "$FEO_DIR/examples/$example" ]; then
        check "Example $example exists" 0
    else
        check "Example $example exists" 1
    fi
done

# Check CI workflows
CI_COUNT=$(ls "$FEO_DIR/.github/workflows/"*.yml 2>/dev/null | wc -l || echo "0")
echo "  CI workflows found: $CI_COUNT"
if [ "$CI_COUNT" -ge 1 ]; then
    check "CI workflows exist" 0
else
    check "CI workflows exist" 1
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
section "Summary"

echo "Date: $(date)"
echo "FEO_DIR: $FEO_DIR"
echo ""
echo "PASS: $PASS"
echo "FAIL: $FAIL"
echo "SKIP: $SKIP"
echo "TOTAL: $((PASS + FAIL + SKIP))"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "STATUS: ALL PASS (${SKIP} skipped)"
    exit 0
else
    echo "STATUS: $FAIL FAILURES"
    exit 1
fi
