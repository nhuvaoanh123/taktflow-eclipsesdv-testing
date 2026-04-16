---
document_id: TS-001
title: "Eclipse SDV + S-CORE Testing Strategy"
version: "2.0"
status: active
date: 2026-03-21
lessons_from: "LoLa pilot (score-communication) — 66 gaps found, 22 closed"
aligned_with: "Eclipse S-CORE upstream testing practices (researched 2026-03-21)"
---

# Testing Strategy

Current-state note: this strategy document preserves the original cross-ecosystem
test model and lessons learned. The active local pytest entry point today is
`modules/` (per `pytest.ini`), and some QNX references below are historical or
upstream-context notes rather than the current default Pi target.

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

---

## 11. CI/CD Pipeline (Aligned with S-CORE Upstream)

S-CORE runs 6 CI workflows per module. We adopt the same pattern.

### 11.1 Required Workflows Per Module

```yaml
# .github/workflows/{module}-build.yml
on: [push, pull_request]
jobs:
  build_and_test:
    runs-on: ubuntu-24.04
    strategy:
      matrix:
        config: ["", "--config=linux_x86_64_score_gcc_12_2_0_posix"]
    steps:
      - uses: actions/checkout@v4
        with: {submodules: recursive}
      - uses: bazel-contrib/setup-bazel@0.18.0
      - run: bazel build ${{ matrix.config }} //...
      - run: bazel test ${{ matrix.config }} //... --build_tests_only

  sanitizers:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
        with: {submodules: recursive}
      - uses: bazel-contrib/setup-bazel@0.18.0
      - run: bazel test --config=asan_ubsan_lsan //... --build_tests_only
      - run: bazel test --config=tsan //... --build_tests_only

  coverage:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
        with: {submodules: recursive}
      - uses: bazel-contrib/setup-bazel@0.18.0
      - run: bazel coverage //... --combined_report=lcov
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: bazel-out/_coverage/_coverage_report.dat

  regression:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
        with: {submodules: recursive}
      - run: |
          sudo modprobe vcan
          sudo ip link add vcan0 type vcan
          sudo ip link set up vcan0
      - run: bash scripts/regression-test-lola.sh
```

### 11.2 Quality Gates (Blocking PR Merge)

| Gate | Threshold | Upstream Practice |
|---|---|---|
| Build | Exit 0, zero warnings | Same |
| Unit tests | 100% pass | Same |
| ASan/UBSan/LSan | Zero violations | Same |
| TSan | Zero data races | Same (excluded from integration tests) |
| Coverage | >80% line for ASIL-B components | Same |
| Regression | All known-input tests pass | Our addition |
| Format | clang-format clean | Same |
| Copyright | Headers present | Same |

---

## 12. Integration Test Environments (Aligned with S-CORE)

### 12.1 Docker (Linux Testing)

S-CORE uses OCI images built by Bazel with `rules_oci`. We adopt their pattern:

```
Environment: Ubuntu 24.04 Docker container
Shared memory: 1 GB (required for LoLa)
Init process: enabled (signal handling)
Auto-cleanup: container removed after test
Packages: bash, binutils, coreutils, libatomic1, libstdc++6
```

**Usage:** `bazel test //quality/integration_testing/...`

Already works — we just haven't used it. S-CORE's Docker integration
test infrastructure is in `score-communication/quality/integration_testing/`.

### 12.2 QNX QEMU (Target Testing)

S-CORE runs QNX in QEMU for CI target testing:

```
Runner: QEMU aarch64 or x86_64 user-mode
Serial: Multi-serial-port harness (16 channels)
Process isolation: Each process gets dedicated serial device
Exit code: Sentinel line in serial output ("EXIT_CODE=N")
```

**Status:** Blocked by toolchains_qnx#46 (checksum stale).
When unblocked, `score-communication/quality/integration_testing/environments/qnx8_qemu/`
has the full QEMU runner ready.

