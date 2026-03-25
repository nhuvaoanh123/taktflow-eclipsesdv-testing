---
document_id: SCORE-LOG-INDEX
title: "score-logging — ASPICE + QM Document Registry"
version: "1.0"
status: active
date: 2026-03-25
---

# score-logging — Document Registry

DLT-compatible structured logging for all S-CORE modules. **QM rated** but used as
a foundation by ASIL-B components — logging must not corrupt caller state.

## Module Profile

| Attribute | Value |
|---|---|
| Module | score_logging v0.0.0 |
| Language | C++17 + Rust |
| Build | Bazel 8.3.0 |
| ASIL | QM |
| Platforms | x86_64 Linux, AArch64, QNX 8.0 |
| Key consumers | score-feo, score-communication, score-persistency, score-lifecycle |

## Components

| Component | ASIL | Description |
|---|---|---|
| `score/mw/log` | QM | Logging frontend: shared-memory writer, fake/console recorders |
| `score/mw/log/rust` | QM | Rust language bindings for the logging frontend |
| `score/datarouter` | QM | DLT daemon bridge: routes log records to DLT Viewer / syslog |
| `score/mw/log/legacy_non_verbose_api` | QM | Backward-compatible DLT non-verbose API |

## Safety Properties

| Property | Requirement | Status |
|---|---|---|
| Object Seam mocks | Callers must be testable without real daemon | VERIFIED — fake_recorder, session_handle_mock.h |
| No allocation in hot path | Circular buffer avoids malloc | STRUCTURAL (not yet instrumented) |
| Atomic writes | Torn writes must not be visible to readers | STRUCTURAL (not yet verified via TSan) |
| Rust unsafe justification | All unsafe blocks must have # SAFETY: comment | TEST WRITTEN (not run) |

## Requirement ID Format

| Level | Pattern | Example |
|---|---|---|
| SWR | `SWR-LOG-NNN` | SWR-LOG-001 |
| Integration | `INT-LOG-NNN` | INT-LOG-001 |
| Security | `SEC-LOG-NNN` | SEC-LOG-001 |

## ASPICE Work Products

| Process | Work Product | Status |
|---|---|---|
| SWE.1 | Software requirements | TRLC declared, not activated |
| SWE.3 | Software detailed design | score/mw/log/design/ exists |
| SWE.4 | Unit test specification | Test files created (pending execution) |
| SWE.5 | Integration test spec | test_dependency_chain.py (pending run) |
| SWE.6 | System test results | Not yet executed |
| SUP.1 | Quality assurance | TRLC + Bazel quality gates |
