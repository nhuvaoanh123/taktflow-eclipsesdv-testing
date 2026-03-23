---
document_id: GAP-LC-MULTI
title: "Multi-Perspective Gap Analysis — score-lifecycle"
version: "1.0"
status: verified
date: 2026-03-23
---

# Multi-Perspective Gap Analysis — score-lifecycle

Same work, 10 different eyes. Each stakeholder asks different questions.

Bench results: score_lifecycle_health v0.0.0 — BUILD PASS (59 targets, 1,087 actions, 232s), 5/6 unit tests PASS, dual-language C++17 + Rust, 13 CI workflows.

---

## 1. ASPICE Auditor

*"Show me the evidence chain."*

| # | Gap | Status | Fix Path | Effort |
|---|------|--------|----------|--------|
| 1.1 | Build evidence captured with full action count and timing | CLOSED | Bench log: 59 targets, 1,087 actions, 232s on 16-core laptop. Reproducible. | Done |
| 1.2 | Unit test results documented with pass/fail per target | CLOSED | 5/6 PASS with named targets. Smoke failure root-caused to missing fakechroot (environment, not code). | Done |
| 1.3 | No formal verification report (SWE.4) | OPEN | Create verification report linking test results to requirements. Currently just console logs. | 2d |
| 1.4 | No traceability matrix (requirements to tests) | OPEN | Map each health monitoring requirement to its test target. Module has no explicit requirements doc. | 3d |
| 1.5 | Version 0.0.0 — no baseline for assessment | OPEN | Upstream must release v0.1.0+ before any process assessment can reference a controlled baseline. | Blocked upstream |
| 1.6 | Coverage targets defined (C++ >=76%, Rust >=93%) but not measured | OPEN | Run `bazel coverage` targets and capture lcov/llvm-cov reports. Targets exist in CI but not executed locally. | 1d |
| 1.7 | No independent review of test evidence | OPEN | All bench execution by single engineer. ASPICE SWE.4 requires review by someone other than the author. | 1d |
| 1.8 | Sanitizer results missing (SWE.4 robustness) | OPEN | ASan/TSan/UBSan targets not yet run. Required for robustness evidence in verification report. | 1d |

**Verdict:** Build and unit test evidence is solid (CLOSED). But no verification report, no traceability, no coverage, no sanitizers — would fail ASPICE Level 2 on verification completeness.

---

## 2. Security Engineer

*"A daemon with watchdog and health monitoring — what can go wrong?"*

| # | Gap | Status | Fix Path | Effort |
|---|------|--------|----------|--------|
| 2.1 | Launch Manager daemon privilege level unknown | OPEN | Audit whether launch_manager requires root or CAP_SYS_ADMIN. Daemon managing process lifecycle likely needs elevated privileges. Document minimum required capabilities. | 2d |
| 2.2 | IPC between clients and daemon not authenticated | OPEN | Control Client, Lifecycle Client, Recovery Client communicate with Launch Manager — no mutual authentication. Any local process could send lifecycle commands. | 3d |
| 2.3 | FlatBuffers config deserialization not fuzz-tested | OPEN | 3 .fbs schemas parsed at startup. Malformed flatbuffer could crash daemon. Run flatbuffers verifier + fuzz with libFuzzer. | 2d |
| 2.4 | Watchdog interface (IWatchdogIf) not tested for missed deadlines | OPEN | WatchdogImpl in saf/ subsystem — no test verifies behavior when watchdog is NOT petted. Miss path is safety-critical. | 2d |
| 2.5 | Rust FFI boundary is an attack surface | OPEN | C++/Rust FFI uses `unsafe` blocks. No audit of memory safety at boundary. Miri not yet run on FFI paths. | 3d |
| 2.6 | stub_supervisor_api_client feature flag disables security in tests | OPEN | Rust tests use stub that bypasses real supervisor API. Verify stub is never compiled into production binary. Feature flag audit needed. | 1d |
| 2.7 | Only 2 mocks — insufficient for security isolation testing | OPEN | applicationcontextmock and lifecyclemanagermock only. No mock for watchdog, recovery, or process state — can't test error paths in isolation. | 3d |

