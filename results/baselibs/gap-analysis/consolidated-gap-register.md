---
document_id: GAP-BL-REGISTER
title: "Consolidated Gap Register — score-baselibs"
version: "1.0"
status: initial
date: 2026-03-22
---

# Consolidated Gap Register — score-baselibs

## Overview

This register consolidates all identified gaps for score-baselibs across six analysis perspectives. Unlike LoLa (which uses 10 perspectives as a deployed service), baselibs is evaluated from 6 perspectives appropriate for a foundation library.

**Total gaps identified: 34**

---

## Perspective 1: ASPICE Auditor (6 Gaps)

*Focus: Requirements traceability, verification reports, process compliance.*

| ID | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| ASPICE-BL-001 | No requirements-to-test traceability matrix | OPEN | Generate from Bazel test targets mapped to `score/os` API headers | 2 days |
| ASPICE-BL-002 | Missing verification report for local execution | OPEN | Execute test suite, produce structured report (JSON + PDF) | 1 day |
| ASPICE-BL-003 | No documented review of test adequacy | OPEN | Coverage analysis + gap assessment per module | 1 day |
| ASPICE-BL-004 | Change impact analysis not documented | OPEN | Map dependency graph: which S-CORE modules consume which baselibs APIs | 2 days |
| ASPICE-BL-005 | No regression test strategy document | OPEN | Define which tests must pass on every baselibs version bump | 1 day |
| ASPICE-BL-006 | Verification environment not qualified | OPEN | Document host OS, compiler version, Bazel version, sanitizer versions | 0.5 day |

### Details

**ASPICE-BL-001: Requirements-to-Test Traceability**
ASPICE SWE.4 requires bidirectional traceability between software requirements and test cases. score-baselibs has well-structured tests but no explicit traceability matrix linking API requirements to specific test targets. For ASIL-B components, this traceability must be auditable.

**Fix path:** Parse `BUILD` files to extract test targets, map each to the header file (API) it exercises, and generate a traceability CSV. This can be automated with a Bazel query + Python script.

**ASPICE-BL-002: Local Verification Report**
An ASPICE audit requires evidence that verification was performed in a controlled environment. Upstream CI logs are not sufficient — we need our own execution records with timestamps, environment details, and pass/fail status.

**Fix path:** Execute the test suite and capture structured output. Template already exists from LoLa pipeline.

**ASPICE-BL-003: Test Adequacy Review**
Coverage metrics alone are insufficient. We need a documented assessment that the tests are adequate for the risk level of each module. ASIL-B modules require MC/DC coverage for safety-critical decision points.

**ASPICE-BL-004: Change Impact Analysis**
When baselibs updates (e.g., new upstream commit), which downstream modules are affected? This dependency map must be documented so that regression testing scope is clear.

**ASPICE-BL-005: Regression Test Strategy**
Define the minimum test set that must pass when we pin a new baselibs version. This should include all ASIL-B tests plus integration smoke tests from LoLa.

**ASPICE-BL-006: Verification Environment Qualification**
Document the exact environment (OS, compiler, Bazel, sanitizers) used for verification. This is a one-time activity per environment change.

---

## Perspective 2: Safety Engineer (7 Gaps)

*Focus: ASIL-B verification evidence, freedom from interference, fault tolerance.*

| ID | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| SAFETY-BL-001 | No ASIL decomposition documented for baselibs modules | OPEN | Classify each `score/` package by ASIL level | 3 days |
| SAFETY-BL-002 | Concurrency primitives lack WCET budgets | OPEN | Benchmark mutex, condvar, lock-free operations under load | 3 days |
| SAFETY-BL-003 | TSan verification not yet executed locally | OPEN | Run full suite under TSan, document zero-race evidence | 1 day |
| SAFETY-BL-004 | No fault injection testing for OS API failures | OPEN | Verify error handling when OS calls fail (ENOMEM, EAGAIN, etc.) | 3 days |
| SAFETY-BL-005 | Shared memory APIs lack integrity checks | OPEN | Verify CRC/checksum on shared memory segments | 2 days |
| SAFETY-BL-006 | No stack usage analysis for safety-critical functions | OPEN | Static analysis with `-fstack-usage` or equivalent | 1 day |
| SAFETY-BL-007 | Freedom from interference between QM and ASIL partitions | OPEN | Verify memory isolation between QM utility code and ASIL concurrency code | 2 days |

### Details

**SAFETY-BL-001: ASIL Decomposition**
Not all baselibs modules are ASIL-B. Utility functions (string helpers, logging) may be QM, while `score/os` mutex wrappers and `score/concurrency` lock-free structures are likely ASIL-B. This classification must be explicit.

