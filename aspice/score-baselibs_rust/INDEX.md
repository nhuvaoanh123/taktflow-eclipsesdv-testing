---
document_id: SCORE-BLR-INDEX
title: "Eclipse S-CORE Base Libraries (Rust) — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-baselibs_rust — Document Registry

Foundation Rust libraries for S-CORE Rust modules (kyron, orchestrator, persistency, feo).

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 87 |
| Contributors | 14 |
| Language | Rust |
| Build | Bazel + Cargo |
| ASIL | B |
| Upstream Safety Docs | 5 (safety plan, package FDR, plan FDR, safety manual, FMEA/DFA) |

## Components

| Component | ASIL | Description |
|---|---|---|
| `containers_rust` | B | Fixed-size containers (no heap allocation) |
| `log` | QM | Rust logging abstraction with global/local logger |

## Safety Goals

### SG-BLR-001: Container Memory Safety

- **ASIL**: B
- **Traces down**: FSR-BLR-001
- **Fault Tolerance Time**: 0 ms

Fixed-size containers SHALL prevent buffer overflow and SHALL panic (abort in ASIL-B context) on out-of-bounds access rather than producing undefined behavior.

## Upstream Safety Documents (already in SAF-functional-safety/)

- `safety_manual.rst`
- `module_safety_plan.rst`
- `module_safety_plan_fdr.rst`
- `module_safety_package_fdr.rst`
- `fmea.rst` + `dfa.rst` (log component)
