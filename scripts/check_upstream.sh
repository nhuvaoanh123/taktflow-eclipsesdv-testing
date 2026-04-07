#!/usr/bin/env bash
# check_upstream.sh — Check all submodules for upstream changes
# Usage: ./scripts/check_upstream.sh [--json] [--ecosystem <name>]
#
# Compares pinned submodule commits against upstream main/master branch.
# Uses GitHub API (gh) so no cloning required.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

JSON_OUTPUT=false
FILTER_ECOSYSTEM=""
SHOW_HELP=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --json) JSON_OUTPUT=true; shift ;;
        --ecosystem) FILTER_ECOSYSTEM="$2"; shift 2 ;;
        --help|-h) SHOW_HELP=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if $SHOW_HELP; then
    echo "Usage: $0 [--json] [--ecosystem <name>]"
    echo ""
    echo "Options:"
    echo "  --json              Output results as JSON"
    echo "  --ecosystem <name>  Filter by ecosystem (kuksa, velocitas, leda, chariott,"
    echo "                      ibeji, ankaios, uprotocol, sdv-blueprints, score)"
    echo ""
    echo "Examples:"
    echo "  $0                          # Check all submodules"
    echo "  $0 --ecosystem score        # Check only eclipse-score modules"
    echo "  $0 --json                   # JSON output for automation"
    exit 0
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Counters
total=0
up_to_date=0
behind=0
errors=0

# Collect JSON entries
json_entries=()

# Get all submodule info from .gitmodules
get_submodules() {
    git config --file .gitmodules --get-regexp 'submodule\..*\.url' | while read -r key url; do
        name="${key#submodule.}"
        name="${name%.url}"
        path=$(git config --file .gitmodules "submodule.${name}.path")
        echo "${name}|${path}|${url}"
    done
}

# Extract GitHub owner/repo from URL
parse_github_url() {
    local url="$1"
    echo "$url" | sed -E 's|https://github.com/(.+)\.git$|\1|; s|https://github.com/(.+)$|\1|'
}

# Get ecosystem from submodule name
get_ecosystem() {
    local name="$1"
    echo "$name" | sed -E 's/^([^-]+).*/\1/'
}

# Get pinned commit from git submodule status
get_pinned_commits() {
    git submodule status 2>/dev/null | sed -E 's/^[-+ ]?([0-9a-f]+) ([^ ]+).*/\2|\1/'
}

# Cache pinned commits
declare -A PINNED_COMMITS
while IFS='|' read -r path sha; do
    PINNED_COMMITS["$path"]="$sha"
done < <(get_pinned_commits)

echo ""
if ! $JSON_OUTPUT; then
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}  Eclipse SDV Upstream Tracker — $(date '+%Y-%m-%d %H:%M')${NC}"
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
fi

current_ecosystem=""

while IFS='|' read -r name path url; do
    ecosystem=$(get_ecosystem "$name")

    # Filter by ecosystem if requested
    if [[ -n "$FILTER_ECOSYSTEM" && "$ecosystem" != "$FILTER_ECOSYSTEM" ]]; then
        continue
    fi

    total=$((total + 1))

    # Print ecosystem header
    if ! $JSON_OUTPUT && [[ "$ecosystem" != "$current_ecosystem" ]]; then
        current_ecosystem="$ecosystem"
        echo -e "${CYAN}${BOLD}── ${ecosystem^^} ──${NC}"
    fi

    # Get pinned SHA
    pinned_sha="${PINNED_COMMITS[$path]:-unknown}"

    # Get upstream info via GitHub API
    gh_repo=$(parse_github_url "$url")

    # Try main, then master
    upstream_info=$(gh api "repos/${gh_repo}/commits/main" \
        --jq '.sha + "|" + .commit.message' 2>/dev/null) || \
    upstream_info=$(gh api "repos/${gh_repo}/commits/master" \
        --jq '.sha + "|" + .commit.message' 2>/dev/null) || \
    upstream_info=""

    if [[ -z "$upstream_info" ]]; then
        errors=$((errors + 1))
        if ! $JSON_OUTPUT; then
            echo -e "  ${RED}✗${NC} ${name} — ${RED}API error${NC}"
        fi
        json_entries+=("{\"name\":\"$name\",\"status\":\"error\"}")
        continue
    fi

    upstream_sha="${upstream_info%%|*}"
    upstream_msg="${upstream_info#*|}"
    # Take first line of commit message
    upstream_msg="${upstream_msg%%$'\n'*}"
    # Truncate long messages
    if [[ ${#upstream_msg} -gt 60 ]]; then
        upstream_msg="${upstream_msg:0:57}..."
    fi

    short_pinned="${pinned_sha:0:7}"
    short_upstream="${upstream_sha:0:7}"

    if [[ "$pinned_sha" == "$upstream_sha" ]]; then
        up_to_date=$((up_to_date + 1))
        if ! $JSON_OUTPUT; then
            echo -e "  ${GREEN}✓${NC} ${name} — up to date (${short_pinned})"
        fi
        json_entries+=("{\"name\":\"$name\",\"ecosystem\":\"$ecosystem\",\"status\":\"current\",\"pinned\":\"$short_pinned\"}")
    else
        behind=$((behind + 1))

        # Count commits behind (best effort)
        commits_behind=""
        count=$(gh api "repos/${gh_repo}/compare/${short_pinned}...${short_upstream}" \
            --jq '.ahead_by' 2>/dev/null) || count=""

        if [[ -n "$count" ]]; then
            commits_behind=" (${count} commits behind)"
        fi

        if ! $JSON_OUTPUT; then
            echo -e "  ${YELLOW}↑${NC} ${name}${commits_behind}"
            echo -e "     pinned: ${short_pinned} → upstream: ${short_upstream}"
            echo -e "     latest: ${upstream_msg}"
        fi
        json_entries+=("{\"name\":\"$name\",\"ecosystem\":\"$ecosystem\",\"status\":\"behind\",\"pinned\":\"$short_pinned\",\"upstream\":\"$short_upstream\",\"commits_behind\":\"${count:-unknown}\",\"latest_msg\":\"$upstream_msg\"}")
    fi

done < <(get_submodules)

echo ""

if $JSON_OUTPUT; then
    echo "["
    for i in "${!json_entries[@]}"; do
        if [[ $i -lt $((${#json_entries[@]} - 1)) ]]; then
            echo "  ${json_entries[$i]},"
        else
            echo "  ${json_entries[$i]}"
        fi
    done
    echo "]"
else
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "  Total: ${total}  ${GREEN}✓ Current: ${up_to_date}${NC}  ${YELLOW}↑ Behind: ${behind}${NC}  ${RED}✗ Errors: ${errors}${NC}"
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"

    if [[ $behind -gt 0 ]]; then
        echo ""
        echo -e "  To update a submodule:  ${BOLD}git submodule update --init --remote <path>${NC}"
        echo -e "  To update all:          ${BOLD}git submodule update --init --remote${NC}"
    fi
fi
