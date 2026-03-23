---
document_id: GAP-FEO-001
title: "Gap Analysis -- FEO Integration Assessment"
version: "1.0"
status: active
date: 2026-03-23
severity_scale: "Critical > High > Medium > Low"
---

# FEO Gap Analysis

Honest assessment of what was verified, what was claimed but not verified,
and what was never attempted for score-feo (Fixed Execution Order scheduler).

---

## 1. Verified (Genuine PASS)

These results are real and backed by file inspection evidence:

| Claim | Evidence | Confidence |
|---|---|---|
| MODULE.bazel declares score_feo v0.0.0 | File exists, name and version parsed | High |
| 8 crates present in workspace | src/feo, feo-com, feo-time, feo-tracing, feo-tracer, feo-cpp-build, feo-cpp-macros, perfetto-model directories exist | High |
| Root Cargo.toml has workspace with 12 members | [workspace] section with members array | High |
| Cargo.lock pins all Rust dependencies | File exists at root | High |
| Key dependencies declared in MODULE.bazel | score_communication 0.1.2, score_baselibs 0.2.4, score_logging 0.1.2 | High |
| C++ API surface is feo_time.h only | Single header in src/feo-time/include/ | High |
| Examples exist | mini-adas and cycle-benchmark directories present | High |
| Integration test harness exists | tests/rust/feo_tests/ and test_agent/ directories | High |
| CI workflows present | 8 workflow files exist | Medium |

---

## 2. Claimed But Not Actually Verified

These appear plausible from file inspection but require build execution to confirm:

### GAP-001: Build Not Executed (High)

**Claim:** "FEO builds successfully with Bazel 8.3.0"

**Reality:** `bazel build --config=x86_64-linux //...` has not been run. File structure looks correct but build success is unverified. Rust 2024 edition requires specific toolchain version.

**What's needed:** Execute build on Linux laptop, capture action count and exit code.

**Status:** NOT VERIFIED. Pending laptop execution.

---

### GAP-002: Tests Not Executed (High)

**Claim:** "13 feo-time unit tests pass, 1 C++ test passes"

**Reality:** Test files exist but `bazel test //...` has not been run. Cannot confirm pass count, failure modes, or test coverage.

**What's needed:** Run `bazel test --config=x86_64-linux //...`, capture per-target results.

**Status:** NOT VERIFIED. Pending laptop execution.

---

### GAP-003: Lint Not Verified (Medium)

**Claim:** "Rust linting passes with --config=lint-rust"

**Reality:** `.bazelrc` defines the lint-rust config but it has not been executed. Unknown whether codebase has lint warnings.

**What's needed:** Run `bazel build --config=lint-rust //...`, capture warning count.

**Status:** NOT VERIFIED. Pending laptop execution.

---

## 3. Never Attempted

### GAP-004: TRLC Requirements Traceability Not Active (High)

**Problem:** TRLC is declared in the project (configuration files reference it) but no active TRLC checks exist. There are no `.trlc` files actively enforcing requirements traceability. For a deterministic scheduler, requirements like "activities execute in declared order" need formal tracing.

**Fix:** Either activate TRLC with requirement definitions for scheduler guarantees, or document why QM classification exempts this.

---

### GAP-005: Deterministic Scheduling Guarantee Not Tested (High)

**Problem:** FEO's core promise is Fixed Execution Order -- activities execute in a deterministic sequence. No test verifies this guarantee under load, with multiple agents, or across scheduler cycles. The mini-adas example demonstrates the pattern but is not a correctness proof.

**Fix:** Write a test that defines an execution order, runs 10,000 cycles, and asserts order is maintained every cycle. Measure jitter.

---

### GAP-006: IPC Backend Switching Not Tested (Medium)

**Problem:** feo-com supports Linux SHM (default) and iceoryx2 (optional). No test verifies that switching between backends produces identical behavior. Feature-gated code paths are a classic source of bugs.

**Fix:** Run the same integration test suite with both backends, compare results.

---

### GAP-007: Cycle Latency Not Measured (High)

