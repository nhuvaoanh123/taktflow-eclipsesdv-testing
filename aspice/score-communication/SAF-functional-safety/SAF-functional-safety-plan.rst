.. # *******************************************************************************
   # Copyright (c) 2026 Taktflow Systems
   # SPDX-License-Identifier: Apache-2.0
   # *******************************************************************************

SAF — Functional Safety Plan
##############################

Module: score-communication (LoLa)
**********************************

:ASIL Classification: B
:ISO 26262 Reference: Part 6, Part 8, Part 9
:Status: Active

Purpose
=======

This work product defines the functional safety plan for the Communication
Module (LoLa), identifying safety goals, ASIL decomposition, safety analyses,
and safety validation activities required for ASIL-B qualification.

Safety Context
==============

The Communication Module is part of the S-CORE HPC platform deployed on:

- **Raspberry Pi 4 (QNX 8.0)** — Application processor in 3-chip HPC SoC
- Connected to **TMS570 (CVC)** via Ethernet for vehicle signal exchange
- Connected to **STM32L552ZE (HSM)** via USB for security services

Safety-critical use: Vehicle signal data (speed, battery SOC, temperature)
flows through LoLa IPC between processes on the QNX HPC. Incorrect, lost,
or delayed data could lead to wrong actuator commands.

Safety Goals
============

.. list-table::
   :header-rows: 1
   :widths: 15 50 15 20

   * - ID
     - Safety Goal
     - ASIL
     - Fault Tolerance Time
   * - SG-COM-01
     - Data exchanged via LoLa IPC shall not be corrupted
     - B
     - 0 ms (immediate detection)
   * - SG-COM-02
     - Data exchange shall complete within bounded time
     - B
     - 100 ms
   * - SG-COM-03
     - A faulty QM process shall not corrupt ASIL-B data paths
     - B
     - 0 ms (prevention by design)

ASIL Decomposition
==================

Per ISO 26262-9 §5, the module is decomposed as follows:

.. code-block:: text

   ASIL-B (module level)
   ├── ASIL-B: shared_mem_layout (data integrity)
   ├── ASIL-B: message_passing (notification timeliness)
   ├── ASIL-B: skeleton/proxy (data path correctness)
   ├── ASIL-B: partial_restart (fault isolation)
   ├── ASIL-B: runtime (bounded execution)
   ├── QM: service_discovery (availability, not safety)
   ├── QM: methods/RPC (diagnostics, not safety path)
   ├── QM: ipc_tracing (debug only)
   └── QM: configuration (validated at startup)

Freedom from interference between QM and ASIL-B components is ensured by:

1. **Memory isolation**: QM and ASIL-B shared memory regions are in separate OS mappings
2. **Bounded execution**: QM components cannot block ASIL-B message passing paths
3. **Error containment**: QM component failures are detected and do not propagate to ASIL-B paths

Safety Analyses
===============

Dependent Failure Analysis (DFA)
---------------------------------

Per ISO 26262-9 §7, DFA is performed to identify dependent failures:

.. list-table:: DFA Summary
   :header-rows: 1
   :widths: 20 30 25 25

   * - Failure Initiator
     - Affected Components
     - Mitigation
     - Status
   * - Shared resource: OS shared memory
     - shared_mem_layout, skeleton, proxy
     - Separate shm regions per ASIL level; bounds checking on all accesses
     - Analyzed
   * - Communication: message passing notification
     - skeleton → proxy notification
     - Timeout-based detection; alive counter in messages
     - Analyzed
   * - Shared input: configuration file
     - All components
     - Config validated at startup; ASIL-B defaults if config invalid
     - Analyzed
   * - Unintended impact: memory depletion
     - shared_mem_layout
     - Compile-time fixed allocation sizes; no dynamic allocation in ASIL-B path
     - Analyzed
   * - Development: lock-free algorithm correctness
     - shared_mem_layout, message_passing
     - Formal review of atomic operations; stress tests; model checking (future)
     - Analyzed

