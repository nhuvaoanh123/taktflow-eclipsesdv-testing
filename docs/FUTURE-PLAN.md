---
document_id: PLAN-001
title: "Eclipse SDV Testing — Future Plan"
date: 2026-03-23
---

# Future Plan

## What We Accomplished (2026-03-21 to 2026-03-25)

### Day 1 (Mar 21) — LoLa Pilot
- Assessed score-communication (LoLa): 252/252 tests, sanitizers clean, 93.7% coverage
- CAN→LoLa bridge verified on real ECUs
- 12 gaps analyzed through 5 iterations, 10 closed
- Testing strategy + upstream comparison documented

### Day 2-3 (Mar 22-23) — Scale to 5 Modules
- **4 new modules** assessed: baselibs, lifecycle, persistency, feo
- **Bench infrastructure**: laptop (x86_64 build) + Pi (aarch64 target) + Windows PC (dev)
- **738 local pytest tests**, 0 failures across all modules
- **548 upstream Bazel tests pass** on x86_64 bench
- **aarch64 cross-compile proven** (755 baselibs targets)
- **Coverage**: 97.9% (baselibs), 95.3% (persistency), 93.7% (LoLa), 82.1% (lifecycle)
- **10-perspective audits** for all 4 new modules (351 total gaps identified)
- **ASPICE SWE.4 verification reports** for all 4 modules
- **Documentation**: deployment guide, security analysis, tool qualification

### Day 4 (Mar 25) — Extend to 8 Modules (SDV stack)
- **3 new modules** structurally assessed: score-logging, score-orchestrator, kuksa-databroker
- **score-logging**: C++ DLT + Rust bindings, Object Seam mocks verified, deps confirmed
- **score-orchestrator**: Rust orchestration, kyron hash-pinned, proc-macro safety verified
- **kuksa-databroker**: KUKSA.val v1/v2, VSS 4.0, JWT auth, TLS, OpenTelemetry — all structural
- **Test suites created**: build, regression, integration, security for all 3 modules
- **Regression scripts**: bash + pytest for each new module
- **Gap analyses**: v1-initial.md per module — honest about what needs build execution

### Deliverables Created
| Category | Count |
|---|---|
| Test files (pytest) | 29 |
| Result files | 42 |
| Regression scripts | 7 |
| ASPICE verification reports | 7 |
| Documentation files | 7 |
| Gap analyses | 23 |
| **Total artifacts** | **115** |

---

## Remaining Gaps (~60)

### Skipped (not our deliverable)
| Category | Count | Reason |
|---|---|---|
| Safety case / FMEA / DFA | ~30 | Upstream safety engineering — requires domain experts |
| OEM / AUTOSAR mapping | ~15 | Requires OEM-specific context (Munich Electrification product requirements) |

### Closable in future sessions
| Gap | Effort | Priority |
|---|---|---|
| Sanitizers for persistency + feo | 1 hour | High |
| Rust coverage (ferrocene) for lifecycle/persistency/feo | 2 hours | Medium |
| Miri UB detection for lifecycle/persistency | 1 hour | Medium |
| Deploy aarch64 binaries to Pi + run natively | 2 hours | High |
| libFuzzer integration for JSON/KVS | 1 day | Medium |
| SAST pipeline (CodeQL/Semgrep) | 1 day | Low |
| TSan for baselibs | 30 min | Low |

---

## Next Modules to Assess

Following the same assess→build→test→audit pattern:

| Priority | Module | Reason | Status |
|---|---|---|---|
| ~~1~~ | ~~**score-logging**~~ | ~~Foundation — used by lifecycle, persistency, feo~~ | **DONE** (structural) |
| ~~2~~ | ~~**score-orchestrator**~~ | ~~Deployment management — integrates with lifecycle~~ | **DONE** (structural) |
| ~~3~~ | ~~**kuksa-databroker**~~ | ~~Vehicle data broker — central to SDV data flow~~ | **DONE** (structural) |
| 4 | **ankaios** | Alternative workload orchestrator — Rust, simpler than orchestrator | Pending |
| 5 | **velocitas-sdk** | Vehicle app framework — end-user SDK for SDV apps | Pending |
| 6 | **kuksa-can-provider** | CAN→VSS bridge — connects taktflow ECUs to databroker | Pending |

## Immediate Priority: Build Execution for Modules 6-8

These modules are structurally verified but need build + test execution on the Ubuntu laptop:

| Task | Module | Command | Priority |
|---|---|---|---|
| Cargo build | score-logging | `bazel build --config=x86_64-linux //score/...` | High |
| Cargo build | score-orchestrator | `cargo build && bazel build //...` | High |
| Cargo build | kuksa-databroker | `cargo build --workspace` | High |
| Live integration | kuksa-databroker | Run broker + `python3 integration_test/test_databroker.py` | High |
| TSan | score-logging | `bazel test --config=tsan //score/...` | Medium |

---

## Infrastructure Improvements

| Improvement | Effort | Impact |
|---|---|---|
| Set up QEMU aarch64 wrapper on laptop | 2 hours | Run aarch64 tests without Pi |
| GitHub account reinstatement | Pending | Enable git push/pull directly |
| CI pipeline on laptop (cron-based) | 4 hours | Automated nightly regression |
| Pi as CAN bench target | 2 hours | Real CAN bus testing with ECUs |
| Fix Windows→Linux line endings in SCP | 30 min | Add `.gitattributes` with `* text=auto` |

---

## Architecture Decision: QNX Deferred

**Decision:** Linux on Pi replaces QNX as target platform.

**Rationale:**
- QNX toolchain blocked upstream (stale checksum in score-toolchains_qnx)
- All S-CORE modules have Linux OSAL — fully supported
- Upstream CI tests on Linux (Ubuntu 24.04), not QNX
- ASIL-B QNX features (resource manager, safety isolation) only needed for certification
- Can reflash QNX when upstream toolchain is fixed

**Impact:** Unblocked all 5 modules. No QNX-specific gaps remain as blockers.

---

## Key Metrics

| Metric | Value |
|---|---|
| S-CORE + SDV modules assessed (structural) | **8 / ~20** |
| Modules bench-verified (built + tested) | **5** |
| Upstream tests passing (verified modules) | 548 / 549 (99.8%) |
| Local pytest tests (verified modules) | 738 pass, 6 skip |
| Structural tests (new modules) | ~120 (file inspection) |
| Aggregate C++ coverage (verified) | 95.5% (31,846 / 33,349 lines) |
| 10-perspective gaps audited | 351 |
| Gaps closed | ~290 (83%) |
| Gaps remaining (closable) | ~25 |
| Gaps skipped (not our deliverable) | ~45 |

---

**Next session:** Execute builds for modules 6-8 on Ubuntu laptop. Run kuksa-databroker live integration. Then start ankaios and velocitas-sdk assessment.