**Verdict:** Health monitoring daemon is a high-value target. Zero security hardening verified. Watchdog miss path untested. FlatBuffers not fuzzed.

---

## 3. Performance Engineer

*"What are the supervision cycle times?"*

| # | Gap | Status | Fix Path | Effort |
|---|------|--------|----------|--------|
| 3.1 | Build performance characterized | CLOSED | 232s for 1,087 actions on 16-core laptop. Dual C++/Rust compilation. Baseline established. | Done |
| 3.2 | No supervision cycle time measurement | OPEN | Health Monitor performs alive/deadline/logical supervision — cycle period and jitter never measured. Critical for real-time guarantees. | 2d |
| 3.3 | Daemon startup latency unknown | OPEN | Launch Manager cold start time not measured. For fast vehicle boot, startup budget matters (target: <500ms). | 1d |
| 3.4 | Recovery action latency unknown | OPEN | Time from fault detection to recovery action (process restart, escalation) never measured. Recovery time objective undefined. | 2d |
| 3.5 | Loom concurrency tests pass but no real contention benchmarks | OPEN | Rust loom tests verify correctness under model-checked schedules, not real-world contention. Multi-core stress test needed. | 2d |
| 3.6 | No memory profiling of long-running daemon | OPEN | Launch Manager is a long-running daemon. No heap profiling, no leak detection over extended runtime. | 1d |
| 3.7 | FlatBuffers config parse time not profiled | OPEN | 3 schemas parsed at startup. For large configs (100+ supervised processes), parse time could dominate boot. | 1d |

**Verdict:** Build time characterized. Zero runtime performance data. For a health monitoring daemon, supervision timing is the critical metric — and it's completely unmeasured.

---

## 4. Deployment Engineer

*"How do I deploy a lifecycle daemon?"*

| # | Gap | Status | Fix Path | Effort |
|---|------|--------|----------|--------|
| 4.1 | Docker demo available | CLOSED | Upstream provides Docker-based demo for launch_manager. Deployment at least prototyped. | Done |
| 4.2 | 4 example applications available | CLOSED | control_application, cpp_lifecycle_app, cpp_supervised_app, rust_supervised_app — demonstrate deployment patterns. | Done |
| 4.3 | No systemd service file for launch_manager | OPEN | Daemon has no .service unit file. No Type=notify, no watchdog integration with systemd, no restart policy. | 1d |
| 4.4 | FlatBuffers config management not documented | OPEN | 3 .fbs schemas define configuration — no documentation on how to author, validate, or version config files for deployment. | 2d |
| 4.5 | No rollback procedure for daemon upgrade | OPEN | v0.0.0 with no release process. No documented procedure to rollback daemon binary + config if upgrade fails. | 1d |
| 4.6 | QNX deployment path untested | OPEN | qnx/ platform directory exists but QNX build not verified on bench. Only Linux tested. | 3d |
| 4.7 | OSAL platform abstraction not validated cross-platform | OPEN | linux/, qnx/, posix/ directories exist. Only linux/ exercised. No deployment test on QNX or bare POSIX. | 3d |

**Verdict:** Docker demo and examples provide a starting point (CLOSED). But no systemd integration, no config management, no cross-platform deployment validation.

---

## 5. Upstream Eclipse S-CORE Maintainer

*"Is the API stable enough to depend on?"*

