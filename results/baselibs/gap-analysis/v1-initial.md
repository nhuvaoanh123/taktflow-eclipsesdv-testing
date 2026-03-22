---
document_id: GAP-BL-001
title: "Gap Analysis v1 — Initial Assessment Before Execution"
version: "1.0"
status: initial
date: 2026-03-22
---

# Gap Analysis v1 — score-baselibs Initial Assessment Before Execution

## Overview

This document captures the initial gap analysis for **score-baselibs** (S-CORE Base Libraries), performed prior to local test execution. The analysis follows the same 12-gap structure established for LoLa (GAP-LOLA-001) to maintain consistency across our S-CORE evaluation pipeline.

score-baselibs provides the foundational OS abstraction layer, concurrency primitives, memory management, JSON parsing, and networking utilities that all other S-CORE modules depend on. As the lowest layer in the stack, its correctness is critical for ASIL-B safety claims.

## Gap Summary Table

| Gap | Description | Status | Evidence Needed |
|---|---|---|---|
| GAP-001 | Build verification on our host | OPEN | Run `bazel build //score/... --config=bl-x86_64-linux` |
| GAP-002 | Unit test execution | OPEN | Run `bazel test //score/... --config=bl-x86_64-linux` — expect ~363 tests |
| GAP-003 | ASan/UBSan/LSan clean | OPEN | Run with sanitizer config |
| GAP-004 | TSan clean (lock-free code) | OPEN | Critical for ASIL-B concurrency — must verify zero data races |
| GAP-005 | QNX cross-compile | OPEN | Blocked same as LoLa (toolchains_qnx stale checksum) |
| GAP-006 | QNX test execution | OPEN | Blocked — no QNX target |
| GAP-007 | Cross-platform parity | OPEN | score/os APIs must behave identically Linux vs QNX |
| GAP-008 | Coverage measurement | OPEN | Run `bazel coverage` — target >80% |
| GAP-009 | ASIL-B WCET validation | OPEN | No timing budgets defined for concurrency primitives |
| GAP-010 | Integration with LoLa | OPEN | baselibs is a dependency of LoLa — already proven transitively |
| GAP-011 | Mock completeness | OPEN | Verify every OS API has a corresponding mock (Object Seam) |
| GAP-012 | Security fuzzing | OPEN | No fuzzing of shared memory / JSON / network APIs |

---

## Detailed Gap Analysis

### GAP-001: Build Verification on Our Host

**What we know:**
- Upstream CI builds score-baselibs on every PR merge using Bazel with GCC and Clang toolchains.
- The repository uses a hermetic Bazel build with pinned toolchains, so host environment differences should be minimal.
- LoLa (which depends on baselibs) already builds on our host, implying baselibs transitively compiles.

**What we need to verify:**
- Explicit standalone build of `//score/...` with the `bl-x86_64-linux` config to confirm all targets resolve.
- Check for any platform-specific `select()` statements that might behave differently on our kernel version.

**Command:**
```bash
bazel build //score/... --config=bl-x86_64-linux 2>&1 | tee results/baselibs/build-log.txt
```

**Expected outcome:** PASS — high confidence given transitive evidence from LoLa builds.

---

### GAP-002: Unit Test Execution

**What we know:**
- Upstream reports ~363 test targets across score-baselibs modules.
- Tests use Google Test framework with custom matchers for OS abstraction verification.
- Modules include: `score/os`, `score/memory`, `score/json`, `score/concurrency`, `score/network`, and utility libraries.

**What we need to verify:**
- Full test suite passes on our host with zero failures.
- No flaky tests (run at least 3 iterations).
- All test targets actually execute (not just skipped via `tags = ["manual"]`).

**Command:**
```bash
bazel test //score/... --config=bl-x86_64-linux --test_output=errors 2>&1 | tee results/baselibs/test-log.txt
```

**Expected outcome:** PASS — upstream CI enforces green tests on merge.

---

### GAP-003: ASan/UBSan/LSan Clean

**What we know:**
- Address Sanitizer, Undefined Behavior Sanitizer, and Leak Sanitizer are standard in automotive C++ verification.
- Upstream CI likely runs sanitizers but we need to confirm which configs are active.
- baselibs contains low-level memory management (`score/memory`) and OS wrappers that are prime candidates for memory issues.

**What we need to verify:**
- Run full test suite with `-fsanitize=address,undefined,leak` enabled.
- Zero sanitizer findings — any finding in a foundation library propagates to all consumers.

**Command:**
```bash
bazel test //score/... --config=bl-x86_64-linux --config=asan 2>&1 | tee results/baselibs/asan-log.txt
```

**Expected outcome:** PASS — foundation libraries typically have the strictest sanitizer discipline.

---

