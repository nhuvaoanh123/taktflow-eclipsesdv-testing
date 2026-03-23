---
document_id: GAP-FEO-MULTI
title: "Multi-Perspective Gap Analysis -- 10 Stakeholder Views"
version: "1.0"
status: in_progress
date: 2026-03-23
---

# Multi-Perspective Gap Analysis -- FEO (Fixed Execution Order Scheduler)

Same work, 10 different eyes. Each stakeholder asks different questions.

FEO is a QM-rated deterministic scheduler written primarily in Rust (edition 2024)
with 8 crates, minimal C++ (feo_time.h bridge), Bazel 8.3.0 build system,
and Perfetto-based tracing infrastructure.

---

## 1. ASPICE Auditor

*"Show me the evidence chain."*

| Gap | Severity | Issue |
|---|---|---|
| TRLC declared but not active | High | TRLC configuration exists in the project but no `.trlc` requirement files are actively enforced. Zero requirements traced. An auditor sees a traceability tool claimed but not used -- that is worse than not claiming it at all. |
| No formal verification reports | High | Build and test have not been executed. No Bazel test output logs, no action counts, no pass/fail records. Zero evidence artifacts exist. |
| QM process documentation absent | Medium | QM classification appears in project config but no QM process plan exists. What review process applies to QM code? What testing level is required? Not documented. |
| No work product registry | Medium | 8 crates, 12 workspace members, 8 CI workflows -- but no document listing all work products and their configuration status. |
| SWE.3 detailed design missing | Medium | Scheduler algorithm (fixed execution order) is implemented in Rust but not documented. No design document describes the scheduling algorithm, cycle model, or activity lifecycle. |
| No change log or release notes | Low | Version 0.0.0 with no CHANGELOG.md. An auditor cannot determine what changed between revisions. |

**Verdict:** QM has a lower bar than ASIL, but the bar is not zero. Currently below QM Level 1 -- no evidence chain exists. TRLC claim without activation would be flagged as a process nonconformance.

**CLOSED items (pending laptop build):** Build evidence (GAP-001, GAP-002, GAP-003 from v1-initial) will close "no verification reports" when executed.

---

## 2. Security Engineer

*"What attack surfaces did you introduce?"*

| Gap | Severity | Issue |
|---|---|---|
| Linux SHM default has no access control | High | Default IPC backend uses Linux shared memory. Unless permissions are explicitly restricted, any process on the host can read/write scheduler state. Shared memory world-readable is a data integrity risk for a scheduler controlling ADAS activities. |
| iceoryx2 backend security properties unknown | High | When iceoryx2 is selected as IPC backend, what access control model applies? Does it use authenticated shared memory? What happens if a rogue process writes to the iceoryx2 segment? Not analyzed. |
| feo-tracer daemon runs as a separate process | Medium | The tracer daemon reads execution traces. If compromised, an attacker can observe all scheduler timing and activity ordering -- useful for side-channel attacks on deterministic systems. |
| No input validation on agent configuration | Medium | Agent configuration (activity definitions, execution order) loaded from files without schema validation or signature verification. A modified config could change execution order. |
| Protobuf deserialization in perfetto-model | Medium | prost-generated deserialization code processes trace data. Malformed protobuf could trigger panics or memory issues in the trace pipeline. |
| C++ FFI bridge (feo_time.h) is a trust boundary | Medium | Rust safety guarantees end at the FFI boundary. The C++ time bridge could introduce undefined behavior if called incorrectly. Only 1 C++ test exists for this boundary. |

**Verdict:** QM scheduler with world-readable shared memory controlling ADAS task execution. The deterministic ordering itself is a high-value target -- if an attacker can predict or modify execution order, they can influence vehicle behavior.

---

## 3. Performance Engineer

*"Where are the real numbers?"*

| Gap | Severity | Issue |
|---|---|---|
| No cycle latency measurements | Critical | The cycle-benchmark example exists but has never been run. For a deterministic scheduler, cycle time is THE metric. Zero numbers exist. |
| No jitter characterization | Critical | Fixed Execution Order implies low jitter. How low? Never measured. For ADAS task chains, jitter > 100 us may violate timing constraints. |
| No throughput measurement | High | How many activities per cycle? How many cycles per second? What is the overhead per activity? No performance model exists. |
| No memory allocation profiling | Medium | Rust's allocator behavior during scheduling cycles is unknown. Does the scheduler allocate during steady state? Any allocation in the hot path is a real-time violation. |
| Debug vs release build performance unknown | Medium | All work so far is file inspection. When build executes, will it be fastbuild (debug) or opt (release)? Performance numbers from debug builds are meaningless for production. |
| No comparison with alternative schedulers | Low | FEO vs. simple thread priority? FEO vs. AUTOSAR OS scheduling? No baseline comparison to justify the complexity of a custom scheduler framework. |

