---
document_id: SWR-COM-RT
title: "Software Requirements — Runtime"
version: "1.0"
status: draft
aspice_process: SWE.1
component: runtime
source: score/mw/com/design/runtime/
date: 2026-03-20
---

# Software Requirements — Runtime (RT)

## SWR-COM-RT-001: Deadline Timer Creation

- **Traces up**: SSR-COM-RT-001, TSR-COM-004, FSR-COM-003, SG-COM-002
- **Traces down**: `@safety_req SWR-COM-RT-001` in `runtime.cpp`
- **Verified by**: `@verifies SWR-COM-RT-001` in `test_runtime.cpp`
- **ASIL**: B
- **Status**: draft

`subscribeWithDeadline(event_id, deadline_ms, timeout_callback)` SHALL:
1. Create a `CLOCK_MONOTONIC` timer for the subscription
2. Arm the timer with `deadline_ms` interval
3. Reset the timer on every received event
4. On expiry, invoke `timeout_callback(event_id, deadline_ms, elapsed_ms)`

## SWR-COM-RT-002: Timeout Error Callback Invocation

- **Traces up**: SSR-COM-RT-002, TSR-COM-005, FSR-COM-003, SG-COM-002
- **Traces down**: `@safety_req SWR-COM-RT-002` in `runtime.cpp`
- **Verified by**: `@verifies SWR-COM-RT-002` in `test_runtime.cpp`
- **ASIL**: B
- **Status**: draft

The timeout callback SHALL be invoked on a dedicated error-handling thread (not the data reception thread) to prevent blocking the data path. The callback signature:
```cpp
void onTimeout(ServiceId service, EventId event, uint32_t deadline_ms, uint32_t elapsed_ms);
```
