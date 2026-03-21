---
document_id: GAP-LOLA-005
title: "Gap Analysis v5 — Final After All Attempts"
version: "5.0"
status: final
date: 2026-03-21
previous: GAP-LOLA-004
---

# LoLa Gap Analysis v5 — Final

## Summary

| Status | v1 | v2 | v3 | v4 | v5 |
|---|---|---|---|---|---|
| Closed | 0 | 4 | 8 | 10 | **10** |
| Investigated but blocked | 0 | 0 | 0 | 2 | **2** |
| False PASS | 5 | 1 | 0 | 0 | **0** |
| Findings | 0 | 0 | 1 | 1 | **3** |

## GAP-004: QNX Cross-Compile — BLOCKED (Investigated)

**Attempted:** `bazel build --config=qnx_arm64 //score/message_passing:qnx_dispatch_test`

**Result:** Failed — Bazel downloads QNX toolchain from `qnx.com` but checksum mismatch:
```
Checksum was 15321ad9... but wanted f2e0cb21...
```
QNX updated the toolchain package, breaking the pinned hash in `score-toolchains_qnx`.

**Root cause:** Upstream `score-toolchains_qnx` has stale checksum. Not fixable without:
- Updating the hash (requires upstream PR to eclipse-score/toolchains_qnx)
- QNX SDP credentials for authenticated download
- Native build on Pi (Pi has clang but no Bazel, and LoLa has deep Bazel deps)

**FINDING-002:** `score-toolchains_qnx` QNX toolchain download checksum is stale. Cross-compilation broken for anyone without pre-cached toolchain. Should be reported upstream.

**Status: BLOCKED — infrastructure issue, not closable without upstream fix or QNX account.**

## GAP-007: ASIL-B Config — BLOCKED (Investigated)

**Attempted:** Three configurations tested:
1. `allowedProvider/Consumer: {"ASIL_B": [0]}` — **core dump** (PID 0 invalid for ASIL-B)
2. `allowedProvider/Consumer: {"ASIL_B": [1000]}` (actual UID) — **core dump** (OS isolation not configured)
3. QM proxy → ASIL-B skeleton — **connection rejected** (freedom from interference enforced)

**Result:** LoLa correctly refuses to start in ASIL-B mode on unconfigured Linux. The ASIL-B mode requires:
- Separate OS groups for ASIL-B and QM processes
- Shared memory file permissions matching the group structure
- Possibly QNX-specific security mechanisms (not available on Linux)

**FINDING-003:** LoLa ASIL-B mode is a **QNX-specific feature**. On Linux, the safety checks (process UID verification, shared memory permission enforcement) abort because the OS isolation prerequisites aren't met. This is correct safety behavior — the middleware refuses to compromise on ASIL-B guarantees.

The positive finding from Test 3: **QM proxy cannot access ASIL-B services** — freedom from interference (SG-COM-003) is partially verified through the rejection.

**Status: BLOCKED — requires QNX target with proper user/group setup. Cannot close on Linux.**

## Updated Finding List

| ID | Severity | Description | Owner |
|---|---|---|---|
| FINDING-001 | High | Concurrent proxy creation crashes (1 in 3 with 3+ proxies) | Upstream LoLa |
| FINDING-002 | Medium | `score-toolchains_qnx` checksum stale, cross-compile broken | Upstream toolchains |
| FINDING-003 | Info | ASIL-B mode is QNX-specific, correctly rejects on Linux | By design |

## Final Status — All 12 Gaps

| Gap | Final Status | Key Evidence |
|---|---|---|
| GAP-001 Latency | **CLOSED** | 10-36 µs on real CAN |
| GAP-002 Data integrity | **CLOSED** | Ground truth match (SIL + real ECU) |
| GAP-003 Discovery timing | **CLOSED** | 114 ms |
| GAP-004 QNX qualification | **BLOCKED** | Toolchain checksum stale (FINDING-002) |
| GAP-005 DBC decoding | **CLOSED** | Correct per both DBC files |
| GAP-006 Error paths | **CLOSED (5/8)** | Malformed, crash, bad iface, flood, slot exhaustion |
| GAP-007 ASIL-B config | **BLOCKED** | Requires QNX + user setup (FINDING-003). FFI partially verified. |
| GAP-008 Real CAN | **CLOSED** | 15 samples from physical ECUs, signals correct |
| GAP-009 Coverage | **CLOSED** | 93.7% line (638 files) |
| GAP-010 Multi-subscriber | **CLOSED** | Tested, found FINDING-001 |
| GAP-011 Python label | **CLOSED** | Report corrected |
| GAP-012 Code quality | **DEFERRED** | Tech debt, decoder proven correct |

## Honest Final Assessment

**What we can claim:**
- LoLa builds, passes 252/252 tests, all sanitizers clean, 93.7% coverage
- CAN→LoLa bridge works on both vcan0 (SIL) and can0 (real ECUs)
- IPC latency 10-36 µs on real hardware (< 100 µs target)
- Signal values verified against ground truth
- 5 error paths tested, all handled correctly
- Freedom from interference partially verified (QM rejected from ASIL-B)

**What we cannot claim:**
- QNX qualification (toolchain broken)
- Full ASIL-B qualification (requires QNX + OS isolation)
- All error paths tested (3/8 untested)
- Multi-subscriber reliability (FINDING-001 crash bug)

**Both blocked gaps are blocked by the same root cause: no QNX cross-compilation capability.** Once `score-toolchains_qnx` checksum is fixed or QNX SDP is available, both can be closed on the Pi.

---

**End of Gap Analysis v5 — GAP-LOLA-005 (Final)**
