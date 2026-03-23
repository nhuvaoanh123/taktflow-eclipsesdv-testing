.. # *******************************************************************************
   # Copyright (c) 2026 Taktflow Systems
   # SPDX-License-Identifier: Apache-2.0
   # *******************************************************************************

SWE.2 — Software Architectural Design
######################################

Module: score-communication (LoLa)
**********************************

:ASPICE Level: 2
:Safety Classification: ASIL-B
:Status: Active

Purpose
=======

This work product describes the architectural design of the S-CORE Communication
Module (LoLa), decomposing it into components and defining their interfaces and
interactions.

Architectural Overview
======================

The communication module is structured in two layers:

.. code-block:: text

   ┌─────────────────────────────────────────────────────────┐
   │  Application Layer                                      │
   │  (Adaptive AUTOSAR ara::com user API)                   │
   ├─────────────────────────────────────────────────────────┤
   │  High-Level Middleware: mw::com                         │
   │  ┌──────────┐ ┌──────────┐ ┌────────────┐ ┌─────────┐ │
   │  │ Service   │ │ Events/  │ │ Methods    │ │ Partial │ │
   │  │ Discovery │ │ Fields   │ │ (RPC)      │ │ Restart │ │
   │  ├──────────┤ ├──────────┤ ├────────────┤ ├─────────┤ │
   │  │ Skeleton  │ │ Proxy    │ │ Config     │ │ Tracing │ │
   │  │ (Server)  │ │ (Client) │ │ Management │ │         │ │
   │  └─────┬────┘ └─────┬────┘ └─────┬──────┘ └────┬────┘ │
   ├────────┼────────────┼────────────┼──────────────┼──────┤
   │  Low-Level: Message Passing                             │
   │  ┌────────────────────────────────────────────────────┐ │
   │  │  Shared Memory Manager                             │ │
   │  │  ┌───────────────┐  ┌───────────────┐             │ │
   │  │  │ POSIX (Linux)  │  │ QNX Native    │             │ │
   │  │  │ mqueue/shm_open│  │ msg_send/recv │             │ │
   │  │  └───────────────┘  └───────────────┘             │ │
   │  └────────────────────────────────────────────────────┘ │
   ├─────────────────────────────────────────────────────────┤
   │  OS Abstraction (score/os from baselibs)                │
   └─────────────────────────────────────────────────────────┘

Component Decomposition
=======================

.. list-table:: Component Registry
   :header-rows: 1
   :widths: 20 15 15 50

   * - Component
     - ASIL
     - Language
     - Responsibility
   * - **service_discovery**
     - QM
     - C++17
     - Flag-file based service registration and lookup. Handles FindService, OfferService, StopOfferService.
   * - **skeleton**
     - B
     - C++17
     - Server-side abstraction. Manages shared memory allocation, event publication, field updates.
   * - **proxy**
     - B
     - C++17
     - Client-side abstraction. Subscribes to events, reads fields, invokes methods.
   * - **generic_proxy_event**
     - B
     - C++17
     - Type-erased event subscription with sample management and notification callbacks.
   * - **events_fields**
     - B
     - C++17
     - Event publication and field get/set with notification propagation.
   * - **methods**
     - QM
     - C++17
     - Synchronous and asynchronous RPC invocation via message passing.
   * - **shared_mem_layout**
     - B
     - C++17
     - Memory layout manager for zero-copy data slots in shared memory regions.
   * - **message_passing**
     - B
     - C++17
     - Low-level N-to-1 unidirectional message channels. Platform-specific backends.
   * - **message_passing/mqueue**
     - B
     - C++17
     - POSIX message queue implementation for Linux.
   * - **message_passing/qnx**
     - B
     - C++17
     - QNX native message passing implementation (msg_send/msg_receive).
   * - **configuration**
     - QM
     - C++17
     - Runtime configuration loading and validation.
   * - **ipc_tracing**
     - QM
     - C++17
     - Zero-copy communication tracing infrastructure.
   * - **partial_restart**
     - B
     - C++17
     - Fault-tolerant service restart without global impact.
   * - **runtime**
     - B
     - C++17
     - Execution context management, thread pools, scheduling.
   * - **non_allocating_future**
     - B
     - C++17
     - Stack-allocated future for deterministic async operations.

Interface Definitions
=====================

External Interfaces
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Interface
     - Direction
     - Protocol
     - Connected To
   * - ara::com User API
     - Provided
     - C++ header API
     - Application SWCs
   * - Shared Memory
     - Both
     - POSIX shm / QNX typed memory
     - OS kernel
   * - Message Queue
     - Both
     - POSIX mqueue / QNX msg
     - OS kernel
   * - Filesystem (flag files)
     - Both
     - File I/O
     - Service Discovery
   * - score::os
     - Required
     - C++ API
     - baselibs OS abstraction
   * - score::mw::log
     - Required
     - C++ API
     - Logging module