**SAFETY-BL-002: WCET for Concurrency Primitives**
Mutex lock/unlock, condition variable wait/signal, and lock-free queue push/pop are on the critical path for real-time control. Without WCET budgets, we cannot guarantee timing compliance.

**SAFETY-BL-003: TSan Evidence**
Thread Sanitizer is the gold standard for data race detection. For ASIL-B concurrency code, TSan-clean evidence is mandatory. We have not yet executed this locally.

**SAFETY-BL-004: Fault Injection**
OS calls can fail. The Object Seam mocking pattern should allow us to inject failures (e.g., `mmap` returns MAP_FAILED, `pthread_create` returns EAGAIN). We need to verify that all error paths are tested.

**SAFETY-BL-005: Shared Memory Integrity**
Shared memory segments can be corrupted by a faulty writer. baselibs should provide integrity verification (CRC, checksum, or sequence numbers) to detect corruption before consumers process bad data.

**SAFETY-BL-006: Stack Usage Analysis**
Safety-critical functions must not overflow the stack. GCC's `-fstack-usage` flag generates per-function stack consumption reports. This is a standard ASIL-B verification activity.

**SAFETY-BL-007: Freedom from Interference**
ISO 26262 requires demonstration that QM code cannot corrupt ASIL code. If QM utility functions and ASIL concurrency primitives share memory spaces, we need to demonstrate isolation.

---

## Perspective 3: Performance Engineer (5 Gaps)

*Focus: WCET, memory footprint, allocator performance, scalability.*

| ID | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| PERF-BL-001 | No benchmark suite for critical APIs | OPEN | Write Google Benchmark targets for mutex, allocator, JSON parser | 3 days |
| PERF-BL-002 | Memory allocator performance uncharacterized | OPEN | Benchmark allocation patterns: small, large, fragmented, concurrent | 2 days |
| PERF-BL-003 | JSON parser throughput unknown | OPEN | Benchmark against reference payloads (1KB, 100KB, 10MB) | 1 day |
| PERF-BL-004 | Lock-free queue scalability not measured | OPEN | Measure throughput vs thread count (1, 2, 4, 8, 16 producers/consumers) | 2 days |
| PERF-BL-005 | Static memory footprint not reported | OPEN | Analyze `.text`, `.data`, `.bss` sizes per module with `size` or `bloaty` | 1 day |

### Details

**PERF-BL-001: Benchmark Suite**
Performance regressions in foundation libraries propagate to all consumers. A benchmark suite ensures that version bumps do not introduce latency regressions. Google Benchmark integrates cleanly with Bazel.

**PERF-BL-002: Allocator Performance**
If score-baselibs provides a custom allocator (common in automotive for deterministic allocation), its performance under various allocation patterns must be characterized. Fragmentation behavior is especially important for long-running systems.

**PERF-BL-003: JSON Parser Throughput**
JSON parsing is on the configuration path. While not real-time critical, slow parsing delays system startup. Characterize throughput to ensure it meets requirements.

**PERF-BL-004: Lock-Free Queue Scalability**
Lock-free queues should scale with core count. Measure throughput as a function of producer/consumer thread count to verify the implementation does not degrade under contention.

**PERF-BL-005: Static Memory Footprint**
For embedded deployments, binary size matters. Report the contribution of each baselibs module to the final binary to identify any unexpectedly large components.

---

## Perspective 4: Upstream Maintainer (5 Gaps)

*Focus: API compatibility, version pinning, contribution readiness.*

| ID | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| UPSTREAM-BL-001 | No API compatibility check between versions | OPEN | Run `abi-compliance-checker` or `libabigail` on consecutive releases | 2 days |
| UPSTREAM-BL-002 | Version pinning strategy undefined | OPEN | Document policy: pin commit hash vs tag vs branch head | 0.5 day |
| UPSTREAM-BL-003 | Upstream changelog not tracked | OPEN | Monitor eclipse-score/score commits affecting `score/` paths | 1 day |
| UPSTREAM-BL-004 | No local patch management process | OPEN | Define how we carry patches if upstream diverges from our needs | 1 day |
| UPSTREAM-BL-005 | Contribution pathway not established | OPEN | Set up fork, CLA, PR template for upstream contributions | 1 day |

### Details

**UPSTREAM-BL-001: API Compatibility**
When we bump the pinned baselibs version, we need to know if any APIs changed. ABI compatibility tools can automatically detect breaking changes (removed functions, changed signatures, modified struct layouts).

**UPSTREAM-BL-002: Version Pinning**
We must pin a specific commit hash (not a branch head) for reproducibility. Document the pinning policy and the process for evaluating and adopting new versions.

**UPSTREAM-BL-003: Upstream Monitoring**
Track upstream commits that affect the `score/` directory. Set up notifications or a periodic sync process to stay aware of upstream changes.

