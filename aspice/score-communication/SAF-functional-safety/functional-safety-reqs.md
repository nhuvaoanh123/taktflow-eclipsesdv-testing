---
document_id: FSR-COM
title: "Functional Safety Requirements — score-communication (LoLa)"
version: "1.0"
status: draft
iso_26262_part: 3
asil: B
date: 2026-03-20
---

# Functional Safety Requirements

## Human-in-the-Loop (HITL) Comment Lock

Marker standard:
- `<!-- HITL-LOCK START:<id> -->` ... `<!-- HITL-LOCK END:<id> -->`

Rules:
- AI must NEVER edit, reformat, move, or delete text inside HITL-LOCK blocks
- Append-only outside locks — new comments only, prior HITL comments unchanged

---

## FSR-COM-001: Shared Memory Data Integrity Check

- **ASIL**: B
- **Traces up**: SG-COM-001
- **Traces down**: TSR-COM-001, TSR-COM-002
- **Safety mechanism**: SM-COM-001 (CRC-32 per data slot)
- **Allocation**: shared_mem_layout component
- **Status**: draft

The communication module SHALL provide a data integrity verification mechanism for every data slot in shared memory. Corruption SHALL be detected before the subscriber reads the data.

**Rationale**: Shared memory can be corrupted by hardware faults (bit flips), OS bugs, or errant QM process writes. CRC-32 provides sufficient detection capability for ASIL-B.

## FSR-COM-002: Message Sequence Monitoring

- **ASIL**: B
- **Traces up**: SG-COM-001
- **Traces down**: TSR-COM-003
- **Safety mechanism**: SM-COM-002 (alive counter per event channel)
- **Allocation**: message_passing component
- **Status**: draft

The communication module SHALL include a monotonic sequence counter in every notification message. The subscriber SHALL detect sequence gaps (lost messages) and sequence repeats (duplicated messages).

## FSR-COM-003: Deadline Monitoring for ASIL-B Events

- **ASIL**: B
- **Traces up**: SG-COM-002
- **Traces down**: TSR-COM-004, TSR-COM-005
- **Safety mechanism**: SM-COM-003 (deadline supervision timer)
- **Allocation**: runtime component
- **Status**: draft

The communication module SHALL monitor the delivery deadline of ASIL-B classified events. If an event is not delivered to the subscriber within the configured deadline, a timeout error SHALL be reported to the application.

**Rationale**: Stale data in a safety-critical consumer is as dangerous as corrupt data. The consumer must know when data is no longer fresh.

## FSR-COM-004: Bounded Worst-Case Execution Time

- **ASIL**: B
- **Traces up**: SG-COM-002
- **Traces down**: TSR-COM-006
- **Safety mechanism**: SM-COM-004 (lock-free algorithms with bounded loops)
- **Allocation**: shared_mem_layout, message_passing, runtime
- **Status**: draft

All operations on the ASIL-B data path (publish, notify, receive, read) SHALL have a bounded worst-case execution time that is deterministic and independent of system load from QM components.

## FSR-COM-005: Memory Isolation Between ASIL Levels

- **ASIL**: B
- **Traces up**: SG-COM-003
- **Traces down**: TSR-COM-007, TSR-COM-008
- **Safety mechanism**: SM-COM-005 (separate shared memory regions per ASIL level)
- **Allocation**: shared_mem_layout component
- **Status**: draft

The communication module SHALL allocate separate shared memory regions for ASIL-B and QM communication paths. A write operation to a QM shared memory region SHALL NOT be able to modify data in an ASIL-B shared memory region.

**Rationale**: ISO 26262-6 §7.4.4 requires freedom from interference. Physical memory separation is the strongest isolation mechanism.

## FSR-COM-006: QM Process Crash Containment

- **ASIL**: B
- **Traces up**: SG-COM-003
- **Traces down**: TSR-COM-009, TSR-COM-010
- **Safety mechanism**: SM-COM-006 (process crash detection + shared memory cleanup)
- **Allocation**: partial_restart component
- **Status**: draft

If a QM process communicating via LoLa crashes (SIGKILL, SIGSEGV), the communication module SHALL:
1. Detect the crash within 1 second
2. Clean up shared memory resources owned by the crashed process
3. Notify affected subscribers of publisher loss
4. NOT affect any ASIL-B communication path