| # | Gap | Status | Fix Path | Effort |
|---|------|--------|----------|--------|
| 5.1 | Dependencies clearly declared | CLOSED | score_baselibs (0.2.4), score_logging (0.1.0), score_baselibs_rust (0.1.0), flatbuffers, googletest — all versioned and documented. | Done |
| 5.2 | Depended on by score_inc_time — validates API usage | CLOSED | At least one downstream consumer exists, proving API is consumable. | Done |
| 5.3 | Version 0.0.0 despite 218 commits — API contract unstable | OPEN | No semver guarantees. Any commit could break downstream. Need v0.1.0 release with changelog. | Blocked upstream |
| 5.4 | Rust/C++ FFI boundary not documented | OPEN | Dual-language module with FFI — no documentation of which functions cross the boundary, ownership semantics, or ABI stability. | 2d |
| 5.5 | FlatBuffers schema versioning undefined | OPEN | 3 .fbs schemas with no schema evolution policy. Adding/removing fields could break config compatibility. | 2d |
| 5.6 | 13 CI workflows — most of any module but reference-integration disabled | OPEN | reference-integration workflow disabled. The most important workflow for downstream consumers is off. | 1d |
| 5.7 | score_baselibs_rust at 0.1.0 — Rust ecosystem immature | OPEN | Rust dependency at 0.1.0 suggests Rust support is experimental. Breaking changes likely. | Blocked upstream |

**Verdict:** Dependencies properly declared. But v0.0.0 with disabled reference-integration means no API stability guarantee. Downstream consumers (score_inc_time) are at risk.

---

## 6. New Team Member (Onboarding)

*"C++ AND Rust? How do I even start?"*

| # | Gap | Status | Fix Path | Effort |
|---|------|--------|----------|--------|
| 6.1 | 4 example applications cover both languages | CLOSED | cpp_lifecycle_app, cpp_supervised_app for C++ devs; rust_supervised_app for Rust devs; control_application for API usage. Good on-ramp. | Done |
| 6.2 | Docker demo lowers entry barrier | CLOSED | Can run the system without building from source. Good first experience. | Done |
| 6.3 | Dual-language build is complex (C++17 + Rust + Bazel) | OPEN | 1,087 build actions across two toolchains. New member needs C++, Rust, AND Bazel expertise. No "getting started" guide for this combination. | 2d |
| 6.4 | Component architecture not visually documented | OPEN | Launch Manager, Health Monitor, Control Client, Lifecycle Client, Process State Client, Recovery Client — no architecture diagram showing relationships. | 1d |
| 6.5 | Health monitoring concepts (alive/deadline/logical supervision) not explained | OPEN | Three supervision types from AUTOSAR — no primer explaining what each does, when to use which, or how they interact. | 2d |
| 6.6 | Only 2 mocks — hard to write isolated tests | OPEN | New team member wanting to add tests can only mock ApplicationContext and LifecycleManager. Other components require integration test setup. | 3d |
| 6.7 | Rust feature flags (stub_supervisor_api_client) undocumented | OPEN | Feature flag changes test behavior. No explanation of which flags exist, what they do, or when to use them. | 1d |

**Verdict:** Examples and Docker demo are excellent on-ramps (CLOSED). But dual-language complexity, missing architecture docs, and sparse mocks make independent contribution hard.

---

## 7. OEM Integration Engineer

*"Can I use this for ECU lifecycle management?"*

| # | Gap | Status | Fix Path | Effort |
|---|------|--------|----------|--------|
| 7.1 | Health monitoring covers AUTOSAR supervision types | CLOSED | Alive supervision, deadline supervision, logical supervision — all three AUTOSAR Watchdog Manager concepts implemented. | Done |
| 7.2 | Watchdog integration via IWatchdogIf abstraction | CLOSED | Clean interface for external watchdog hardware. WatchdogImpl in saf/ provides reference implementation. | Done |
| 7.3 | No AUTOSAR Adaptive Platform lifecycle state mapping | OPEN | AUTOSAR AP defines FunctionGroupStates (Running, Verify, etc.). No mapping document showing how score-lifecycle states correspond. | 2d |
| 7.4 | No ara::phm compatibility layer | OPEN | AUTOSAR Platform Health Management (ara::phm) defines standardized health monitoring API. Score-lifecycle uses custom API, no adapter. | 5d |
| 7.5 | ECU startup/shutdown sequence not mapped | OPEN | OEMs define strict boot sequences (BSWM → COM → APP). Launch Manager startup ordering must align. No mapping exists. | 3d |
| 7.6 | No multi-ECU lifecycle coordination | OPEN | Single-node lifecycle only. No coordination protocol for lifecycle state across multiple ECUs (vehicle-level state machine). | 5d |
| 7.7 | QNX platform (typical OEM HPC OS) not validated | OPEN | qnx/ directory exists but QNX build/test not executed. Most OEM HPCs run QNX 7.1+. | 3d |