**Verdict:** A scheduler with zero performance data. The cycle-benchmark example is the right tool -- it just needs to be run and results captured with percentile distributions.

---

## 4. Deployment Engineer

*"How do I deploy this?"*

| Gap | Severity | Issue |
|---|---|---|
| No deployment guide | High | Zero documentation on deploying a FEO-scheduled application. How do you configure agents? How do you define activity execution order? What files go where? |
| Tracer daemon lifecycle undefined | High | feo-tracer is a binary daemon. How is it started? How does it connect to the scheduler? What happens if it crashes? No systemd unit, no container config, no orchestration. |
| Multi-agent config management missing | High | FEO supports multiple agents. How do you configure 3 agents with different activity sets? Config format not documented. No example with multiple agents deployed. |
| No health monitoring integration | Medium | FEO does not integrate with score-lifecycle health monitoring. If the scheduler hangs (missed deadline), nobody knows. No watchdog, no heartbeat. |
| Build requires specific Bazel version | Medium | Bazel 8.3.0 required. No Bazelisk wrapper, no version pinning mechanism documented. Developer gets wrong Bazel version, build fails with cryptic errors. |
| Rust 2024 edition toolchain requirement | Medium | Rust edition 2024 is very new. Deployment targets may not have this toolchain version. Cross-compilation and toolchain provisioning not addressed. |
| No resource limits defined | Low | No CPU affinity, no memory limits, no cgroup configuration for the scheduler process. On a shared HPC, resource contention with other S-CORE modules is likely. |

**Verdict:** The scheduler is a library/binary that nobody has deployed outside of test builds. Deployment story is entirely missing.

**CLOSED items (pending laptop build):** Build execution will establish that deployment is at least possible on x86_64-linux.

---

## 5. Upstream Eclipse S-CORE Maintainer

*"Are you using our API correctly?"*

| Gap | Severity | Issue |
|---|---|---|
| Rust 2024 edition creates toolchain requirements | High | Edition 2024 requires a very recent Rust compiler. Other S-CORE modules may not be ready for edition 2024 features. Integration builds across modules could fail. |
| Protobuf dependencies may conflict | Medium | perfetto-model uses prost for protobuf. Other S-CORE modules may use different protobuf versions or generators. Workspace-level dependency conflicts are likely. |
| iceoryx2 version compatibility | Medium | feo-com optionally depends on iceoryx2. If score-communication (LoLa) also uses iceoryx2, version conflicts could arise. No analysis of shared dependency compatibility. |
| score_communication 0.1.2 API contract untested | Medium | FEO depends on score_communication 0.1.2 but no test verifies the API contract. If LoLa changes its API, FEO breaks silently. |
| Bazel 8.3.0 requirement may conflict with other modules | Medium | Other S-CORE modules may target different Bazel versions. No module-level Bazel version compatibility matrix exists. |
| No contribution to upstream test suite | Low | FEO has integration tests but none run as part of the upstream S-CORE CI. FEO could break without upstream knowing. |

**Verdict:** FEO is a well-structured Rust project but its edge-of-ecosystem choices (Rust 2024 edition, prost protobuf, Bazel 8.3.0) create integration friction with the broader S-CORE ecosystem.

---

## 6. New Team Member (Onboarding)

*"How do I understand this?"*

| Gap | Severity | Issue |
|---|---|---|
| 8 crates with unclear relationships | High | feo, feo-com, feo-time, feo-tracing, feo-tracer, feo-cpp-build, feo-cpp-macros, perfetto-model. No architecture diagram shows how they relate. New person sees 8 directories and has to read all Cargo.toml files to understand dependency graph. |
| Agent/worker/activity/scheduler model not documented | High | FEO's core concepts (agents manage activities, scheduler dispatches to workers, signalling coordinates order) are only discoverable by reading Rust source code. No conceptual overview. |
| Rust 2024 edition uses unfamiliar features | Medium | Edition 2024 introduces new syntax and semantics. A developer familiar with Rust 2021 may be confused by new patterns. No migration guide or feature usage documentation. |
| Test agent usage not explained | Medium | test_agent/ exists as a full mock agent for testing. How do you write a new test scenario? What mock capabilities are available? Not documented. |
| C++ bridge (feo-time) crossing language boundary | Medium | Developers comfortable in Rust may not understand the C++ FFI in feo-time. Developers comfortable in C++ may not understand the Rust side. No bridge documentation. |
| Build system dual-track confusion | Low | Both Bazel BUILD files and Cargo.toml files exist. Which is authoritative? When do you use `bazel build` vs `cargo build`? Not explained. |

