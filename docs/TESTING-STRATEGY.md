---
document_id: TS-001
title: "Eclipse SDV + S-CORE Testing Strategy"
version: "1.0"
status: active
date: 2026-03-21
lessons_from: "LoLa pilot (score-communication) — 66 gaps found, 22 closed"
---

# Testing Strategy

## 1. Purpose

This document defines how we test Eclipse SDV and S-CORE modules on the
Taktflow bench. It encodes lessons learned from the LoLa pilot where we
built fast, claimed PASS prematurely, and then spent equal time correcting
false claims through 5 iterations of gap analysis.

**Core principle: a test is not verified until the measurement matches
the requirement text and the output is compared to a known expected value.**

---

## 2. Test Levels

| Level | What It Proves | Who Runs It | Where |
|---|---|---|---|
| **Build** | Code compiles without error | CI / developer | Laptop |
| **Unit** | Upstream tests pass (their code) | CI | Laptop |
| **Integration** | Our code works with their code | CI + manual | Laptop + vcan0 |
| **E2E** | Full data path from hardware to application | Manual | Laptop + can0 + ECUs |
| **Performance** | Latency, throughput, memory under load | Manual | Laptop (debug + release) |
| **Security** | Input validation, access control, crash resilience | Manual | Laptop + vcan0 |
| **Regression** | Known inputs produce known outputs | CI | Laptop + vcan0 |

---

## 3. Test Hierarchy

```
tests/
├── {module}/              One directory per submodule
│   ├── build/             Does it compile?
│   ├── unit/              Do upstream tests pass?
│   ├── integration/       Does our code talk to their code?
│   ├── e2e/               Does data flow end-to-end on real hardware?
│   ├── performance/       How fast? How stable over time?
│   ├── security/          What happens with bad input?
│   └── regression/        Do known inputs give known outputs?
├── common/
│   ├── utils/bazel.py     Bazel build/test helpers
│   ├── utils/can.py       CAN frame encode/decode per DBC
│   └── fixtures/          Known test data
└── bench/
    ├── can/               Physical CAN bus tests
    ├── qnx/               QNX Pi target tests
    └── hil/               Full bench with all ECUs
```

---

## 4. Lessons Learned (From LoLa Pilot)

### 4.1 Measurement Must Match Requirement

**Problem:** We reported "NFR-COM-001 PASS (622 ns)" but 622 ns measured
`InstanceSpecifier::Create()` — a string parsing function. The requirement
asks for IPC latency (skeleton → shared memory → proxy callback).

**Rule:** Before claiming a requirement is verified:
1. Read the requirement text word-for-word
2. Identify what physical quantity it specifies
3. Instrument the exact code path that implements it
4. Measure that path, not something nearby

**Correct measurement:** 8-29 µs (debug), 9-25 µs (release) for actual
decode → allocate → send → receive → callback path.

### 4.2 Always Define Expected Values Before Testing

**Problem:** CAN bridge decoded RPM as 41293, 58077 from SIL traffic.
We said "values received — PASS" without knowing what the correct RPM
should be. The values were garbage — we were decoding the wrong CAN ID.

**Rule:** Before any integration test:
1. Read the DBC / source code of the data sender
2. Calculate the expected decoded value by hand or with Python
3. Compare bridge output to expected value
4. Only report PASS if values match within specified tolerance

**Example:** SIL sends 0x601 with bytes `00 00 FA 00 38 31 00 00`.
Python decode: `current=0mA, temp=250dC=25.0°C, batt=12600mV, RPM=0`.
Bridge output: `Ia=0A, Tm=25C, rpm=0`. Match confirmed.

### 4.3 "It Runs" Is Not "It Works"

**Problem:** CAN bridge received 20 samples from proxy — we claimed
data integrity PASS. But we never verified a single decoded value
against the actual CAN frame bytes.

