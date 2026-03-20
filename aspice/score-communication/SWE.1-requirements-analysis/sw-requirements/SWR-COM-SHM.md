---
document_id: SWR-COM-SHM
title: "Software Requirements — Shared Memory Layout"
version: "1.0"
status: draft
aspice_process: SWE.1
component: shared_mem_layout
source: score/mw/com/design/shared_mem_layout/
date: 2026-03-20
---

# Software Requirements — Shared Memory Layout (SHM)

## SWR-COM-SHM-001: CRC-32 Computation on Write

- **Traces up**: SSR-COM-SHM-001, TSR-COM-001, FSR-COM-001, SG-COM-001
- **Traces down**: `@safety_req SWR-COM-SHM-001` in `shared_mem_layout.cpp`
- **Verified by**: `@verifies SWR-COM-SHM-001` in `test_shared_mem_layout.cpp`
- **ASIL**: B
- **Status**: draft

`writeSlot(slot_index, data_ptr, data_size)` SHALL:
1. Copy `data_size` bytes from `data_ptr` to `slot[slot_index].payload`
2. Compute CRC-32 (polynomial 0xEDB88320) over `slot[slot_index].payload[0..data_size]`
3. Store result in `slot[slot_index].header.crc32`
4. Set `slot[slot_index].header.state` to `VALID` (atomic release store)

## SWR-COM-SHM-002: CRC-32 Verification on Read

- **Traces up**: SSR-COM-SHM-002, TSR-COM-002, FSR-COM-001, SG-COM-001
- **Traces down**: `@safety_req SWR-COM-SHM-002` in `shared_mem_layout.cpp`
- **Verified by**: `@verifies SWR-COM-SHM-002` in `test_shared_mem_layout.cpp`
- **ASIL**: B
- **Status**: draft

`readSlot(slot_index)` SHALL:
1. Load `slot[slot_index].header.state` (atomic acquire load)
2. If state != `VALID`, return `Error::SlotNotReady`
3. Read `slot[slot_index].payload[0..header.data_size]`
4. Compute CRC-32 over the read payload
5. Compare with `header.crc32`
6. If mismatch, return `Error::DataCorrupted`
7. If match, return `Result<DataView>`

## SWR-COM-SHM-003: Lock-Free Slot Allocation

- **Traces up**: SSR-COM-SHM-003, TSR-COM-006, FSR-COM-004, SG-COM-002
- **Traces down**: `@safety_req SWR-COM-SHM-003` in `shared_mem_layout.cpp`
- **Verified by**: `@verifies SWR-COM-SHM-003` in `test_shared_mem_layout.cpp`
- **ASIL**: B
- **Status**: draft

`allocateSlot()` SHALL:
1. Scan slot array for `state == FREE` (starting from `next_alloc_hint`)
2. Attempt `compare_exchange_strong(FREE, WRITING)` on slot state
3. If CAS succeeds, return slot index
4. If CAS fails, try next slot (max 3 full scans)
5. If all scans fail, return `Error::SlotUnavailable`
6. SHALL NOT use any mutex or blocking synchronization

## SWR-COM-SHM-004: ASIL-Separated Memory Object Creation

- **Traces up**: SSR-COM-SHM-004, TSR-COM-007, FSR-COM-005, SG-COM-003
- **Traces down**: `@safety_req SWR-COM-SHM-004` in `shared_mem_layout.cpp`
- **Verified by**: `@verifies SWR-COM-SHM-004` in `test_shared_mem_layout.cpp`
- **ASIL**: B
- **Status**: draft

`createSharedMemory(service_id, asil_level)` SHALL:
- If `asil_level == ASIL_B`: name = `/score_com_asilb_<service_id>`, mode = `0660`
- If `asil_level == QM`: name = `/score_com_qm_<service_id>`, mode = `0666`
- Linux: `shm_open(name, O_CREAT | O_RDWR, mode)` + `ftruncate` + `mmap`
- QNX: `shm_open(name, ...)` with typed memory allocation

## SWR-COM-SHM-005: Guard Byte Initialization and Check

- **Traces up**: SSR-COM-SHM-005, TSR-COM-008, FSR-COM-005, SG-COM-003
- **Traces down**: `@safety_req SWR-COM-SHM-005` in `shared_mem_layout.cpp`
- **Verified by**: `@verifies SWR-COM-SHM-005` in `test_shared_mem_layout.cpp`
- **ASIL**: B
- **Status**: draft

Slot memory layout:
```
[guard_pre: 8 bytes = 0xDEADBEEF × 2]
[header: crc32, state, data_size, epoch, heartbeat_ns]
[payload: data_size bytes]
[guard_post: 8 bytes = 0xDEADBEEF × 2]
```

`readSlot()` SHALL verify `guard_pre` and `guard_post` before returning data.
Corruption SHALL return `Error::GuardByteViolation`.
