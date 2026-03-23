---
document_id: GAP-BL-003
title: "Gap Analysis v3 — After Bench Execution (x86_64 Laptop)"
version: "3.0"
status: verified
date: 2026-03-23
previous: GAP-BL-002
---

# score-baselibs Gap Analysis v3 — After Bench Execution

## Summary

| Status | v1 | v2 | v3 |
|---|---|---|---|
| Closed | 0 | 4 | **8** |
| Blocked | 2 | 2 | **0** |
| Open | 10 | 6 | **3** |
| Findings | 0 | 3 | **4** |

**Method:** Bazel build + test on x86_64 Ubuntu 24.04 laptop (16 cores, 14GB RAM) using `--config=bl-x86_64-linux` with GCC 12.2.0 hermetic toolchain.

---

## Newly Closed Gaps (v2 → v3)

### GAP-001: Build Verification — CLOSED

**Command:** `bazel build --config=bl-x86_64-linux //score/...`
**Result:**
- 755 targets built
- 3,055 total actions (1,744 compiled)
- 200 seconds, Critical Path 24.56s
- **Zero errors**

### GAP-002: Unit Test Execution — CLOSED

**Command:** `bazel test --config=bl-x86_64-linux //score/... --test_output=summary`
**Result:**
- 283 test targets found
- 279 executed, 4 skipped
- **278 PASS, 1 FAIL**
- Failed: `abortsuponexception_toolchain_test` — upstream CI also excludes this test
- Skipped: 4 tests (platform-specific or manual-tagged)

### GAP-003: ASan/UBSan/LSan — CLOSED

**Command:** `bazel test --config=bl-x86_64-linux --config=asan_ubsan_lsan //score/...`
**Result:**
- 279 executed, 4 skipped
- **278 PASS, 1 FAIL** (same toolchain test)
- **Zero memory errors (ASan)**
- **Zero undefined behavior (UBSan)**
- **Zero memory leaks (LSan)**

### GAP-005: QNX Cross-Compile — RECLASSIFIED

Previously BLOCKED. Now reclassified: QNX deferred in favor of Linux on Pi. The aarch64-linux cross-compile path is available via `--config=bl-aarch64-linux`. QNX is no longer a blocker — it's a future optional target.

### GAP-006: QNX Test Execution — RECLASSIFIED

Same as GAP-005. Linux on Pi replaces QNX as the target platform.

---

## Previously Closed (from v2)

- **GAP-010**: Integration with LoLa — transitively proven
- **GAP-011**: Mock completeness — analyzed (FINDING-BL-001)
- **GAP-009**: WCET validation — reclassified as upstream limitation

---

## Remaining Open Gaps

### GAP-004: TSan (Thread Sanitizer) — OPEN
Not yet executed. Upstream CI doesn't run TSan separately for baselibs (only ASan/UBSan/LSan). Would need custom config.

### GAP-008: Coverage Measurement — IN PROGRESS
`bazel coverage --config=bl-x86_64-linux //score/...` running on laptop. Results pending.

### GAP-012: Security Fuzzing — OPEN
No fuzzing infrastructure exists upstream.

---

## Findings

| ID | Severity | Description |
|---|---|---|
| FINDING-BL-001 | Medium | Mock coverage low: concurrency 10%, memory 13.6%, mw/log 7.7% |
| FINDING-BL-002 | Info | No benchmark targets despite google_benchmark dep |
| FINDING-BL-003 | Info | 296 Bazel test targets (file grouping) |
| FINDING-BL-004 | Info | GCC 13.3 (Ubuntu 24.04 system) triggers new warnings vs GCC 12.2 (hermetic). Native aarch64 Pi build requires `-Wno-error` hacks. Proper path: x86_64 build + cross-compile. |

---

## Bench Environment

| Field | Value |
|---|---|
| Host | ASUS TUF Gaming A17 (an-dao) |
| OS | Ubuntu 24.04, Kernel 6.17.0-19-generic |
| CPU | 16 cores @ x86_64 |
| RAM | 14 GB |
| Bazel | 9.0.1 (Bazelisk) → downloads 8.3.1 per .bazelversion |
| GCC | 12.2.0 (hermetic, downloaded by Bazel) |
| Config | `--config=bl-x86_64-linux` |

---

**End of Gap Analysis v3 — GAP-BL-003**
