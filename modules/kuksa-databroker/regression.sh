#!/usr/bin/env bash
# regression.sh — kuksa-databroker regression test runner
#
# Usage:
#   bash modules/kuksa-databroker/regression.sh             # inspection only
#   bash modules/kuksa-databroker/regression.sh --build     # + Cargo build+test
#   bash modules/kuksa-databroker/regression.sh --live      # + live integration tests

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BROKER_DIR="${KUKSA_BROKER_DIR:-$PROJECT_ROOT/eclipse-kuksa-databroker}"

echo "=== kuksa-databroker regression test ==="
echo "Project root : $PROJECT_ROOT"
echo "Broker dir   : $BROKER_DIR"
echo ""

echo "--- Phase 1: File inspection (pytest, no build) ---"
python3 -m pytest \
    "$SCRIPT_DIR/tests/regression/" \
    "$SCRIPT_DIR/tests/integration/" \
    "$SCRIPT_DIR/tests/security/" \
    -v --tb=short 2>&1 | tee /tmp/kuksa-databroker-inspection.log

INSPECTION_RC=${PIPESTATUS[0]}
echo "Inspection tests: $([ $INSPECTION_RC -eq 0 ] && echo PASS || echo FAIL)"

if [[ "${1:-}" == "--build" || "${1:-}" == "--live" ]]; then
    echo ""
    echo "--- Phase 2: Cargo build + unit tests ---"
    cd "$BROKER_DIR"

    cargo build --workspace 2>&1 | tee /tmp/kuksa-databroker-build.log
    BUILD_RC=${PIPESTATUS[0]}

    cargo test --workspace 2>&1 | tee /tmp/kuksa-databroker-test.log
    TEST_RC=${PIPESTATUS[0]}

    echo "Build: $([ $BUILD_RC -eq 0 ] && echo PASS || echo FAIL)"
    echo "Tests: $([ $TEST_RC -eq 0 ] && echo PASS || echo FAIL)"
fi

if [[ "${1:-}" == "--live" ]]; then
    echo ""
    echo "--- Phase 3: Live integration tests ---"
    echo "Starting databroker..."
    cargo run -- --metadata data/vss-core/vss_release_4.0.json &
    BROKER_PID=$!
    sleep 3  # Wait for broker to start

    echo "Running integration tests..."
    cd "$BROKER_DIR/integration_test"
    pip install -q -r requirements.txt
    python3 test_databroker.py 2>&1 | tee /tmp/kuksa-databroker-integration.log
    INT_RC=${PIPESTATUS[0]}

    kill $BROKER_PID 2>/dev/null || true

    echo "Integration: $([ $INT_RC -eq 0 ] && echo PASS || echo FAIL)"
fi

exit $INSPECTION_RC
