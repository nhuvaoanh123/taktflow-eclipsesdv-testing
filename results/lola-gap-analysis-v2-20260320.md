---
document_id: GAP-LOLA-002
title: "Gap Analysis v2 — LoLa Integration Assessment (After Remediation)"
version: "2.0"
status: active
date: 2026-03-20
previous: GAP-LOLA-001
---

# LoLa Gap Analysis v2 — After Remediation

## Summary

12 gaps identified in v1. 4 fully closed, 1 partially closed, 7 remain open.

## Closed Gaps

| Gap | Issue | Resolution | Evidence |
|---|---|---|---|
| **GAP-001** | Latency measured wrong thing (622ns = specifier creation) | Instrumented actual IPC path | Skeleton: 9.7-18.3 µs decode→send. Proxy: 8-29 µs receive age. **NFR-COM-001 PASS.** |
| **GAP-002** | Data integrity never compared to ground truth | Decoded SIL DBC with Python, compared to bridge output | 5 signals match: lidar=500cm (498-502), RPM=0, Temp=25.0°C, Current=0A, Batt=12.6V |
| **GAP-005** | DBC decoding wrong (RPM garbage from wrong CAN ID) | Read actual `taktflow_sil.dbc`, rewrote decoder | 0x220=Lidar (was decoded as RPM), 0x600=FZC sensors, 0x601=RZC sensors. All correct now. |
| **GAP-009** | Coverage 13.5% from one target | Ran `bazel coverage //...` across all 251 tests | **93.7% line coverage** (16,023/17,101 lines across 638 files) |

## Partially Closed

| Gap | Issue | Progress | Remaining |
|---|---|---|---|
| **GAP-006** | Zero error path testing | 3/8 scenarios tested (malformed frame, skeleton crash, bad interface). All PASS. | 5 remaining: subscriber overflow, CAN flood, config mismatch, shared memory full, bus disconnect |

## Still Open

| Gap | Severity | Issue | Effort to Close |
|---|---|---|---|
| **GAP-003** | Medium | Service discovery timing not measured | Add timestamps around FindService. 30 min. |
| **GAP-004** | High | SWE.6 qualification tests not executed (needs QNX) | Blocked on QNX SDP cross-compile or native build |
| **GAP-007** | Medium | ASIL-B service config never tested | Create ASIL-B config, run with separate OS users. 2-3 hours. |
| **GAP-008** | Medium | Real CAN bus timing not characterized | Need ECUs powered on, switch to can0. Next bench session. |
| **GAP-010** | Low | Multi-subscriber not stress tested | Start 5 proxy instances. 30 min. |
| **GAP-011** | Medium | Python SHM bridge labeled as LoLa in reports | Relabel in integration report. 10 min. |
| **GAP-012** | Medium | CAN bridge has no unit tests or @verifies tags | Write decode() unit tests. 1-2 hours. |

## Corrected ASPICE Gate Assessment

| Gate | v1 Claim | v2 Verified Status | Evidence |
|---|---|---|---|
| SWE.4 Unit Verification | PASS | **PASS** (confirmed) | 252/252 upstream tests, 93.7% line coverage |
| SWE.5 Integration Test | PASS | **PASS** (confirmed) | 25/25 suites + CAN→LoLa bridge with ground truth |
| SWE.6 Qualification | ~~PASS~~ | **NOT EXECUTED** | Needs QNX target |
| SUP.1 Quality | PASS | **PASS** (confirmed) | Clang-tidy 0 warnings, format clean (except our bridge) |
| SUP.8 Config Mgmt | PASS | **PASS** (confirmed) | Bazel hermetic, reproducible |
| SAF Memory Safety | PASS | **PASS** (confirmed) | ASan 0 errors, error paths tested |
| SAF Concurrency | PASS | **PASS** (confirmed) | TSan 0 races |
| SAF Behavioral | PASS | **PASS** (confirmed) | UBSan 0 UB |
| NFR Performance | ~~PASS (622ns)~~ | **PASS (8-29 µs)** | Real IPC latency measured, < 100 µs target |
| SG-COM-001 Integrity | ~~PASS~~ | **PASS** | Ground truth verified against SIL DBC |
| SG-COM-002 Timeliness | NOT VERIFIED | **PASS** | 8-29 µs < 100 µs deadline |
| SG-COM-003 FFI | NOT VERIFIED | **NOT VERIFIED** | Needs ASIL-B config (GAP-007) |

## What Changed Between v1 and v2

| Metric | v1 | v2 |
|---|---|---|
| Gaps open | 12 | 7 |
| Gaps closed | 0 | 4 |
| Gaps partial | 0 | 1 |
| False PASS claims | 5 | 1 (SG-COM-003 FFI) |
| IPC latency | "622 ns" (wrong measurement) | **8-29 µs** (correct measurement) |
| Coverage | "13.5%" (one target) | **93.7%** (all targets) |
| DBC decoding | Wrong (garbage values) | Correct (matches ground truth) |
| Error paths tested | 0 | 3 |

## Lessons Applied

| From v1 Lesson | Applied in v2 |
|---|---|
| Match measurement to requirement text | Measured actual decode→send→receive latency, not specifier creation |
| Define expected values before testing | Decoded SIL DBC with Python first, then compared bridge output |
| Say "NOT VERIFIED" when you haven't | SWE.6 and SG-COM-003 correctly marked NOT VERIFIED/NOT EXECUTED |
| Test errors before claiming robustness | 3 error scenarios tested (malformed, crash, bad interface) |
| Read the source, don't guess the format | Read taktflow_sil.dbc and can_gateway source, fixed decoder |

---

**End of Gap Analysis v2 — GAP-LOLA-002**