Internal Interfaces
-------------------

.. code-block:: text

   skeleton ──── publishes via ──── shared_mem_layout ──── backed by ──── OS shm
       │                                                                    │
       └── notifies via ── message_passing ── mqueue (Linux) / qnx (QNX) ──┘
                                │
   proxy ───── subscribes via ──┘
       │
       └── discovers via ── service_discovery ── flag files

Data Flow
=========

Publisher (Skeleton) Path
-------------------------

1. Application calls ``skeleton.events.Offer()``
2. Service discovery creates flag file announcing service
3. Application writes data via ``skeleton.events.Send(sample)``
4. Data written directly to shared memory slot (zero-copy)
5. Notification sent via message passing to all subscribers
6. Subscribers notified via callback

Subscriber (Proxy) Path
-------------------------

1. Application calls ``proxy.FindService(service_id)``
2. Service discovery scans flag files, returns handle
3. Application calls ``proxy.events.Subscribe()``
4. Message passing channel established to skeleton
5. On notification, proxy reads directly from shared memory (zero-copy)
6. Application callback invoked with data reference

ASIL Decomposition
==================

.. list-table:: ASIL Classification per Component
   :header-rows: 1
   :widths: 30 15 55

   * - Component
     - ASIL
     - Justification
   * - shared_mem_layout
     - B
     - Memory corruption directly impacts safety-critical data exchange
   * - message_passing
     - B
     - Notification loss could cause stale data in safety-critical consumers
   * - skeleton / proxy
     - B
     - Core data path for ASIL-B classified signals
   * - generic_proxy_event
     - B
     - Sample management errors could deliver wrong data to safety consumers
   * - service_discovery
     - QM
     - Service availability is not safety-critical (detected by timeout)
   * - methods (RPC)
     - QM
     - Used for diagnostics and configuration, not safety-critical path
   * - ipc_tracing
     - QM
     - Debug/analysis only, not in safety-critical data path
   * - configuration
     - QM
     - Read at startup, validated before use

Design Decisions
================

DD-COM-001: Zero-Copy over Message Copying
-------------------------------------------
**Decision:** Use shared memory with direct pointer access instead of message copying.

**Rationale:** Automotive real-time constraints require sub-100µs latency.
Message copying introduces O(n) overhead proportional to data size.
Zero-copy provides O(1) latency regardless of payload size.

**Trade-off:** Higher complexity in memory management and lifecycle coordination.

DD-COM-002: Flag Files for Service Discovery
----------------------------------------------
**Decision:** Use filesystem flag files instead of a broker/registry process.

**Rationale:** No single point of failure. No additional process overhead.
Compatible with both Linux and QNX without platform-specific IPC.

**Trade-off:** Filesystem polling introduces small discovery latency.

DD-COM-003: Lock-Free Data Structures
--------------------------------------
**Decision:** Use atomic operations and lock-free algorithms for shared memory access.

**Rationale:** Mutexes are not suitable for ASIL-B communication:
priority inversion risk, unbounded blocking time, deadlock potential.

**Trade-off:** Lock-free algorithms are harder to verify for correctness.

DD-COM-004: Separate Linux and QNX Message Passing
----------------------------------------------------
**Decision:** Maintain two distinct message passing backends (mqueue for Linux,
native for QNX) instead of a single POSIX-only implementation.

**Rationale:** QNX native messaging provides better real-time guarantees and
integrates with QNX's microkernel architecture. POSIX mqueue on QNX has
limitations compared to native messaging.

Referenced Design Documents
===========================

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Document
     - Location in source
   * - Service Discovery Design
     - ``score/mw/com/design/service_discovery/README.md``
   * - Shared Memory Layout Design
     - ``score/mw/com/design/shared_mem_layout/README.md``
   * - Events/Fields Design
     - ``score/mw/com/design/events_fields/README.md``
   * - Skeleton/Proxy Design
     - ``score/mw/com/design/skeleton_proxy/README.md``
   * - Methods Design
     - ``score/mw/com/design/methods/README.md``
   * - Runtime Design
     - ``score/mw/com/design/runtime/README.md``
   * - Partial Restart Design
     - ``score/mw/com/design/partial_restart/README.md``
   * - IPC Tracing Design
     - ``score/mw/com/design/ipc_tracing/README.md``
   * - Configuration Design
     - ``score/mw/com/design/configuration/README.md``
   * - Message Passing Client-Server Design
     - ``score/message_passing/design/client-server.md``
   * - Error Handling Guide
     - ``score/mw/com/doc/error_handling_guide.md``
   * - User API Examples
     - ``score/mw/com/doc/user_facing_API_examples.md``
