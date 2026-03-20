---
document_id: SSR-COM
title: "Software Safety Requirements — score-communication (LoLa)"
version: "1.0"
status: draft
iso_26262_part: 6
asil: B
date: 2026-03-20
---

# Software Safety Requirements

Per-component allocation. Component prefix in ID maps to implementation.

---

## Shared Memory Layout (SHM)

### SSR-COM-SHM-001: CRC-32 Write Implementation

- **ASIL**: B
- **Traces up**: TSR-COM-001
- **Traces down**: SWR-COM-SHM-001
- **Allocation**: `score/mw/com/impl/shared_mem_layout/`
- **Status**: draft

The `SharedMemoryLayout::writeSlot()` function SHALL compute CRC-32 (ISO 3309 polynomial) over the data payload bytes and store the result in `slot.header.crc32` before making the slot visible to readers.

### SSR-COM-SHM-002: CRC-32 Read Verification

- **ASIL**: B
- **Traces up**: TSR-COM-002
- **Traces down**: SWR-COM-SHM-002
- **Allocation**: `score/mw/com/impl/shared_mem_layout/`
- **Status**: draft

The `SharedMemoryLayout::readSlot()` function SHALL recompute CRC-32 over the read payload and compare against `slot.header.crc32`. On mismatch, the function SHALL return `score::Result<Error::DataCorrupted>` and SHALL NOT return the payload to the caller.

### SSR-COM-SHM-003: Lock-Free Slot Allocation

- **ASIL**: B
- **Traces up**: TSR-COM-006
- **Traces down**: SWR-COM-SHM-003
- **Allocation**: `score/mw/com/impl/shared_mem_layout/`
- **Status**: draft

Slot allocation SHALL use atomic `compare_exchange_strong` on the slot state field. The allocation loop SHALL have a bounded retry count (max 3 attempts). If all retries fail, the function SHALL return `Error::SlotUnavailable` without blocking.

### SSR-COM-SHM-004: ASIL-Separated Memory Objects

- **ASIL**: B
- **Traces up**: TSR-COM-007
- **Traces down**: SWR-COM-SHM-004
- **Allocation**: `score/mw/com/impl/shared_mem_layout/`
- **Status**: draft

The module SHALL create shared memory objects with naming convention:
- ASIL-B: `/score_com_asilb_<service_id>`
- QM: `/score_com_qm_<service_id>`

ASIL-B objects SHALL be created with `0660` permissions (owner + group read-write). QM processes SHALL NOT be in the ASIL-B group.

### SSR-COM-SHM-005: Guard Byte Verification

- **ASIL**: B
- **Traces up**: TSR-COM-008
- **Traces down**: SWR-COM-SHM-005
- **Allocation**: `score/mw/com/impl/shared_mem_layout/`
- **Status**: draft

Each slot SHALL have 8 guard bytes before and after the data payload, initialized to `0xDEADBEEF`. On `readSlot()`, guard bytes SHALL be verified. Corruption SHALL return `Error::GuardByteViolation`.

---

## Message Passing (MP)

### SSR-COM-MP-001: Alive Counter Implementation

- **ASIL**: B
- **Traces up**: TSR-COM-003
- **Traces down**: SWR-COM-MP-004
- **Allocation**: `score/mw/com/message_passing/`
- **Status**: draft

The message passing sender SHALL maintain a `uint32_t` alive counter per channel, incrementing by 1 on every send. The counter SHALL wrap at `UINT32_MAX` to 0. The receiver SHALL track the expected next counter value and report `Error::SequenceGap` or `Error::SequenceRepeat` on mismatch.

---

## Runtime (RT)

### SSR-COM-RT-001: Deadline Timer per Subscription

- **ASIL**: B
- **Traces up**: TSR-COM-004
- **Traces down**: SWR-COM-RT-001
- **Allocation**: `score/mw/com/impl/runtime/`
- **Status**: draft

For each ASIL-B event subscription, the runtime SHALL create a monotonic timer (POSIX: `timer_create(CLOCK_MONOTONIC)`; QNX: `TimerCreate`). The timer SHALL be reset on every received event. Timer expiry SHALL invoke the subscriber's timeout callback.

### SSR-COM-RT-002: Timeout Error Callback

- **ASIL**: B
- **Traces up**: TSR-COM-005
- **Traces down**: SWR-COM-RT-002
- **Allocation**: `score/mw/com/impl/runtime/`
- **Status**: draft

The timeout callback SHALL provide: event identifier (`ServiceId`, `EventId`), configured deadline (milliseconds), elapsed time since last event (milliseconds). The callback SHALL be invoked from a dedicated error-handling thread, not the data reception thread.

---

## Partial Restart (PR)

### SSR-COM-PR-001: Heartbeat Monitoring

- **ASIL**: B
- **Traces up**: TSR-COM-009
- **Traces down**: SWR-COM-PR-001
- **Allocation**: `score/mw/com/impl/partial_restart/`
- **Status**: draft

The publisher SHALL write `clock_gettime(CLOCK_MONOTONIC)` to `shm_header.heartbeat_ns` at the configured heartbeat interval. Subscribers SHALL check `(now - heartbeat_ns) > 3 * heartbeat_interval` on every read. Expired heartbeat SHALL trigger `Error::PublisherCrashed`.

### SSR-COM-PR-002: Crash Cleanup Procedure

- **ASIL**: B
- **Traces up**: TSR-COM-010
- **Traces down**: SWR-COM-PR-002
- **Allocation**: `score/mw/com/impl/partial_restart/`
- **Status**: draft

On publisher crash detection:
1. Increment `shm_header.epoch` (atomic)
2. Set all slot states to `INVALID` (atomic)
3. Notify subscribers via error callback `Error::PublisherCrashed`
4. Unlink shared memory object after last subscriber detaches (`shm_unlink`)
5. Remove service discovery flag file
6. Total cleanup time SHALL be < 100 ms
