#!/usr/bin/env bash
# =============================================================================
# regression-test-persistency.sh
#
# Regression test runner for score-persistency (ASIL-D KVS library).
# Executes build, unit tests, integration tests, benchmarks, and quality checks.
#
# Usage:
#   ./scripts/regression-test-persistency.sh [PERSISTENCY_DIR]
#
# Environment:
#   PERSISTENCY_DIR   Path to score-persistency repo (default: ../score-persistency)
#   BAZEL_CONFIG      Bazel config to use (default: per-x86_64-linux)
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PERSISTENCY_DIR="${1:-${PERSISTENCY_DIR:-$(cd "$SCRIPT_DIR/.." && pwd)/score-persistency}}"
BAZEL_CONFIG="${BAZEL_CONFIG:---config=per-x86_64-linux}"

PASS=0
FAIL=0
SKIP=0
RESULTS=()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

log_info()  { echo -e "\033[1;34m[INFO]\033[0m  $*"; }
log_pass()  { echo -e "\033[1;32m[PASS]\033[0m  $*"; PASS=$((PASS + 1)); RESULTS+=("PASS: $*"); }
log_fail()  { echo -e "\033[1;31m[FAIL]\033[0m  $*"; FAIL=$((FAIL + 1)); RESULTS+=("FAIL: $*"); }
log_skip()  { echo -e "\033[1;33m[SKIP]\033[0m  $*"; SKIP=$((SKIP + 1)); RESULTS+=("SKIP: $*"); }
log_section() { echo -e "\n\033[1;36m========== $* ==========\033[0m"; }

run_step() {
    local description="$1"
    shift
    log_info "Running: $description"
    if "$@" 2>&1; then
        log_pass "$description"
        return 0
    else
        log_fail "$description"
        return 1
    fi
}

# ---------------------------------------------------------------------------
# 1. Pre-flight checks
# ---------------------------------------------------------------------------

log_section "PRE-FLIGHT CHECKS"

# Check bazel
if command -v bazel &>/dev/null; then
    log_pass "bazel found: $(bazel --version 2>/dev/null | head -1)"
else
    log_fail "bazel not found on PATH"
fi

# Check cargo
if command -v cargo &>/dev/null; then
    log_pass "cargo found: $(cargo --version 2>/dev/null)"
else
    log_fail "cargo not found on PATH"
fi

# Check rustc
if command -v rustc &>/dev/null; then
    log_pass "rustc found: $(rustc --version 2>/dev/null)"
else
    log_fail "rustc not found on PATH"
fi

# Check persistency directory
if [ -d "$PERSISTENCY_DIR" ]; then
    log_pass "score-persistency directory: $PERSISTENCY_DIR"
else
    log_fail "score-persistency directory not found: $PERSISTENCY_DIR"
    echo ""
    echo "ERROR: Cannot continue without score-persistency source."
    echo "Set PERSISTENCY_DIR or pass the path as an argument."
    exit 1
fi

cd "$PERSISTENCY_DIR"

# ---------------------------------------------------------------------------
# 2. Build
# ---------------------------------------------------------------------------

log_section "BUILD"

run_step "Build all sources (//src/...)" \
    bazel build "$BAZEL_CONFIG" //src/... || true

run_step "Build all tests (//tests/...)" \
    bazel build "$BAZEL_CONFIG" //tests/... || true

# ---------------------------------------------------------------------------
# 3. C++ Unit Tests
# ---------------------------------------------------------------------------

log_section "C++ UNIT TESTS"

run_step "C++ unit tests (//:test_kvs_cpp)" \
    bazel test "$BAZEL_CONFIG" //:test_kvs_cpp --test_output=errors || true

# Also try the src/cpp path
run_step "C++ unit tests (//src/cpp/...)" \
    bazel test "$BAZEL_CONFIG" //src/cpp/... --test_output=errors || true

# ---------------------------------------------------------------------------
# 4. Rust Unit Tests
# ---------------------------------------------------------------------------

log_section "RUST UNIT TESTS"

run_step "Rust unit tests (//src/rust/rust_kvs:tests)" \
    bazel test "$BAZEL_CONFIG" //src/rust/rust_kvs:tests --test_output=errors || true

# ---------------------------------------------------------------------------
# 5. Component Integration Tests (CIT)
# ---------------------------------------------------------------------------

log_section "COMPONENT INTEGRATION TESTS"

run_step "Python CIT (//:cit_tests)" \
    bazel test "$BAZEL_CONFIG" //:cit_tests --test_output=errors || true

# ---------------------------------------------------------------------------
# 6. Benchmarks
# ---------------------------------------------------------------------------

log_section "BENCHMARKS"

run_step "C++ KVS benchmark (//:bm_kvs_cpp)" \
    bazel test "$BAZEL_CONFIG" //:bm_kvs_cpp --test_output=errors || true

# ---------------------------------------------------------------------------
# 7. Clippy (Rust lint)
# ---------------------------------------------------------------------------

log_section "RUST QUALITY"

if command -v cargo &>/dev/null; then
    run_step "cargo clippy" \
        cargo clippy --all-targets -- -D warnings || true
else
    log_skip "cargo clippy (cargo not available)"
fi

# ---------------------------------------------------------------------------
# 8. Format Check
# ---------------------------------------------------------------------------

log_section "CODE QUALITY"

run_step "Format check (//:format.check)" \
    bazel test "$BAZEL_CONFIG" //:format.check --test_output=errors || true

# ---------------------------------------------------------------------------
# 9. Summary
# ---------------------------------------------------------------------------

log_section "SUMMARY"

TOTAL=$((PASS + FAIL + SKIP))

echo ""
echo "  Total:   $TOTAL"
echo "  Passed:  $PASS"
echo "  Failed:  $FAIL"
echo "  Skipped: $SKIP"
echo ""

if [ ${#RESULTS[@]} -gt 0 ]; then
    echo "Details:"
    for r in "${RESULTS[@]}"; do
        echo "  $r"
    done
fi

echo ""

if [ "$FAIL" -gt 0 ]; then
    echo -e "\033[1;31mRESULT: SOME CHECKS FAILED\033[0m"
    exit 1
else
    echo -e "\033[1;32mRESULT: ALL CHECKS PASSED\033[0m"
    exit 0
fi
