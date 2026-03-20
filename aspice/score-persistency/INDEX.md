---
document_id: SCORE-PER-INDEX
title: "Eclipse S-CORE Persistency — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-persistency — Document Registry

Key-value storage (KVS) for non-volatile data on the QNX HPC.

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 379 |
| Contributors | 38 |
| Language | Rust |
| Build | Bazel + Cargo |
| ASIL | B |
| Target Chip | Pi (QNX) |
| Upstream Safety Docs | 8 (safety plan, FMEA, DFA, safety manual, FDR, security plan) |

## Components

| Component | ASIL | Description |
|---|---|---|
| `kvs` | B | Key-value store core — get, set, remove, snapshot |
| `json` | QM | JSON serialization backend |

## Safety Goals

### SG-PER-001: Data Persistence Integrity

- **ASIL**: B
- **Traces down**: FSR-PER-001, FSR-PER-002
- **Fault Tolerance Time**: Power cycle (data must survive)

Stored key-value data SHALL NOT be corrupted or lost due to normal shutdown, unexpected power loss, or process crash. Data read after restart SHALL match the last successfully committed write.

### SG-PER-002: Snapshot Atomicity

- **ASIL**: B
- **Traces down**: FSR-PER-003
- **Fault Tolerance Time**: 0 ms

Snapshot operations (save/restore) SHALL be atomic. A partial snapshot (due to crash during write) SHALL NOT corrupt the existing stored data. The system SHALL roll back to the last valid snapshot on recovery.

## Requirement ID Format

| Level | Pattern | Example |
|---|---|---|
| SG | `SG-PER-NNN` | SG-PER-001 |
| FSR | `FSR-PER-NNN` | FSR-PER-001 |
| TSR | `TSR-PER-NNN` | TSR-PER-001 |
| SSR | `SSR-PER-[COMP]-NNN` | SSR-PER-KVS-001 |
| SWR | `SWR-PER-[COMP]-NNN` | SWR-PER-KVS-001 |

## Traceability Chain

```
SG-PER-001: Data Persistence Integrity
├── FSR-PER-001: Write-Ahead Logging
│   └── TSR-PER-001 → SSR-PER-KVS-001 → SWR-PER-KVS-001
├── FSR-PER-002: CRC Verification on Read
│   └── TSR-PER-002 → SSR-PER-KVS-002 → SWR-PER-KVS-002
SG-PER-002: Snapshot Atomicity
└── FSR-PER-003: Atomic Snapshot with Rollback
    └── TSR-PER-003 → SSR-PER-KVS-003 → SWR-PER-KVS-003
```

## Upstream Safety Documents (from score-persistency repo)

Already placed in SAF-functional-safety/:
- `safety_manual.rst` — Module safety manual
- `module_safety_plan.rst` — Module safety plan
- `module_safety_plan_fdr.rst` — Safety plan FDR
- `module_safety_package_fdr.rst` — Safety package FDR
- `fmea.rst` — Failure mode and effects analysis
- `dfa.rst` — Dependent failure analysis
- `module_security_plan_fdr.rst` — Security plan FDR
- `module_security_package_fdr.rst` — Security package FDR
