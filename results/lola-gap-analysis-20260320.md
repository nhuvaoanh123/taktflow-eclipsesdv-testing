---
document_id: GAP-LOLA-001
title: "Gap Analysis — LoLa Integration Assessment"
version: "1.0"
status: active
date: 2026-03-20
severity_scale: "Critical > High > Medium > Low"
---

# LoLa Gap Analysis

Honest assessment of what was verified, what was claimed but not verified,
and what was never attempted.

---

## 1. Verified (Genuine PASS)

These results are real and backed by evidence:

| Claim | Evidence | Confidence |
|---|---|---|
| LoLa upstream builds | `bazel build //...` exit 0, 6465 actions | High |
| 252/252 upstream tests pass | Bazel test output, all PASSED | High |
| ASan finds zero memory errors | `--config=asan_ubsan_lsan` all 252 PASS | High |
| TSan finds zero data races | `--config=tsan` all 224 PASS | High |
| Clang-tidy zero warnings | 841 files analyzed, exit 0 | High |
| IPC bridge example works | Skeleton published, proxy received samples 3+4, hash validated | High |
| Our CAN bridge compiles in Bazel | `bazel build //...can_bridge` exit 0, 490 actions | High |
| CAN bridge skeleton reads from vcan0 | 500 frames read, process didn't crash | Medium |
| Proxy received 20 samples from skeleton | Sequence numbers in output | Medium |
| vcan0 and can_gateway.main unaffected | PID same, traffic flowing after test | High |

---

## 2. Claimed But Not Actually Verified

These appear as PASS in the test reports but the evidence doesn't support the claim:

### GAP-001: NFR-COM-001 Latency Mis-Verified (High)

**Claim:** "IPC latency < 100 µs — PASS (622 ns)"

**Reality:** The 622 ns benchmark measures `InstanceSpecifier::Create()` — a string parsing operation. It does NOT measure:
- Skeleton `Allocate()` → `Send()` time
- Shared memory write latency
- Message passing notification latency
- Proxy `GetNewSamples()` callback invocation time
- End-to-end CAN frame → proxy callback time

**What's needed:** Instrument the CAN bridge with timestamps:
```cpp
auto t0 = steady_clock::now();  // before Send()
// ... in proxy callback:
auto t1 = steady_clock::now();  // on receive
auto latency = t1 - t0;        // actual IPC latency
```

**Status:** NOT VERIFIED. Remove PASS from reports.

---

### GAP-002: SG-COM-001 Data Integrity Not Verified (High)

**Claim:** "Data integrity — PASS (signal values consistent)"

**Reality:** We never compared decoded values against expected values. The RPM shows 41293, 58077, etc. from CAN ID 0x220 — but we don't know:
- What the SIL vECU actually encodes in 0x220
- What the correct decoded RPM should be
- Whether our `decode()` function produces correct output

The existing IPC bridge hash validation (samples 3+4) verifies LoLa's transport integrity, not our signal decoder's correctness.

**What's needed:**
1. Get the actual SIL DBC/encoding for CAN ID 0x220
2. Send a known CAN frame with known values via `cansend`
3. Verify decoded output matches expected values exactly

**Status:** NOT VERIFIED. Remove PASS from reports.

---

### GAP-003: FR-COM-003 Service Discovery Timing Not Measured (Medium)

**Claim:** "Service discovery — PASS (FindService succeeded)"

**Reality:** FindService succeeded, but we never measured how long it took. The requirement may have a timing constraint. We just know it didn't hang.

**What's needed:** Log timestamp before `FindService()` and after handle returned. Report actual discovery time.

**Status:** PARTIALLY VERIFIED (functional yes, timing no).

---

### GAP-004: ASPICE SWE.6 Qualification Claims Premature (High)

**Claim:** "SWE.6 Qualification Test — PASS"

**Reality:** The SWE.6 qualification test plan defines 8 tests (QT-COM-001 through QT-COM-008) that must run on QNX. We ran zero of them. The live test on Linux is an integration test (SWE.5), not a qualification test (SWE.6).

**Status:** NOT EXECUTED. SWE.6 should say "NOT STARTED."

---

## 3. Never Attempted

### GAP-005: DBC Decoding Correctness (High)

**Problem:** CAN ID 0x220 is decoded as `motor_rpm = uint16 at offset 0`. The SIL vECU (`can_gateway.main`) uses its own encoding that we haven't looked at. RPM values of 41293, 58077 are clearly wrong — no motor runs at 58000 RPM.

**Root cause:** We assumed a DBC layout without checking the actual SIL source code.

**Fix:** Read `can_gateway.main` source, extract the actual CAN frame encoding for 0x220, 0x600, 0x601. Update `decode()` to match.

---

### GAP-006: Error Path Testing (High)

None of these were tested:

| Error Scenario | What could happen | Tested? |
|---|---|---|
| Skeleton crash during Send() | Proxy gets stale data or error | No |
| Proxy crash during GetNewSamples() | Skeleton continues, shared memory leaked? | No |
| Malformed CAN frame (short DLC) | Buffer overread in decode()? | No |
| CAN socket disconnected | Skeleton hangs on read()? | No |
| Shared memory full (all slots used) | Allocate() returns error — handled? | No |
| 5+ simultaneous proxies | Resource exhaustion? | No |
| Service config mismatch | Wrong eventId, wrong serviceId | No |
| CAN bus flood (100% utilization) | Skeleton can't keep up? | No |

**Fix:** Write explicit negative test cases for each scenario.

---

### GAP-007: ASIL-B Service Configuration (Medium)