**Verdict:** A sophisticated Rust project that assumes deep familiarity with the domain, the language, and the build system. Onboarding time: days to weeks, not hours.

---

## 7. OEM Integration Engineer

*"Can I map my ADAS task chains to this scheduler?"*

| Gap | Severity | Issue |
|---|---|---|
| ADAS task chain mapping not demonstrated | High | The mini-adas example exists but its relationship to real ADAS task chains (perception -> fusion -> planning -> actuation) is not documented. How do you map a 10ms perception chain to FEO activities? |
| Deterministic scheduling guarantee not proven | High | FEO promises fixed execution order. No test proves this under realistic load. An OEM needs formal evidence that the scheduler maintains order under worst-case conditions. |
| Multi-rate scheduling not demonstrated | High | ADAS requires different task rates (10ms perception, 20ms fusion, 100ms planning). Does FEO support multi-rate scheduling? The single-rate cycle model may not be sufficient. |
| No AUTOSAR RTE mapping | Medium | OEMs using AUTOSAR expect RTE (Runtime Environment) compatibility. FEO is a custom scheduler with no AUTOSAR mapping. Integration requires a bridge layer. |
| No worst-case execution time (WCET) analysis | Medium | For safety-critical ADAS scheduling, WCET per activity is required. FEO provides no WCET analysis tooling or methodology. |
| Target platform unclear | Medium | FEO builds for x86_64-linux. OEM HPCs are typically aarch64 (ARM). Cross-compilation capability not verified. |

**Verdict:** FEO has the right architecture for ADAS scheduling but lacks the evidence an OEM needs: determinism proof, multi-rate support, WCET analysis, and a mapping methodology.

---

## 8. Regulatory / Compliance Officer

*"QM means lower bar, but does it mean no bar?"*

| Gap | Severity | Issue |
|---|---|---|
| QM with safety-relevant implications | High | FEO is QM-rated but controls execution order of potentially ASIL-rated activities. ISO 26262 Part 6 Clause 5 requires that QM elements providing services to ASIL elements be analyzed for interference. No Freedom From Interference (FFI) analysis exists. |
| No hazard analysis for scheduler failure modes | High | What happens if the scheduler misses a deadline? What if execution order is violated? What if a worker panics? These are safety-relevant failure modes even in a QM component. No FMEA or hazard analysis. |
| TRLC claimed but not active | Medium | Claiming a requirements traceability tool without using it creates a false impression of process maturity. A regulator would flag this as misleading. |
| No tool qualification for Bazel or rustc | Medium | Bazel 8.3.0 and rustc (edition 2024) are unqualified tools. For QM, this is acceptable under ISO 26262 but should be explicitly documented as a limitation. |
| No independent review of scheduler algorithm | Medium | The fixed execution order algorithm was implemented and tested by the same team. No independent review or formal verification of the scheduling logic. |
| No configuration management plan | Low | Version 0.0.0, no CHANGELOG, no release process. A regulator expects at least basic CM even for QM. |

**Verdict:** QM has a lower bar but deterministic scheduling sits at the boundary of safety-relevance. If ASIL-rated activities depend on FEO's execution order guarantee, FEO effectively becomes safety-relevant regardless of its own classification. FFI analysis is the critical missing piece.

---

## 9. Test Automation Engineer

*"Can I run this in CI?"*

| Gap | Severity | Issue |
|---|---|---|
| 8 CI workflows exist but results not captured | High | CI pipeline exists but we have not collected any run results. No logs, no artifacts, no pass/fail history. The pipeline may be green or permanently broken -- unknown. |
| Integration test agent not documented | High | test_agent/ provides mock agent capabilities but no documentation on how to write new test scenarios. CI cannot expand test coverage without understanding the framework. |
| No test result parsing | Medium | Bazel test output is in its own format. No JUnit XML conversion, no structured JSON output for CI dashboard integration. |
| cycle-benchmark not in CI | Medium | The cycle-benchmark example should run in CI as a performance regression gate. Currently, benchmark results are not captured or tracked. |
| No fuzz testing | Medium | Rust code can still be fuzzed (cargo-fuzz). The protobuf deserialization, configuration parsing, and FFI boundary are all fuzz targets. Zero fuzz campaigns exist. |
| No coverage measurement | Medium | `bazel coverage` or cargo-tarpaulin not configured. Test coverage percentage unknown for all 8 crates. |
| TRLC not integrated in CI | Low | TRLC declared but not active means CI cannot enforce requirement traceability. Even if activated later, CI integration is missing. |

