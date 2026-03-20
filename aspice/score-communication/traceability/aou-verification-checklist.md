---
document_id: AOU-CHECK-COM
title: "AoU Verification Checklist — score-communication (LoLa) on Taktflow Bench"
version: "1.0"
status: draft
date: 2026-03-20
---

# Assumptions of Use (AoU) Verification Checklist

When deploying LoLa on our 3-chip HPC SoC (Pi QNX + TMS570 + L552ZE), every
AoU defined by upstream S-CORE MUST be verified. AoU violations can defeat
safety mechanisms and invalidate the ASIL-B qualification.

Source: `score-communication/score/mw/com/requirements/safety_analysis/aou.trlc`

## Checklist

| # | AoU | ASIL | Mitigates | Verification on Our Bench | Status |
|---|---|---|---|---|---|
| 1 | **MonotonicSemiDynamicMemoryAllocation** — Enough shared memory configured for all LoLa allocations | B | TooMuchMemoryAllocated | Verify Pi QNX memory config: `sysctl -a | grep shm`. Confirm LoLa pool size > max usage in perf benchmark. | Planned |
| 2 | **CorrectlyConfiguredMaximumNumberOfSubscriber** — Correct max subscriber count per event per service instance | B | InMemoryConfigurationWrong, TooFewMemoryAllocated, SendingEventSendsToWrongConsumer | Review deployment JSON config on Pi. Count actual subscribers per service in bench test E2E-BENCH-03. | Planned |
| 3 | **CorrectlyConfiguredMaximumNumberOfMaximumElementsPerSubscriber** — Correct max elements per subscriber | B | InMemoryConfigurationWrong, TooFewMemoryAllocated | Review deployment JSON config. Stress test with max element count. | Planned |
| 4 | **CorrectlyConfiguredAsilLevel** — Correct ASIL level per process and per service instance | B | InMemoryConfigurationWrong | Verify deployment config: ASIL-B services have `asil: B` flag. QM processes run under different OS user than ASIL-B processes (see AoU #8). | Planned |
| 5 | **OnlyLoLaSupportedTypes** — Only LoLa-compatible types transmitted (DefaultConstructible, CopyAssignable, not polymorphic, no dynamic memory) | B | MemoryAllocatedInWrongSection | Compile-time check: `static_assert` in application code. Review all service interfaces. | Planned |
| 6 | **NoApisFromImplementationNamespace** — No direct use of `impl` namespace APIs | B | MisusedApis | Code review of our application SWCs. grep for `::impl::` in application code. | Planned |
| 7 | **NoGuaranteesForNotifications** — Safety goals must not depend on notification delivery guarantees | B | SendingEventOnlyPartiallyNotifiesConsumer | Review our safety goals: SG-COM-002 uses deadline monitoring (FSR-COM-003) as mitigation, not notification guarantees. **Verified by design.** | Verified |
| 8 | **DifferentUserForAsilAndQmProcesses** — ASIL-B and QM processes run under different OS users | B | (Freedom from Interference) | QNX: create `asil_user` and `qm_user`. Configure process manifest accordingly. Verify with `pidin -f a` on QNX. | Planned |
| 9 | **CorrectlyConfiguredElementSize** — Element size in config matches actual data type size | B | TooFewMemoryAllocated, InMemoryConfigurationWrong | Review deployment config: `element_size` field matches `sizeof(T)` for each event type. | Planned |
| 10 | **NoSafetyGoalHarmedIfServiceNotOffered** — Safety goals survive service discovery failure | B | CreationOfSkeletonNotPossible, ServiceNotOffered | Review our safety concept: SG-COM-002 deadline monitoring detects missing service. No safety goal depends solely on service availability. | Planned |
| 11 | **ApplicationNotifiesAboutSkippedSamples** — Application handles `GetNewSamples()` returning fewer samples than expected | B | Consumer misses intermediate values | Application code review: check all `GetNewSamples()` return values. | Planned |
| 12 | **SignalSafetyAssumptions** — Signal mechanism does not transport data, only triggers | QM | — | Verify our services don't use Signals for safety-critical data exchange. | N/A (QM) |

## Verification Evidence

For each AoU marked "Verified", evidence must be stored in:
`aspice/score-communication/SAF-functional-safety/aou-evidence/`

Evidence types:
- **Config review**: Screenshot/dump of deployment JSON config
- **Code review**: grep results showing no violations
- **Test result**: Bench test log showing correct behavior
- **Design review**: Reference to safety concept document

## Integration with Bench Test Plan

AoU verification SHALL be performed during **Phase 3a** (Week 5) of the bench test plan when LoLa is deployed on the Linux laptop with USB CAN connection to ECUs.

AoU #8 (different OS users) SHALL be verified during **QNX target qualification** (SWE.6 QT-COM-006).