**Problem:** The cycle-benchmark example exists but no latency numbers have been captured. For a deterministic scheduler, cycle time distribution (p50/p95/p99) is the critical performance metric.

**Fix:** Run cycle-benchmark, capture 10,000+ cycles, report percentile distribution.

---

### GAP-008: Multi-Agent Deployment Not Tested (Medium)

**Problem:** FEO supports multi-agent deployment (test_agent exists for testing). No test verifies agent lifecycle (start, execute, stop) with multiple concurrent agents.

**Fix:** Write integration test with 3+ agents, verify all complete their scheduled activities without deadlock.

---

### GAP-009: Tracer Daemon Integration Not Tested (Medium)

**Problem:** feo-tracer exists as a binary daemon for collecting Perfetto traces. No test verifies that the tracer correctly collects traces from feo-tracing instrumentation and produces valid Perfetto format output.

**Fix:** Run a traced scheduler cycle, collect output with feo-tracer, validate Perfetto format.

---

### GAP-010: C++ Time Bridge Correctness (Medium)

**Problem:** feo_time.h provides C++ access to FEO time primitives. Only 1 C++ test exists. The FFI boundary between Rust and C++ is a known source of undefined behavior (lifetime issues, type mismatches).

**Fix:** Add C++ tests for edge cases: zero duration, overflow, concurrent access. Run with AddressSanitizer.

---

### GAP-011: Protobuf Model Compatibility (Low)

**Problem:** perfetto-model uses prost for protobuf code generation. No test verifies that generated traces are compatible with the Perfetto UI (ui.perfetto.dev). Format version skew is possible.

**Fix:** Generate a trace, load it in Perfetto UI, verify it renders correctly.

---

### GAP-012: Cross-Module Integration with LoLa (Medium)

**Problem:** FEO is designed to work with LoLa (score-communication) for deterministic data exchange. No test verifies FEO scheduling LoLa send/receive operations on cycle boundaries. This is the core integration point for the ADAS use case.

**Fix:** Write an integration test where FEO schedules LoLa skeleton.Send() and proxy.GetNewSamples() at specific cycle phases.

---

## 4. Priority Order for Closing Gaps

| Priority | Gap | Effort | Impact |
|---|---|---|---|
| 1 | GAP-001: Execute build | 15 min (just run it) | Confirms buildability |
| 2 | GAP-002: Execute tests | 15 min (just run it) | Real test results |
| 3 | GAP-005: Deterministic order test | 2-3 hours | Core FEO guarantee |
| 4 | GAP-007: Cycle latency benchmark | 1 hour | Performance baseline |
| 5 | GAP-003: Execute lint | 10 min | Code quality baseline |
| 6 | GAP-004: TRLC activation | 4-8 hours | Requirements traceability |
| 7 | GAP-006: IPC backend comparison | 2-3 hours | Backend equivalence |
| 8 | GAP-008: Multi-agent test | 2-3 hours | Deployment correctness |
| 9 | GAP-010: C++ bridge edge cases | 1-2 hours | FFI safety |
| 10 | GAP-012: FEO+LoLa integration | 4-8 hours | System integration |
| 11 | GAP-009: Tracer validation | 1-2 hours | Observability chain |
| 12 | GAP-011: Perfetto compatibility | 30 min | Trace format |

**Total effort to close gaps 1-5:** ~4 hours of focused work.

---

## 5. Lessons Learned (Provisional)

| # | Lesson | Principle |
|---|---|---|
| 1 | File existence proves structure, not correctness | **Build it and test it before claiming it works** |
| 2 | QM classification does not mean "no testing needed" | **Deterministic scheduling has implicit safety requirements** |
| 3 | Optional features (iceoryx2) create untested code paths | **Test every feature combination, not just the default** |
| 4 | TRLC declared but not active is worse than no TRLC | **Active tooling or remove the claim** |
| 5 | 8 crates means 28 potential dependency edges to test | **Workspace complexity grows quadratically** |

---

**End of Gap Analysis GAP-FEO-001**
