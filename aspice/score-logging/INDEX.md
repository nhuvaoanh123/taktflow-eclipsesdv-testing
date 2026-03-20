---
document_id: SCORE-LOG-INDEX
title: "Eclipse S-CORE Logging — ASPICE Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-logging — Document Registry

Centralized logging daemon with shared-memory backend.

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 102 |
| Contributors | 22 |
| Languages | C++, Rust |
| Build | Bazel |
| ASIL | QM (logging is not safety-critical path) |
| Target Chip | Pi (QNX) |

## Components

| Component | ASIL | Description |
|---|---|---|
| Log Frontend | QM | Shared memory circular buffer writer, per-process |
| Log Backend (File) | QM | File output backend, reads from shared memory |
| Log Backend (DataRouter) | QM | Network forwarding of log entries |
| Configuration | QM | Runtime log level configuration |

## Note

Logging is classified QM because it is not in the safety-critical data path. However, it shares the shared memory infrastructure with LoLa (baselibs), so its implementation must not interfere with ASIL-B shared memory regions (freedom from interference verified by baselibs DFA).

No safety goals defined for this module. ASPICE SWE.1-SWE.6 documentation applies without SAF work products.
