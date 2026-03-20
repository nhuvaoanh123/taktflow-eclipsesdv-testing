---
document_id: INTEG-SIPGW
title: "Upstream Integration Map — score-inc_someip_gateway"
version: "1.0"
status: active
date: 2026-03-20
---

# Upstream S-CORE ↔ Taktflow ASPICE Integration Map — SOME/IP Gateway

## Upstream Status

| Aspect | Status |
|---|---|
| Stakeholder Requirements | **Defined** — `docs/requirements/stakeholder.rst` |
| Feature Requirements | **Defined** — `docs/requirements/feature/index.rst` |
| Component Requirements | **Defined** — `docs/requirements/component/index.rst` |
| Architecture | **Defined** — `docs/architecture/` with registration design + car window overview |
| TC8 Conformance | **Defined** — `docs/tc8_conformance/` SOME/IP conformance tests |

## Upstream Requirement Hierarchy

```
stkh_req__some_ip_gateway__*  (Stakeholder)
  └── feat_req__some_ip_gateway__*  (Feature)
       └── comp_req__gatewayd__*  (Component — ASIL-B daemon)
           comp_req__someipd__*  (Component — QM SOME/IP stack)
           comp_req__network_service__*  (Component — ASIL-B IPC)
```

## Component Classification

| Component | ASIL | Role on Bench |
|---|---|---|
| `gatewayd` | B | Main gateway daemon on TMS570 — routes CAN↔SOME/IP |
| `someipd` | QM | SOME/IP protocol stack wrapper |
| `network_service` | B | IPC service for Ethernet communication |

## Taktflow Safety Goal Mapping

| Taktflow SG | Upstream Architecture | Bench Role |
|---|---|---|
| SG-SIPGW-001 (Signal Integrity) | `docs/architecture/dec_someipgw_registration.rst` | TMS570 bridges pedal/motor/temp CAN signals to Pi QNX |
| SG-SIPGW-002 (Bridge Availability) | `docs/architecture/score-someip-car-window-overview.drawio` | Ethernet link monitoring TMS570↔Pi |

## Bench Integration

```
Zone ECUs (G474RE, F413ZH)
    │ CAN
    ▼
TMS570 (CVC) — runs gatewayd (ASIL-B) + someipd (QM)
    │ Ethernet (SOME/IP)
    ▼
Pi (QNX) — receives vehicle signals via LoLa (score-communication)
    │ Network
    ▼
Laptop (Linux) — Eclipse SDV stack for testing
```

## TC8 Conformance Tests

Source: `docs/tc8_conformance/requirements.rst`

TC8 is the AUTOSAR conformance test suite for SOME/IP. The upstream gateway module includes conformance test requirements that can be validated on our bench.

## Gaps

1. **Implementation**: Incubation stage (27 commits). Architecture and requirements defined but code is early.
2. **FMEA/DFA**: Not yet created upstream. Our SG-SIPGW-001/002 provide initial safety analysis.
3. **TMS570 Port**: No existing port to TMS570. Would need bare-metal C++ implementation of gatewayd.
