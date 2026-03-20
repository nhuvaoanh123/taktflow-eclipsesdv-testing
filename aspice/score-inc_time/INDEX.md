---
document_id: SCORE-TIME-INDEX
title: "Eclipse S-CORE Time Sync — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-inc_time — Document Registry

Time synchronization between chips in the 3-chip HPC SoC.

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 13 |
| Contributors | 3 |
| Language | C++ |
| Build | Bazel |
| ASIL | B |
| Target Chips | Pi (QNX) ↔ TMS570 (CVC) |
| Status | Incubation |

## Bench Role

Synchronizes clocks between the 3 chips so that timestamps from Pi, TMS570, and L552ZE are comparable:

```
Pi (QNX) ◄──Ethernet──► TMS570 (CVC) ◄──CAN──► Zone ECUs
   │                        │
   └── PTP / time sync ─────┘
```

## Safety Goals

### SG-TIME-001: Clock Synchronization Accuracy

- **ASIL**: B
- **Fault Tolerance Time**: 1 sync cycle

The time difference between Pi and TMS570 clocks SHALL be less than 1 ms after synchronization. Sync loss SHALL be detected and reported.

## Note

Early incubation — critical for correlating timestamps between chips (e.g., CAN frame timestamp on TMS570 vs. databroker timestamp on Pi). Maps to IEEE 802.1AS / gPTP concepts.
