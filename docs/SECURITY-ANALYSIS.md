---
document_id: SEC-ANALYSIS-001
title: "Security Analysis — S-CORE Module Stack"
date: 2026-03-23
---

# Security Analysis — S-CORE Module Stack

## 1. Sanitizer Evidence

| Module | ASan | UBSan | LSan | TSan |
|---|---|---|---|---|
| LoLa | Clean (252 tests) | Clean | Clean | Clean (224 tests) |
| baselibs | Clean (278 tests) | Clean | Clean | Not run |
| lifecycle | Clean (5 tests) | — | — | — |
| persistency | Not run | Not run | Not run | Not run |
| feo | Not run | Not run | Not run | Not run |

## 2. Memory Safety
- **LoLa + baselibs**: Zero memory errors across 530 tests under ASan
- **Rust components** (lifecycle, persistency, feo): Memory-safe by language design
- **C++ components**: Protected by sanitizer coverage

## 3. Input Validation
| Module | Input Boundary | Validation Status |
|---|---|---|
| LoLa | CAN bus frames, shared memory | Verified via edge-case tests |
| baselibs | OS API wrappers | Object Seam pattern, mock-tested |
| lifecycle | FlatBuffers config, process signals | Schema-validated (FlatBuffers) |
| persistency | KVS keys/values, JSON, file I/O | CRC validation (Adler-32), JSON parsing |
| feo | IPC messages, scheduler config | Protobuf-validated (prost) |

## 4. Known Security Gaps
1. No fuzzing (libFuzzer/AFL) for any module
2. No SAST (static application security testing) beyond clang-tidy
3. Shared memory permissions (LoLa: world-readable 0666 for QM)
4. persistency: Adler-32 CRC is not cryptographic — not tamper-proof
5. lifecycle: Launch manager daemon runs with elevated privileges
6. feo: IPC shared memory (iceoryx2/Linux SHM) permissions not audited

## 5. Recommendations
- Priority 1: Add libFuzzer targets for JSON parsing (baselibs), KVS operations (persistency)
- Priority 2: Audit shared memory permissions across LoLa, feo
- Priority 3: SAST integration in CI (CodeQL or Semgrep)
