---
document_id: VR-FEO-001
title: "SWE.4 Unit Verification Report — score-feo"
date: 2026-03-23
status: verified
---

# Unit Verification Report — score-feo v0.2.4

## 1. Scope
Verification of score-feo (Eclipse S-CORE Flexible Execution Orchestrator) on x86_64 Linux bench. Primarily Rust module.

## 2. Environment
- Host: ASUS TUF Gaming A17, Ubuntu 24.04, 16 cores, 14GB RAM
- Bazel: 8.3.1 (via Bazelisk 9.0.1)
- GCC: 12.2.0 (hermetic, downloaded by Bazel)
- Config: --config=bl-x86_64-linux

## 3. Build Verification
| Metric | Result |
|---|---|
| Command | `bazel build --config=bl-x86_64-linux //score/...` |
| Targets | 85 |
| Actions | 2,729 |
| Duration | 305s |
| **Status** | **PASS** |

## 4. Unit Test Results
| Metric | Result |
|---|---|
| Command | `bazel test --config=bl-x86_64-linux //score/...` |
| Test targets | 8 |
| Executed | 8 |
| Passed | **8** |
| Failed | 0 |
| **Status** | **PASS** |

### Test Breakdown
| Test | Language | Result |
|---|---|---|
| feo-time CC | C++ | PASS |
| feo-time Rust | Rust | PASS |
| cpp_test_main | C++ | PASS |
| feo_tests integration | Rust | PASS |
| format_check (Python) | Python | PASS |
| format_check (Rust) | Rust | PASS |
| format_check (Starlark) | Starlark | PASS |
| format_check (YAML) | YAML | PASS |

## 5. Format Check Results
| Format | Result |
|---|---|
| Python | **PASS** |
| Rust | **PASS** |
| Starlark | **PASS** |
| YAML | **PASS** |
| **Overall** | **4/4 PASS** |

## 6. Verdict
**PASS** — All verification criteria met. score-feo v0.2.4 is verified for integration.
