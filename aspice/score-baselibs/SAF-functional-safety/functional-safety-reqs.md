---
document_id: FSR-BL
title: "Functional Safety Requirements — score-baselibs"
version: "1.0"
status: draft
iso_26262_part: 3
asil: B
date: 2026-03-20
---

# Functional Safety Requirements

## FSR-BL-001: Bounds-Checked Shared Memory Access

- **ASIL**: B
- **Traces up**: SG-BL-001
- **Traces down**: TSR-BL-001, TSR-BL-002
- **Safety mechanism**: SM-BL-001 (compile-time size validation + runtime bounds check)
- **Allocation**: score/memory/shared_memory
- **Status**: draft

All shared memory read/write operations SHALL perform bounds checking against the allocated region size. Out-of-bounds access SHALL return `score::Result<Error>` without performing the access.

## FSR-BL-002: No Dynamic Allocation on ASIL-B Path

- **ASIL**: B
- **Traces up**: SG-BL-001
- **Traces down**: TSR-BL-003
- **Safety mechanism**: SM-BL-002 (static allocation enforcement)
- **Allocation**: score/memory, score/concurrency
- **Status**: draft

ASIL-B classified baselibs components SHALL NOT use dynamic heap allocation (`new`, `malloc`) after initialization. All memory SHALL be statically allocated or allocated from fixed-size pools at startup.

## FSR-BL-003: Lock-Free Concurrency Primitives

- **ASIL**: B
- **Traces up**: SG-BL-002
- **Traces down**: TSR-BL-004
- **Safety mechanism**: SM-BL-003 (atomic operations only)
- **Allocation**: score/concurrency
- **Status**: draft

Concurrency primitives used on ASIL-B data paths SHALL be lock-free. They SHALL use only atomic operations (`std::atomic`, memory fences) and SHALL NOT use mutexes, condition variables, or semaphores.

## FSR-BL-004: Abort-on-Exception Policy

- **ASIL**: B
- **Traces up**: SG-BL-002
- **Traces down**: TSR-BL-005
- **Safety mechanism**: SM-BL-004 (custom termination handler)
- **Allocation**: score/language/safecpp
- **Status**: draft

If a C++ exception is thrown in an ASIL-B context, the safecpp module SHALL abort the process immediately via `std::terminate`. No exception propagation SHALL occur on the ASIL-B path.

## FSR-BL-005: OS Abstraction Behavioral Parity

- **ASIL**: B
- **Traces up**: SG-BL-003
- **Traces down**: TSR-BL-006, TSR-BL-007
- **Safety mechanism**: SM-BL-005 (cross-platform test suite)
- **Allocation**: score/os
- **Status**: draft

The score/os abstraction layer SHALL provide identical return codes, error semantics, and timing behavior for all ASIL-B APIs on both Linux and QNX. Platform-specific extensions SHALL be in separate, clearly marked namespaces (`score::os::linux`, `score::os::qnx`).
