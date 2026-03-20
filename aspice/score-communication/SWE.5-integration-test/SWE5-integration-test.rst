.. # *******************************************************************************
   # Copyright (c) 2026 Taktflow Systems
   # SPDX-License-Identifier: Apache-2.0
   # *******************************************************************************

SWE.5 — Software Integration and Integration Test
###################################################

Module: score-communication (LoLa)
**********************************

:ASPICE Level: 2
:Safety Classification: ASIL-B
:Status: Active

Purpose
=======

This work product defines the integration test strategy for the Communication
Module, verifying correct interaction between components and with external
modules on the target platform.

Integration Strategy
====================

Integration follows a bottom-up approach:

.. code-block:: text

   Level 1: message_passing + OS backend (mqueue/qnx)
       ↓ verified
   Level 2: shared_mem_layout + message_passing
       ↓ verified
   Level 3: skeleton + proxy + shared_mem_layout + message_passing
       ↓ verified
   Level 4: service_discovery + skeleton + proxy (full mw::com)
       ↓ verified
   Level 5: mw::com + external modules (logging, lifecycle, orchestrator)

Test Environment
================

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Environment
     - Configuration
     - Purpose
   * - CI (Linux)
     - Ubuntu 24.04, Docker, Bazel
     - Automated integration on every PR
   * - QNX Target
     - Raspberry Pi 4, QNX 8.0, Bazel cross-compile
     - Platform validation on real RTOS
   * - HIL Bench
     - Linux laptop + Pi QNX + CAN ECUs
     - Full system integration with real hardware

Integration Test Cases
======================

Level 1: Message Passing ↔ OS
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 35 25 25

   * - ID
     - Test Description
     - Platform
     - Pass Criteria
   * - IT-MP-001
     - Short message round-trip between two processes via mqueue
     - Linux
     - Message received within 1ms, data matches
   * - IT-MP-002
     - Medium message round-trip between two processes via mqueue
     - Linux
     - Message received, payload integrity verified
   * - IT-MP-003
     - N-to-1 fan-in: 10 senders, 1 receiver, 1000 messages each
     - Linux
     - All 10,000 messages received, no loss, no corruption
   * - IT-MP-004
     - Short message round-trip via QNX native messaging
     - QNX
     - Message received within 1ms
   * - IT-MP-005
     - Message passing under memory pressure (90% RAM used)
     - Linux
     - Graceful degradation, no crash, error reported

Level 2: Shared Memory ↔ Message Passing
------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 35 25 25

   * - ID
     - Test Description
     - Platform
     - Pass Criteria
   * - IT-SHM-001
     - Write data to shared memory slot, notify via message passing, reader verifies
     - Linux
     - Data matches, latency < 200µs
   * - IT-SHM-002
     - Concurrent writers (3 processes) to different slots in same shared memory region
     - Linux
     - No corruption, all data verifiable
   * - IT-SHM-003
     - Shared memory region cleanup after publisher crash (SIGKILL)
     - Linux
     - Region reclaimed, subscriber notified of publisher loss
   * - IT-SHM-004
     - Shared memory communication on QNX typed memory
     - QNX
     - Data exchange functional, latency measured

Level 3: Skeleton ↔ Proxy ↔ Shared Memory
-------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 35 25 25

   * - ID
     - Test Description
     - Platform
     - Pass Criteria
   * - IT-SP-001
     - Skeleton publishes 1000 events, proxy receives all via subscription
     - Linux
     - All 1000 events received, data matches, order preserved
   * - IT-SP-002
     - Multiple proxies (5) subscribe to same skeleton
     - Linux
     - All 5 proxies receive all events
   * - IT-SP-003
     - Field get/set round-trip: proxy sets field, skeleton reads new value
     - Linux
     - Value propagated within 1ms
   * - IT-SP-004
     - Method invocation: proxy calls method on skeleton, receives result
     - Linux
     - Result matches expected, timeout < 10ms
   * - IT-SP-005
     - Skeleton publishes events on QNX, proxy receives on same QNX instance
     - QNX
     - All events received, latency measured

Level 4: Full mw::com with Service Discovery
----------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 35 25 25

   * - ID
     - Test Description
     - Platform
     - Pass Criteria
   * - IT-SD-001
     - Skeleton offers service, proxy discovers it, establishes communication
     - Linux
     - Discovery < 500ms, communication established
   * - IT-SD-002
     - Skeleton stops offering, proxy detects service loss
     - Linux
     - Proxy notified, handles gracefully
   * - IT-SD-003
     - Partial restart: kill skeleton process, restart, proxy reconnects
     - Linux
     - Proxy auto-reconnects within 5s, communication resumes
   * - IT-SD-004
     - 20 services offered simultaneously, all discovered by single proxy
     - Linux
     - All 20 services found, no discovery failures
   * - IT-SD-005
     - Full mw::com communication on QNX with native service discovery
     - QNX
     - End-to-end communication functional

Level 5: Cross-Module Integration
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 35 25 25

   * - ID
     - Test Description
     - Platform
     - Pass Criteria
   * - IT-XM-001
     - mw::com + logging: verify communication events are logged
     - Linux
     - Log entries contain service offer/discover/send/receive events
   * - IT-XM-002
     - mw::com + lifecycle: verify service shutdown on lifecycle SHUTDOWN signal
     - Linux
     - All services cleanly stopped, shared memory released
   * - IT-XM-003
     - mw::com + orchestrator: service started by orchestrator, communicates via LoLa
     - Linux
     - Orchestrator manages lifecycle, IPC functional
   * - IT-XM-004
     - mw::com + feo: events published on FEO cycle boundary
     - Linux
     - Events arrive deterministically within FEO cycle
   * - IT-XM-005
     - mw::com integrated on QNX HPC with lifecycle + logging
     - QNX
     - Full stack operational on target

Existing Integration Test Infrastructure
=========================================

Location: ``quality/integration_testing/``

:Framework: Docker-based multi-process tests
:Execution: ``bazel test //quality/integration_testing/...``
:Prerequisites: Docker with rootless mode or user permissions

Testing Guidelines
==================

Documented in: ``score/mw/com/test/testing_guidelines.md``

- Integration tests MUST use real multi-process communication (no mocking of IPC)
- Tests MUST clean up shared memory and flag files after execution
- QNX tests MUST be tagged with ``qnx`` for conditional execution
- ASIL-B integration tests MUST include negative test cases (error paths)