FMEA
----

Per ISO 26262-9 §8, FMEA is performed on ASIL-B components:

.. list-table:: FMEA Summary (Top-Level)
   :header-rows: 1
   :widths: 15 20 20 20 25

   * - ID
     - Failure Mode
     - Effect
     - Detection
     - Mitigation
   * - FM-001
     - Data corruption in shared memory slot
     - Consumer reads wrong value
     - CRC-32 per slot (SR-COM-003)
     - Re-read on CRC failure; error callback
   * - FM-002
     - Notification message lost
     - Consumer misses data update
     - Sequence counter gap detection
     - Consumer polls on timeout; error logged
   * - FM-003
     - Publisher writes beyond slot boundary
     - Adjacent slot corrupted
     - Compile-time size checks; guard bytes
     - Process terminated by OS
   * - FM-004
     - Service discovery returns stale handle
     - Proxy connects to dead service
     - Heartbeat check after connection
     - Re-discovery triggered
   * - FM-005
     - Partial restart leaves shared memory in inconsistent state
     - New service instance reads garbage
     - Epoch counter in shared memory header
     - Full cleanup on restart; version check
   * - FM-006
     - Thread starvation in runtime (priority inversion)
     - ASIL-B event delivery delayed beyond WCET
     - Deadline monitoring in runtime
     - Priority inheritance protocol (QNX); error escalation

Detailed DFA and FMEA documents:

- ``third_party/traceability/doc/safety_analysis.md`` (existing)
- Upstream S-CORE DFA: ``score-score/docs/safety/fdr_reports_safety_analyses_DFA.rst``

Safety Validation Activities
============================

.. list-table::
   :header-rows: 1
   :widths: 15 35 25 25

   * - ID
     - Activity
     - Method
     - Status
   * - SV-001
     - Verify data integrity under concurrent access
     - Fault injection (SWE.4 FI-001..FI-007)
     - Planned
   * - SV-002
     - Verify bounded latency under nominal load
     - Performance benchmarks (NFR-COM-001)
     - Planned
   * - SV-003
     - Verify freedom from interference (QM → ASIL-B)
     - Stress test: QM publisher flooding while ASIL-B path active
     - Planned
   * - SV-004
     - Verify partial restart isolation
     - Kill/restart service while others communicate
     - Planned
   * - SV-005
     - Verify on QNX target platform
     - Full integration test suite on Pi QNX 8.0
     - Planned
   * - SV-006
     - Code coverage analysis (ASIL-B components)
     - Branch coverage ≥ 80% via bazel coverage
     - Planned
   * - SV-007
     - Static analysis clean
     - clang-tidy zero warnings on ASIL-B code
     - Active (CI gate)

Safety Work Products Checklist
==============================

Per ISO 26262-6 and S-CORE process description:

.. list-table::
   :header-rows: 1
   :widths: 40 20 20 20

   * - Work Product
     - Required
     - Status
     - Location
   * - Module Safety Plan
     - Yes
     - This document
     - aspice/SAF-functional-safety/
   * - Safety Requirements (SR-COM-*)
     - Yes
     - Created
     - aspice/SWE.1-requirements-analysis/
   * - ASIL Decomposition
     - Yes
     - Created
     - This document + SWE.2
   * - DFA Report
     - Yes
     - Created
     - This document
   * - FMEA Report
     - Yes
     - Created
     - This document
   * - Safety Manual
     - Yes
     - Planned
     - aspice/SAF-functional-safety/
   * - Verification Report (safety tests)
     - Yes
     - Planned
     - aspice/SWE.4-unit-verification/
   * - Safety Validation Report
     - Yes
     - Planned
     - aspice/SWE.6-qualification-test/
   * - FDR (Formal Design Review) Records
     - Yes
     - Planned
     - aspice/SAF-functional-safety/
