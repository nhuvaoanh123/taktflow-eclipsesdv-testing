---
document_id: SCORE-SEC-INDEX
title: "Eclipse S-CORE Security & Cryptography — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-inc_security_crypto — Document Registry

Security and cryptography feature for S-CORE — **your scorehsm is the reference implementation**.

## Module Profile

| Attribute | Value |
|---|---|
| Upstream Commits | 1 (incubation — 43 requirements defined, no implementation) |
| Language | Starlark (spec only) |
| ASIL | B |
| Target Chip | L552ZE (HSM) — TrustZone hardware crypto |
| Your Implementation | `scorehsm/` submodule — 274 tests, 10 phases complete |

## Relationship to scorehsm

| Aspect | score-inc_security_crypto | Your scorehsm |
|---|---|---|
| Status | 43 requirements, no code | 274 tests, CI green |
| Crypto backend | Not implemented | STM32L552 AES/PKA/HASH/RNG |
| Key storage | Not implemented | TrustZone secure world |
| Transport | Not implemented | USB CDC (Pi ↔ L552ZE) |
| Language | — | Rust (firmware + host) |

## Safety Goals

### SG-SEC-001: Key Material Never Leaves HSM

- **ASIL**: B
- **Traces down**: FSR-SEC-001
- **Fault Tolerance Time**: 0 ms

Private keys and symmetric keys SHALL never leave the L552ZE TrustZone secure world. Only opaque key handles and computed results (ciphertext, MACs, signatures) cross the USB boundary.

### SG-SEC-002: Crypto Operation Integrity

- **ASIL**: B
- **Traces down**: FSR-SEC-002
- **Fault Tolerance Time**: 0 ms

Cryptographic operations (AES, HMAC, ECDSA) SHALL produce correct results. Hardware crypto accelerator output SHALL be verified against known test vectors during initialization.

## Note

The 43 upstream requirements in `score-inc_security_crypto` directly map to your `scorehsm` implementation. Your scorehsm already covers FSR-01 through FSR-16 with 274 tests. Refer to `scorehsm/docs/` for the complete V-model artifact set.
