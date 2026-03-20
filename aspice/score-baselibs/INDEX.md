---
document_id: SCORE-BL-INDEX
title: "Eclipse S-CORE Base Libraries — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# score-baselibs — Document Registry

Foundation C++ libraries for all S-CORE modules. Explicitly classified **QM to ASIL-B**.

## Module Profile

| Attribute | Value |
|---|---|
| Commits | 957 |
| Contributors | 64 |
| Language | C++17 |
| Build | Bazel |
| ASIL | QM to ASIL-B |
| Platforms | x86_64 Linux, AArch64 Linux, x86_64/AArch64 QNX 8.0 |
| Target Chip | All (Pi QNX + TMS570 + L552ZE via cross-compile) |

## Components

| Component | ASIL | Description |
|---|---|---|
| `score/os` | B | OS abstraction (POSIX, Linux, QNX APIs) |
| `score/os/utils/qnx/resource_manager` | B | QNX resource manager framework |
| `score/memory/shared_memory` | B | Shared memory allocation (named, anonymous, offset pointers) |
| `score/concurrency` | B | Lock-free data structures, futures, thread safety |
| `score/result` | B | Result/Error types (no exceptions) |
| `score/mw/log` | QM | Logging frontend (shared memory writer, circular buffer) |
| `score/json` | QM | JSON serialization/deserialization |
| `score/filesystem` | QM | File abstraction |
| `score/language/safecpp` | B | Safe math, scoped functions, abort-on-exception |
| `score/static_reflection_with_serialization` | QM | Compile-time reflection + serialization |
| `score/bitmanipulation` | QM | Bit manipulation utilities |

## Requirement ID Format

| Level | Pattern | Example |
|---|---|---|
| STK | `STK-BL-NNN` | STK-BL-001 |
| SYS | `SYS-BL-NNN` | SYS-BL-001 |
| SG | `SG-BL-NNN` | SG-BL-001 |
| FSR | `FSR-BL-NNN` | FSR-BL-001 |
| TSR | `TSR-BL-NNN` | TSR-BL-001 |
| SSR | `SSR-BL-[COMP]-NNN` | SSR-BL-SHM-001 |
| SWR | `SWR-BL-[COMP]-NNN` | SWR-BL-OS-001 |

Component prefixes: OS (os abstraction), SHM (shared_memory), CON (concurrency), RES (result), LOG (mw/log), JSON (json), FS (filesystem), SAFE (safecpp), SER (serialization), BIT (bitmanipulation), QRM (qnx resource_manager)
