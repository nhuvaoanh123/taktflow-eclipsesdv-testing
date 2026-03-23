---
document_id: TQ-001
title: "Tool Qualification — ISO 26262-8 Table 4"
date: 2026-03-23
---

# Tool Qualification per ISO 26262-8

## Tool Classification

| Tool | TI | TCL | Justification |
|---|---|---|---|
| Bazel 8.3-8.4 | TI1 | TCL1 | Build orchestrator — errors result in build failure, not silent corruption |
| GCC 12.2.0 | TI2 | TCL2 | Compiler — could inject errors into object code |
| Rust (Ferrocene) | TI2 | TCL2 | Compiler — same as GCC. Ferrocene is ISO 26262 qualified. |
| GoogleTest | TI1 | TCL1 | Test framework — false PASS is possible but mitigated by sanitizers |
| ASan/UBSan/LSan | TI1 | TCL1 | Verification tool — false negatives possible but cannot introduce errors |
| TSan | TI1 | TCL1 | Verification tool — same as ASan |
| LCOV | TI1 | TCL1 | Coverage measurement — under-reporting possible, not over-reporting |
| Clang-Tidy | TI1 | TCL1 | Static analysis — advisory, does not modify code |
| Python/pytest | TI1 | TCL1 | Test orchestration — same as GoogleTest |
| Git | TI1 | TCL1 | Configuration management — errors are detectable |
| QEMU | TI2 | TCL2 | Emulation — behavioral differences vs real hardware possible |

## Qualification Evidence

### TI1 Tools (no qualification needed)
These tools cannot introduce errors into the safety-related item. No further qualification required per ISO 26262-8 clause 11.4.6.

### TI2 Tools (qualification required)
| Tool | Qualification Method | Evidence |
|---|---|---|
| GCC 12.2.0 | Use case analysis + test results | 278/279 tests pass, 97.9% coverage, sanitizers clean |
| Ferrocene Rust | Vendor-qualified | Ferrocene is ISO 26262 ASIL-D qualified Rust compiler |
| QEMU | Comparison with target | aarch64 cross-compile proven; native Pi execution validates QEMU results |

## Notes
- Bazel hermetic builds ensure reproducibility (same toolchain, same output)
- Ferrocene Rust compiler is the only vendor-qualified compiler in the stack
- GCC qualification relies on extensive test evidence rather than vendor certification
