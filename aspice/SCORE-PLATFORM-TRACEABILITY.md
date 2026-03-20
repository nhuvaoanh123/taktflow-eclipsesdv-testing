# Eclipse S-CORE Platform Traceability — 3-Chip HPC SoC

## Platform Safety Goal Allocation

```
┌──────────────────────────────────────────────────────────────────┐
│  HPC SoC Platform Safety Goals                                   │
│                                                                  │
│  PSG-001: Vehicle data integrity end-to-end                      │
│  PSG-002: System fault detection and safe state transition        │
│  PSG-003: Security of key material and crypto operations          │
│  PSG-004: Deterministic real-time execution                       │
└──────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Pi (QNX)   │     │  TMS570 (CVC)│     │  L552ZE (HSM)│
│             │     │              │     │              │
│ SG-COM-*    │     │ SG-FEO-*     │     │ SG-SEC-*     │
│ SG-PER-*    │     │ SG-SIPGW-*   │     │              │
│ SG-LC-*     │     │ SG-DAAL-*    │     │              │
│ SG-KYR-*    │     │ SG-TIME-*    │     │              │
│ SG-ORC-*    │     │              │     │              │
│ SG-BL-*     │     │ SG-BL-*      │     │              │
└─────────────┘     └──────────────┘     └──────────────┘
```

## Cross-Module Safety Chain: Vehicle Signal Flow

```
PSG-001: Vehicle Data Integrity End-to-End

Physical Sensor
  │ (ADC/SPI on zone ECU)
  ▼
SG-DAAL-001 ──► DAAL reads sensor (TMS570)
  │
  ▼
SG-SIPGW-001 ──► SOME/IP gateway bridges to Ethernet (TMS570→Pi)
  │
  ▼
SG-COM-001 ──► LoLa IPC delivers to consumer process (Pi QNX)
  │
  ▼
SG-PER-001 ──► Persistency stores value if needed (Pi QNX)
  │
  ▼
SG-KYR-001 ──► Kyron async runtime processes the data (Pi QNX)
  │
  ▼
SG-LC-001 ──► Health monitor verifies process is alive (Pi QNX)
```

## Cross-Module Safety Chain: Fault Detection → Safe State

```
PSG-002: System Fault Detection and Safe State Transition

Process crash detected
  │
  ▼
SG-COM-003 ──► LoLa partial restart isolates crashed service
  │
  ▼
SG-LC-001 ──► Health monitor detects fault via deadline supervision
  │
  ▼
SG-ORC-001 ──► Orchestrator attempts automatic restart
  │
  ▼ (if restart fails)
SG-LC-002 ──► Lifecycle manager initiates orderly shutdown
  │
  ▼
SG-LC-003 ──► Watchdog not serviced → hardware reset (TPS3823)
```

## Module Dependency Matrix

| Module | Depends On | Used By |
|---|---|---|
| **score-baselibs** | OS kernel | ALL S-CORE modules |
| **score-baselibs_rust** | std (Rust) | kyron, orchestrator, persistency, feo |
| **score-communication** | baselibs | Application SWCs, lifecycle |
| **score-lifecycle** | baselibs, communication | orchestrator, all managed processes |
| **score-orchestrator** | kyron, lifecycle | Application deployment |
| **score-kyron** | baselibs_rust | orchestrator, persistency |
| **score-persistency** | kyron, baselibs_rust | Application SWCs |
| **score-feo** | baselibs_rust | Application SWCs (deterministic scheduling) |
| **score-inc_someip_gateway** | baselibs | communication (inter-ECU bridge) |
| **score-inc_security_crypto** | (hardware HSM) | baselibs (TLS), communication (SecOC) |
| **score-inc_daal** | baselibs | inc_someip_gateway (sensor data source) |
| **score-inc_time** | baselibs | communication, feo (synchronized timestamps) |
| **score-logging** | baselibs | ALL (non-safety, QM) |

## ASPICE Documentation Coverage

| Module | INDEX | SG | FSR | TSR | SSR | SWR | Trace Matrix | Safety Docs | Status |
|---|---|---|---|---|---|---|---|---|---|
| score-communication | Y | 3 | 6 | 10 | 12 | 14 | Y | DFA+FMEA+Plan | Complete |
| score-baselibs | Y | 3 | 5 | 7 | 7 | 8 | Y | — | Complete |
| score-persistency | Y | 2 | 3 | 3 | 3 | 3 | tree | Upstream 8 docs | Complete |
| score-lifecycle | Y | 3 | 5 | 5 | 5 | 5 | tree | Upstream 2 docs | Complete |
| score-feo | Y | 2 | 3 | 3 | 3 | 3 | tree | — | Complete |
| score-kyron | Y | 2 | 3 | 3 | 3 | 3 | tree | — | Complete |
| score-orchestrator | Y | 1 | 2 | 2 | 2 | 2 | tree | — | Complete |
| score-logging | Y | — | — | — | — | — | — | — | QM only |
| score-baselibs_rust | Y | 1 | 1 | — | — | — | — | Upstream 5 docs | Complete |
| score-inc_someip_gateway | Y | 2 | 2 | — | — | — | — | Upstream arch | Complete |
| score-inc_security_crypto | Y | 2 | 2 | — | — | — | — | scorehsm 274 tests | Complete |
| score-inc_daal | Y | 1 | — | — | — | — | — | — | Stub |
| score-inc_time | Y | 1 | — | — | — | — | — | — | Stub |
| **TOTAL** | 13 | 26 | 32 | 33 | 35 | 38 | 2 full + 5 tree | 15 upstream | |

## Total Requirement Count (S-CORE Platform)

| Level | Count |
|---|---|
| Platform Safety Goals (PSG) | 4 |
| Safety Goals (SG) | 26 |
| Functional Safety Reqs (FSR) | 32 |
| Technical Safety Reqs (TSR) | 33 |
| Software Safety Reqs (SSR) | 35 |
| Software Requirements (SWR) | 38 |
| **Total** | **168** |
| **Bidirectional Links** | **~320** |
