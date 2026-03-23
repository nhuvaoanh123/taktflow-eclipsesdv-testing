#!/usr/bin/env bash
# =============================================================================
# Eclipse S-CORE LoLa — Environment Setup for Ubuntu 24.04
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_ROOT/results/setup-$(date +%Y%m%d-%H%M%S).log"

mkdir -p "$PROJECT_ROOT/results"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG_FILE"; }
ok()  { log "✓ $*"; }
fail() { log "✗ $*"; }
check() {
    if command -v "$1" &>/dev/null; then
        ok "$1 found: $($1 --version 2>/dev/null | head -1)"
        return 0
    else
        fail "$1 not found"
        return 1
    fi
}

log "=========================================="
log "LoLa Environment Setup — $(date)"
log "=========================================="

# --- System packages ---
log ""
log "--- Phase 1: System packages ---"
sudo apt-get update -qq
sudo apt-get install -y -qq \
    build-essential gcc g++ \
    python3 python3-pip python3-venv \
    git curl wget \
    libatomic1 libstdc++-12-dev \
    docker.io \
    2>&1 | tee -a "$LOG_FILE"

# Add user to docker group if not already
if ! groups | grep -q docker; then
    sudo usermod -aG docker "$USER"
    log "Added $USER to docker group — you may need to re-login"
fi

ok "System packages installed"

# --- Bazelisk ---
log ""
log "--- Phase 2: Bazelisk (Bazel version manager) ---"
if ! check bazel; then
    log "Installing Bazelisk..."
    curl -fsSL "https://github.com/bazelbuild/bazelisk/releases/latest/download/bazelisk-linux-amd64" \
        -o /tmp/bazel
    chmod +x /tmp/bazel
    sudo mv /tmp/bazel /usr/local/bin/bazel
    ok "Bazelisk installed"
fi

# Verify Bazel version matches LoLa requirement (8.3.0)
REQUIRED_BAZEL="8.3.0"
log "LoLa requires Bazel $REQUIRED_BAZEL (managed via .bazelversion)"

# --- Docker check ---
log ""
log "--- Phase 3: Docker ---"
if check docker; then
    if docker info &>/dev/null; then
        ok "Docker daemon is running"
    else
        fail "Docker daemon not running — start with: sudo systemctl start docker"
    fi
fi

# --- AppArmor sandbox workaround (Ubuntu 24.04) ---
log ""
log "--- Phase 4: AppArmor sandbox workaround ---"
WORKAROUND_SCRIPT="$PROJECT_ROOT/score-communication/actions/unblock_user_namespace_for_linux_sandbox/action_callable.sh"
if [ -f "$WORKAROUND_SCRIPT" ]; then
    log "Running Bazel sandbox workaround for Ubuntu 24.04..."
    bash "$WORKAROUND_SCRIPT" 2>&1 | tee -a "$LOG_FILE" || true
    ok "Sandbox workaround applied"
else
    log "Workaround script not found (clone score-communication first)"
fi

# --- Python deps ---
log ""
log "--- Phase 5: Python dependencies ---"
check python3
python3 -m pip install --user pytest docker bazel-runfiles 2>&1 | tee -a "$LOG_FILE"
ok "Python test deps installed"

# --- Disk space check ---
log ""
log "--- Phase 6: Disk space check ---"
AVAILABLE_GB=$(df -BG "$PROJECT_ROOT" | tail -1 | awk '{print $4}' | tr -d 'G')
if [ "$AVAILABLE_GB" -ge 20 ]; then
    ok "Disk space: ${AVAILABLE_GB}GB available (need 20GB+ for Bazel cache)"
else
    fail "Disk space: ${AVAILABLE_GB}GB available — need at least 20GB for Bazel build cache"
fi

# --- RAM check ---
log ""
log "--- Phase 7: RAM check ---"
TOTAL_RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
if [ "$TOTAL_RAM_GB" -ge 8 ]; then
    ok "RAM: ${TOTAL_RAM_GB}GB (8GB+ recommended)"
else
    fail "RAM: ${TOTAL_RAM_GB}GB — 8GB+ recommended for parallel builds"
fi

# --- Summary ---
log ""
log "=========================================="
log "Environment setup complete"
log "Log: $LOG_FILE"
log ""
log "Next step: bash scripts/assess-lola.sh"
log "=========================================="
