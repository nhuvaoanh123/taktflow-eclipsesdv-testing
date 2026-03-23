---
document_id: SCORE-LC-INDEX
title: "Eclipse S-CORE Lifecycle — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-lifecycle — Document Registry

Launch manager daemon + health monitor for the QNX HPC.

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 218 |
| Contributors | 29 |
| Languages | C++, Rust |
| Build | Bazel |
| ASIL | B (health monitor), QM (launch manager) |
| Platforms | Linux, QNX 7, QNX 8 |
| Target Chip | Pi (QNX) |
| Upstream Safety Docs | 2 (FMEA + DFA for health monitor) |

## Components

| Component | ASIL | Description |
|---|---|---|
| **Launch Manager Daemon** | QM | Process group management, startup/shutdown ordering, dependency resolution, recovery actions |
| **Health Monitor** | B | Alive supervision, deadline supervision, logical supervision, external watchdog integration |
| **Lifecycle Client Library** | B | Client API for processes to register with lifecycle manager |

## Safety Goals

### SG-LC-001: Fault Detection via Health Monitoring

- **ASIL**: B
- **Traces down**: FSR-LC-001, FSR-LC-002, FSR-LC-003
- **Fault Tolerance Time**: Configurable per supervision (default 200 ms)

The health monitor SHALL detect process faults (hung, crashed, deadline missed) within the configured supervision timeout and trigger the configured recovery action.

### SG-LC-002: Orderly Shutdown on Critical Fault

- **ASIL**: B
- **Traces down**: FSR-LC-004
- **Fault Tolerance Time**: 5 seconds

When an ASIL-B supervised process fails and recovery is not possible, the lifecycle manager SHALL initiate an orderly shutdown of all dependent process groups to reach a safe state.

### SG-LC-003: External Watchdog Integration

- **ASIL**: B
- **Traces down**: FSR-LC-005
- **Fault Tolerance Time**: Watchdog timeout (hardware-dependent)

The health monitor SHALL periodically service the external hardware watchdog (TPS3823 on bench). If the health monitor itself fails, the watchdog SHALL trigger a hardware reset.

## Traceability Chain

```
SG-LC-001: Fault Detection
├── FSR-LC-001: Alive Supervision
│   └── TSR-LC-001 → SSR-LC-HM-001 → SWR-LC-HM-001
├── FSR-LC-002: Deadline Supervision
│   └── TSR-LC-002 → SSR-LC-HM-002 → SWR-LC-HM-002
└── FSR-LC-003: Logical Supervision
    └── TSR-LC-003 → SSR-LC-HM-003 → SWR-LC-HM-003

SG-LC-002: Orderly Shutdown
└── FSR-LC-004: Graceful Shutdown Sequence
    └── TSR-LC-004 → SSR-LC-LM-001 → SWR-LC-LM-001

SG-LC-003: External Watchdog
└── FSR-LC-005: Watchdog Servicing
    └── TSR-LC-005 → SSR-LC-HM-004 → SWR-LC-HM-004
```

## Statistics

- **Safety goals**: 3
- **FSR**: 5
- **Complete chains**: 5
- **ASIL-B requirements**: ~70%
