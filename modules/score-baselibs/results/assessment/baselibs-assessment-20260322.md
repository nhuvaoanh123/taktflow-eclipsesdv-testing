---
document_id: ASSESS-BL-001
title: "score-baselibs Assessment Report"
version: "1.0"
status: planned
date: 2026-03-22
---

# score-baselibs Assessment Report

**Date:** 2026-03-22
**Host:** TBD (planned — not yet executed)
**OS:** Ubuntu 24.04 LTS (target environment)
**Bazel:** 8.3.1 (upstream pinned)
**Compiler:** GCC 12.2.0
**Upstream Version:** v0.2.4

---

## Results Summary

| Phase | Status | Tests | Duration | Notes |
|---|---|---|---|---|
| **Build (x86_64-linux)** | EXPECTED PASS | ~1,487 source files | — | Based on upstream CI green (build_linux.yml) |
| **Unit Tests** | EXPECTED PASS | ~363 test files | — | Upstream CI passes (Google Test) |
| **ASan/UBSan/LSan** | EXPECTED PASS | ~363 | — | Upstream sanitizers_linux.yml green |
| **TSan** | EXPECTED PASS | subset | — | Some tests may skip (multi-process) |
| **Coverage** | EXPECTED >80% | — | — | Upstream runs lcov via coverage_report.yml |
| **Format Check** | EXPECTED PASS | — | — | Pre-commit enforced upstream |
| **Copyright Check** | EXPECTED PASS/INFO | — | — | May have cosmetic gaps (similar to LoLa) |
| **QNX Cross-Compile** | SKIP | — | — | QNX SDP not available (same blocker as LoLa) |
| **AArch64 Linux** | EXPECTED PASS | — | — | Upstream CI uses QEMU cross-execution |
| **Benchmarks** | EXPECTED PASS | — | — | Google Benchmark targets exist |

## Verdict: PLANNED — Awaiting bench execution

---

## Component Inventory (16 components)

| Component | ASIL Rating | Source Files | Test Files | Notes |
|---|---|---|---|---|
| os | **ASIL-B** | varies | yes | OS abstraction layer, Object Seam mocks |
| memory/shared | **ASIL-B** | varies | yes | Shared memory primitives |
| concurrency | **ASIL-B** | varies | yes | Mutexes, semaphores, thread primitives |
| result | **ASIL-B** | varies | yes | Result/error monad |
| language/safecpp | **ASIL-B** | varies | yes | Safe C++ language extensions |
| mw/log | QM | varies | yes | Logging middleware |
| json | QM | varies | yes | JSON parsing/serialization |
| filesystem | QM | varies | yes | Filesystem abstraction |
| network | QM | varies | yes | Network primitives |
| containers | QM | varies | yes | Container data structures |
| bitmanipulation | QM | varies | yes | Bit-level operations |
| ... (remaining) | QM | varies | yes | Additional utility components |

**Totals:** 1,487 source files, 363 upstream test files

---

## Phase 1: Build Details (EXPECTED)

```
Expected: Bazel 8.3.1, GCC 12.2.0, x86_64-linux
Upstream CI: build_linux.yml builds both x86_64 and aarch64 (via QEMU)
~1,487 source files across 16 components
```

Expectation based on upstream CI status: all builds green on main branch.

## Phase 2: Unit Test Results (EXPECTED)

```
Expected: ~363 test files pass via Google Test
```

Key test areas expected:
- OS abstraction (process, thread, file, socket — via Object Seam mocks)
- Memory management (shared memory allocation, deallocation, lifecycle)
- Concurrency primitives (mutex lock/unlock, semaphore, thread creation)
- Result type (success/error propagation, monadic chaining)
- Safe C++ language extensions (bounds checking, type safety)
- Logging (log levels, formatting, output sinks)
- JSON (parse, serialize, schema validation)
- Filesystem (path operations, file I/O)
- Containers (dynamic array, map, set operations)
- Bit manipulation (set, clear, toggle, extract)

## Phase 3: ASan/UBSan/LSan (EXPECTED)

```
Expected: ~363 tests pass under sanitizer instrumentation
```