### 12.3 Physical Bench (Our Addition)

Not in S-CORE upstream — this is our contribution:

```
CAN interface: can0 (USB CAN adapter to physical ECUs)
ECUs: STM32 (G474RE, F413ZH, L552ZE) + TMS570
Bus: 500 kbps, 120Ω terminated
Signals: Decoded per taktflow_vehicle.dbc + taktflow_sil.dbc
```

---

## 13. Traceability Automation (Aligned with S-CORE TRLC/Lobster)

### 13.1 Upstream Approach

S-CORE uses TRLC (requirement language) + Lobster (traceability engine):

```
Requirements (.trlc)  →  Lobster config  →  Traceability report
     ↑                       ↑                     ↑
  AssumedSystemReq       lobster_*.yaml       auto-generated
  FeatReq                maps types to         shows gaps,
  CompReq                Lobster needs          orphans,
  FailureMode                                   coverage
  AoU (control measures)
```

The `safety_software_unit` Bazel rule links everything:
```python
safety_software_unit(
    reqs = [":requirements.trlc"],    # What to build
    impl = [":source_files"],          # Code that implements it
    design = [":plantuml_diagrams"],   # How it's designed
    tests = [":unit_tests"],           # How it's verified
)
```

### 13.2 Our Adoption Path

**Phase 1 (now):** Continue with markdown requirements + `@verifies` tags.
Use `trace-gen.py` pattern from taktflow-embedded for automated validation.

**Phase 2 (Sprint 2):** Convert 65 requirements to TRLC format.
Install TRLC + Lobster. Generate automated traceability reports.

**Phase 3 (Sprint 4):** Adopt `safety_software_unit` Bazel rule for
our bridge code. Full automated req→design→impl→test linkage.

### 13.3 Tag Convention (Immediate)

In C++ source code:
```cpp
/// @safety_req SSR-COM-SHM-001
void SharedMemoryLayout::writeSlot() { ... }
```

In C++ test code:
```cpp
/// @verifies SWR-COM-SHM-001
TEST(SharedMemTest, WriteSlot_CRC) { ... }
```

In Python test code:
```python
@pytest.mark.verifies("SWR-COM-SHM-001")
def test_write_slot_crc():
```

---

## 14. Verification Methods Catalog (Aligned with S-CORE Process)

S-CORE defines 8 verification methods. We track which ones we apply per module.

| # | Method | Description | Applied to LoLa? |
|---|---|---|---|
| 1 | **Structural coverage** | Statement + branch coverage (white-box) | YES — 93.7% line |
| 2 | **Interface testing** | Parameter passing, data format, protocol, error, stress | YES — CAN decoder, LoLa API |
| 3 | **Fault injection** | Error code injection, data corruption, process crash | PARTIAL — crash + malformed tested |
| 4 | **Boundary value analysis** | Min, max, just-above, just-below, nominal | YES — DLC 0-8, max values |
| 5 | **Equivalence classes** | Valid, invalid, special input partitions | PARTIAL — valid + invalid DLC |
| 6 | **Fuzz testing** | Semi-random malformed input | YES — edge-case CAN frames |
| 7 | **Inspection** | Manual code walkthrough | NO — not done |
| 8 | **Analysis** | Control/data flow analysis | NO — not done |

**Rule:** For ASIL-B components, methods 1-6 are mandatory.
Methods 7-8 are recommended.

Each test file should declare which method it implements:
```python
class TestDecoder:
    """Verification method: boundary value analysis (#4) + equivalence classes (#5)."""
```

---

## 15. Static Analysis (Aligned with S-CORE CodeQL)

### 15.1 Upstream Practice

S-CORE uses CodeQL with MISRA-C++ coding standards:
```bash
bazel test --config=codeql //...
# → SARIF output + CSV report
```

Plus clang-tidy with project-specific `.clang-tidy` config.

### 15.2 Our Practice

