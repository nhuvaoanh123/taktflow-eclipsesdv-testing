.. # *******************************************************************************
   # Copyright (c) 2026 Taktflow Systems
   # SPDX-License-Identifier: Apache-2.0
   # *******************************************************************************

SWE.1 — Software Requirements Analysis
#######################################

Module: score-communication (LoLa)
**********************************

:ASPICE Level: 2
:Safety Classification: ASIL-B (QM + ASIL-B mixed)
:Status: Active (1295 commits, 65 contributors)

Purpose
=======

This work product captures the software requirements for the Eclipse S-CORE
Communication Module (LoLa — Low Latency), a zero-copy shared-memory based
IPC middleware implementing the Adaptive AUTOSAR ara::com specification.

Requirement Sources
===================

.. list-table:: Requirement Source Traceability
   :header-rows: 1
   :widths: 20 30 50

   * - Source ID
     - Source
     - Description
   * - AUTOSAR-ACOM
     - Adaptive AUTOSAR ara::com R22-11
     - Communication Management specification
   * - ISO26262-6
     - ISO 26262 Part 6
     - Product development at the software level
   * - ISO26262-8
     - ISO 26262 Part 8
     - Supporting processes
   * - SCORE-PLAT
     - S-CORE Platform Requirements
     - Platform-level feature requirements
   * - SCORE-SAF
     - S-CORE Safety Plan
     - Safety requirements from platform safety plan

Functional Requirements
=======================

FR-COM-001: Zero-Copy Shared Memory IPC
----------------------------------------
The communication module SHALL provide zero-copy data exchange between
processes using shared memory as the underlying transport mechanism.

:Priority: High
:ASIL: B
:Rationale: Minimizes latency and CPU overhead for safety-critical real-time data exchange.
:Verification: SWE.4 unit tests + SWE.5 integration tests
:Source: AUTOSAR-ACOM, SCORE-PLAT

FR-COM-002: Publisher/Subscriber Pattern
----------------------------------------
The module SHALL implement the publisher/subscriber communication pattern
with skeleton (server) and proxy (client) abstractions.

:Priority: High
:ASIL: QM
:Rationale: AUTOSAR ara::com mandates skeleton/proxy pattern for service-oriented communication.
:Verification: SWE.4 unit tests
:Source: AUTOSAR-ACOM

FR-COM-003: Service Discovery
-----------------------------
The module SHALL provide automatic service registration and discovery using
a flag-file based mechanism on the local filesystem.

:Priority: High
:ASIL: QM
:Rationale: Services must be discoverable without manual configuration.
:Verification: SWE.5 integration tests
:Source: AUTOSAR-ACOM

FR-COM-004: Event/Field Communication
--------------------------------------
The module SHALL support event-driven communication (fire-and-forget) and
field communication (get/set with notification) patterns.

:Priority: High
:ASIL: B
:Rationale: Core ara::com patterns for vehicle signal exchange.
:Verification: SWE.4 unit tests
:Source: AUTOSAR-ACOM

FR-COM-005: Method Invocation (RPC)
-----------------------------------
The module SHALL support synchronous and asynchronous remote procedure call
(method) invocation between proxy and skeleton.

:Priority: Medium
:ASIL: QM
:Rationale: Required for request-response patterns (e.g., diagnostic services).
:Verification: SWE.4 unit tests
:Source: AUTOSAR-ACOM

FR-COM-006: Multi-Platform Support
-----------------------------------
The module SHALL support Linux (POSIX) and QNX operating systems with
platform-specific message passing implementations.

:Priority: High
:ASIL: B
:Rationale: Target platforms include QNX 8.0 (Pi HPC) and Linux (development/SIL).
:Verification: SWE.5 integration tests on both platforms
:Source: SCORE-PLAT

FR-COM-007: Thread Safety
--------------------------
All public API operations SHALL be thread-safe using atomic data structures
and lock-free algorithms where applicable.

:Priority: High
:ASIL: B
:Rationale: Safety-critical systems require deterministic concurrent access.
:Verification: SWE.4 concurrency tests
:Source: SCORE-SAF, ISO26262-6

FR-COM-008: Message Passing Foundation
--------------------------------------
The module SHALL provide a low-level message passing layer supporting:

- Short messages (~8 bytes payload)
- Medium messages (~16 bytes payload)
- N-to-1 unidirectional channel topology

:Priority: High
:ASIL: B
:Rationale: Foundation for skeleton/proxy communication and service discovery notifications.
:Verification: SWE.4 unit tests
:Source: AUTOSAR-ACOM

FR-COM-009: IPC Tracing
------------------------
The module SHALL provide zero-copy, binding-agnostic communication tracing
for debugging and performance analysis.

:Priority: Medium
:ASIL: QM
:Rationale: Required for development and field diagnostics.
:Verification: SWE.6 qualification tests
:Source: SCORE-PLAT

