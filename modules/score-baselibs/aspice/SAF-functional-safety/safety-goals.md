---
document_id: SG-BL
title: "Safety Goals — score-baselibs"
version: "1.0"
status: draft
iso_26262_part: 3
asil: B
date: 2026-03-20
---

# Safety Goals

## Context

Base libraries provide foundational services (OS abstraction, shared memory, concurrency, result types) used by all ASIL-B S-CORE modules (LoLa, lifecycle, FEO, persistency). A defect in baselibs propagates to all dependent safety-critical modules.

## SG-BL-001: Memory Safety

- **ASIL**: B
- **Traces down**: FSR-BL-001, FSR-BL-002
- **Fault Tolerance Time**: 0 ms

Shared memory operations provided by baselibs SHALL NOT cause memory corruption, buffer overflows, or use-after-free conditions in any calling module.

## SG-BL-002: Deterministic Execution

- **ASIL**: B
- **Traces down**: FSR-BL-003, FSR-BL-004
- **Fault Tolerance Time**: 100 ms

Concurrency primitives and OS abstractions SHALL have bounded worst-case execution time. No baselibs API SHALL introduce priority inversion or unbounded blocking on the ASIL-B path.

## SG-BL-003: Platform Behavioral Equivalence

- **ASIL**: B
- **Traces down**: FSR-BL-005
- **Fault Tolerance Time**: N/A (design-time)

The OS abstraction layer SHALL guarantee identical observable behavior on Linux and QNX for all ASIL-B classified APIs. Platform-specific differences SHALL be confined to the OS backend implementation.
