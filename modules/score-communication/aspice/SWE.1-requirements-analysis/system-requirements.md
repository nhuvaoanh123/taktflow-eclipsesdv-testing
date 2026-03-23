---
document_id: SYS-COM
title: "System Requirements — score-communication (LoLa)"
version: "1.0"
status: draft
aspice_process: SWE.1
date: 2026-03-20
---

# System Requirements

## SYS-COM-001: Shared Memory IPC

- **Traces up**: STK-COM-001, STK-COM-005
- **Traces down**: SWR-COM-SHM-001, SWR-COM-SHM-002, SWR-COM-SHM-003
- **ASIL**: B
- **Status**: implemented

The system SHALL provide inter-process communication based on shared memory, enabling zero-copy data exchange between publisher and subscriber processes on the same ECU.

## SYS-COM-002: Sub-Millisecond Latency

- **Traces up**: STK-COM-001
- **Traces down**: SWR-COM-MP-001, SWR-COM-SHM-004
- **ASIL**: B
- **Status**: implemented

The system SHALL deliver published data to subscribers within 100 microseconds (p99) for short messages (≤16 bytes) under nominal load conditions.

## SYS-COM-003: AUTOSAR ara::com Compliance

- **Traces up**: STK-COM-002
- **Traces down**: SWR-COM-SK-001, SWR-COM-PX-001, SWR-COM-EF-001, SWR-COM-MT-001
- **ASIL**: QM
- **Status**: implemented

The system SHALL implement the Adaptive AUTOSAR Communication Management API patterns including:
- Skeleton (service provider) and Proxy (service consumer) abstractions
- Event, Field, and Method communication patterns
- FindService / OfferService / StopOfferService service discovery

## SYS-COM-004: ASIL-B Data Integrity

- **Traces up**: STK-COM-003
- **Traces down**: SG-COM-001, SG-COM-002, SG-COM-003, SSR-COM-SHM-001, SSR-COM-MP-001
- **ASIL**: B
- **Status**: implemented

The system SHALL guarantee that data exchanged via ASIL-B classified communication paths is not corrupted, lost without detection, or delivered out of bounds.

## SYS-COM-005: Linux and QNX Platform Support

- **Traces up**: STK-COM-004
- **Traces down**: SWR-COM-MP-002, SWR-COM-MP-003
- **ASIL**: B
- **Status**: implemented

The system SHALL support execution on:
- Linux (Ubuntu 24.04+, POSIX APIs: shm_open, mmap, mqueue)
- QNX 8.0 (QNX native messaging: msg_send, msg_receive, typed memory)

The user-level API SHALL be identical on both platforms.

## SYS-COM-006: Dynamic Service Discovery

- **Traces up**: STK-COM-006
- **Traces down**: SWR-COM-SD-001, SWR-COM-SD-002, SWR-COM-SD-003
- **ASIL**: QM
- **Status**: implemented

The system SHALL provide automatic service registration and discovery using a filesystem-based mechanism (flag files) that does not require a central broker process.

## SYS-COM-007: Fault Isolation and Partial Restart

- **Traces up**: STK-COM-007
- **Traces down**: SWR-COM-PR-001, SWR-COM-PR-002, SWR-COM-PR-003, FSR-COM-005
- **ASIL**: B
- **Status**: implemented

The system SHALL support partial restart of individual communication services without affecting other running services. A crashing publisher SHALL NOT corrupt subscriber state.

## SYS-COM-008: Communication Tracing

- **Traces up**: STK-COM-008
- **Traces down**: SWR-COM-TR-001, SWR-COM-TR-002
- **ASIL**: QM
- **Status**: implemented

The system SHALL provide zero-copy, binding-agnostic communication tracing that captures publish/subscribe/discover events with timestamps for debugging and performance analysis.

## SYS-COM-009: FEO Integration

- **Traces up**: STK-COM-009
- **Traces down**: SWR-COM-RT-001, SWR-COM-RT-002
- **ASIL**: B
- **Status**: planned

The system SHALL integrate with the Fixed Execution Order (FEO) framework such that data publication and consumption occur at deterministic cycle boundaries.

## SYS-COM-010: Multi-Subscriber Scalability

- **Traces up**: STK-COM-010
- **Traces down**: SWR-COM-EF-002, SWR-COM-SHM-005
- **ASIL**: QM
- **Status**: implemented

The system SHALL support at least 10 concurrent subscribers to a single publisher without message loss or latency degradation beyond 2x the single-subscriber baseline.