**Problem:** All tests used `"asil-level": "QM"` in the config. No test used ASIL-B configuration which involves:
- Separate shared memory regions per ASIL level
- Different OS users for ASIL-B vs QM processes
- ASIL-B specific error handling paths

**Fix:** Create a second config with `"asil-level": "ASIL_B"`, run with separate user accounts, verify memory isolation.

---

### GAP-008: Real CAN Bus Timing (Medium)

**Problem:** All tests used vcan0 (virtual CAN — zero propagation delay, zero bus arbitration). Real CAN at 500 kbps has:
- ~230 µs per standard frame
- Bus arbitration delays under load
- Error frames and retransmission

**Fix:** Run with `can0` (physical USB CAN adapter) and powered ECUs. Measure end-to-end latency from ECU transmission to proxy callback.

---

### GAP-009: Full Code Coverage (Medium)

**Problem:** Reported 13.5% coverage from one test target. This number is meaningless. Full coverage across all 252 tests was never measured.

**Fix:** Run `bazel coverage //...` (all targets). Takes 30+ minutes. Report actual line/branch coverage for ASIL-B components (target: 80% branch per our SWE.4 plan).

---

### GAP-010: Multi-Subscriber Stress Test (Low)

**Problem:** Config allows 5 subscribers. We only tested 1 proxy. The upstream `multiple_proxies` integration test exists but wasn't run with our CAN bridge.

**Fix:** Start 5 proxy instances simultaneously, verify all receive data without loss.

---

### GAP-011: Python SHM Bridge Is Not LoLa (Medium)

**Problem:** The Python `can-lola-bridge.py` (Section 8.2 in integration report) uses POSIX `/dev/shm` directly — it does NOT use the LoLa API. It "mimics" the pattern but doesn't prove LoLa integration. The report presents it alongside actual LoLa results, which is misleading.

**Fix:** Either label it clearly as "non-LoLa proof of concept" or remove it from LoLa-specific reports. The C++ `can_bridge` binary IS the real LoLa integration.

---

### GAP-012: CAN Bridge Code Quality (Medium)

**Problem:** The CAN bridge `main.cpp` was written for speed, not quality:
- No error handling on `read()` partial reads
- `decode()` uses `memcpy` without endianness checks (assumes little-endian)
- No MISRA/AUTOSAR C++ compliance
- No unit tests for `decode()` function
- No `@safety_req` or `@verifies` tags

**Fix:** Write unit tests for `decode()` with known CAN frames. Add error handling. Add traceability tags.

---

## 4. Report Corrections Required

The following statements in existing reports need to be corrected:

| Report | Current Claim | Corrected Claim |
|---|---|---|
| `lola-assessment-20260320.md` | "NFR (Performance) — PASS (622 ns baseline)" | "NFR — NOT VERIFIED (622 ns measures specifier creation, not IPC latency)" |
| `lola-integration-report-20260320.md` | "SWE.6 (Qualification) — PASS" | "SWE.6 — NOT EXECUTED (requires QNX target)" |
| `lola-integration-report-20260320.md` | "SG-COM-001 Data integrity — PASS" | "SG-COM-001 — PARTIALLY VERIFIED (LoLa transport OK, signal decoder unverified)" |
| `lola-can-bridge-test-report-20260320.md` | "Requirements Verified: NFR-COM-001" | "NFR-COM-001 — NOT VERIFIED (latency not measured)" |
| `lola-can-bridge-test-report-20260320.md` | "Requirements Verified: SG-COM-001" | "SG-COM-001 — NOT VERIFIED (no ground truth comparison)" |

---

## 5. Priority Order for Closing Gaps

| Priority | Gap | Effort | Impact |
|---|---|---|---|
| 1 | GAP-005: Get actual SIL DBC, fix decoder | 1 hour | Fixes all signal values |
| 2 | GAP-001: Instrument actual IPC latency | 1 hour | Real NFR-COM-001 number |
| 3 | GAP-002: Test with known CAN frames + expected values | 1 hour | Proves data integrity |
| 4 | GAP-006: Error path tests (at least crash + malformed) | 2-3 hours | Safety evidence |
| 5 | GAP-012: Unit tests for decode() | 1-2 hours | Code quality |
| 6 | GAP-009: Full coverage run | 30 min (just run it) | Real coverage number |
| 7 | GAP-010: Multi-subscriber test | 30 min | Scalability evidence |
| 8 | GAP-007: ASIL-B config test | 2-3 hours | Safety classification |
| 9 | GAP-008: Real CAN bus test | Next bench session | Physical timing |
| 10 | GAP-004: QNX qualification | Needs SDP | Target platform |
| 11 | GAP-011: Relabel Python bridge | 10 min | Report accuracy |

**Total effort to close gaps 1-7:** ~8 hours of focused work.

---

## 6. Lessons Learned

| # | Lesson | Principle |
|---|---|---|
| 1 | A number is not a verification unless it measures what the requirement asks | **Match measurement to requirement text word-for-word** |
| 2 | "It runs" is not "it works" — output must be compared to expected values | **Always define expected values before testing** |
| 3 | Volume of documentation does not compensate for missing evidence | **One honest test > ten impressive documents** |
| 4 | Happy path testing creates false confidence | **Test errors before claiming robustness** |
| 5 | Speed of delivery pressures toward overclaiming | **Say "NOT VERIFIED" when you haven't verified** |
| 6 | Assumed encodings cause silent failures | **Read the source, don't guess the format** |

---

**End of Gap Analysis GAP-LOLA-001**
