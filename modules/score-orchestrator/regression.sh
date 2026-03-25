#!/usr/bin/env bash
# regression.sh — score-orchestrator regression test runner
#
# Usage:
#   bash modules/score-orchestrator/regression.sh             # inspection only
#   bash modules/score-orchestrator/regression.sh --build     # + Cargo + Bazel

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ORCH_DIR="${SCORE_ORCH_DIR:-$PROJECT_ROOT/score-orchestrator}"

echo "=== score-orchestrator regression test ==="
echo "Project root : $PROJECT_ROOT"
echo "Orch dir     : $ORCH_DIR"
echo ""

echo "--- Phase 1: File inspection (pytest, no build) ---"
python3 -m pytest \
    "$SCRIPT_DIR/tests/regression/" \
    "$SCRIPT_DIR/tests/integration/" \
    "$SCRIPT_DIR/tests/security/" \
    -v --tb=short 2>&1 | tee /tmp/score-orchestrator-inspection.log

INSPECTION_RC=${PIPESTATUS[0]}
echo ""
echo "Inspection tests: $([ $INSPECTION_RC -eq 0 ] && echo PASS || echo FAIL)"

if [[ "${1:-}" == "--build" ]]; then
    echo ""
    echo "--- Phase 2: Cargo build + test ---"
    cd "$ORCH_DIR"

    echo "Building (cargo)..."
    cargo build 2>&1 | tee /tmp/score-orchestrator-cargo-build.log
    CARGO_BUILD_RC=${PIPESTATUS[0]}

    echo "Testing (cargo)..."
    cargo test 2>&1 | tee /tmp/score-orchestrator-cargo-test.log
    CARGO_TEST_RC=${PIPESTATUS[0]}

    echo ""
    echo "--- Phase 3: Bazel build + test ---"
    echo "Building (bazel)..."
    bazel build --config=x86_64-linux //... 2>&1 | tee /tmp/score-orchestrator-bazel-build.log
    BAZEL_BUILD_RC=${PIPESTATUS[0]}

    echo "Testing (bazel)..."
    bazel test --config=x86_64-linux //... --build_tests_only \
        --test_output=summary 2>&1 | tee /tmp/score-orchestrator-bazel-test.log
    BAZEL_TEST_RC=${PIPESTATUS[0]}

    echo ""
    echo "Cargo build : $([ $CARGO_BUILD_RC -eq 0 ] && echo PASS || echo FAIL)"
    echo "Cargo test  : $([ $CARGO_TEST_RC -eq 0 ] && echo PASS || echo FAIL)"
    echo "Bazel build : $([ $BAZEL_BUILD_RC -eq 0 ] && echo PASS || echo FAIL)"
    echo "Bazel test  : $([ $BAZEL_TEST_RC -eq 0 ] && echo PASS || echo FAIL)"

    exit $(( INSPECTION_RC + CARGO_BUILD_RC + CARGO_TEST_RC + BAZEL_BUILD_RC + BAZEL_TEST_RC ))
fi

exit $INSPECTION_RC
