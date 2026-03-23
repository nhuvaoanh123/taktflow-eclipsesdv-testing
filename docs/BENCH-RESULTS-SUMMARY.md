---
document_id: BENCH-SUMMARY-001
title: "S-CORE Bench Execution Summary"
version: "1.0"
status: verified
date: 2026-03-23
bench: "ASUS TUF Gaming A17, Ubuntu 24.04, 16 cores, 14GB RAM"
---

# S-CORE Bench Execution Summary

## Environment

| Field | Value |
|---|---|
| Build Machine | ASUS TUF Gaming A17 (an-dao@192.168.0.158) |
| OS | Ubuntu 24.04, Kernel 6.17.0-19-generic, x86_64 |
| CPU | 16 cores AMD Ryzen 7 |
| RAM | 14 GB |
| Bazel | 9.0.1 (Bazelisk) → per-module .bazelversion |
| GCC | 12.2.0 (hermetic, downloaded by Bazel) |
| Test Target | Raspberry Pi 4, Ubuntu 24.04 Server, aarch64 (taktflow-pi@192.168.0.197) |

---

## Module Results

### 1. score-communication (LoLa) — ASIL-B

| Phase | Result | Detail |
|---|---|---|
| Build | **PASS** | 1,203 targets, 6,465 actions |
| Unit Tests | **252/252 PASS** | 1 skipped (QNX-only) |
| ASan/UBSan/LSan | **PASS** | 0 errors |
| TSan | **PASS** | 0 data races (224/224) |
| Coverage | **93.7%** | 16,023/17,101 lines |
| Clang-Tidy | **PASS** | 0 warnings across 841 files |

### 2. score-baselibs — ASIL QM to B

| Phase | Result | Detail |
|---|---|---|
| Build | **PASS** | 755 targets, 3,055 actions, 200s |
| Unit Tests | **278/279 PASS** | 1 upstream-excluded (toolchain test) |
| ASan/UBSan/LSan | **278/279 PASS** | 0 memory errors, 0 UB, 0 leaks |
| Coverage | **97.9%** | 14,791/15,112 lines across 697 files |

### 3. score-lifecycle — QM

| Phase | Result | Detail |
|---|---|---|
| Build | **PASS** | 59 targets, 1,087 actions (C++ + Rust), 232s |
| Unit Tests | **6/6 PASS** | Including loom (Rust concurrency) |
| ASan | **PASS** | 5/5 unit tests clean |
| Coverage | **82.1%** | 316/385 lines (target >=76%) |
| Smoke Test | **PASS** | Fixed with fakechroot |

### 4. score-persistency — ASIL-D

| Phase | Result | Detail |
|---|---|---|
| Build | **PASS** | 9 targets, 755 actions (C++ + Rust), 67s |
| C++ Unit Tests | **PASS** | test_kvs_cpp |
| Rust Unit Tests | **PASS** | rust_kvs:tests |
| CIT C++ | **PASS** | Python integration tests |
| CIT Rust | **PASS** | Python integration tests |
| Coverage (C++) | **95.3%** | 716/751 lines |
| Benchmarks | **PASS** | bm_kvs_cpp executed |

### 5. score-feo — QM

| Phase | Result | Detail |
|---|---|---|
| Build | **PASS** | 85 targets, 2,729 actions (Rust + C++), 305s |
| Unit Tests | **8/8 PASS** | Including multi-agent integration (8.3s) |
| Format | **4/4 PASS** | Python, Rust, Starlark, YAML |
| Coverage (C++) | N/A | feo-time only; Rust needs ferrocene |

---

## Aggregate Totals

| Metric | Value |
|---|---|
| Modules verified | **5** |
| Total build targets | **2,111** |
| Total test targets | **553** |
| Tests passed | **548** |
| Tests failed | **0** (after fixes) |
| Local pytest tests | **738 pass, 6 skip** |
| 10-perspective gaps audited | **351** |

## Coverage Summary

| Module | Lines Hit | Lines Total | Coverage |
|---|---|---|---|
| LoLa | 16,023 | 17,101 | **93.7%** |
| score-baselibs | 14,791 | 15,112 | **97.9%** |
| score-lifecycle | 316 | 385 | **82.1%** |
| score-persistency | 716 | 751 | **95.3%** |
| score-feo | — | — | Rust (ferrocene needed) |
| **Total C++** | **31,846** | **33,349** | **95.5%** |

## Sanitizer Summary

| Module | ASan | UBSan | LSan | TSan |
|---|---|---|---|---|
| LoLa | **Clean** | **Clean** | **Clean** | **Clean** |
| score-baselibs | **Clean** | **Clean** | **Clean** | — |
| score-lifecycle | **Clean** | — | — | — |
| score-persistency | — | — | — | — |
| score-feo | — | — | — | — |

---

## Remaining Open Gaps (code-closable)

| Gap | Modules | Effort |
|---|---|---|
| TSan for baselibs | baselibs | 30 min |
| Full sanitizers for persistency/feo | 2 modules | 1 hour |
| Rust coverage (ferrocene) | lifecycle, persistency, feo | 2 hours |
| aarch64 cross-compile + Pi deploy | all 5 | 2 hours |
| Clippy/Miri for lifecycle/persistency | 2 modules | 1 hour |

## Non-Code Gaps (documentation/process)

| Category | Count | Effort |
|---|---|---|
| ASPICE process artifacts | ~50 gaps | 2-3 weeks |
| Safety case / FMEA / DFA | ~30 gaps | 2-3 weeks |
| Security testing (fuzzing) | ~15 gaps | 1-2 weeks |
| Deployment guides | ~15 gaps | 1 week |
| OEM / AUTOSAR mapping | ~15 gaps | 1-2 weeks |
| Tool qualification (ISO 26262) | ~10 gaps | 1 week |

---

**Report generated:** 2026-03-23
