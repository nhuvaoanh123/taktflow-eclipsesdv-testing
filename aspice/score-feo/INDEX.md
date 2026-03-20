---
document_id: SCORE-FEO-INDEX
title: "Eclipse S-CORE FEO — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-feo — Document Registry

Fixed Execution Order framework for deterministic real-time scheduling.

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 52 |
| Contributors | 20 |
| Language | Rust |
| Build | Bazel + Cargo |
| ASIL | B |
| Target Chip | TMS570 (CVC) — safety-critical lockstep core |

## Safety Goals

### SG-FEO-001: Deterministic Task Execution Order

- **ASIL**: B
- **Traces down**: FSR-FEO-001, FSR-FEO-002
- **Fault Tolerance Time**: 1 cycle period

Tasks registered with FEO SHALL execute in the exact configured order on every cycle. No re-ordering, skipping, or double-execution SHALL occur under any system load condition.

### SG-FEO-002: Cycle Time Bounded Execution

- **ASIL**: B
- **Traces down**: FSR-FEO-003
- **Fault Tolerance Time**: 1 cycle period

Each FEO cycle SHALL complete within the configured cycle time. Overrun SHALL be detected and reported.

## Traceability Chain

```
SG-FEO-001: Deterministic Order
├── FSR-FEO-001: Static Task Graph
│   └── TSR-FEO-001 → SSR-FEO-SCHED-001 → SWR-FEO-SCHED-001
└── FSR-FEO-002: No Dynamic Task Addition at Runtime
    └── TSR-FEO-002 → SSR-FEO-SCHED-002 → SWR-FEO-SCHED-002

SG-FEO-002: Cycle Time Bounded
└── FSR-FEO-003: Overrun Detection
    └── TSR-FEO-003 → SSR-FEO-SCHED-003 → SWR-FEO-SCHED-003
```