| Tool | Status | Target |
|---|---|---|
| clang-tidy | Running (0 warnings on LoLa) | Continue — gate in CI |
| CodeQL/MISRA | Not yet | Add for our bridge code |
| cppcheck | Not yet | Consider for bridge code |
| Clippy (Rust) | N/A | When Rust modules tested |

**Rule:** Static analysis must run before claiming code quality.
"Compiles without error" is not "code quality verified."

---

## 16. Multi-Config Matrix Testing (Aligned with S-CORE)

S-CORE tests with 3+ compiler configs per PR:

| Config | Compiler | Purpose |
|---|---|---|
| Default | GCC 15.2.0 | Primary development |
| LLVM | Clang 19.1.7 | Cross-compiler validation |
| GCC 12 | GCC 12.2.0 | S-CORE standard toolchain |
| QNX | QCC 12.2.0 | Target platform |
| Release | `-c opt` | Performance measurement |

**Our practice:** Test with at least default + release configs.
Add LLVM when CI pipeline is set up.

---

## 17. Test Metadata and Derivation (Aligned with S-CORE)

S-CORE annotates each test with:
- **TestType:** What method was used (boundary, fuzz, interface, etc.)
- **DerivationTechnique:** How the test was derived (requirement, risk, experience)
- **RequirementLink:** Which requirement this test verifies

**Our adoption:** Add to every test function:
```python
@pytest.mark.metadata(
    method="boundary_value_analysis",
    derived_from="SWR-COM-SHM-001",
    platform="x86_64-linux",
)
def test_decode_lidar_max_distance():
    """Boundary: max distance_cm = 1200 (DBC range [0|1200])."""
```

---

## 18. Cross-Module Integration (Aligned with S-CORE Reference Integration)

S-CORE's `score-reference_integration` repo builds all modules together
and runs feature integration tests across module boundaries.

**Our equivalent:** Build and test S-CORE modules together:

```
Phase 1 (done): LoLa alone — 252 tests pass
Phase 2 (next): LoLa + baselibs — verify shared memory foundation
Phase 3: LoLa + lifecycle — health monitoring of LoLa processes
Phase 4: LoLa + persistency — store vehicle signals
Phase 5: Full stack — all S-CORE modules + CAN bridge
```

Each phase requires:
1. All previous phase modules still build together
2. New module's upstream tests pass
3. Cross-module integration test passes
4. No regression in previous module tests

---

## 19. Summary: Our Strategy vs Upstream

| Practice | S-CORE Upstream | Our Strategy v2 | Status |
|---|---|---|---|
| CI per PR | 6 workflows | Defined in §11 | To implement |
| Multi-config matrix | 3+ configs | 2 configs (default + release) | To implement |
| Docker integration | OCI + custom runner | Use their infra directly | Ready |
| QNX QEMU | Multi-serial harness | Use their infra when unblocked | Blocked |
| TRLC requirements | Full TRLC pipeline | Phase 1: markdown, Phase 2: TRLC | Phase 1 |
| Lobster traceability | Automated | Phase 1: manual, Phase 2: Lobster | Phase 1 |
| CodeQL/MISRA | SARIF output | To add | To implement |
| 8 verification methods | All defined | 6/8 applied to LoLa | Ongoing |
| Test metadata | Per-test annotation | Defined in §17 | To implement |
| Reference integration | Cross-module build | Defined in §18 | Phase 1 done |
| Sanitizers | ASan+UBSan+LSan+TSan | Same | Done |
| Coverage | >80% line ASIL-B | 93.7% achieved for LoLa | Done |
| Real hardware testing | Not in upstream | Our bench (CAN + ECUs) | Done |
| Multi-perspective review | Not in upstream | 10 perspectives, 66 gaps | Done |
| Ground truth verification | Not in upstream | DBC decode comparison | Done |

**Key insight:** S-CORE has better automation and process rigor.
We have better real-world validation and gap discovery methodology.
The combined strategy is stronger than either alone.
