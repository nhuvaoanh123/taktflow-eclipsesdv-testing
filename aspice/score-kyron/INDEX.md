---
document_id: SCORE-KYR-INDEX
title: "Eclipse S-CORE Kyron — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-kyron — Document Registry

Safe async runtime for Rust — like tokio but designed for safety-critical automotive.

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 308 |
| Contributors | 18 |
| Language | Rust |
| Build | Bazel + Cargo |
| ASIL | B |
| Platforms | Linux, QNX 8 |
| Target Chip | Pi (QNX) |
| QNX Notes | `internal_docs/qnx.md` — QNX-specific implementation details |

## Safety Goals

### SG-KYR-001: Deterministic Async Execution

- **ASIL**: B
- **Traces down**: FSR-KYR-001, FSR-KYR-002
- **Fault Tolerance Time**: Task deadline

Async tasks scheduled on Kyron SHALL execute without unbounded blocking. The runtime SHALL guarantee progress on all spawned tasks within a bounded number of scheduler ticks.

### SG-KYR-002: No Unsafe Memory in Runtime Core

- **ASIL**: B
- **Traces down**: FSR-KYR-003
- **Fault Tolerance Time**: 0 ms

The Kyron runtime core SHALL minimize use of `unsafe` Rust. All `unsafe` blocks SHALL be documented with safety invariants, reviewed by safety engineer, and verified by MIRI where applicable.

## Traceability Chain

```
SG-KYR-001: Deterministic Async Execution
├── FSR-KYR-001: Bounded Task Queue
│   └── TSR-KYR-001 → SSR-KYR-RT-001 → SWR-KYR-RT-001
└── FSR-KYR-002: Cooperative Cancellation
    └── TSR-KYR-002 → SSR-KYR-RT-002 → SWR-KYR-RT-002

SG-KYR-002: No Unsafe Memory
└── FSR-KYR-003: Unsafe Block Documentation + Review
    └── TSR-KYR-003 → SSR-KYR-RT-003 → SWR-KYR-RT-003
```
