---
document_id: GAP-LC-REGISTER
status: initial
date: 2026-03-22
---

# Consolidated Gap Register: score_lifecycle_health v0.0.0

## Overview

This register consolidates gaps from 6 perspectives adapted for a daemon/service module (not just a library). score_lifecycle_health includes the Launch Manager daemon and Health Monitor library, requiring analysis beyond typical library-level concerns.

**Total gaps:** 34
**Status:** All open (initial assessment)

---

## Perspective 1: ASPICE Auditor (6 gaps)

| ID        | Gap                                        | Severity | Fix Path                                                        | Effort |
|-----------|--------------------------------------------|----------|-----------------------------------------------------------------|--------|
| ASPICE-01 | No SWE.4 unit test traceability            | High     | Map 5 test targets to SWE.3 design elements                    | 1 SP   |
| ASPICE-02 | Missing SWE.5 integration test plan        | High     | Create integration test plan for daemon + client libs           | 2 SP   |
| ASPICE-03 | No SWE.6 qualification test for daemon     | Medium   | Define qualification criteria for Launch Manager daemon         | 2 SP   |
| ASPICE-04 | Coverage metrics not linked to requirements| Medium   | Map C++ 76% / Rust 93% targets to requirement coverage          | 1 SP   |
| ASPICE-05 | No change impact analysis process          | Medium   | Establish CIA for dual C++/Rust codebase changes                | 1 SP   |
| ASPICE-06 | CI workflow documentation incomplete       | Low      | Document all 13 CI workflows with purpose and trigger conditions| 1 SP   |

## Perspective 2: Safety Engineer (6 gaps)

Focus: Health monitor alive/deadline/logical supervision has safety-relevant aspects.

| ID       | Gap                                          | Severity | Fix Path                                                         | Effort |
|----------|----------------------------------------------|----------|------------------------------------------------------------------|--------|
| SAFE-01  | No FMEA for health monitor supervision modes | Critical | Perform FMEA on alive, deadline, and logical supervision         | 3 SP   |
| SAFE-02  | Missing safety manual for health monitor     | High     | Create safety manual per ISO 26262 Part 8                        | 2 SP   |
| SAFE-03  | Miri test scope insufficient for safety claim| High     | Extend Miri tests to cover all safety-relevant Rust paths        | 2 SP   |
| SAFE-04  | No fault injection testing for daemon        | High     | Implement fault injection for Launch Manager crash/hang scenarios | 3 SP   |
| SAFE-05  | Watchdog supervision not verified            | Medium   | Verify watchdog interaction with external watchdog manager        | 1 SP   |
| SAFE-06  | No DFA for health monitor / daemon boundary  | Medium   | Dependent failure analysis for Rust lib <-> C++ daemon interface | 2 SP   |

## Perspective 3: Deployment Engineer (7 gaps)

Focus: Daemon deployment, systemd integration, watchdog, recovery.

| ID       | Gap                                          | Severity | Fix Path                                                         | Effort |
|----------|----------------------------------------------|----------|------------------------------------------------------------------|--------|
| DEPL-01  | No systemd unit file for Launch Manager      | High     | Create .service unit with watchdog and restart policies          | 1 SP   |
| DEPL-02  | Daemon startup sequence not documented       | High     | Document startup dependencies and ordering constraints           | 1 SP   |
| DEPL-03  | No recovery strategy for daemon crash        | High     | Define restart policy, state recovery, client notification       | 2 SP   |
| DEPL-04  | FlatBuffers config deployment not validated   | Medium   | Validate config schema versions during deployment                | 1 SP   |
| DEPL-05  | QNX deployment path undefined                | Medium   | Define QNX target filesystem layout and startup integration      | 2 SP   |
| DEPL-06  | Docker demo not representative of target     | Low      | Align Docker demo with actual deployment topology                | 1 SP   |
| DEPL-07  | No resource limits defined for daemon        | Medium   | Define cgroup/rlimit constraints for memory and CPU              | 1 SP   |

## Perspective 4: Performance Engineer (5 gaps)

Focus: Supervision cycle time, daemon startup time, resource consumption.

| ID       | Gap                                          | Severity | Fix Path                                                         | Effort |
|----------|----------------------------------------------|----------|------------------------------------------------------------------|--------|
| PERF-01  | No supervision cycle time benchmark          | High     | Benchmark alive/deadline check cycle time (<= 1ms target)        | 2 SP   |
| PERF-02  | Daemon startup time not measured             | High     | Measure cold start time, target <= 500ms to ready state          | 1 SP   |
| PERF-03  | No memory profile for health monitor         | Medium   | Profile heap allocation in Rust health monitor library           | 1 SP   |
| PERF-04  | IPC latency not characterized                | Medium   | Measure client-to-daemon IPC round-trip time                     | 2 SP   |
| PERF-05  | No scalability test for supervised processes | Medium   | Test with 50/100/200 supervised processes                        | 2 SP   |

## Perspective 5: Upstream Maintainer (5 gaps)

Focus: Rust/C++ FFI boundary, FlatBuffers compatibility, CI sustainability.