**Rule:** Running without crash is a build test, not a functional test.
Functional verification requires:
- Known input (specific CAN frame bytes)
- Known expected output (decoded signal values)
- Assertion that actual output equals expected output

### 4.4 Don't Guess the Data Format

**Problem:** We assumed CAN ID 0x220 was "motor RPM" based on our own
`can-sim.py` definitions. The actual SIL uses 0x220 for `Lidar_Distance`
(from `taktflow_vehicle.dbc`). Our decoder was completely wrong.

**Rule:** Always read the authoritative source:
- DBC file for CAN signal encoding
- protobuf/TRLC file for API contracts
- Source code of the sender for actual behavior

Never assume — read, then verify.

### 4.5 Volume of Documentation ≠ Quality of Verification

**Problem:** We created 768 docs, 168 requirements, 320 bidirectional
links. Impressive numbers. But they described what SHOULD be tested,
not what WAS tested. The reports had 5 false PASS claims.

**Rule:** One honest test with measured values is worth more than
ten impressive documents. Don't write the report before running the test.

### 4.6 Test Errors Before Claiming Robustness

**Problem:** All initial testing was happy-path only. When we finally
tested error paths (malformed frames, skeleton crash, CAN flood),
everything worked — but we hadn't checked before claiming robustness.

**Rule:** Error path tests are mandatory for safety claims:
- Malformed/short input
- Process crash during operation
- Resource exhaustion (memory, file descriptors, queue full)
- Invalid configuration
- Network/bus disconnection

### 4.7 Stress Tests Find Real Bugs

**Problem:** Multi-subscriber test (5 proxies) found FINDING-001 —
concurrent proxy creation causes abort. This is a real LoLa bug that
252 upstream tests didn't catch because they start proxies sequentially.

**Rule:** Always test concurrency limits:
- Max subscribers simultaneously
- Max message rate
- Max payload size
- Maximum uptime (hours, not seconds)

### 4.8 Distinguish Platform Testing from Code Testing

**Problem:** We proved LoLa works on Linux laptop. But the target
platform is QNX on Pi. "Works on Linux" ≠ "works on QNX." The QNX
dispatch test was skipped, ASIL-B mode crashes on Linux (by design).

**Rule:** Label every test result with the platform:
- "PASS on x86_64-linux" is not "PASS on aarch64-qnx"
- "PASS on vcan0" is not "PASS on can0"
- "PASS in debug build" is not "PASS in release build"

### 4.9 File Upstream Issues, Don't Just Document Them

**Problem:** We found 3 issues in upstream S-CORE code but initially
only documented them internally. They existed as "findings" in our gap
analysis, invisible to the upstream maintainers.

**Rule:** When you find an upstream issue:
1. Reproduce it reliably
2. Write minimal reproduction steps
3. File a GitHub issue immediately (not "later")
4. Reference the issue number in your test report

Filed: communication#220 (proxy crash), toolchains_qnx#46 (checksum).

### 4.10 Multi-Perspective Review Finds More Than Single-Lens Testing

**Problem:** Our v1-v5 gap analysis (test engineer perspective) found
12 gaps. The 10-perspective analysis found 66 gaps. We missed 54 gaps
by only looking through one lens.

**Rule:** After completing testing, review results from at least 3
additional perspectives:
- Security: what can an attacker exploit?
- Performance: what are the real numbers (percentiles, not averages)?
- Deployment: can someone else run this without your help?

---

## 5. Test Execution Protocol

### 5.1 Before Testing a New Module

```
1. Read the module's README and architecture docs
2. Read the actual DBC/proto/config files (don't assume)
3. Identify upstream tests and run them first
4. Define expected values for integration tests (Python decode)
5. Set up regression test with known inputs BEFORE testing
```

### 5.2 During Testing

```
1. Run build first — if it fails, stop and fix
2. Run upstream unit tests — verify THEIR code works
3. Run our integration tests — verify OUR code with THEIR code
4. For every numeric claim, record:
   - What exactly was measured
   - What requirement it maps to
   - What the expected value was
   - What the actual value was
5. Test at least 3 error paths before claiming robustness
```