**Verdict:** Health monitoring architecture aligns well with AUTOSAR concepts (CLOSED). But no AUTOSAR API compatibility, no multi-ECU coordination, and QNX untested.

---

## 8. Regulatory / ISO 26262 Compliance

*"Can the health monitor be part of the safety case?"*

| # | Gap | Status | Fix Path | Effort |
|---|------|--------|----------|--------|
| 8.1 | Unit tests exist for core safety components | CLOSED | health_monitoring_lib tested with C++ tests, Rust unit tests, AND Rust loom concurrency tests. Three test types provide multi-angle verification. | Done |
| 8.2 | Watchdog subsystem exists in saf/ directory | CLOSED | Safety-related code separated into saf/ subsystem. Architectural separation supports freedom from interference argument. | Done |
| 8.3 | No FMEA for health monitoring failure modes | OPEN | What if Health Monitor itself crashes? What if watchdog petting is delayed by OS scheduling? No failure mode analysis. | 3d |
| 8.4 | No safety manual for integrators | OPEN | ISO 26262-8 Clause 12 requires SEooC safety manual. No document defines assumptions of use, safety mechanisms, or ASIL capability. | 5d |
| 8.5 | Loom tests verify concurrency but not to ISO 26262 standard | OPEN | Loom model-checks thread interleavings — excellent for correctness. But no mapping to ISO 26262 Part 6 Clause 9 (verification of software units). | 2d |
| 8.6 | No diagnostic coverage analysis for watchdog | OPEN | Watchdog is a safety mechanism. ISO 26262-5 Table D.5 requires diagnostic coverage metrics. WatchdogImpl not analyzed. | 3d |
| 8.7 | Tool qualification for Rust compiler missing | OPEN | Rust compiler (rustc) used for safety-related health monitoring code. No TQL per ISO 26262-8 Clause 11. Rust is not yet qualified by any tool vendor. | 5d |
| 8.8 | No dependent failure analysis (DFA) | OPEN | Health Monitor and Launch Manager run on same CPU, share memory. Common cause and cascading failure analysis required. | 3d |

**Verdict:** Good architectural foundations — safety code separated, multi-type testing including concurrency verification (CLOSED). But no FMEA, no safety manual, no diagnostic coverage, no tool qualification. Cannot be part of a safety case today.

---

## 9. Test Automation Engineer

*"13 CI workflows — what actually works?"*

| # | Gap | Status | Fix Path | Effort |
|---|------|--------|----------|--------|
| 9.1 | Build verified: 59 targets, 1,087 actions | CLOSED | Full build passes. Reproducible on 16-core laptop in 232s. | Done |
| 9.2 | 5/6 unit tests pass | CLOSED | Only smoke test fails due to missing fakechroot (environment issue, not code bug). Core functionality verified. | Done |
| 9.3 | 13 CI workflows defined (most of any S-CORE module) | CLOSED | build, test, coverage, format, copyright, clippy, miri, license, gitlint, qnx8, bzlmod, reference-integration, docs-cleanup. Comprehensive pipeline. | Done |
| 9.4 | Smoke test blocked by fakechroot dependency | OPEN | integration/smoke:smoke requires fakechroot not available in bench environment. Need to install fakechroot or create Docker-based test environment. | 1d |
| 9.5 | Miri and clippy defined but not executed locally | OPEN | CI has miri and clippy workflows. Not run on bench. Miri would catch undefined behavior in unsafe Rust/FFI code. | 1d |
| 9.6 | Coverage targets exist but not executed | OPEN | CI has coverage workflow. Not run locally. Need lcov for C++ and llvm-cov for Rust. Targets: C++ >=76%, Rust >=93%. | 1d |
| 9.7 | reference-integration workflow disabled | OPEN | The integration test workflow is disabled upstream. Most valuable for catching cross-module regressions. | Blocked upstream |
| 9.8 | No local test orchestration script | OPEN | No single `./run-all-tests.sh` that replicates what CI does. Must run 13 workflows manually to reproduce CI locally. | 1d |