### GAP-004: TSan Clean (Lock-Free Code)

**What we know:**
- score-baselibs provides concurrency primitives (mutexes, condition variables, lock-free queues) that LoLa and other modules depend on.
- Thread Sanitizer is the only reliable way to detect data races in lock-free code.
- ASIL-B requires freedom from interference — data races in concurrency primitives would be a safety violation.
- Lock-free algorithms are notoriously difficult to get right; even a single missed memory ordering is a latent defect.

**What we need to verify:**
- Full test suite passes under TSan with zero race reports.
- Specific focus on `score/concurrency` and any shared-memory primitives.
- Verify that TSan annotations (if any) are correct and not suppressing real races.

**Command:**
```bash
bazel test //score/... --config=bl-x86_64-linux --config=tsan 2>&1 | tee results/baselibs/tsan-log.txt
```

**Expected outcome:** PASS with caveats — TSan may produce false positives on custom lock-free code that uses relaxed memory orderings. Any finding requires manual analysis.

---

### GAP-005: QNX Cross-Compile

**What we know:**
- score-baselibs is designed to be cross-platform (Linux + QNX) via the `score/os` abstraction layer.
- The `toolchains_qnx` external dependency has a stale checksum issue (same blocker we hit with LoLa).
- QNX compilation is required for production deployment but not for functional verification of business logic.

**What we need to verify:**
- Once toolchain issue is resolved, build `//score/... --config=bl-aarch64-qnx`.
- Verify all `score/os/qnx/` platform implementations compile without warnings.

**Current blocker:** `toolchains_qnx` repository rule fails with SHA256 mismatch. Same root cause as LoLa GAP-005. Fix requires upstream to update checksums or us to patch `WORKSPACE`.

**Expected outcome:** BLOCKED — tracked in LoLa pipeline, fix applies to both.

---

### GAP-006: QNX Test Execution

**What we know:**
- QNX test execution requires either a QNX target board or QNX VM.
- We do not currently have a QNX execution environment in our test infrastructure.
- Upstream likely has QNX CI runners but this is not publicly confirmed.

**What we need to verify:**
- All tests pass on QNX target.
- Platform-specific code paths (POSIX vs QNX resource managers) behave correctly.
- Timer resolution and thread scheduling differences do not cause test failures.

**Current blocker:** No QNX target available. Dependent on GAP-005 resolution plus hardware/VM provisioning.

**Expected outcome:** BLOCKED — long-term infrastructure gap.

---

### GAP-007: Cross-Platform Parity

**What we know:**
- `score/os` provides an abstraction layer with platform-specific implementations under `linux/` and `qnx/` subdirectories.
- The API contract should guarantee identical behavior regardless of platform.
- Differences in POSIX compliance between Linux and QNX (e.g., `clock_gettime` resolution, `mmap` semantics, `pthread` behavior) can cause subtle divergences.

**What we need to verify:**
- Every public API in `score/os` has both a Linux and QNX implementation.
- Mock implementations (Object Seam pattern) cover the full API surface.
- No platform-specific behavior leaks through the abstraction.

**Evidence path:** Static analysis of the source tree to map Linux vs QNX implementation files 1:1.

**Expected outcome:** Likely PASS — the architecture is explicitly designed for this, but verification is needed.

---

### GAP-008: Coverage Measurement

**What we know:**
- Upstream does not publish coverage metrics publicly for score-baselibs.
- Foundation libraries should target >80% line coverage, with ASIL-B components targeting >90%.
- Bazel supports `--instrument_test_targets` and `--combined_report` for LCOV output.

**What we need to verify:**
- Overall line coverage across all `score/` packages.
- Per-module breakdown to identify any under-tested areas.
- ASIL-B critical modules (`score/os`, `score/concurrency`) meet the 90% threshold.

**Command:**
```bash
bazel coverage //score/... --config=bl-x86_64-linux --combined_report=lcov 2>&1 | tee results/baselibs/coverage-log.txt
```

**Expected outcome:** Likely >80% overall given the test count (~363 tests), but specific modules may have coverage gaps.

---

### GAP-009: ASIL-B WCET Validation

**What we know:**
- Worst-Case Execution Time analysis is required for ASIL-B components that participate in real-time control paths.
- score-baselibs concurrency primitives (mutex lock/unlock, condition variable wait/signal) are on the critical path.
- No WCET budgets are defined in the upstream repository for any baselibs API.
- Static WCET analysis tools (e.g., aiT, Chronos) require target-specific configuration.

**What we need to verify:**
- Identify which baselibs APIs are on ASIL-B critical paths.
- Define WCET budgets for those APIs.
- Measure actual execution times under worst-case conditions.

**Expected outcome:** OPEN — this is a process gap, not a code gap. Requires safety engineering input.

