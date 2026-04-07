#!/usr/bin/env bash
# update_upstream.sh — Pull all submodules to latest upstream, report what changed
# Usage: ./scripts/update_upstream.sh [--ecosystem <name>] [--dry-run]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

DRY_RUN=false
FILTER_ECOSYSTEM=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --ecosystem) FILTER_ECOSYSTEM="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: $0 [--ecosystem <name>] [--dry-run]"
            echo ""
            echo "Updates all submodule pins to latest upstream commits."
            echo "Run your tests after to see what broke."
            echo ""
            echo "Options:"
            echo "  --ecosystem <name>  Only update one ecosystem"
            echo "  --dry-run           Show what would change without updating"
            exit 0 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

get_ecosystem() {
    echo "$1" | sed -E 's/^([^-]+).*/\1/'
}

parse_github_url() {
    echo "$1" | sed -E 's|https://github.com/(.+)\.git$|\1|; s|https://github.com/(.+)$|\1|'
}

echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
if $DRY_RUN; then
    echo -e "${BOLD}  Eclipse SDV Upstream Update (DRY RUN) — $(date '+%Y-%m-%d %H:%M')${NC}"
else
    echo -e "${BOLD}  Eclipse SDV Upstream Update — $(date '+%Y-%m-%d %H:%M')${NC}"
fi
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo ""

updated=0
skipped=0
errors=0
changelog=""

# Get pinned commits
declare -A PINNED
while IFS='|' read -r path sha; do
    PINNED["$path"]="$sha"
done < <(git submodule status 2>/dev/null | sed -E 's/^[-+ ]?([0-9a-f]+) ([^ ]+).*/\2|\1/')

# Iterate submodules
git config --file .gitmodules --get-regexp 'submodule\..*\.url' | while read -r key url; do
    name="${key#submodule.}"
    name="${name%.url}"
    path=$(git config --file .gitmodules "submodule.${name}.path")
    ecosystem=$(get_ecosystem "$name")

    if [[ -n "$FILTER_ECOSYSTEM" && "$ecosystem" != "$FILTER_ECOSYSTEM" ]]; then
        continue
    fi

    gh_repo=$(parse_github_url "$url")
    pinned="${PINNED[$path]:-unknown}"

    # Get upstream HEAD
    upstream_sha=$(gh api "repos/${gh_repo}/commits/main" --jq '.sha' 2>/dev/null) || \
    upstream_sha=$(gh api "repos/${gh_repo}/commits/master" --jq '.sha' 2>/dev/null) || \
    upstream_sha=""

    if [[ -z "$upstream_sha" ]]; then
        echo -e "  ${RED}✗${NC} ${name} — cannot reach upstream"
        continue
    fi

    if [[ "$pinned" == "$upstream_sha" ]]; then
        continue  # already current, skip silently
    fi

    short_old="${pinned:0:7}"
    short_new="${upstream_sha:0:7}"

    # Get commit count
    count=$(gh api "repos/${gh_repo}/compare/${short_old}...${short_new}" \
        --jq '.ahead_by' 2>/dev/null) || count="?"

    if $DRY_RUN; then
        echo -e "  ${YELLOW}↑${NC} ${name}: ${short_old} → ${short_new} (+${count} commits)"
    else
        # Actually update: init if needed, fetch, checkout
        if [[ ! -d "${path}/.git" ]] && [[ ! -f "${path}/.git" ]]; then
            git submodule init "$path" 2>/dev/null || true
        fi

        if git submodule update --remote "$path" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} ${name}: ${short_old} → ${short_new} (+${count} commits)"
        else
            echo -e "  ${RED}✗${NC} ${name}: update failed"
        fi
    fi
done

echo ""
if $DRY_RUN; then
    echo -e "${BOLD}  Dry run complete. Run without --dry-run to apply.${NC}"
else
    echo -e "${BOLD}  Done. Now run your tests to see what broke.${NC}"
    echo -e "  If anything is wrong: ${BOLD}git checkout -- . && git submodule update${NC}"
fi
echo ""
