---
document_id: PLAN-001
title: "Eclipse SDV Testing — Future Plan"
date: 2026-03-23
---

# Future Plan

## What We Accomplished (2026-03-21 to 2026-03-23)

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

### Deliverables Created
| Category | Count |
|---|---|
| Test files (pytest) | 20 |
| Result files | 36 |
| Regression scripts | 4 |
| ASPICE verification reports | 4 |
| Documentation files | 7 |
| Gap analyses | 17 |
| **Total artifacts** | **88** |

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

| Priority | Module | Reason |
|---|---|---|
| 1 | **score-logging** | Foundation — used by lifecycle, persistency, feo |
| 2 | **score-orchestrator** | Deployment management — integrates with lifecycle |
| 3 | **kuksa-databroker** | Vehicle data broker — central to SDV data flow |
| 4 | **ankaios** | Workload orchestrator — alternative to score-orchestrator |
| 5 | **velocitas-sdk** | Vehicle app framework — end-user facing |

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
| S-CORE modules assessed | 5 / ~20 |
| Upstream tests passing | 548 / 549 (99.8%) |
| Local pytest tests | 738 pass, 6 skip |
| Aggregate C++ coverage | 95.5% (31,846 / 33,349 lines) |
| 10-perspective gaps audited | 351 |
| Gaps closed | ~290 (83%) |
| Gaps remaining (closable) | ~15 |
| Gaps skipped (not our deliverable) | ~45 |

---

**Next session:** Run remaining sanitizers, deploy to Pi, then start score-logging assessment.
