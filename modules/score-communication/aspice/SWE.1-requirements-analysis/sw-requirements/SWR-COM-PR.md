---
document_id: SWR-COM-PR
title: "Software Requirements — Partial Restart"
version: "1.0"
status: draft
aspice_process: SWE.1
component: partial_restart
source: score/mw/com/design/partial_restart/
date: 2026-03-20
---

# Software Requirements — Partial Restart (PR)

## SWR-COM-PR-001: Heartbeat Monitoring Implementation

- **Traces up**: SSR-COM-PR-001, TSR-COM-009, FSR-COM-006, SG-COM-003
- **Traces down**: `@safety_req SWR-COM-PR-001` in `partial_restart.cpp`
- **Verified by**: `@verifies SWR-COM-PR-001` in `test_partial_restart.cpp`
- **ASIL**: B
- **Status**: draft

Publisher side:
```cpp
// In publisher tick (called at heartbeat_interval)
shm_header->heartbeat_ns.store(clock_gettime_ns(CLOCK_MONOTONIC), std::memory_order_release);
```

Subscriber side:
```cpp
// On every readSlot()
auto now = clock_gettime_ns(CLOCK_MONOTONIC);
auto hb = shm_header->heartbeat_ns.load(std::memory_order_acquire);
if ((now - hb) > 3 * heartbeat_interval_ns) {
    return Error::PublisherCrashed;
}
```

## SWR-COM-PR-002: Crash Cleanup Implementation

- **Traces up**: SSR-COM-PR-002, TSR-COM-010, FSR-COM-006, SG-COM-003
- **Traces down**: `@safety_req SWR-COM-PR-002` in `partial_restart.cpp`
- **Verified by**: `@verifies SWR-COM-PR-002` in `test_partial_restart.cpp`
- **ASIL**: B
- **Status**: draft

`cleanupCrashedPublisher(service_id)` SHALL:
1. `shm_header->epoch.fetch_add(1, std::memory_order_release)`
2. For each slot: `slot.state.store(INVALID, std::memory_order_release)`
3. Invoke `subscriber_error_callback(Error::PublisherCrashed)` for all subscribers
4. Wait for all subscribers to call `detach()`
5. `shm_unlink(shm_name)`
6. `unlink(flag_file_path)`
7. Total execution time SHALL be < 100 ms

## SWR-COM-PR-003: Subscriber Re-Discovery After Crash

- **Traces up**: SYS-COM-007
- **Traces down**: `@safety_req SWR-COM-PR-003` in `partial_restart.cpp`
- **Verified by**: `@verifies SWR-COM-PR-003` in `test_partial_restart.cpp`
- **ASIL**: QM
- **Status**: draft

After receiving `Error::PublisherCrashed`, the subscriber's `FindService` handler SHALL automatically re-scan for the service at the configured re-discovery interval (default: 1 second). When the service reappears, the subscription SHALL be automatically re-established.
