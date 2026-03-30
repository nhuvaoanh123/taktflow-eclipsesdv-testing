#!/usr/bin/env bash
# Update all git submodules to latest upstream and report drift.
#
# Usage:
#   bash scripts/update-submodules.sh          # update all
#   bash scripts/update-submodules.sh --dry-run # show drift only
#
# Output: results/submodule-update-<date>.log

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$PROJECT_ROOT/results"
DATE="$(date +%Y-%m-%d_%H%M%S)"
LOG_FILE="$LOG_DIR/submodule-update-${DATE}.log"
SKIP_FILE="$SCRIPT_DIR/windows-skip.txt"
TESTED_FILE="$PROJECT_ROOT/config/tested-commits.yaml"
DRY_RUN=false

if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

mkdir -p "$LOG_DIR"

# Detect Windows (MSYS/Git Bash/Cygwin)
IS_WINDOWS=false
case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) IS_WINDOWS=true ;;
esac

# Load skip list for Windows
SKIP_LIST=()
if $IS_WINDOWS && [[ -f "$SKIP_FILE" ]]; then
    while IFS= read -r line; do
        [[ -z "$line" || "$line" == \#* ]] && continue
        SKIP_LIST+=("$line")
    done < "$SKIP_FILE"
fi

should_skip() {
    local name="$1"
    for skip in "${SKIP_LIST[@]+"${SKIP_LIST[@]}"}"; do
        [[ "$name" == "$skip" ]] && return 0
    done
    return 1
}

echo "=== Submodule Update: $DATE ===" | tee "$LOG_FILE"
echo "Platform: $(uname -s) | Dry run: $DRY_RUN" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

cd "$PROJECT_ROOT"

# Capture before state
declare -A BEFORE
while IFS= read -r line; do
    # Format: " <sha> <path> (<desc>)" or "+<sha> <path> (<desc>)"
    sha=$(echo "$line" | awk '{print $1}' | tr -d '+- ')
    path=$(echo "$line" | awk '{print $2}')
    BEFORE["$path"]="$sha"
done < <(git submodule status 2>/dev/null)

# Update
UPDATED=0
SKIPPED=0
FAILED=0

if ! $DRY_RUN; then
    for path in "${!BEFORE[@]}"; do
        name=$(basename "$path")
        if should_skip "$name"; then
            echo "SKIP (Windows): $path" | tee -a "$LOG_FILE"
            ((SKIPPED++))
            continue
        fi
        if git submodule update --remote --merge "$path" 2>>"$LOG_FILE"; then
            ((UPDATED++))
        else
            echo "FAIL: $path" | tee -a "$LOG_FILE"
            ((FAILED++))
        fi
    done
fi

# Capture after state and report drift
echo "" | tee -a "$LOG_FILE"
echo "--- Drift Report ---" | tee -a "$LOG_FILE"
printf "%-50s %-12s %-12s %s\n" "MODULE" "BEFORE" "AFTER" "STATUS" | tee -a "$LOG_FILE"
echo "$(printf '%.0s-' {1..90})" | tee -a "$LOG_FILE"

CHANGED=0
while IFS= read -r line; do
    sha=$(echo "$line" | awk '{print $1}' | tr -d '+- ')
    path=$(echo "$line" | awk '{print $2}')
    before="${BEFORE[$path]:-unknown}"
    short_before="${before:0:10}"
    short_after="${sha:0:10}"
    if [[ "$before" != "$sha" ]]; then
        status="UPDATED"
        ((CHANGED++))
    else
        status="current"
    fi
    printf "%-50s %-12s %-12s %s\n" "$path" "$short_before" "$short_after" "$status" | tee -a "$LOG_FILE"
done < <(git submodule status 2>/dev/null)

# Check for build system version changes
echo "" | tee -a "$LOG_FILE"
echo "--- Build System Changes ---" | tee -a "$LOG_FILE"
for bv in $(find . -maxdepth 3 -name ".bazelversion" -not -path "./.git/*" 2>/dev/null); do
    dir=$(dirname "$bv")
    ver=$(cat "$bv" 2>/dev/null || echo "?")
    echo "  $dir: Bazel $ver" | tee -a "$LOG_FILE"
done

# Summary
echo "" | tee -a "$LOG_FILE"
echo "=== Summary ===" | tee -a "$LOG_FILE"
echo "  Total submodules: ${#BEFORE[@]}" | tee -a "$LOG_FILE"
echo "  Updated: $CHANGED" | tee -a "$LOG_FILE"
echo "  Skipped: $SKIPPED" | tee -a "$LOG_FILE"
echo "  Failed: $FAILED" | tee -a "$LOG_FILE"
echo "  Log: $LOG_FILE" | tee -a "$LOG_FILE"