**Verdict:** Good CI infrastructure (8 workflows) but zero captured results. The test agent framework is a strength but its documentation gap limits CI expansion. Run the pipeline, capture the results, add coverage -- that closes most gaps.

**CLOSED items (pending laptop build):** Executing `bazel build //...` and `bazel test //...` will produce the first CI-equivalent results.

---

## 10. System Architect

*"How does FEO fit with LoLa and the rest of S-CORE?"*

| Gap | Severity | Issue |
|---|---|---|
| FEO + LoLa integration not tested | Critical | FEO schedules activities, LoLa provides IPC. The core integration point -- scheduling LoLa send/receive on cycle boundaries -- has never been tested. This is THE use case for both modules together. |
| Communication middleware dependency unclear | High | feo-com provides IPC for FEO. LoLa (score-communication) also provides IPC. Which is used when? Does FEO use feo-com internally and LoLa for external communication? The architectural boundary is not clear. |
| No lifecycle integration | High | FEO does not integrate with score-lifecycle. Scheduler process not supervised, no health monitoring, no graceful shutdown via lifecycle manager. |
| No orchestrator integration | Medium | FEO agents are not managed by score-orchestrator. No workload manifest, no dynamic agent deployment. |
| Tracer daemon is a standalone process | Medium | feo-tracer runs independently. In a production system, it should be managed by the lifecycle/orchestrator. Currently orphaned. |
| Cross-module Bazel build not verified | Medium | Building FEO alongside LoLa, lifecycle, persistency in a single workspace has never been attempted. Module dependency conflicts are likely. |
| No hardware abstraction for time | Medium | feo-time provides time primitives but relies on Linux clock_gettime. On QNX or bare-metal, a different time source is needed. Platform portability not verified. |
| score_logging integration depth unknown | Low | FEO depends on score_logging 0.1.2 but how deeply is logging integrated? Are scheduler decisions logged? Can you debug execution order from logs? |

**Verdict:** FEO is designed to be the scheduling backbone for S-CORE applications, but it has been developed and tested in isolation. The LoLa+FEO integration is the single most important gap to close -- it is the reason both modules exist. Until scheduler-driven IPC is demonstrated, FEO and LoLa are two separate proofs of concept.

**CLOSED items (pending laptop build):** Build execution will prove FEO compiles with its declared S-CORE dependencies.

---

## Cross-Perspective Summary

| Perspective | Gap Count | Key Theme |
|---|---|---|
| ASPICE Auditor | 6 | TRLC claimed not active, zero evidence artifacts, no process docs |
| Security Engineer | 6 | World-readable SHM, no input validation, FFI trust boundary |
| Performance Engineer | 6 | Zero performance numbers, no cycle latency, no jitter data |
| Deployment Engineer | 7 | No deploy guide, tracer lifecycle undefined, toolchain requirements |
| Upstream Maintainer | 6 | Rust 2024 edition friction, protobuf/Bazel version conflicts |
| New Team Member | 6 | 8 crates unclear, agent/worker model undocumented, dual build system |
| OEM Integration | 6 | No ADAS mapping, no determinism proof, no multi-rate, no WCET |
| Regulatory | 6 | QM with safety implications, no FFI analysis, no hazard analysis |
| Test Automation | 7 | 8 CI workflows but zero results captured, no fuzz, no coverage |
| System Architect | 8 | FEO+LoLa untested, no lifecycle/orchestrator, isolated development |

**Total unique gaps identified: 64**

**Top recurring themes:**
1. **Zero execution evidence** -- file structure verified, build never run
2. **Determinism claimed, not proven** -- core FEO guarantee has no test
3. **FEO + LoLa integration is the missing centerpiece** -- both exist in isolation
4. **TRLC declared but inactive** -- worse than not claiming traceability
5. **QM with safety-relevant implications** -- scheduler controls ASIL activity execution

---

**The honest conclusion:** FEO is architecturally sound -- 8 well-structured Rust crates, a clean agent/worker/activity model, Perfetto tracing, and dual IPC backends. The code structure suggests a mature design. But from every perspective except "does the code exist?", the evidence is zero. No build output, no test results, no performance numbers, no integration with LoLa, no deployment documentation. The most critical gap is not any individual item -- it is that FEO and LoLa have never been tested together, despite being designed as complementary modules (deterministic scheduling + deterministic IPC). Closing the build/test gaps (4 hours of effort) will dramatically improve the picture. Closing the FEO+LoLa integration gap requires a focused effort but would prove the core value proposition of both modules.
