---
document_id: VR-PS-001
title: "SWE.4 Unit Verification Report — score-persistency"
date: 2026-03-23
status: verified
---

# Unit Verification Report — score-persistency v0.2.4

## 1. Scope
Verification of score-persistency (Eclipse S-CORE key-value store persistence layer) on x86_64 Linux bench. ASIL-D rated module. Dual-language module (C++ and Rust).

## 2. Environment
- Host: ASUS TUF Gaming A17, Ubuntu 24.04, 16 cores, 14GB RAM
- Bazel: 8.3.1 (via Bazelisk 9.0.1)
- GCC: 12.2.0 (hermetic, downloaded by Bazel)
- Config: --config=bl-x86_64-linux

## 3. Build Verification
| Metric | Result |
|---|---|
| Command | `bazel build --config=bl-x86_64-linux //score/...` |
| Targets | 9 |
| Actions | 755 |
| Duration | 67s |
| **Status** | **PASS** |

## 4. Unit Test Results
### C++ Unit Tests
| Metric | Result |
|---|---|
| Test | test_kvs_cpp |
| **Status** | **PASS** |

### Rust Unit Tests
| Metric | Result |
|---|---|
| Test | rust_kvs:tests |
| **Status** | **PASS** |

## 5. Component Integration Tests (CIT)
### CIT C++
| Metric | Result |
|---|---|
| **Status** | **PASS** |

### CIT Rust
| Metric | Result |
|---|---|
| **Status** | **PASS** |

## 6. Benchmark Results
| Metric | Result |
|---|---|
| Test | bm_kvs_cpp |
| **Status** | **PASS** |

## 7. Code Coverage (C++)
| Metric | Result |
|---|---|
| Command | `bazel coverage --config=bl-x86_64-linux //score/...` |
| Files instrumented | 21 |
| Lines hit | 716 |
| Lines total | 751 |
| **Coverage** | **95.3%** |

## 8. Safety Classification
| Attribute | Value |
|---|---|
| ASIL Rating | **ASIL-D** |
| Languages | C++, Rust |
| Coverage requirement | Met (95.3%) |

## 9. Verdict
**PASS** — All verification criteria met. score-persistency v0.2.4 (ASIL-D) is verified for integration.
