---
document_id: SWR-COM-MP
title: "Software Requirements — Message Passing"
version: "1.0"
status: draft
aspice_process: SWE.1
component: message_passing
source: score/message_passing/
date: 2026-03-20
---

# Software Requirements — Message Passing (MP)

## SWR-COM-MP-001: Short Message Send (Linux/mqueue)

- **Traces up**: SYS-COM-002
- **Traces down**: `@safety_req SWR-COM-MP-001` in `mqueue_sender.cpp`
- **Verified by**: `@verifies SWR-COM-MP-001` in `test_mqueue.cpp`
- **ASIL**: B
- **Status**: draft

`send(channel, payload_8bytes)` SHALL write the 8-byte payload to the POSIX message queue in non-blocking mode (`O_NONBLOCK`). If the queue is full, SHALL return `Error::QueueFull` without blocking.

## SWR-COM-MP-002: Platform Backend — Linux (mqueue)

- **Traces up**: SYS-COM-005
- **Traces down**: `@safety_req SWR-COM-MP-002` in `mqueue_sender.cpp`, `mqueue_receiver.cpp`
- **Verified by**: `@verifies SWR-COM-MP-002` in `test_mqueue.cpp`
- **ASIL**: B
- **Status**: draft

The Linux message passing backend SHALL use POSIX message queues (`mq_open`, `mq_send`, `mq_receive`). Queue names SHALL follow `/score_mp_<channel_id>`.

## SWR-COM-MP-003: Platform Backend — QNX (native)

- **Traces up**: SYS-COM-005
- **Traces down**: `@safety_req SWR-COM-MP-003` in `qnx_sender.cpp`, `qnx_receiver.cpp`
- **Verified by**: `@verifies SWR-COM-MP-003` in `test_qnx_messaging.cpp`
- **ASIL**: B
- **Status**: draft

The QNX message passing backend SHALL use QNX native messaging (`MsgSend`, `MsgReceive`, `MsgReply`). Channel creation SHALL use `ChannelCreate()` with appropriate flags for the ASIL level.

## SWR-COM-MP-004: Alive Counter per Channel

- **Traces up**: SSR-COM-MP-001, TSR-COM-003, FSR-COM-002, SG-COM-001
- **Traces down**: `@safety_req SWR-COM-MP-004` in `message_passing.cpp`
- **Verified by**: `@verifies SWR-COM-MP-004` in `test_message_passing.cpp`
- **ASIL**: B
- **Status**: draft

Message format:
```
[alive_counter: uint32_t] [payload: 8 or 16 bytes]
```

Sender: `counter++` before every `send()`.
Receiver: `if (received_counter != expected_counter) → Error::SequenceGap/Repeat`.
Wrap at `UINT32_MAX → 0` is valid (no error).
