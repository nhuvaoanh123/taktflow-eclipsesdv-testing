.. # *******************************************************************************
   # Copyright (c) 2026 Taktflow Systems
   # SPDX-License-Identifier: Apache-2.0
   # *******************************************************************************

SWE.6 — Software Qualification Test
#####################################

Module: score-communication (LoLa)
**********************************

:ASPICE Level: 2
:Safety Classification: ASIL-B
:Status: Planned

Purpose
=======

This work product defines the qualification test plan for the Communication
Module, verifying that the integrated software meets all specified requirements
in the target environment.

Qualification Environment
=========================

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Target
     - Hardware
     - Configuration
   * - QNX HPC
     - Raspberry Pi 4 (QNX 8.0)
     - Part of 3-chip SoC: Pi + TMS570 + L552ZE
   * - Linux Laptop
     - Linux Laptop
     - SDV stack host, test runner, USB CAN
   * - HIL Bench
     - Full bench
     - 4 ECUs on CAN bus, Rigol oscilloscope

Qualification Test Cases
========================

QT-COM-001: End-to-End Event Communication on QNX
---------------------------------------------------
:Requirement: FR-COM-001, FR-COM-004, FR-COM-006
:ASIL: B
:Procedure:
   1. Deploy skeleton process on QNX Pi
   2. Deploy proxy process on QNX Pi
   3. Skeleton publishes 10,000 temperature events (30ms interval)
   4. Proxy receives and validates all events
:Pass: All 10,000 events received, data matches, no corruption

QT-COM-002: Service Discovery Lifecycle on QNX
------------------------------------------------
:Requirement: FR-COM-003
:ASIL: QM
:Procedure:
   1. Start skeleton on QNX — offers service
   2. Start proxy on QNX — discovers service via flag file
   3. Communication established
   4. Stop skeleton — proxy detects loss
   5. Restart skeleton — proxy re-discovers and reconnects
:Pass: Full lifecycle completed without manual intervention

QT-COM-003: Multi-Subscriber Broadcasting on QNX
--------------------------------------------------
:Requirement: FR-COM-002, FR-COM-004
:ASIL: B
:Procedure:
   1. Deploy 1 skeleton + 5 proxy processes on QNX
   2. Skeleton publishes 1,000 events
   3. All 5 proxies verify receipt
:Pass: All 5 proxies receive all 1,000 events

QT-COM-004: Latency Qualification on QNX
------------------------------------------
:Requirement: NFR-COM-001, SR-COM-002
:ASIL: B
:Procedure:
   1. Deploy skeleton + proxy on QNX
   2. Publish 10,000 short messages, measure end-to-end latency
   3. Compute p50, p95, p99 latency
:Pass: p99 < 100 µs

QT-COM-005: Fault Tolerance — Partial Restart on QNX
------------------------------------------------------
:Requirement: FR-COM-010, SR-COM-001
:ASIL: B
:Procedure:
   1. Deploy 3 services communicating via LoLa on QNX
   2. SIGKILL service #2
   3. Verify services #1 and #3 continue operating
   4. Restart service #2
   5. Verify service #2 re-establishes communication
:Pass: No crash or data corruption in services #1 and #3

QT-COM-006: Freedom from Interference — QM vs ASIL-B
------------------------------------------------------
:Requirement: SR-COM-001, SG-COM-03
:ASIL: B
:Procedure:
   1. Deploy ASIL-B publisher + subscriber pair on QNX
   2. Deploy QM "rogue" process that floods shared memory operations
   3. Verify ASIL-B data path is not affected
:Pass: ASIL-B latency unchanged, no data corruption

QT-COM-007: Integration with Vehicle Data Flow (HIL)
------------------------------------------------------
:Requirement: FR-COM-001, FR-COM-004
:ASIL: B
:Procedure:
   1. TMS570 CVC sends vehicle signals over Ethernet to QNX Pi
   2. Receiver process on Pi publishes signals via LoLa skeleton
   3. Consumer process on Pi subscribes via LoLa proxy
   4. Consumer validates signal values against known ECU output
:Pass: Signal values match within tolerance, latency < 10ms

QT-COM-008: Long-Duration Stability on QNX
--------------------------------------------
:Requirement: NFR-COM-001, NFR-COM-002
:ASIL: B
:Procedure:
   1. Deploy skeleton + 3 proxies on QNX
   2. Continuous communication at 100 Hz for 24 hours
   3. Monitor memory usage, latency, message loss
:Pass: Zero message loss, memory stable (no leak), latency p99 stable

Qualification Exit Criteria
============================

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Criterion
     - Target
     - Status
   * - All QT-COM-* test cases executed
     - 8/8
     - Planned
   * - All ASIL-B test cases pass
     - 100%
     - Planned
   * - Latency qualification (QT-COM-004)
     - p99 < 100 µs
     - Planned
   * - 24-hour stability (QT-COM-008)
     - Zero loss, stable memory
     - Planned
   * - DFA/FMEA review complete
     - All items analyzed
     - Created
   * - Safety validation report signed
     - Safety engineer approval
     - Planned
