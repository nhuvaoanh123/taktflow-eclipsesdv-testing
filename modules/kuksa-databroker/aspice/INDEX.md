---
document_id: KUKSA-DB-INDEX
title: "eclipse-kuksa-databroker — ASPICE + Security Document Registry"
version: "1.0"
status: active
date: 2026-03-25
---

# KUKSA.val Databroker — Document Registry

Central vehicle signal data broker for the Eclipse SDV stack. **QM rated.**
All vehicle signals flow through this component — it is the highest-value
target in the SDV architecture.

## Module Profile

| Attribute | Value |
|---|---|
| Module | kuksa-databroker v0.6.1-dev |
| Language | Rust (edition 2021) |
| Build | Cargo |
| ASIL | QM |
| gRPC port | 55555 (default) |
| API | KUKSA.val v1 + v2 (protobuf/gRPC) + VISS2 |
| VSS data | data/vss-core/vss_release_4.0.json |

## Components

| Component | Type | Description |
|---|---|---|
| `databroker` | Binary | gRPC server: VSS get/set/subscribe, authorization, filter, query |
| `databroker-proto` | Library | KUKSA.val v1/v2 protobuf definitions (prost/tonic) |
| `databroker-cli` | Binary | CLI client for interactive signal access |
| `lib/common` | Library | Shared types and utilities |

## Security Properties

| Property | Status |
|---|---|
| JWT authorization (signal-level) | STRUCTURAL (module present, not live-tested) |
| TLS gRPC support | STRUCTURAL (certificates present) |
| Wildcard subscription documented | VERIFIED |
| OpenTelemetry observability | STRUCTURAL |
| Input validation (malformed proto) | NOT TESTED |
| Sanitizers (ASan/UBSan) | NOT RUN |

## Integration in Taktflow SDV Stack

```
TMS570 / STM32 ECU
    └─▶ CAN bus (500 kbps)
        └─▶ kuksa-can-provider (taktflow_vehicle.dbc mapping)
            └─▶ kuksa-databroker (VSS gRPC, port 55555)
                └─▶ velocitas vehicle app (subscribes to Vehicle.Speed etc.)
                └─▶ taktflow dashboard (WebSocket → displayed)
```

## Requirement ID Format

| Level | Pattern | Example |
|---|---|---|
| SWR | `SWR-KUKSA-NNN` | SWR-KUKSA-001 |
| Integration | `INT-KUKSA-NNN` | INT-KUKSA-001 |
| Security | `SEC-KUKSA-NNN` | SEC-KUKSA-001 |

## ASPICE Work Products

| Process | Work Product | Status |
|---|---|---|
| SWE.1 | Requirements | KUKSA GitHub issues |
| SWE.3 | Design | doc/ directory present |
| SWE.4 | Unit test spec | Test files created (pending run) |
| SWE.5 | Integration test spec | integration_test/test_databroker.py (pending run) |
| SWE.6 | System test results | Not yet executed |
| SEC | Security analysis | test_safety_contracts.py (JWT, TLS, wildcard) |