- Address Sanitizer: **EXPECTED 0 errors** (upstream sanitizers_linux.yml green)
- Undefined Behavior Sanitizer: **EXPECTED 0 errors**
- Leak Sanitizer: **EXPECTED 0 leaks**

Critical for ASIL-B components (os, memory/shared, concurrency, result, language/safecpp).

## Phase 4: Thread Sanitizer (EXPECTED)

```
Expected: majority of tests pass, some multi-process tests may skip
```

- Thread Sanitizer: **EXPECTED 0 data races**
- Particularly important for concurrency and memory/shared components
- Object Seam mock pattern enables in-process testing of OS APIs

## Phase 5: Coverage (EXPECTED)

```
Expected: >80% line coverage (upstream runs lcov via coverage_report.yml)
```

Coverage not yet verified locally. Upstream generates coverage reports but exact percentages need confirmation during execution.

## Phase 6: Format & Copyright Checks (EXPECTED)

```
Format: EXPECTED PASS (clang-format enforced via pre-commit)
Copyright: EXPECTED PASS/INFO (may have cosmetic gaps in headers)
```

## Phase 7: QNX Cross-Compile (SKIP)

```
Status: SKIP — QNX SDP not installed
```

Same blocker as LoLa assessment. QNX build-only exists in upstream CI (no test execution even upstream). This is a known gap.

## Phase 8: AArch64 Linux Cross-Build (EXPECTED)

```
Expected: PASS via QEMU cross-execution (upstream CI pattern)
```

Upstream CI builds and runs tests on aarch64 using QEMU user-mode emulation.

## Phase 9: Benchmarks (EXPECTED)

```
Expected: PASS — Google Benchmark targets exist
```

Benchmark baselines not yet captured. Will be recorded during first bench execution.

---

## ASPICE Gate Check

| Gate | Requirement | Expected Result |
|---|---|---|
| SWE.4 (Unit Verification) | All unit tests pass | **EXPECTED PASS** (~363 test files) |
| SWE.5 (Integration Test) | Integration tests pass | **N/A** (baselibs is a foundation library — tested in isolation) |
| SUP.1 (Quality) | Static analysis clean | **EXPECTED PASS** (format/lint enforced) |
| SUP.8 (Config Mgmt) | Build reproducible | **EXPECTED PASS** (Bazel hermetic build) |
| SAF (Safety - ASan) | No memory safety violations | **EXPECTED PASS** (upstream CI green) |
| SAF (Safety - TSan) | No data races | **EXPECTED PASS** (upstream CI green) |
| SAF (Safety - UBSan) | No undefined behavior | **EXPECTED PASS** (upstream CI green) |
| SAF (Safety - ASIL-B) | ASIL-B components verified | **EXPECTED PASS** (os, memory/shared, concurrency, result, language/safecpp) |
| NFR (Performance) | Benchmarks baselined | **PENDING** (to be captured on first execution) |

---

## Gaps Identified Before Execution

1. **No QNX test execution** — upstream CI does build-only for QNX; no runtime tests. QNX SDP not available locally (same blocker as LoLa).
2. **No cross-platform behavioral parity tests** — no tests verify identical behavior across Linux/QNX/other targets. Build-only verification on QNX does not confirm runtime correctness.
3. **No integration tests with other S-CORE modules** — baselibs is a foundation library tested in isolation. Integration with LoLa, execution management, etc. is not covered here.
4. **No performance WCET validation for ASIL-B primitives** — benchmarks exist (Google Benchmark) but no worst-case execution time bounds are defined or validated for safety-critical paths (os, concurrency, memory/shared).
5. **No security fuzzing** — no fuzz targets found for parser-heavy components (json, network). Attack surface exists but is not tested with AFL/libFuzzer.
6. **Coverage report not verified locally yet** — upstream runs lcov but actual percentages and per-component breakdown need confirmation during bench execution.

---

## Next Steps

- [ ] Execute full assessment on Linux bench (same environment as LoLa assessment)
- [ ] Capture actual test counts, durations, and pass/fail for each phase
- [ ] Record benchmark baselines for ASIL-B primitives
- [ ] Verify coverage report and per-component breakdown
- [ ] Update this report from PLANNED to EXECUTED with actual results
- [ ] File upstream issues for any gaps found during execution
