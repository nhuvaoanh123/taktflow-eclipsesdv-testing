---
document_id: SCORE-SIPGW-INDEX
title: "Eclipse S-CORE SOME/IP Gateway — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-inc_someip_gateway — Document Registry

SOME/IP gateway bridging CAN signals from TMS570 to Pi QNX via Ethernet.

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 27 |
| Contributors | 9 |
| Language | C++ |
| Build | Bazel |
| ASIL | B (vehicle signal path) |
| Target Chip | TMS570 (CVC) — CAN↔Ethernet bridge |
| Status | Incubation |

## Bench Role

This is the **critical bridge** between the CAN bus (zone ECUs) and the QNX HPC (Pi):

```
Zone ECUs ──CAN──► TMS570 ──SOME/IP over Ethernet──► Pi (QNX)
                    ↑                                   ↑
              inc_someip_gateway                  LoLa (mw::com)
```

## Safety Goals

### SG-SIPGW-001: Signal Integrity Across CAN↔Ethernet Bridge

- **ASIL**: B
- **Traces down**: FSR-SIPGW-001
- **Fault Tolerance Time**: 100 ms

Vehicle signals bridged from CAN to SOME/IP SHALL arrive at the QNX consumer with identical values. No data transformation error, byte-order mistake, or signal loss SHALL occur silently.

### SG-SIPGW-002: Bridge Availability

- **ASIL**: B
- **Traces down**: FSR-SIPGW-002
- **Fault Tolerance Time**: 1 second

Loss of Ethernet connectivity between TMS570 and Pi SHALL be detected within 1 second. The gateway SHALL buffer critical signals during transient disconnections and replay them on reconnection.

## Upstream Docs (already in ASPICE folders)

- Architecture: `docs/architecture/` (registration design, car window overview)
- Requirements: `docs/requirements/` (stakeholder, feature, component)
- Conformance: `docs/tc8_conformance/` (SOME/IP conformance tests)
