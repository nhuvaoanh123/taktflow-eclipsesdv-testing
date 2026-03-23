---
document_id: INTEG-COM
title: "Upstream Integration Map — score-communication (LoLa)"
version: "1.0"
status: active
date: 2026-03-20
---

# Upstream S-CORE ↔ Taktflow ASPICE Integration Map

This document maps between the upstream S-CORE TRLC requirement IDs and our
Taktflow ASPICE requirement IDs, establishing bidirectional traceability between
the two systems.

## Tooling Difference

| Aspect | S-CORE Upstream | Taktflow ASPICE |
|---|---|---|
| Requirement tool | **TRLC** (`.trlc` files) | **Markdown** (`.md` files) |
| Traceability tool | **Lobster** | **trace-gen.py** |
| ID format | `PackageName.TypeName` (e.g., `Communication.EventType@1`) | `LEVEL-MOD-NNN` (e.g., `FSR-COM-001`) |
| Safety analysis | `FailureMode` + `AoU` in TRLC | FMEA + DFA in markdown |
| Build system | Bazel | Independent |
| Hierarchy | AssumedSystemReq → FeatReq → CompReq | STK → SYS → SG → FSR → TSR → SSR → SWR |

## Requirement Level Mapping

| Taktflow Level | S-CORE Level | S-CORE Type |
|---|---|---|
| STK-COM-* | (not in TRLC — stakeholder context) | — |
| SYS-COM-* | `AssumedSystemReq` | `ScoreReq.AssumedSystemReq` |
| SG-COM-* | (derived from safety analysis) | `ScoreReq.FailureMode` effects |
| FSR-COM-* | `FeatReq` (safety-tagged) | `ScoreReq.FeatReq` |
| TSR-COM-* | (decomposed from FeatReq) | — |
| SSR-COM-* | `CompReq` (safety-tagged) | `ScoreReq.CompReq` |
| SWR-COM-* | `CompReq` (implementation) | `ScoreReq.CompReq` |
| (safety) | `FailureMode` + `AoU` | `ScoreReq.FailureMode`, `ScoreReq.AoU` |

---

## AssumedSystemReq ↔ SYS-COM Mapping

| S-CORE AssumedSystemReq | ASIL | Taktflow SYS-COM | Mapping Notes |
|---|---|---|---|
| `InterProcessCommunication@1` | B | **SYS-COM-001** (Shared Memory IPC) | Direct match — core IPC requirement |
| `IntraProcessCommunication@1` | B | — | Not in our scope (single-process) |
| `SafeCommunication@1` | B | **SYS-COM-004** (ASIL-B Data Integrity) | Safety aspect of communication |
| `SupportForTimeBasedArchitectures@1` | B | **SYS-COM-009** (FEO Integration) | Deterministic timing |
| `SupportForDataDrivenArchitecture@1` | QM | — | Event-driven, covered implicitly |
| `SupportForRequestDrivenArchitecture@1` | QM | — | RPC, covered implicitly |
| `ErrorHandling@1` | B | — | Covered by baselibs (Score::Result) |
| `StableApplicationInterfaces@1` | B | **SYS-COM-003** (ara::com Compliance) | API stability |
| `ExtensibleExternalCommunication@1` | B | — | SOME/IP (future, not LoLa scope) |
| `SecureCommunication@1` | QM | — | Security, separate scope |
| `TracingOfCommunication@1` | B | **SYS-COM-008** (Communication Tracing) | Direct match |
| `ProgrammingLanguagesForApplicationDevelopment@1` | QM | — | Platform-level, not LoLa-specific |

---

## FeatReq ↔ FSR-COM / SG-COM Mapping

### Safety-Critical Feature Requirements (ASIL-B)

