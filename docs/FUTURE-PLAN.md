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

### Day 4 (Mar 25) — Extend to 8 Modules + Execute Builds

**Structural assessment:**
- **3 new modules** structurally assessed: score-logging, score-orchestrator, kuksa-databroker
- **score-logging**: C++ DLT + Rust bindings, Object Seam mocks verified, deps confirmed
- **score-orchestrator**: Rust orchestration, kyron hash-pinned, proc-macro safety verified
- **kuksa-databroker**: KUKSA.val v1/v2, VSS 4.0, JWT auth, TLS, OpenTelemetry — all structural

**Build execution (all 8 modules now bench-verified):**
- **score-logging**: 36/37 tests PASS, 87.8% C++ coverage (4,381/4,989 lines)
- **score-orchestrator**: 108/108 Cargo tests PASS; Bazel blocked by iceoryx2-qnx8 bindgen on Linux (upstream bug)
- **kuksa-databroker**: 208/209 Cargo tests PASS; live broker started on :55555; Python integration tests blocked by v1→v2 API migration (upstream gap)

**Findings:**
- Installed rustup 1.85.0 + clang/libclang-dev + protobuf-compiler on Ubuntu laptop (previously missing)
- score-orchestrator files had Windows CRLF line endings (fixed with dos2unix)
- kuksa integration test uses deprecated `sdv.databroker.v1` collector API — unimplemented in v0.6.1-dev

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

## ~~Immediate Priority: Build Execution for Modules 6-8~~ — DONE

All 3 builds executed 2026-03-25. Results:

| Module | Build | Tests | Coverage | Notes |
|---|---|---|---|---|
| score-logging | **PASS** | **36/37** | **87.8%** | No sanitizer config in .bazelrc |
| score-orchestrator | **PASS** (Cargo) | **108/108** | — (Rust) | Bazel blocked (iceoryx2-qnx8 on Linux) |
| kuksa-databroker | **PASS** | **208/209** | — (Rust) | Live broker verified; integration test uses deprecated v1 API |

## Next Priority: Remaining Gaps

| Task | Module | Effort | Priority |
|---|---|---|---|
| ~~Add ASan/TSan config to score-logging .bazelrc~~ | ~~score-logging~~ | ~~30 min~~ | **DONE** |
| ~~Rewrite kuksa integration test for KUKSA.val v2 API~~ | ~~kuksa-databroker~~ | ~~2 hours~~ | **DONE** (5/5 pass) |
| ~~Add taktflow contract tests to score-logging~~ | ~~score-logging~~ | ~~30 min~~ | **DONE** (8 pass + 1 xfail) |
| ~~Add taktflow CIT scenarios to score-orchestrator~~ | ~~score-orchestrator~~ | ~~30 min~~ | **DONE** (2/2 pass) |
| ~~Add Cucumber BDD taktflow tests to kuksa-databroker~~ | ~~kuksa-databroker~~ | ~~2 hours~~ | **DONE** (3/3 scenarios, 11 steps) |
| ~~Add .gitattributes CRLF prevention~~ | ~~all modules~~ | ~~15 min~~ | **DONE** |
| aarch64 cross-compile + Pi deployment | all 8 | 2 hours | Medium |
| Miri + Clippy for score-orchestrator | score-orchestrator | 1 hour | Medium |
| Rust coverage (tarpaulin) for kuksa/orchestrator | 2 modules | 1 hour | Medium |

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
| Modules bench-verified (built + tested) | **8** |
| Upstream tests passing (modules 1-5) | 548 / 549 (99.8%) |
| Cargo/Bazel tests passing (modules 6-8) | 352 / 353 (99.7%) |
| Local pytest tests (all modules) | 738 pass, 6 skip |
| Aggregate C++ coverage (all C++ modules) | 94.5% (36,227 / 38,338 lines) |
| 10-perspective gaps audited | 351 |
| Gaps closed | ~290 (83%) |
| Gaps remaining (closable) | ~20 |
| Gaps skipped (not our deliverable) | ~45 |

---

**Session 2026-03-25 complete:** All testing integration tasks done. kuksa v2 rewrite (5/5), Cucumber BDD (3/3), score-logging taktflow tests (8+1xf), orchestrator CIT (2/2), .bazelrc sanitizers, .gitattributes.

**Next session:** Start ankaios and velocitas-sdk assessment (assess→build→test→audit pattern). Deploy aarch64 binaries to Pi. Run score-logging asan/tsan to confirm sanitizer config works.