**UPSTREAM-BL-004: Local Patch Management**
If we need to fix a bug or add a feature before upstream accepts it, we need a clean patch management process (e.g., `git format-patch` with metadata).

**UPSTREAM-BL-005: Contribution Pathway**
Establish the ability to contribute fixes back to upstream. This includes fork setup, Eclipse CLA, and PR template compliance.

---

## Perspective 5: New Team Member (5 Gaps)

*Focus: Documentation, build instructions, onboarding friction.*

| ID | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| ONBOARD-BL-001 | No local build guide for score-baselibs | OPEN | Write step-by-step build instructions for our environment | 1 day |
| ONBOARD-BL-002 | Architecture overview missing | OPEN | Document module dependency graph and platform abstraction strategy | 2 days |
| ONBOARD-BL-003 | Test execution guide not written | OPEN | Document how to run tests, interpret results, debug failures | 1 day |
| ONBOARD-BL-004 | Object Seam pattern not explained | OPEN | Write guide explaining the mocking architecture and how to add new mocks | 1 day |
| ONBOARD-BL-005 | No troubleshooting guide for common issues | OPEN | Document known issues (QNX toolchain, Bazel cache, sanitizer false positives) | 1 day |

### Details

**ONBOARD-BL-001: Local Build Guide**
A new team member should be able to build score-baselibs within 30 minutes of cloning the repo. Document prerequisites, Bazel setup, and the specific build commands for our environment.

**ONBOARD-BL-002: Architecture Overview**
Explain the module structure, the platform abstraction layer, and how baselibs fits into the S-CORE stack. A dependency graph (generated from Bazel query) is essential.

**ONBOARD-BL-003: Test Execution Guide**
How to run tests, what the expected output looks like, how to interpret failures, and how to debug with sanitizers enabled.

**ONBOARD-BL-004: Object Seam Pattern**
The Object Seam pattern is central to baselibs' testability. New team members need to understand how mocks are structured, how to inject them, and how to add new mocks for new OS APIs.

**ONBOARD-BL-005: Troubleshooting Guide**
Known issues and their workarounds. The QNX toolchain checksum failure, Bazel remote cache configuration, and sanitizer false positive suppression should all be documented.

---

## Perspective 6: System Architect (6 Gaps)

*Focus: Integration with other S-CORE modules, API surface management, evolution.*

| ID | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| ARCH-BL-001 | No dependency graph of baselibs consumers | OPEN | Bazel query to enumerate all reverse dependencies | 1 day |
| ARCH-BL-002 | API surface area not quantified | OPEN | Count public headers, exported symbols, API versioning scheme | 1 day |
| ARCH-BL-003 | No interface stability classification | OPEN | Classify APIs as stable, experimental, or deprecated | 2 days |
| ARCH-BL-004 | Integration test coverage with LoLa undefined | OPEN | Map which baselibs APIs LoLa exercises vs total API surface | 1 day |
| ARCH-BL-005 | Platform abstraction leakage not assessed | OPEN | Audit whether platform-specific types/defines leak through public headers | 1 day |
| ARCH-BL-006 | Module boundary enforcement not verified | OPEN | Check that internal headers are not exposed via Bazel visibility rules | 1 day |

### Details

**ARCH-BL-001: Consumer Dependency Graph**
Know which S-CORE modules depend on which baselibs packages. A change in `score/os/mutex.h` potentially affects every module that uses mutexes. This graph informs regression testing scope.

**ARCH-BL-002: API Surface Quantification**
How large is the API surface? How many public headers, how many exported functions? A smaller, well-defined API surface is easier to maintain and verify.

**ARCH-BL-003: Interface Stability Classification**
Not all APIs are equally stable. Some may be experimental or subject to change. Classifying stability helps consumers make informed dependency decisions.

**ARCH-BL-004: LoLa Integration Coverage**
LoLa is the primary consumer we are evaluating. Map exactly which baselibs APIs LoLa calls to understand the tested vs untested surface area.

**ARCH-BL-005: Platform Abstraction Leakage**
The purpose of `score/os` is to hide platform differences. If QNX-specific types or Linux-specific defines leak through public headers, the abstraction is broken. Audit all public headers for platform-conditional code.

**ARCH-BL-006: Module Boundary Enforcement**
Bazel's `visibility` attribute can enforce that internal implementation headers are not accessible to external consumers. Verify this is correctly configured to prevent accidental coupling.

---

## Gap Summary by Perspective