FR-COM-010: Partial Restart
----------------------------
The module SHALL support partial restart of communication services without
affecting other running services.

:Priority: Medium
:ASIL: B
:Rationale: Fault isolation — a failing service should not bring down the entire communication stack.
:Verification: SWE.5 integration tests
:Source: SCORE-SAF, ISO26262-6

Non-Functional Requirements
============================

NFR-COM-001: Latency
---------------------
Intra-ECU message delivery latency SHALL be less than 100 microseconds for
short messages under nominal load.

:Priority: High
:ASIL: B
:Verification: Performance benchmarks (score/mw/com/performance_benchmarks/)
:Source: SCORE-PLAT

NFR-COM-002: Memory Usage
--------------------------
The shared memory footprint for a single service instance SHALL not exceed
configurable limits defined at compile time.

:Priority: High
:ASIL: B
:Verification: Resource monitoring tests
:Source: SCORE-PLAT

NFR-COM-003: Build System
--------------------------
The module SHALL build with Bazel 6.0+ and support cross-compilation for
aarch64-linux and aarch64-qnx targets.

:Priority: High
:ASIL: QM
:Verification: CI build matrix
:Source: SCORE-PLAT

Safety Requirements
===================

SR-COM-001: Freedom from Interference
--------------------------------------
The shared memory layout SHALL ensure that a QM publisher cannot corrupt
ASIL-B subscriber data through buffer overflow or pointer arithmetic errors.

:Priority: Critical
:ASIL: B
:Rationale: ISO 26262-6 §7.4.4 — Freedom from interference between elements of different ASIL.
:Verification: SAF FMEA + SWE.4 fault injection tests
:Source: ISO26262-6, SCORE-SAF

SR-COM-002: Deterministic Execution
------------------------------------
The communication path for ASIL-B classified events SHALL have bounded
worst-case execution time (WCET) independent of QM traffic.

:Priority: Critical
:ASIL: B
:Verification: Performance benchmarks + timing analysis
:Source: ISO26262-6, SCORE-SAF

SR-COM-003: Error Detection
-----------------------------
The module SHALL detect and report communication errors including:

- Shared memory corruption (CRC or signature check)
- Service timeout (deadline monitoring)
- Message sequence errors (alive counter)

:Priority: High
:ASIL: B
:Verification: SWE.4 fault injection tests + SAF FMEA
:Source: ISO26262-6, SCORE-SAF

Assumed System Requirements
============================

Documented in: ``score/mw/com/requirements/assumed_system_requirements/README.md``

- Operating system provides POSIX shared memory (``shm_open``, ``mmap``)
- Filesystem available for service discovery flag files
- Process isolation enforced by OS kernel
- Clock source with microsecond resolution available

Requirements Traceability
==========================

.. list-table:: Traceability Matrix
   :header-rows: 1
   :widths: 15 15 15 15 15 15 10

   * - Req ID
     - Architecture (SWE.2)
     - Design (SWE.3)
     - Unit Test (SWE.4)
     - Integration (SWE.5)
     - Safety (SAF)
     - Status
   * - FR-COM-001
     - shared_mem_layout
     - zero-copy impl
     - shared_mem tests
     - ipc_e2e tests
     - DFA
     - Implemented
   * - FR-COM-002
     - skeleton_proxy
     - generic_proxy/skeleton
     - proxy_event tests
     - service_comm tests
     - —
     - Implemented
   * - FR-COM-003
     - service_discovery
     - find_service_handler
     - discovery tests
     - multi-process tests
     - —
     - Implemented
   * - FR-COM-004
     - events_fields
     - generic_proxy_event
     - event/field tests
     - pub-sub tests
     - FMEA
     - Implemented
   * - FR-COM-005
     - methods
     - generic_proxy
     - method tests
     - rpc tests
     - —
     - Implemented
   * - FR-COM-006
     - message_passing
     - mqueue + qnx impl
     - platform tests
     - cross-platform CI
     - —
     - Implemented
   * - FR-COM-007
     - concurrency design
     - atomic data structs
     - thread-safety tests
     - stress tests
     - DFA
     - Implemented
   * - FR-COM-008
     - message_passing
     - client-server design
     - msg passing tests
     - —
     - —
     - Implemented
   * - FR-COM-009
     - ipc_tracing
     - trace impl
     - trace tests
     - —
     - —
     - Implemented
   * - FR-COM-010
     - partial_restart
     - restart impl
     - restart tests
     - restart integration
     - FMEA
     - Implemented
   * - SR-COM-001
     - shared_mem_layout
     - bounds checking
     - fault injection
     - —
     - DFA + FMEA
     - Implemented
   * - SR-COM-002
     - runtime
     - WCET bounded paths
     - perf benchmarks
     - —
     - DFA
     - In Progress
   * - SR-COM-003
     - error handling
     - error detection
     - error tests
     - —
     - FMEA
     - Implemented
