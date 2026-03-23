---
document_id: SG-COM
title: "Safety Goals — score-communication (LoLa)"
version: "1.0"
status: draft
iso_26262_part: 3
asil: B
date: 2026-03-20
---

# Safety Goals

## Context

The Communication Module (LoLa) runs on the QNX HPC (Raspberry Pi 4) as part of a 3-chip SoC (Pi + TMS570 + L552ZE). Vehicle signal data (speed, battery SOC, temperature, torque commands) flows through LoLa IPC between processes on the HPC. Incorrect, lost, or delayed data could propagate to the TMS570 CVC, which controls actuators (motor, steering, brakes) via CAN bus.

## Hazardous Events

| ID | Hazardous Event | Severity | Exposure | Controllability | ASIL |
|---|---|---|---|---|---|
| HE-COM-001 | Corrupted torque command transmitted to CVC via LoLa | S2 | E4 | C2 | B |
| HE-COM-002 | Stale/delayed battery temperature causes missed thermal runaway alert | S2 | E3 | C2 | B |
| HE-COM-003 | QM process corruption propagates to ASIL-B data path | S2 | E3 | C2 | B |

## Safety Goals

### SG-COM-001: Data Integrity

- **ASIL**: B
- **Hazardous Event**: HE-COM-001
- **Traces up**: SYS-COM-004
- **Traces down**: FSR-COM-001, FSR-COM-002
- **Fault Tolerance Time**: 0 ms (immediate detection required)

Data exchanged via LoLa IPC between ASIL-B classified processes SHALL NOT be corrupted during transmission through shared memory.

### SG-COM-002: Data Timeliness

- **ASIL**: B
- **Hazardous Event**: HE-COM-002
- **Traces up**: SYS-COM-002, SYS-COM-004
- **Traces down**: FSR-COM-003, FSR-COM-004
- **Fault Tolerance Time**: 100 ms

Data published to ASIL-B subscribers SHALL be delivered within a bounded worst-case time. Failure to deliver within the deadline SHALL be detected.

### SG-COM-003: Freedom from Interference

- **ASIL**: B
- **Hazardous Event**: HE-COM-003
- **Traces up**: SYS-COM-004
- **Traces down**: FSR-COM-005, FSR-COM-006
- **Fault Tolerance Time**: 0 ms (prevention by design)

A faulty QM process communicating via LoLa SHALL NOT corrupt, block, or delay ASIL-B classified data paths.
