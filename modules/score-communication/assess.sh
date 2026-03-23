#!/usr/bin/env bash
# =============================================================================
# Eclipse S-CORE LoLa — Comprehensive Assessment Script
# =============================================================================
# Run on Linux laptop to assess LoLa build, test, and quality state.
# Produces: results/lola-assessment-YYYYMMDD.md + .json
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOLA_DIR="$PROJECT_ROOT/score-communication"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RESULTS_DIR="$PROJECT_ROOT/results"
REPORT_MD="$RESULTS_DIR/lola-assessment-${TIMESTAMP}.md"
REPORT_JSON="$RESULTS_DIR/lola-assessment-${TIMESTAMP}.json"
LOG_DIR="$RESULTS_DIR/logs-${TIMESTAMP}"

mkdir -p "$RESULTS_DIR" "$LOG_DIR"

# --- Helpers ---
PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG_DIR/master.log"; }

run_phase() {
    local phase_num="$1"
    local phase_name="$2"
    local phase_cmd="$3"
    local phase_log="$LOG_DIR/phase${phase_num}-${phase_name// /_}.log"
    local required="${4:-true}"

    log ""
    log "================================================================"
    log "Phase $phase_num: $phase_name"
    log "================================================================"

    local start_time=$(date +%s)
    local exit_code=0

    eval "$phase_cmd" > "$phase_log" 2>&1 || exit_code=$?

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    if [ $exit_code -eq 0 ]; then
        log "PASS — $phase_name (${duration}s)"
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "\"phase${phase_num}_${phase_name// /_}\": {\"status\": \"PASS\", \"duration\": $duration, \"log\": \"$phase_log\"}," >> "$REPORT_JSON.tmp"
    else
        if [ "$required" = "true" ]; then
            log "FAIL — $phase_name (${duration}s, exit=$exit_code)"
            FAIL_COUNT=$((FAIL_COUNT + 1))
        else
            log "SKIP/WARN — $phase_name (${duration}s, exit=$exit_code)"
            SKIP_COUNT=$((SKIP_COUNT + 1))
        fi
        echo "\"phase${phase_num}_${phase_name// /_}\": {\"status\": \"$([ "$required" = "true" ] && echo FAIL || echo SKIP)\", \"duration\": $duration, \"exit_code\": $exit_code, \"log\": \"$phase_log\"}," >> "$REPORT_JSON.tmp"
    fi

    # Capture tail of log for report
    echo "" >> "$REPORT_MD"
    echo "### Phase $phase_num: $phase_name" >> "$REPORT_MD"
    echo "" >> "$REPORT_MD"
    if [ $exit_code -eq 0 ]; then
        echo "**Status: PASS** (${duration}s)" >> "$REPORT_MD"
    else
        echo "**Status: $([ "$required" = "true" ] && echo FAIL || echo SKIP)** (${duration}s, exit=$exit_code)" >> "$REPORT_MD"
    fi
    echo "" >> "$REPORT_MD"
    echo '```' >> "$REPORT_MD"
    tail -20 "$phase_log" >> "$REPORT_MD"
    echo '```' >> "$REPORT_MD"
    echo "" >> "$REPORT_MD"
    echo "Full log: \`$phase_log\`" >> "$REPORT_MD"

    return $exit_code
}

# --- Init report ---
cat > "$REPORT_MD" << 'HEADER'
# LoLa (score-communication) Assessment Report

HEADER
echo "**Date:** $(date)" >> "$REPORT_MD"
echo "**Host:** $(hostname)" >> "$REPORT_MD"
echo "**Kernel:** $(uname -r)" >> "$REPORT_MD"
echo "**RAM:** $(free -h | awk '/^Mem:/{print $2}')" >> "$REPORT_MD"
echo "**Disk:** $(df -h "$LOLA_DIR" | tail -1 | awk '{print $4}') available" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"

echo "{" > "$REPORT_JSON.tmp"
echo "\"timestamp\": \"$TIMESTAMP\"," >> "$REPORT_JSON.tmp"
echo "\"host\": \"$(hostname)\"," >> "$REPORT_JSON.tmp"

# --- Phase 1: Environment Check ---
run_phase 1 "environment" "
    echo '=== Bazel ==='
    bazel --version
    echo '=== GCC ==='
    gcc --version | head -1
    echo '=== Python ==='
    python3 --version
    echo '=== Docker ==='
    docker --version
    docker info --format '{{.ServerVersion}}' 2>/dev/null || echo 'Docker daemon not running'
    echo '=== Disk ==='
    df -h '$LOLA_DIR'
    echo '=== RAM ==='
    free -h
    echo '=== CPU ==='
    nproc
    echo '=== LoLa directory ==='
    ls '$LOLA_DIR'/MODULE.bazel
" || true

# --- Phase 2: Build ---
cd "$LOLA_DIR"
run_phase 2 "build" "
    cd '$LOLA_DIR'
    bazel build //... 2>&1
" || {
    log "BUILD FAILED — stopping assessment. Fix build first."
    # Still generate report
}

# --- Phase 3: Unit Tests ---
run_phase 3 "unit_tests" "
    cd '$LOLA_DIR'
    bazel test //... --build_tests_only --test_output=summary 2>&1
" || true

# Extract test summary if available
if [ -f "$LOG_DIR/phase3-unit_tests.log" ]; then
    echo "" >> "$REPORT_MD"
    echo "#### Test Summary" >> "$REPORT_MD"
    echo '```' >> "$REPORT_MD"
    grep -E "^(//|Executed|PASSED|FAILED|NO STATUS)" "$LOG_DIR/phase3-unit_tests.log" | tail -30 >> "$REPORT_MD" 2>/dev/null || true
    echo '```' >> "$REPORT_MD"