---

### GAP-010: Integration with LoLa

**What we know:**
- LoLa depends on score-baselibs for OS abstraction, shared memory, and concurrency primitives.
- Our LoLa test execution already exercises baselibs code paths transitively.
- When LoLa tests pass, they implicitly verify that the baselibs APIs used by LoLa are correct.

**What we need to verify:**
- Which baselibs APIs are actually exercised by LoLa tests (coverage intersection).
- Whether any baselibs APIs are NOT tested through LoLa integration (the untested surface).
- Version pinning: confirm LoLa's `MODULE.bazel` pins a specific baselibs commit.

**Expected outcome:** PARTIAL PASS — transitive verification covers integration correctness, but standalone baselibs coverage may reveal gaps not hit by LoLa.

---

### GAP-011: Mock Completeness

**What we know:**
- score-baselibs uses the Object Seam pattern for mocking OS calls — each OS API has a mock variant that can be injected during testing.
- Complete mock coverage is essential for consumers (like LoLa) to write deterministic unit tests.
- Incomplete mocks force consumers to either skip testing or write integration tests (slower, less deterministic).

**What we need to verify:**
- Every public API in `score/os` has a corresponding mock in `score/os/mocklib` (or equivalent).
- Mock behavior matches real implementation semantics (error codes, return values, side effects).
- Mock injection mechanism works correctly with Bazel dependency overrides.

**Evidence path:** Static enumeration of public headers vs mock headers, automated completeness check.

**Expected outcome:** Likely PASS — the Object Seam pattern is a core architectural decision, so mocks should be comprehensive.

---

### GAP-012: Security Fuzzing

**What we know:**
- score-baselibs includes parsers (JSON), network protocol handlers, and shared memory APIs — all classic fuzzing targets.
- No fuzzing targets (`cc_fuzz_test` or `LLVMFuzzerTestOneInput`) are visible in the upstream repository.
- Automotive security (ISO 21434) increasingly requires fuzzing of attack surfaces.
- Shared memory APIs are particularly sensitive — malformed data from another process could cause crashes.

**What we need to verify:**
- Identify all input-parsing code paths in score-baselibs.
- Write or locate fuzz targets for JSON parsing, network protocol handling, and shared memory deserialization.
- Run fuzz campaigns (minimum 1M iterations per target) and report findings.

**Expected outcome:** GAP CONFIRMED — fuzzing is likely missing and will need to be added as part of our security verification strategy.

---

## Honest Assessment

### What We Already Know

1. **Upstream CI is green.** score-baselibs merges are gated on passing CI, meaning the codebase compiles and all tests pass on upstream infrastructure.

2. **LoLa transitively proves baselibs.** Our LoLa test execution (GAP-LOLA-001) already exercises score-baselibs code paths. LoLa's ~170+ tests depend on baselibs OS abstraction, shared memory, and concurrency primitives. When those tests pass, baselibs is implicitly verified for those use cases.

3. **Mature codebase with strong contributor base.** score-baselibs has ~64 contributors (vs ~20 for LoLa), indicating a more mature and more thoroughly reviewed codebase. Foundation libraries attract more scrutiny because every bug propagates to all consumers.

4. **Architecture is sound.** The Object Seam pattern for OS mocking, the clean Linux/QNX split, and the comprehensive test suite all indicate professional-grade engineering.

### What We Need to Verify Locally

1. **Build on our host** — confirm hermetic build reproduces on our specific Linux version.
2. **Run tests locally** — verify zero failures outside upstream CI.
3. **Measure coverage** — quantify what percentage of baselibs is tested, especially ASIL-B modules.
4. **Sanitizer runs** — ASan, UBSan, LSan, TSan to verify memory safety and concurrency correctness.
5. **Mock completeness audit** — ensure every OS API has a testable mock.

### Predicted Outcome

**HIGH confidence of PASS.**

score-baselibs is the most mature component in the S-CORE stack. Its risk profile is lower than LoLa because:
- It is a library, not a service — no deployment, orchestration, or runtime state machine complexity.
- It has 3x more contributors than LoLa, meaning more review cycles.
- It is transitively verified by every S-CORE module that depends on it.
- The primary gaps (QNX, WCET, fuzzing) are infrastructure/process gaps, not code quality gaps.

The main unknowns are coverage depth for ASIL-B components and whether TSan finds any races in lock-free code. Both are verifiable through execution.

---

## Next Steps

1. Execute GAP-001 and GAP-002 (build + test) — estimated 30 minutes.
2. Execute GAP-003 and GAP-004 (sanitizers) — estimated 1 hour.
3. Execute GAP-008 (coverage) — estimated 30 minutes.
4. Produce v2 gap analysis with execution evidence.
