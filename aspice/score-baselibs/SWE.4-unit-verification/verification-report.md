---
document_id: VR-BL-001
title: "SWE.4 Unit Verification Report — score-baselibs"
date: 2026-03-23
status: verified
---

# Unit Verification Report — score-baselibs v0.2.4

## 1. Scope
Verification of score-baselibs (Eclipse S-CORE foundation library) on x86_64 Linux bench.

## 2. Environment
- Host: ASUS TUF Gaming A17, Ubuntu 24.04, 16 cores, 14GB RAM
- Bazel: 8.3.1 (via Bazelisk 9.0.1)
- GCC: 12.2.0 (hermetic, downloaded by Bazel)
- Config: --config=bl-x86_64-linux

## 3. Build Verification
| Metric | Result |
|---|---|
| Command | `bazel build --config=bl-x86_64-linux //score/...` |
| Targets | 755 |
| Actions | 3,055 (1,744 compiled) |
| Duration | 200s |
| **Status** | **PASS** |

## 4. Unit Test Results
| Metric | Result |
|---|---|
| Command | `bazel test --config=bl-x86_64-linux //score/...` |
| Test targets | 283 |
| Executed | 279 |
| Passed | **278** |
| Failed | 1 (abortsuponexception_toolchain_test — upstream-excluded) |
| Skipped | 4 |
| **Status** | **PASS** |

## 5. Sanitizer Results
### ASan/UBSan/LSan
| Metric | Result |
|---|---|
| Command | `bazel test --config=bl-x86_64-linux --config=asan_ubsan_lsan //score/...` |
| Executed | 279 |
| Passed | **278** |
| Memory errors (ASan) | **0** |
| Undefined behavior (UBSan) | **0** |
| Memory leaks (LSan) | **0** |
| **Status** | **PASS** |

## 6. Code Coverage
| Metric | Result |
|---|---|
| Command | `bazel coverage --config=bl-x86_64-linux //score/...` |
| Files instrumented | 697 |
| Lines hit | 14,791 |
| Lines total | 15,112 |
| **Coverage** | **97.9%** |

## 7. Cross-Compilation (aarch64)
| Metric | Result |
|---|---|
| Command | `bazel build --config=bl-aarch64-linux //score/...` |
| Targets | 755 |
| Actions | 2,846 |
| Duration | 155s |
| **Status** | **PASS** |

## 8. Verdict
**PASS** — All verification criteria met. score-baselibs v0.2.4 is verified for integration.