| S-CORE FeatReq | ASIL | Taktflow ID | Mapping |
|---|---|---|---|
| `Communication.SupportForTimeBasedArchitecture@1` | B | SYS-COM-009 | FEO integration |
| `Communication.CommunicationInterfaces@1` | B | FSR-COM-001 → SWR-COM-SK/PX | Skeleton/Proxy framework |
| `Communication.EventType@1` | B | FSR-COM-001 → SWR-COM-EF-001 | Event publication |
| `Communication.Method@1` | B | SWR-COM-MT-001 | RPC invocation |
| `Communication.ProducerConsumerPattern@1` | B | FSR-COM-001 | Zero-copy pub/sub |
| `Communication.ServiceInstance@1` | B | SWR-COM-SD-001 | Service instances |
| `Communication.ServiceInstanceNames@1` | B | SWR-COM-SD-002 | POSIX path naming |
| `Communication.Versioning@1` | B | SWR-COM-SD-003 | Version discovery |
| `Communication.ServiceLocationTransparency@1` | B | SYS-COM-003 | Binding-agnostic API |
| `Communication.StatelessCommunication@1` | B | — | Implicit in zero-copy |
| `Communication.ServiceInstanceGranularity@1` | B | SYS-COM-010 | Multi-instance |
| `Communication.ServiceDiscovery@1` | B | FSR-COM-003 via SWR-COM-SD | Flag-file discovery |
| `Communication.SafeCommunication@1` | B | **SG-COM-003** (FFI) | Freedom from interference |
| `Communication.DataCorruption@1` | B | **SG-COM-001** → FSR-COM-001 | Data integrity |
| `Communication.DataReordering@1` | B | **SG-COM-001** → FSR-COM-002 | Sequence monitoring |
| `Communication.DataRepetition@1` | B | **SG-COM-001** → FSR-COM-002 | Alive counter |
| `Communication.DataLoss@1` | B | **SG-COM-002** → FSR-COM-003 | Deadline monitoring |
| `Communication.MultiBindingDeploymentConfiguration@1` | B | SWR-COM-CF-001 | Config file |
| `Communication.DeploymentConfigurationAtRuntime@1` | B | SWR-COM-CF-002 | Runtime config load |
| `Communication.SupportForTracing@1` | B | SWR-COM-TR-001 | Zero-copy tracing |
| `Communication.CommunicationASILLevel@1` | B | **SG-COM-003** | ASIL-B support |
| `Communication.ErrorHandling@1` | B | — | Score::Result (baselibs) |

### QM Feature Requirements

| S-CORE FeatReq | Taktflow ID | Notes |
|---|---|---|
| `Communication.SupportForDataDrivenArchitecture@1` | — | Implicit |
| `Communication.SupportForRequestDrivenArchitecture@1` | — | Implicit |
| `Communication.Signal@1` | — | Not yet in our scope |
| `Communication.ZeroCopy@1` | SYS-COM-001 | QM classification upstream |
| `Communication.SupportForMultipleProgrammingLanguages@1` | — | Platform-level |
| `Communication.SupportForProgrammingLanguageIdioms@1` | — | Platform-level |
| `Communication.UseProgrammingLanguageInfrastructure@1` | — | Platform-level |
| `Communication.FullyMockablePublicAPI@1` | — | Test infrastructure |
| `Communication.FakeBinding@1` | — | Test infrastructure |
| `Communication.MultiBindingSupport@1` | — | Architecture decision |
| `Communication.BindingAgnosticPublicAPI@1` | SYS-COM-003 | ara::com |
| `Communication.AccessControlList*@1` | — | Security scope |

---

## FailureMode ↔ FMEA Mapping

| S-CORE FailureMode | GuideWord | ASIL | Taktflow FMEA ID | Interface |
|---|---|---|---|---|
| `InMemoryConfigurationWrong` | LossOfFunction | B | FM-001 (≈) | `mw.com.Runtime.Initialize` |
| `CreationOfSkeletonNotPossible` | LossOfFunction | B | — (mitigated by AoU) | `mw.com.Skeleton.Create` |
| `ServiceOfferedWithoutInitialFieldValue` | LossOfFunction | B | — | `mw.com.Skeleton.OfferService` |
| `ServiceNotOffered` | LossOfFunction | B | FM-004 (≈) | `mw.com.Skeleton.OfferService` |
| `ServiceOfferedOnWrongBinding` | UnintendedFunction | B | — (config error) | `mw.com.Skeleton.OfferService` |
| `ServiceOfferedUnderWrongIds` | UnintendedFunction | B | — (config error) | `mw.com.Skeleton.OfferService` |

