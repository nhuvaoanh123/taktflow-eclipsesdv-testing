---
document_id: SCORE-DAAL-INDEX
title: "Eclipse S-CORE DAAL — ASPICE Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-inc_daal — Document Registry

Data Abstraction and Access Layer — sensor/actuator HAL for the TMS570.

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 11 |
| Contributors | 6 |
| Language | C++ |
| Build | Bazel |
| ASIL | B (sensor data path) |
| Target Chip | TMS570 (CVC) |
| Status | Incubation |

## Bench Role

DAAL sits between the TMS570's sensor/actuator hardware and the SOME/IP gateway:

```
Pedal sensors (SPI) ──► DAAL ──► SOME/IP Gateway ──► Pi (QNX)
Motor current (ADC) ──► DAAL ──►
NTC temps (ADC)     ──► DAAL ──►
```

## Safety Goals

### SG-DAAL-001: Sensor Data Accuracy

- **ASIL**: B
- **Fault Tolerance Time**: 1 sensor read cycle

Sensor values read through DAAL SHALL accurately represent the physical measurement within the sensor's specified tolerance. No data type conversion, scaling, or offset error SHALL occur silently.

## Note

Early incubation — architecture defined but minimal implementation. Maps directly to your taktflow-embedded MCAL layer (Adc, Spi, Pwm in `firmware/bsw/mcal/`). Your existing AUTOSAR BSW is more mature than this upstream module.
