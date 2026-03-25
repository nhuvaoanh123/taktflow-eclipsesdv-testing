#!/usr/bin/env bash
# regression.sh — score-logging regression test runner
#
# Runs all file-inspection tests (no build required) + Bazel build/test
# if explicitly requested. Designed to run on Ubuntu 24.04 laptop.
#
# Usage:
#   bash modules/score-logging/regression.sh             # inspection only
#   bash modules/score-logging/regression.sh --build     # + Bazel build+test
#
# Environment:
#   SCORE_LOGGING_DIR   Path to score-logging checkout (default: ./score-logging)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOGGING_DIR="${SCORE_LOGGING_DIR:-$PROJECT_ROOT/score-logging}"

echo "=== score-logging regression test ==="
echo "Project root : $PROJECT_ROOT"
echo "Logging dir  : $LOGGING_DIR"
echo ""

# ---- File inspection tests (always run) ------------------------------------
echo "--- Phase 1: File inspection (pytest, no build) ---"
python3 -m pytest \
    "$SCRIPT_DIR/tests/regression/" \
    "$SCRIPT_DIR/tests/integration/" \
    "$SCRIPT_DIR/tests/security/" \
    -v --tb=short 2>&1 | tee /tmp/score-logging-inspection.log

INSPECTION_RC=${PIPESTATUS[0]}
echo ""
echo "Inspection tests: $([ $INSPECTION_RC -eq 0 ] && echo PASS || echo FAIL)"

# ---- Bazel build + tests (optional) ----------------------------------------
if [[ "${1:-}" == "--build" ]]; then
    echo ""
    echo "--- Phase 2: Bazel build + unit tests ---"
    cd "$LOGGING_DIR"

    echo "Building all targets..."
    bazel build --config=x86_64-linux //score/... 2>&1 | tee /tmp/score-logging-build.log
    BUILD_RC=${PIPESTATUS[0]}

    echo "Running unit tests..."
    bazel test --config=x86_64-linux //score/... --build_tests_only \
        --test_output=summary 2>&1 | tee /tmp/score-logging-test.log
    TEST_RC=${PIPESTATUS[0]}

    echo ""
    echo "Build: $([ $BUILD_RC -eq 0 ] && echo PASS || echo FAIL)"
    echo "Tests: $([ $TEST_RC -eq 0 ] && echo PASS || echo FAIL)"

    exit $(( INSPECTION_RC + BUILD_RC + TEST_RC ))
fi

exit $INSPECTION_RC