### 5.3 After Testing

```
1. Write test report with measured values, not assumptions
2. Mark anything not measured as "NOT VERIFIED"
3. Run multi-perspective gap analysis (at least security + performance)
4. File upstream issues for any bugs found
5. Update traceability matrix with actual evidence links
```

---

## 6. Platform Matrix

| Platform | Interface | Build | Use For |
|---|---|---|---|
| x86_64-linux (laptop) | vcan0 | `bazel build //...` | Development, SIL, CI |
| x86_64-linux (laptop) | can0 | `bazel build //...` | Real ECU integration |
| x86_64-linux (laptop) | release | `bazel build -c opt //...` | Performance measurement |
| aarch64-qnx (Pi) | — | cross-compile or native | Target qualification |
| aarch64-linux (Pi) | — | cross-compile | Alternative target |

**Rule:** Every test result must specify which row it was measured on.

---

## 7. Acceptance Criteria Per Level

### Build
- Exit code 0
- No warnings (or warnings explicitly accepted)

### Unit
- All upstream tests pass (100%)
- Coverage measured and recorded (target: >80% line for ASIL-B)

### Integration
- Known input → expected output (with tolerance)
- Ground truth verified (DBC decode or sender source code)
- At least 3 error paths tested

### E2E
- Physical hardware in the loop (real CAN bus, real ECUs)
- Signal values match physical state
- Latency measured with percentiles (p50, p95, p99)

### Performance
- Debug AND release builds measured
- Percentile distribution (not just min/max)
- Memory stability over time (>2 minutes minimum)
- Jitter measured (max - min)

### Security
- Edge-case inputs (DLC 0, max values, malformed)
- Process crash recovery
- Access control verified (if applicable)

### Regression
- Known CAN frames with known expected decoded values
- Automated (scriptable, CI-runnable)
- Exit code 0 = all pass, non-zero = failure

---

## 8. Known Infrastructure Gaps

| Gap | Impact | Workaround |
|---|---|---|
| No CI pipeline | Tests run manually via SSH | Run `assess-lola.sh` + `regression-test-lola.sh` |
| QNX cross-compile broken | Can't test on target | Test on Linux, document platform limitation |
| No devcontainer | Can't reproduce environment | Use `setup-lola-env.sh` on Ubuntu 24.04 |
| CAN hardware needed for E2E | CI can't run E2E | CI uses vcan0, E2E requires manual bench session |
| ASIL-B needs QNX | Can't verify freedom from interference | Document as blocked, test QM path only |

---

## 9. Reporting Template

Every test report must include:

```markdown
## Environment
- Host, OS, kernel, CPU, RAM
- Build type (debug/release)
- CAN interface (vcan0/can0)
- Module version (git commit)

## Test Results
| Test ID | Requirement | Expected | Actual | Match | Platform |

## Measurements (if performance)
| Metric | p50 | p95 | p99 | Max | Build |

## Error Paths Tested
| Scenario | Expected Behavior | Actual | PASS/FAIL |

## Known Limitations
- What was NOT tested and why
- Platform restrictions
- Upstream issues encountered
```

---

## 10. Findings Register

All findings (bugs, issues, unexpected behavior) tracked here and filed upstream.

| ID | Severity | Module | Description | Upstream Issue | Status |
|---|---|---|---|---|---|
| FINDING-001 | High | score-communication | Concurrent proxy crash (3+ proxies) | communication#220 | Open |
| FINDING-002 | Medium | score-toolchains_qnx | Checksum stale, cross-compile broken | toolchains_qnx#46 | Open |
| FINDING-003 | Info | score-communication | ASIL-B mode is QNX-only (correct behavior) | — | By design |

---

**This strategy was written after making every mistake listed in Section 4.
Follow it to avoid making them again.**
