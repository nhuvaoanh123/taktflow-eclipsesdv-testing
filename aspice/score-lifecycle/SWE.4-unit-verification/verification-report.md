---
document_id: VR-LC-001
title: "SWE.4 Unit Verification Report — score-lifecycle"
date: 2026-03-23
status: verified
---

# Unit Verification Report — score-lifecycle v0.2.4

## 1. Scope
Verification of score-lifecycle (Eclipse S-CORE lifecycle management) on x86_64 Linux bench. Dual-language module (C++ and Rust).

## 2. Environment
- Host: ASUS TUF Gaming A17, Ubuntu 24.04, 16 cores, 14GB RAM
- Bazel: 8.3.1 (via Bazelisk 9.0.1)
- GCC: 12.2.0 (hermetic, downloaded by Bazel)
- Config: --config=bl-x86_64-linux

## 3. Build Verification
| Metric | Result |
|---|---|
| Command | `bazel build --config=bl-x86_64-linux //score/...` |
| Targets | 59 |
| Actions | 1,087 |
| Duration | 232s |
| **Status** | **PASS** |

## 4. Unit Test Results
| Metric | Result |
|---|---|
| Command | `bazel test --config=bl-x86_64-linux //score/...` |
| Test targets | 6 |
| Executed | 6 |
| Passed | **6** |
| Failed | 0 |
| **Status** | **PASS** |

### Test Breakdown
| Test | Language | Result |
|---|---|---|
| cpp_tests | C++ | PASS |
| loom_tests | Rust | PASS |
| tests | Rust | PASS |
| identifier_hash_UT | C++ | PASS |
| processstateclient_UT | C++ | PASS |
| smoke | Integration | PASS |

## 5. Sanitizer Results
### ASan/UBSan/LSan
| Metric | Result |
|---|---|
| Command | `bazel test --config=bl-x86_64-linux --config=asan_ubsan_lsan //score/...` |
| Executed | 5 |
| Passed | **5** |
| Memory errors (ASan) | **0** |
| Undefined behavior (UBSan) | **0** |
| Memory leaks (LSan) | **0** |
| **Status** | **PASS** |

## 6. Code Coverage
| Metric | Result |
|---|---|
| Command | `bazel coverage --config=bl-x86_64-linux //score/...` |
| Files instrumented | 65 |
| Lines hit | 316 |
| Lines total | 385 |
| **Coverage** | **82.1%** |
| Target | >=76% |

## 7. Verdict
**PASS** — All verification criteria met. score-lifecycle v0.2.4 is verified for integration. Coverage at 82.1% exceeds the 76% target threshold.
