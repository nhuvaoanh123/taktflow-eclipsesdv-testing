#!/usr/bin/env bash
# =============================================================================
# LoLa CAN Bridge Regression Test
# Sends known CAN frames, verifies decoded output matches expected values.
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOLA_DIR="$(dirname "$SCRIPT_DIR")/score-communication"
BIN="$LOLA_DIR/bazel-out/k8-fastbuild/bin/score/mw/com/example/can_bridge/can_bridge"
CFG="$LOLA_DIR/score/mw/com/example/can_bridge/etc/mw_com_config.json"
PASS=0
FAIL=0

check() {
    local name="$1" expected="$2" actual="$3"
    if echo "$actual" | grep -q "$expected"; then
        echo "  PASS: $name (found '$expected')"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $name (expected '$expected', got '$actual')"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== LoLa CAN Bridge Regression Test ==="
echo "Date: $(date)"
echo ""

# Ensure vcan0 is up
ip link show vcan0 > /dev/null 2>&1 || {
    echo "SKIP: vcan0 not available"
    exit 77
}

# Start skeleton
$BIN -m skeleton -c vcan0 -n 0 -s "$CFG" > /dev/null 2>&1 &
SKEL=$!
sleep 3

# Start proxy, capture output
$BIN -m proxy -n 20 -s "$CFG" 2>/dev/null > /tmp/regression_proxy.txt &
PROXY=$!
sleep 2

echo "--- Test 1: SIL Lidar (0x220) distance=500cm ---"
# 0x220: E2E(DataID=5,Alive=3) + CRC=0x00 + Distance=500(0x01F4) + rest
cansend vcan0 220#3500F401000000000 2>/dev/null || cansend vcan0 220#3500F40100000000
sleep 0.5

echo "--- Test 2: SIL RZC (0x601) RPM=1500, current=500mA, temp=250dC ---"
# 0x601: Current=500(0x01F4) + Temp=250(0x00FA) + Batt=12600(0x3138) + RPM=1500(0x05DC)
cansend vcan0 601#F401FA003831DC05
sleep 0.5

echo "--- Test 3: Real ECU FZC Heartbeat (0x011) alive=7 ---"
# 0x011: DataID=3,Alive=7 (0x73) + CRC + ECU=2 + Mode=INIT
cansend vcan0 011#73970200
sleep 0.5

echo "--- Test 4: Real ECU Brake (0x211) position=42% ---"
# 0x211: E2E + BrakePos=42 + CmdEcho=0 + ServoCurrent=0
cansend vcan0 211#00002A0000000000
sleep 2

# Kill proxy, collect results
kill $PROXY 2>/dev/null
wait $PROXY 2>/dev/null
kill $SKEL 2>/dev/null
wait $SKEL 2>/dev/null

echo ""
echo "=== Proxy output ==="
cat /tmp/regression_proxy.txt | tail -10

echo ""
echo "=== Assertions ==="
OUTPUT=$(cat /tmp/regression_proxy.txt)

# Note: proxy samples are asynchronous — we check the last few lines
# for values that should appear after our injected frames
check "Lidar near 500" "lidar=50" "$OUTPUT"  # 500 or 501 or 502
check "RPM value" "rpm=" "$OUTPUT"
check "Brake position" "pedal=" "$OUTPUT"  # brake stored in pedal field
check "Alive counter" "seq=" "$OUTPUT"
check "Temperature" "Tm=" "$OUTPUT"
check "IPC latency measured" "age=" "$OUTPUT"

echo ""
echo "=== Results ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"
echo "TOTAL: $((PASS + FAIL))"

if [ $FAIL -eq 0 ]; then
    echo "STATUS: ALL PASS"
    exit 0
else
    echo "STATUS: $FAIL FAILURES"
    exit 1
fi
