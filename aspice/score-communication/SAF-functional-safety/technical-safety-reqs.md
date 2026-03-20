---
document_id: TSR-COM
title: "Technical Safety Requirements — score-communication (LoLa)"
version: "1.0"
status: draft
iso_26262_part: 4
asil: B
date: 2026-03-20
---

# Technical Safety Requirements

## TSR-COM-001: CRC-32 Calculation on Data Slot Write

- **ASIL**: B
- **Traces up**: FSR-COM-001
- **Traces down**: SSR-COM-SHM-001, SWR-COM-SHM-001
- **Allocation**: shared_mem_layout
- **Status**: draft

On every write to a shared memory data slot, the module SHALL compute a CRC-32 checksum over the entire data payload and store it in the slot header.

## TSR-COM-002: CRC-32 Verification on Data Slot Read

- **ASIL**: B
- **Traces up**: FSR-COM-001
- **Traces down**: SSR-COM-SHM-002, SWR-COM-SHM-002
- **Allocation**: shared_mem_layout
- **Status**: draft

On every read from a shared memory data slot, the module SHALL recompute the CRC-32 checksum and compare it against the stored value. If mismatch, the read SHALL return an error and invoke the application error callback.

## TSR-COM-003: Alive Counter in Notification Messages

- **ASIL**: B
- **Traces up**: FSR-COM-002
- **Traces down**: SSR-COM-MP-001, SWR-COM-MP-004
- **Allocation**: message_passing
- **Status**: draft

Every notification message sent through the message passing layer SHALL include a monotonically incrementing 32-bit alive counter. The receiver SHALL compare the received counter against the expected value (previous + 1). Gaps or repeats SHALL trigger a sequence error callback.

## TSR-COM-004: Configurable Event Deadline

- **ASIL**: B
- **Traces up**: FSR-COM-003
- **Traces down**: SSR-COM-RT-001, SWR-COM-RT-001
- **Allocation**: runtime
- **Status**: draft

Each ASIL-B event subscription SHALL have a configurable deadline timeout (default: 100 ms). The runtime SHALL start a timer on the last received event and trigger a timeout error if no new event arrives within the deadline.

## TSR-COM-005: Timeout Error Reporting

- **ASIL**: B
- **Traces up**: FSR-COM-003
- **Traces down**: SSR-COM-RT-002, SWR-COM-RT-002
- **Allocation**: runtime
- **Status**: draft

When an event deadline expires, the module SHALL invoke the application's error handler callback with the event identifier and the elapsed time since the last received event.

## TSR-COM-006: Lock-Free Publish Path

- **ASIL**: B
- **Traces up**: FSR-COM-004
- **Traces down**: SSR-COM-SHM-003, SWR-COM-SHM-003
- **Allocation**: shared_mem_layout, message_passing
- **Status**: draft

The entire publish path (allocate slot → write data → compute CRC → send notification) SHALL use only lock-free operations (atomic compare-and-swap, memory fences). No mutex, semaphore, or blocking lock SHALL be used on the ASIL-B publish path.

## TSR-COM-007: Separate Shared Memory Regions per ASIL

- **ASIL**: B
- **Traces up**: FSR-COM-005
- **Traces down**: SSR-COM-SHM-004, SWR-COM-SHM-004
- **Allocation**: shared_mem_layout
- **Status**: draft

The module SHALL create distinct OS-level shared memory objects (POSIX: separate `shm_open` names; QNX: separate typed memory regions) for ASIL-B and QM service instances. ASIL-B regions SHALL have read-write permissions only for ASIL-B processes; QM processes SHALL NOT have write access to ASIL-B regions.

## TSR-COM-008: Guard Bytes Between Data Slots

- **ASIL**: B
- **Traces up**: FSR-COM-005
- **Traces down**: SSR-COM-SHM-005, SWR-COM-SHM-005
- **Allocation**: shared_mem_layout
- **Status**: draft

Each data slot in shared memory SHALL be surrounded by guard bytes (minimum 8 bytes, pattern 0xDEADBEEF). On every read, the guard bytes SHALL be verified. Guard byte corruption indicates a buffer overrun from an adjacent slot.

## TSR-COM-009: Process Crash Detection via Heartbeat

- **ASIL**: B
- **Traces up**: FSR-COM-006
- **Traces down**: SSR-COM-PR-001, SWR-COM-PR-001
- **Allocation**: partial_restart
- **Status**: draft

Each publisher process SHALL periodically update a heartbeat timestamp in its shared memory header (interval: configurable, default 200 ms). Subscribers SHALL monitor the heartbeat. If the heartbeat is not updated within 3× the interval, the publisher SHALL be considered crashed.

## TSR-COM-010: Shared Memory Cleanup on Publisher Crash

- **ASIL**: B
- **Traces up**: FSR-COM-006
- **Traces down**: SSR-COM-PR-002, SWR-COM-PR-002
- **Allocation**: partial_restart
- **Status**: draft

When a publisher crash is detected (via heartbeat timeout or OS notification), the module SHALL:
1. Mark all data slots owned by the crashed publisher as invalid (epoch increment)
2. Release the shared memory region after all subscribers have detached
3. Remove the service discovery flag file
4. NOT block or delay any ASIL-B subscribers of other services