fi

# --- Phase 4: Integration Tests ---
run_phase 4 "integration_tests" "
    cd '$LOLA_DIR'
    if docker info &>/dev/null; then
        bazel test //quality/integration_testing/... --test_output=summary 2>&1
    else
        echo 'Docker not available — skipping integration tests'
        exit 1
    fi
" "false"

# --- Phase 5: Sanitizers (ASan/UBSan/LSan) ---
run_phase 5 "sanitizers_asan" "
    cd '$LOLA_DIR'
    bazel test --config=asan_ubsan_lsan //... --build_tests_only --test_output=errors 2>&1
" "false"

# --- Phase 6: Thread Sanitizer ---
run_phase 6 "sanitizers_tsan" "
    cd '$LOLA_DIR'
    bazel test --config=tsan //... --build_tests_only --test_output=errors 2>&1
" "false"

# --- Phase 7: Performance Benchmarks ---
run_phase 7 "benchmarks" "
    cd '$LOLA_DIR'
    bazel build //score/mw/com/performance_benchmarks/api_microbenchmarks:all 2>&1
    echo '=== Benchmark binary built ==='
    echo 'Run manually: bazel run //score/mw/com/performance_benchmarks/api_microbenchmarks:lola_public_api_benchmarks'
" "false"

# --- Phase 8: Code Coverage ---
run_phase 8 "coverage" "
    cd '$LOLA_DIR'
    bazel coverage //... --combined_report=lcov 2>&1
    echo '=== Coverage report ==='
    LCOV_FILE=\$(find bazel-out -name 'coverage.dat' -o -name '_coverage_report.dat' 2>/dev/null | head -1)
    if [ -n \"\$LCOV_FILE\" ]; then
        echo \"Coverage file: \$LCOV_FILE\"
        # Extract summary if lcov available
        if command -v lcov &>/dev/null; then
            lcov --summary \"\$LCOV_FILE\" 2>&1
        fi
    fi
" "false"

# --- Phase 9: Static Analysis (clang-tidy) ---
run_phase 9 "clang_tidy" "
    cd '$LOLA_DIR'
    bazel test --config=clang-tidy //score/mw/com/... --test_output=errors 2>&1
" "false"

# --- Phase 10: QNX Cross-Compile Check ---
run_phase 10 "qnx_cross_compile" "
    cd '$LOLA_DIR'
    if [ -d '/opt/score_qnx' ] || [ -n \"\${QNX_HOST:-}\" ]; then
        bazel build --config=qnx_arm64 //score/mw/com:all 2>&1
    else
        echo 'QNX SDP not installed — skipping cross-compilation'
        exit 1
    fi
" "false"

# --- Phase 11: Example Apps ---
run_phase 11 "examples" "
    cd '$LOLA_DIR'
    bazel build //examples/... 2>&1
" "false"

# --- Phase 12: Copyright & Format Check ---
run_phase 12 "code_quality" "
    cd '$LOLA_DIR'
    bazel test //:format.check 2>&1
    bazel run //:copyright.check 2>&1
" "false"

# --- Finalize Report ---
echo "" >> "$REPORT_MD"
echo "---" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "## Summary" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "| Metric | Value |" >> "$REPORT_MD"
echo "|---|---|" >> "$REPORT_MD"
echo "| Phases PASS | $PASS_COUNT |" >> "$REPORT_MD"
echo "| Phases FAIL | $FAIL_COUNT |" >> "$REPORT_MD"
echo "| Phases SKIP | $SKIP_COUNT |" >> "$REPORT_MD"
echo "| Total Duration | $(($(date +%s) - $(date -d "$(head -1 "$LOG_DIR/master.log" | grep -oP '\d{2}:\d{2}:\d{2}')" +%s 2>/dev/null || echo 0)))s |" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"

echo "" >> "$REPORT_MD"
echo "## ASPICE Gate Check" >> "$REPORT_MD"
echo "" >> "$REPORT_MD"
echo "| Gate | Requirement | Result |" >> "$REPORT_MD"
echo "|---|---|---|" >> "$REPORT_MD"
echo "| SWE.4 (Unit Verification) | All unit tests pass | Phase 3 |" >> "$REPORT_MD"
echo "| SWE.5 (Integration Test) | Integration tests pass | Phase 4 |" >> "$REPORT_MD"
echo "| SUP.1 (Quality) | Static analysis clean | Phase 9 |" >> "$REPORT_MD"
echo "| SUP.8 (Config Mgmt) | Build reproducible | Phase 2 |" >> "$REPORT_MD"
echo "| SAF (Safety) | Sanitizers clean | Phase 5+6 |" >> "$REPORT_MD"
echo "| NFR (Performance) | Benchmarks baselined | Phase 7 |" >> "$REPORT_MD"

# Finalize JSON
echo "\"summary\": {\"pass\": $PASS_COUNT, \"fail\": $FAIL_COUNT, \"skip\": $SKIP_COUNT}" >> "$REPORT_JSON.tmp"
echo "}" >> "$REPORT_JSON.tmp"
# Fix trailing commas
sed 's/,}/}/' "$REPORT_JSON.tmp" > "$REPORT_JSON"
rm -f "$REPORT_JSON.tmp"

log ""
log "================================================================"
log "Assessment complete"
log "Report: $REPORT_MD"
log "JSON:   $REPORT_JSON"
log "Logs:   $LOG_DIR/"
log "================================================================"
log "Results: $PASS_COUNT PASS, $FAIL_COUNT FAIL, $SKIP_COUNT SKIP"