| Perspective | Gap Count | Critical | Effort (days) |
|---|---|---|---|
| ASPICE Auditor | 6 | ASPICE-BL-001, ASPICE-BL-002 | 7.5 |
| Safety Engineer | 7 | SAFETY-BL-002, SAFETY-BL-003, SAFETY-BL-007 | 15 |
| Performance Engineer | 5 | PERF-BL-001, PERF-BL-004 | 9 |
| Upstream Maintainer | 5 | UPSTREAM-BL-002 | 5.5 |
| New Team Member | 5 | ONBOARD-BL-001 | 6 |
| System Architect | 6 | ARCH-BL-001, ARCH-BL-005 | 7 |
| **Total** | **34** | **10 critical** | **50 days** |

---

## Priority Roadmap

### Sprint 1: Execution & Evidence (2 weeks)

**Goal:** Produce local verification evidence that closes the highest-impact gaps.

| Priority | Gap IDs | Activity | Days |
|---|---|---|---|
| P0 | GAP-001, GAP-002 | Build + test execution on our host | 1 |
| P0 | GAP-003, GAP-004 | Sanitizer runs (ASan, UBSan, LSan, TSan) | 1 |
| P0 | GAP-008 | Coverage measurement | 0.5 |
| P1 | ASPICE-BL-002 | Produce verification report from execution data | 1 |
| P1 | ASPICE-BL-006 | Document verification environment | 0.5 |
| P1 | SAFETY-BL-003 | TSan evidence document for ASIL-B | 1 |
| P1 | ONBOARD-BL-001 | Write local build guide (based on our execution experience) | 1 |
| P2 | ARCH-BL-001 | Generate consumer dependency graph | 1 |
| P2 | UPSTREAM-BL-002 | Document version pinning policy | 0.5 |
| P2 | GAP-011 | Mock completeness audit | 1 |

**Sprint 1 deliverables:**
- Verified build and test pass on our host
- Sanitizer-clean evidence
- Coverage report with per-module breakdown
- Verification environment document
- Local build guide

---

### Sprint 2: Safety & Architecture (2 weeks)

**Goal:** Close safety-critical gaps and establish architectural understanding.

| Priority | Gap IDs | Activity | Days |
|---|---|---|---|
| P0 | SAFETY-BL-001 | ASIL decomposition for all baselibs modules | 3 |
| P0 | SAFETY-BL-002 | WCET benchmarking for concurrency primitives | 3 |
| P1 | SAFETY-BL-004 | Fault injection test design | 2 |
| P1 | ARCH-BL-004 | Map LoLa integration coverage | 1 |
| P1 | ARCH-BL-005 | Platform abstraction leakage audit | 1 |
| P2 | ASPICE-BL-001 | Requirements-to-test traceability matrix | 2 |

**Sprint 2 deliverables:**
- ASIL classification per module
- WCET measurements for critical APIs
- Fault injection test plan
- LoLa-baselibs integration coverage map
- Traceability matrix (draft)

---

### Sprint 3: Hardening & Process (2 weeks)

**Goal:** Close remaining gaps, establish ongoing processes.

| Priority | Gap IDs | Activity | Days |
|---|---|---|---|
| P1 | SAFETY-BL-005 | Shared memory integrity verification | 2 |
| P1 | SAFETY-BL-006 | Stack usage analysis | 1 |
| P1 | SAFETY-BL-007 | Freedom from interference analysis | 2 |
| P1 | PERF-BL-001 | Benchmark suite (initial targets) | 2 |
| P2 | GAP-012 | Fuzzing target design (JSON parser first) | 2 |
| P2 | UPSTREAM-BL-003 | Set up upstream monitoring | 1 |
| P2 | ONBOARD-BL-002 | Architecture overview document | 2 |
| P2 | ARCH-BL-006 | Module boundary verification | 1 |

**Sprint 3 deliverables:**
- Safety analysis complete for ASIL-B components
- Initial benchmark suite
- Fuzzing targets for high-risk parsers
- Upstream monitoring in place
- Architecture documentation

---

## Dependencies and Blockers

| Blocker | Affects | Resolution |
|---|---|---|
| QNX toolchain checksum | GAP-005, GAP-006, GAP-007 | Upstream fix or local WORKSPACE patch |
| No QNX target hardware | GAP-006 | Procurement or VM provisioning |
| WCET tooling | SAFETY-BL-002 | Select and license WCET analysis tool |
| Fuzzing infrastructure | GAP-012 | Set up OSS-Fuzz or ClusterFuzz integration |

---

## Relationship to LoLa Gap Register

score-baselibs and LoLa share several gap categories:

- **QNX blockers** (GAP-005/006) are identical root cause — fix once, applies to both.
- **ASPICE process gaps** (traceability, verification reports) use the same templates.
- **Safety gaps** are complementary — LoLa's safety verification depends on baselibs safety evidence.
- **Upstream management** follows the same policy for both modules.

Closing baselibs gaps strengthens the entire S-CORE verification pipeline because baselibs is the foundation layer.
