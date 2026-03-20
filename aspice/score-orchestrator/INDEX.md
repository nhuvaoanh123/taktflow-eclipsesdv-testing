---
document_id: SCORE-ORC-INDEX
title: "Eclipse S-CORE Orchestrator — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-orchestrator — Document Registry

Service orchestration framework for managing workloads on QNX HPC.

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 312 |
| Contributors | 18 |
| Language | Rust |
| Build | Bazel + Cargo |
| ASIL | QM (orchestration logic), B (safety-critical service management) |
| Platforms | Linux, QNX 8 |
| Target Chip | Pi (QNX) |
| QNX Notes | `internal_docs/qnx.md` — QNX-specific details |

## Safety Goals

### SG-ORC-001: Safety-Critical Service Availability

- **ASIL**: B
- **Traces down**: FSR-ORC-001, FSR-ORC-002
- **Fault Tolerance Time**: 5 seconds

ASIL-B classified services managed by the orchestrator SHALL be restarted automatically on crash within the configured recovery timeout. The orchestrator SHALL NOT itself become a single point of failure.

## Traceability Chain

```
SG-ORC-001: Safety-Critical Service Availability
├── FSR-ORC-001: Automatic Service Restart
│   └── TSR-ORC-001 → SSR-ORC-MGR-001 → SWR-ORC-MGR-001
└── FSR-ORC-002: Orchestrator Self-Monitoring
    └── TSR-ORC-002 → SSR-ORC-MGR-002 → SWR-ORC-MGR-002
```