**Verdict:** Strong CI foundation (13 workflows, CLOSED). Build and unit tests verified. But sanitizers, coverage, miri, and clippy not yet executed locally. reference-integration disabled upstream.

---

## 10. System Architect

*"How does lifecycle fit the Taktflow architecture?"*

| # | Gap | Status | Fix Path | Effort |
|---|------|--------|----------|--------|
| 10.1 | Build proves lifecycle can coexist with LoLa in S-CORE ecosystem | CLOSED | Both score-lifecycle and score-lola (mw/com) build successfully. Dependency chain validated: baselibs → logging → lifecycle. | Done |
| 10.2 | Downstream dependency (score_inc_time) validates architectural role | CLOSED | score_inc_time depends on score_lifecycle — proves lifecycle is a foundational module in the S-CORE stack. | Done |
| 10.3 | LoLa processes not managed by lifecycle | OPEN | LoLa skeleton/proxy processes (tested in previous bench) run standalone. Not supervised by Launch Manager. Integration gap. | 3d |
| 10.4 | No orchestrator integration | OPEN | score-orchestrator should define workload manifests that Launch Manager executes. Not tested together. | 3d |
| 10.5 | Multi-process supervision architecture not validated | OPEN | Launch Manager manages multiple processes. Never tested with >2 supervised processes simultaneously. Scalability unknown. | 2d |
| 10.6 | Recovery escalation policy not tested | OPEN | Health Monitor detects faults → Recovery Client acts. But escalation chain (restart → reset → safe state) never exercised end-to-end. | 3d |
| 10.7 | Platform abstraction (OSAL) limits portability claims | OPEN | linux/, qnx/, posix/ exist but only Linux validated. Architecture assumes portability not yet proven. | 3d |
| 10.8 | FEO (Fixed Execution Order) integration with supervision cycles | OPEN | Health monitoring supervision should align with FEO deterministic scheduling. No integration point defined. | 3d |

**Verdict:** Lifecycle is correctly positioned as a foundational module (CLOSED). But no integration with LoLa, orchestrator, or FEO. Multi-process supervision and recovery escalation untested.

---

## Cross-Perspective Summary

| # | Perspective | Gaps | Closed | Open | Blocked | Key Theme |
|---|-------------|------|--------|------|---------|-----------|
| 1 | ASPICE Auditor | 8 | 2 | 5 | 1 | Evidence captured but no formal reports or traceability |
| 2 | Security Engineer | 7 | 0 | 7 | 0 | Daemon attack surface unaudited, watchdog miss path untested |
| 3 | Performance Engineer | 7 | 1 | 6 | 0 | Build profiled, zero runtime supervision timing data |
| 4 | Deployment Engineer | 7 | 2 | 5 | 0 | Docker demo exists, no systemd or cross-platform deployment |
| 5 | Upstream Maintainer | 7 | 2 | 3 | 2 | Dependencies clean, v0.0.0 means no API stability |
| 6 | New Team Member | 7 | 2 | 5 | 0 | Examples excellent, dual-language complexity undocumented |
| 7 | OEM Integration | 7 | 2 | 5 | 0 | AUTOSAR supervision concepts match, no API compatibility |
| 8 | Regulatory (ISO 26262) | 8 | 2 | 6 | 0 | Safety architecture exists, no FMEA/safety manual/TQL |
| 9 | Test Automation | 8 | 3 | 4 | 1 | 13 CI workflows + 5/6 tests pass, sanitizers/coverage not run |
| 10 | System Architect | 8 | 2 | 6 | 0 | Foundational role proven, no integration with other modules |

**Total gaps identified: 74**
**Closed: 18 (24%)** | **Open: 52 (70%)** | **Blocked upstream: 4 (5%)**

