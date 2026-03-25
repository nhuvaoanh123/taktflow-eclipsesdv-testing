---
document_id: SCORE-ORCH-INDEX
title: "score-orchestrator — ASPICE + QM Document Registry"
version: "1.0"
status: active
date: 2026-03-25
---

# score-orchestrator — Document Registry

Rust workload orchestration framework for S-CORE. **QM rated.**
Manages program lifecycle and deployment across ECU software partitions.

## Module Profile

| Attribute | Value |
|---|---|
| Module | score_orchestrator v0.0.0 (workspace v0.0.3) |
| Language | Rust (edition 2021) |
| Build | Bazel 8.3.0 + Cargo (dual) |
| Rust toolchain | 1.85.0 (pinned) |
| ASIL | QM |
| Key consumers | score-feo (activity scheduling), ECU deployment tooling |

## Components

| Component | Type | Description |
|---|---|---|
| `src/orchestration` | Library | Core: programs, actions, events, api, core, testing |
| `src/orchestration_macros` | Proc-macro | Derive macros for program definition |
| `src/xtask` | Binary | Cargo task runner (codegen, benchmarks) |
| `tests/test_scenarios/rust` | CIT | Component integration test scenarios |

## Security Properties

| Property | Status |
|---|---|
| kyron pinned by rev hash | VERIFIED |
| iceoryx2-ipc feature-gated | VERIFIED |
| proc-macro: no unsafe | VERIFIED |
| proc-macro: no fs access | VERIFIED |
| Cargo.lock reproducible build | VERIFIED (lock file present) |

## Requirement ID Format

| Level | Pattern | Example |
|---|---|---|
| SWR | `SWR-ORCH-NNN` | SWR-ORCH-001 |
| Integration | `INT-ORCH-NNN` | INT-ORCH-001 |
| Security | `SEC-ORCH-NNN` | SEC-ORCH-001 |

## ASPICE Work Products

| Process | Work Product | Status |
|---|---|---|
| SWE.1 | Software requirements | Not yet defined |
| SWE.3 | Detailed design | src/orchestration/doc/ exists |
| SWE.4 | Unit test spec | Test files created (pending execution) |
| SWE.5 | Integration test spec | test_dependency_chain.py (pending run) |
| SWE.6 | CIT results | tests/test_scenarios/rust/ (pending run) |