| ID       | Gap                                          | Severity | Fix Path                                                         | Effort |
|----------|----------------------------------------------|----------|------------------------------------------------------------------|--------|
| UPST-01  | Rust/C++ FFI boundary not tested             | High     | Add FFI boundary tests for health_monitoring_lib <-> C++ daemon  | 2 SP   |
| UPST-02  | FlatBuffers schema backward compat unknown   | High     | Establish schema evolution policy and compat tests               | 2 SP   |
| UPST-03  | 13 CI workflows may have redundancy          | Medium   | Audit and consolidate CI workflows for maintainability           | 1 SP   |
| UPST-04  | Rust nightly dependency for Miri is fragile  | Medium   | Pin nightly version, add fallback for Miri breakage              | 1 SP   |
| UPST-05  | Mock coverage insufficient for contributors  | Low      | Expand mocks from 2 to full interface coverage for test ease     | 2 SP   |

## Perspective 6: System Architect (5 gaps)

Focus: Integration with LoLa, orchestrator, and persistency modules.

| ID       | Gap                                          | Severity | Fix Path                                                         | Effort |
|----------|----------------------------------------------|----------|------------------------------------------------------------------|--------|
| ARCH-01  | No integration test with score_LoLa          | High     | Validate lifecycle state transitions with LoLa middleware        | 3 SP   |
| ARCH-02  | Orchestrator handshake undefined             | High     | Define and test startup/shutdown handshake protocol              | 2 SP   |
| ARCH-03  | Persistency interaction not tested           | Medium   | Test state persistence across daemon restart cycles              | 2 SP   |
| ARCH-04  | No system-level lifecycle sequence diagram   | Medium   | Create sequence diagrams for boot, shutdown, and fault recovery  | 1 SP   |
| ARCH-05  | Multi-instance deployment not addressed      | Low      | Define strategy for multiple Launch Manager instances            | 1 SP   |

---

## Summary Statistics

| Perspective          | Gaps | Critical | High | Medium | Low | Total Effort |
|----------------------|------|----------|------|--------|-----|--------------|
| ASPICE Auditor       | 6    | 0        | 2    | 3      | 1   | 8 SP         |
| Safety Engineer      | 6    | 1        | 3    | 2      | 0   | 13 SP        |
| Deployment Engineer  | 7    | 0        | 3    | 3      | 1   | 9 SP         |
| Performance Engineer | 5    | 0        | 2    | 3      | 0   | 8 SP         |
| Upstream Maintainer  | 5    | 0        | 2    | 2      | 1   | 8 SP         |
| System Architect     | 5    | 0        | 2    | 2      | 1   | 9 SP         |
| **Total**            | **34** | **1**  | **14** | **15** | **4** | **55 SP** |

---

## 3-Sprint Roadmap

### Sprint 1: Foundation (Weeks 1-2) -- 20 SP

**Focus:** Build, test, and safety fundamentals.

- ASPICE-01: Unit test traceability (1 SP)
- ASPICE-02: Integration test plan (2 SP)
- SAFE-01: Health monitor FMEA (3 SP)
- SAFE-04: Fault injection testing (3 SP)
- DEPL-01: Systemd unit file (1 SP)
- DEPL-02: Startup sequence docs (1 SP)
- DEPL-03: Recovery strategy (2 SP)
- PERF-02: Daemon startup time (1 SP)
- UPST-01: FFI boundary tests (2 SP)
- ARCH-02: Orchestrator handshake (2 SP)
- ASPICE-06: CI workflow documentation (1 SP)
- DEPL-07: Resource limits (1 SP)

### Sprint 2: Quality Deepening (Weeks 3-4) -- 19 SP

**Focus:** Coverage, performance, and safety documentation.

- ASPICE-03: Qualification test definition (2 SP)
- ASPICE-04: Coverage-requirement mapping (1 SP)
- SAFE-02: Safety manual (2 SP)
- SAFE-03: Extended Miri scope (2 SP)
- SAFE-06: DFA analysis (2 SP)
- PERF-01: Supervision cycle benchmark (2 SP)
- PERF-03: Memory profiling (1 SP)
- PERF-04: IPC latency characterization (2 SP)
- UPST-02: FlatBuffers compat policy (2 SP)
- UPST-03: CI workflow audit (1 SP)
- ARCH-04: System sequence diagrams (1 SP)
- UPST-04: Nightly pin strategy (1 SP)

### Sprint 3: Integration and Hardening (Weeks 5-6) -- 16 SP

**Focus:** System integration, scalability, and remaining items.

- ASPICE-05: Change impact analysis process (1 SP)
- SAFE-05: Watchdog verification (1 SP)
- DEPL-04: FlatBuffers config validation (1 SP)
- DEPL-05: QNX deployment path (2 SP)
- DEPL-06: Docker demo alignment (1 SP)
- PERF-05: Scalability testing (2 SP)
- UPST-05: Mock expansion (2 SP)
- ARCH-01: LoLa integration test (3 SP)
- ARCH-03: Persistency interaction test (2 SP)
- ARCH-05: Multi-instance strategy (1 SP)
