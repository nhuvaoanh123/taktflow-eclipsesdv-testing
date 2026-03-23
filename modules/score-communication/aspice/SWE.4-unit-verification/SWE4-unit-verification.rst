.. # *******************************************************************************
   # Copyright (c) 2026 Taktflow Systems
   # SPDX-License-Identifier: Apache-2.0
   # *******************************************************************************

SWE.4 — Software Unit Verification
####################################

Module: score-communication (LoLa)
**********************************

:ASPICE Level: 2
:Safety Classification: ASIL-B
:Status: Active

Purpose
=======

This work product documents the unit verification strategy, test plan, and
results for the S-CORE Communication Module (LoLa).

Verification Strategy
=====================

.. list-table:: Verification Methods per ASIL
   :header-rows: 1
   :widths: 20 40 40

   * - ASIL
     - Required Methods (ISO 26262-6 Table 9)
     - Applied Methods
   * - B
     - Requirements-based testing, interface testing, fault injection, resource usage
     - All required + structural coverage (statement + branch)
   * - QM
     - Requirements-based testing
     - Requirements-based testing + interface testing

Test Framework
==============

:Framework: GoogleTest (gtest) + Google Benchmark
:Build System: Bazel ``cc_test`` rules
:Coverage Tool: ``bazel coverage`` with lcov
:Static Analysis: clang-tidy (configured via ``.clang-tidy``)

Test Execution
--------------

.. code-block:: bash

   # Run all unit tests
   bazel test //score/mw/com/...

   # Run specific component tests
   bazel test //score/mw/com/impl:all
   bazel test //score/mw/com/message_passing:all

   # Run with coverage
   bazel coverage //score/mw/com/...

   # Run benchmarks
   bazel run //score/mw/com/performance_benchmarks:all

Test Plan
=========

.. list-table:: Unit Test Coverage by Component
   :header-rows: 1
   :widths: 25 10 15 50

   * - Component
     - ASIL
     - Coverage Target
     - Test Focus
   * - shared_mem_layout
     - B
     - Branch ≥80%
     - Memory slot allocation/deallocation, bounds checking, concurrent access, overflow protection
   * - message_passing
     - B
     - Branch ≥80%
     - Short/medium message send/receive, channel creation/destruction, N-to-1 fan-in, platform backends (mqueue + qnx)
   * - skeleton
     - B
     - Branch ≥80%
     - Service offer/stop-offer, event publication, field update, lifecycle management
   * - proxy
     - B
     - Branch ≥80%
     - Service discovery, event subscription, field read, method invocation
   * - generic_proxy_event
     - B
     - Branch ≥80%
     - Sample acquisition, notification callbacks, GetSampleSize validation, buffer management
   * - events_fields
     - B
     - Branch ≥80%
     - Event fire, field get/set, notification propagation, subscriber management
   * - service_discovery
     - QM
     - Statement ≥70%
     - Flag file creation/deletion, service matching, concurrent discovery
   * - methods (RPC)
     - QM
     - Statement ≥70%
     - Synchronous call, async call with future, timeout handling, error propagation
   * - partial_restart
     - B
     - Branch ≥80%
     - Graceful shutdown, reconnection, state recovery, isolation verification
   * - configuration
     - QM
     - Statement ≥70%
     - Config loading, validation, default values, error handling
   * - runtime
     - B
     - Branch ≥80%
     - Thread pool management, scheduling, WCET bounded paths
   * - non_allocating_future
     - B
     - Branch ≥80%
     - Stack allocation, value setting, waiting, timeout, exception safety

Fault Injection Tests (ASIL-B)
==============================

.. list-table:: Fault Injection Test Cases
   :header-rows: 1
   :widths: 15 35 25 25

   * - ID
     - Fault Injected
     - Expected Behavior
     - Requirement
   * - FI-001
     - Shared memory corruption (bit flip in data slot)
     - CRC check detects corruption, error callback invoked
     - SR-COM-003
   * - FI-002
     - Message queue full (back-pressure)
     - Sender receives error, no data loss on receiver side
     - SR-COM-003
   * - FI-003
     - Service discovery flag file deleted mid-communication
     - Ongoing communication continues, re-discovery on timeout
     - FR-COM-010
   * - FI-004
     - Publisher process crash during write
     - Shared memory slot marked invalid, subscriber not affected
     - SR-COM-001
   * - FI-005
     - Subscriber process crash during read
     - Publisher continues publishing, slot recycled after timeout
     - SR-COM-001
   * - FI-006
     - Concurrent write to same shared memory slot
     - Lock-free algorithm prevents data corruption, atomic CAS
     - SR-COM-001, FR-COM-007
   * - FI-007
     - Message sequence number gap (lost notification)
     - Subscriber detects gap, requests re-sync
     - SR-COM-003

Performance Benchmarks
======================

Location: ``score/mw/com/performance_benchmarks/``

.. list-table:: Benchmark Targets
   :header-rows: 1
   :widths: 30 20 20 30

   * - Benchmark
     - Target
     - Measurement
     - Requirement
   * - Intra-ECU event latency (short msg)
     - < 100 µs (p99)
     - Publish → subscriber callback
     - NFR-COM-001
   * - Intra-ECU event latency (large payload)
     - < 200 µs (p99)
     - Publish → subscriber callback
     - NFR-COM-001
   * - Throughput (events/sec)
     - > 100,000
     - Single publisher, single subscriber
     - NFR-COM-001
   * - Memory per service instance
     - < configurable limit
     - RSS after service creation
     - NFR-COM-002
   * - Service discovery time
     - < 500 ms
     - FindService → handle returned
     - FR-COM-003

Static Analysis
===============

:Tool: clang-tidy
:Configuration: ``.clang-tidy`` in repository root
:Checks: cert-*, bugprone-*, performance-*, readability-*
:Gate: Zero warnings on CI (warnings treated as errors)

Code Review Checklist
=====================

Documented in: ``score/mw/com/design/codeinspectionchecklists.md``

- All ASIL-B code changes require 2 reviewers
- QM code changes require 1 reviewer
- Safety-related changes require safety engineer review
- Performance-sensitive changes require benchmark comparison