---

## Priority Roadmap

### Phase 1: Complete Verification (Week 1) — 7 gaps

| Priority | Gap | Perspective | Effort |
|----------|-----|-------------|--------|
| P0 | Run sanitizers (ASan/TSan/UBSan) | ASPICE, Regulatory | 1d |
| P0 | Run coverage (C++ >=76%, Rust >=93%) | ASPICE, Test Auto | 1d |
| P0 | Run miri + clippy locally | Test Automation | 1d |
| P0 | Fix smoke test (install fakechroot) | Test Automation | 1d |
| P1 | Create local test orchestration script | Test Automation | 1d |
| P1 | Measure supervision cycle time | Performance | 2d |
| P1 | Measure daemon startup latency | Performance | 1d |

### Phase 2: Documentation & Security (Weeks 2-3) — 12 gaps

| Priority | Gap | Perspective | Effort |
|----------|-----|-------------|--------|
| P1 | Architecture diagram (components + relationships) | New Team Member | 1d |
| P1 | AUTOSAR lifecycle state mapping | OEM Integration | 2d |
| P1 | FlatBuffers config documentation | Deployment | 2d |
| P1 | Audit Launch Manager privilege requirements | Security | 2d |
| P1 | Fuzz FlatBuffers deserialization | Security | 2d |
| P2 | Rust/C++ FFI boundary documentation | Upstream, New Team | 2d |
| P2 | Health monitoring supervision primer | New Team Member | 2d |
| P2 | FlatBuffers schema versioning policy | Upstream | 2d |
| P2 | Feature flag documentation | New Team Member | 1d |
| P2 | Verification report (SWE.4) | ASPICE | 2d |
| P2 | Traceability matrix | ASPICE | 3d |
| P2 | systemd service file | Deployment | 1d |

### Phase 3: Safety & Integration (Weeks 4-6) — 14 gaps

| Priority | Gap | Perspective | Effort |
|----------|-----|-------------|--------|
| P2 | FMEA for health monitoring | Regulatory | 3d |
| P2 | Diagnostic coverage analysis for watchdog | Regulatory | 3d |
| P2 | Dependent failure analysis (DFA) | Regulatory | 3d |
| P2 | LoLa process supervision integration | System Architect | 3d |
| P2 | Multi-process supervision scalability test | System Architect | 2d |
| P2 | Recovery escalation end-to-end test | System Architect | 3d |
| P3 | Safety manual (SEooC) | Regulatory | 5d |
| P3 | ara::phm compatibility layer | OEM Integration | 5d |
| P3 | Multi-ECU lifecycle coordination | OEM Integration | 5d |
| P3 | QNX build and test validation | Deployment, OEM | 3d |
| P3 | Orchestrator integration | System Architect | 3d |
| P3 | FEO integration | System Architect | 3d |
| P3 | Rust compiler tool qualification | Regulatory | 5d |
| P3 | Additional mocks for isolation testing | Security, New Team | 3d |

### Blocked — Requires Upstream Action

| Gap | Blocker | Action |
|-----|---------|--------|
| v0.0.0 — no API stability | Upstream release process | Monitor for v0.1.0 release |
| reference-integration CI disabled | Upstream decision | File issue requesting re-enablement |
| score_baselibs_rust at 0.1.0 | Rust ecosystem maturity | Track upstream Rust API stabilization |
| ASPICE baseline assessment | Needs versioned release | Blocked by v0.0.0 |

---

**The honest conclusion:** score-lifecycle has the strongest CI infrastructure of any S-CORE module (13 workflows) and a solid architecture (health monitoring with three AUTOSAR supervision types, safety-separated watchdog, dual-language implementation). Our bench verified 5/6 tests pass and the full build works. That's 18 gaps CLOSED from real evidence. But 52 gaps remain OPEN — zero runtime performance data, zero security audit, no safety case artifacts, and no integration with other S-CORE modules. The v0.0.0 version number is honest: this is pre-release software with production-grade ambitions but prototype-grade verification.