*Note: S-CORE has 30+ FailureModes in the upstream TRLC. Our FMEA (FM-001..FM-006) covers the top-level safety-critical paths. Full mapping requires reading the complete `failure_modes.trlc`.*

---

## AoU ↔ Safety Mechanism Mapping

| S-CORE AoU | ASIL | Mitigates | Taktflow SM/FSR |
|---|---|---|---|
| `MonotonicSemiDynamicMemoryAllocation` | B | TooMuchMemoryAllocated | FSR-BL-002 (No dynamic alloc) |
| `CorrectlyConfiguredMaximumNumberOfSubscriber` | B | InMemoryConfigurationWrong + others | SWR-COM-CF-001 |
| `CorrectlyConfiguredMaximumNumberOfMaximumElementsPerSubscriber` | B | InMemoryConfigurationWrong + others | SWR-COM-CF-001 |
| `CorrectlyConfiguredAsilLevel` | B | InMemoryConfigurationWrong | SWR-COM-SHM-004 (ASIL separation) |
| `OnlyLoLaSupportedTypes` | B | MemoryAllocatedInWrongSection | — (compile-time check) |
| `NoApisFromImplementationNamespace` | B | MisusedApis | — (API design) |
| `NoGuaranteesForNotifications` | B | SendingEventOnlyPartiallyNotifiesConsumer | FSR-COM-003 (deadline monitoring) |
| `DifferentUserForAsilAndQmProcesses` | B | — | TSR-COM-007 (ASIL memory separation) |

---

## Source File Locations

### Upstream TRLC Requirement Files

```
score-communication/
├── score/mw/com/requirements/
│   ├── assumed_system_requirements/
│   │   └── assumed_system_requirements.trlc    ← 12 AssumedSystemReqs
│   ├── feature_requirements/
│   │   └── feature_requirements_ipc.trlc       ← 33 FeatReqs
│   ├── component_requirements/
│   │   ├── component_requirements_ipc.trlc     ← 200+ CompReqs
│   │   └── component_requirements_ipc_methods.trlc
│   └── safety_analysis/
│       ├── failure_modes.trlc                   ← 30+ FailureModes
│       └── aou.trlc                             ← 18+ AoUs
└── third_party/traceability/
    └── config/trlc/score_model/
        └── score_requirements_model.rsl         ← Metamodel definition
```

### Taktflow ASPICE Requirement Files

```
aspice/score-communication/
├── SWE.1-requirements-analysis/
│   ├── stakeholder-requirements.md              ← 10 STK-COM
│   ├── system-requirements.md                   ← 10 SYS-COM
│   └── sw-requirements/
│       ├── SWR-COM-SHM.md                       ← 5 SWR (shared memory)
│       ├── SWR-COM-MP.md                        ← 4 SWR (message passing)
│       ├── SWR-COM-RT.md                        ← 2 SWR (runtime)
│       └── SWR-COM-PR.md                        ← 3 SWR (partial restart)
├── SAF-functional-safety/
│   ├── safety-goals.md                          ← 3 SG-COM
│   ├── functional-safety-reqs.md                ← 6 FSR-COM
│   ├── technical-safety-reqs.md                 ← 10 TSR-COM
│   └── sw-safety-reqs.md                        ← 12 SSR-COM
└── traceability/
    ├── traceability-matrix.md                   ← Bidirectional matrix
    └── upstream-integration-map.md              ← THIS FILE
```

## Integration Notes

1. **S-CORE CompReqs (200+) are more granular than our SWR (14)**. Our SWR captures the safety-critical subset. Full mapping would require reading the complete `component_requirements_ipc.trlc`.

2. **S-CORE FailureModes use FMEA guidewords** (TooEarly, TooLate, Wrong, LossOfFunction, etc.) which map to our FMEA FM-001..FM-006 but at a finer granularity.

3. **S-CORE AoUs (Assumptions of Use)** are constraints on integrators — they map to our FSR/TSR safety mechanisms. When we deploy LoLa on our QNX Pi bench, we must verify all AoU conditions are met.

4. **Lobster traceability** is the authoritative upstream tool. Our trace-gen.py can validate our Taktflow IDs independently. The integration map (this file) bridges the two systems.

5. **Version field**: All S-CORE TRLC requirements have `version = 1`. When upstream increments, we must review and update our mapped requirements.
