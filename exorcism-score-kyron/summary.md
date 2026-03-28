# Project Analysis: score-kyron

## Overview
| Item | Value |
|------|-------|
| Languages | Rust, Python |
| Build System | Cargo, Bazel, Python/pyproject |
| Total Files | 166 |
| Total LOC | 34,279 |
| Total Functions | 2058 |
| State Machines | 22 |
| Communication Patterns | 0 |
| External Dependencies | 43 |

## Language Breakdown
- **Rust**: 138 files, 28,845 LOC
- **Python**: 28 files, 5,434 LOC

## Architecture Overview
Build system: **Cargo, Bazel, Python/pyproject**

### State Machines Detected
- `src/logging_tracing/src/tracing.rs:51` — match on `tracing_mode` (2 states)
- `src/kyron-foundation/src/containers/reusable_objects.rs:159` — match on `self.states[index].0.compare_exchange(
                OBJECT_TAKEN,
                OBJECT_POOL_GONE,
                ::core::sync::atomic::Ordering::AcqRel,
                ::core::sync::atomic::Ordering::Acquire,
            )` (2 states)
- `src/kyron-foundation/src/containers/reusable_objects.rs:193` — match on `self.this.state.0.compare_exchange(
                    OBJECT_TAKEN,
                    OBJECT_FREE,
                    ::core::sync::atomic::Ordering::AcqRel,
                    ::core::sync::atomic::Ordering::Acquire,
                )` (2 states)
- `src/kyron/src/channels/spsc.rs:270` — match on `self.state` (2 states)
- `src/kyron/src/channels/spmc_broadcast.rs:301` — match on `self.state` (2 states)
- `src/kyron/src/futures/sleep.rs:76` — match on `self.state` (3 states)
- `src/kyron/src/futures/reusable_box_future.rs:186` — match on `self.states[index].0.compare_exchange(
                FUTURE_TAKEN,
                FUTURE_POOL_GONE,
                ::core::sync::atomic::Ordering::AcqRel,
                ::core::sync::atomic::Ordering::Acquire,
            )` (2 states)
- `src/kyron/src/futures/reusable_box_future.rs:228` — match on `self.this.state.0.compare_exchange(
                    FUTURE_TAKEN,
                    FUTURE_FREE,
                    ::core::sync::atomic::Ordering::AcqRel,
                    ::core::sync::atomic::Ordering::Acquire,
                )` (2 states)
- `src/kyron/src/scheduler/join_handle.rs:67` — match on `self.state` (3 states)
- `src/kyron/src/scheduler/workers/worker_types.rs:234` — match on `self.state.0.swap(WORKER_STATE_NOTIFIED, Ordering::SeqCst)` (6 states)

## Key Findings

### High Complexity Functions (cc > 10)
- try_from (src/logging_tracing/src/tracing.rs:29) cc=13
- format_timestamp (src/logging_tracing/src/tracing.rs:244) cc=14
- is_leap (src/logging_tracing/src/tracing.rs:286) cc=11
- main (src/xtask/src/main.rs:20) cc=18
- from (src/kyron-foundation/src/types.rs:30) cc=13
- pop_local (src/kyron-foundation/src/containers/spmc_queue.rs:354) cc=11
- steal_internal (src/kyron-foundation/src/containers/spmc_queue.rs:398) cc=21
- push_to_mpmc (src/kyron-foundation/src/containers/spmc_queue.rs:477) cc=11
- test_concurrent_push_pop (src/kyron-foundation/src/containers/trigger_queue.rs:322) cc=11
- test_pop_into_vec_concurrent (src/kyron-foundation/src/containers/trigger_queue.rs:369) cc=11
- test_broadcast_channel_mt_sender_receiver (src/kyron/src/channels/spmc_broadcast.rs:642) cc=18
- poll (src/kyron/src/futures/sleep.rs:72) cc=12
- fuzzy_polling_before_in_after (src/kyron/src/time/mod.rs:597) cc=14
- count_less_eq_than (src/kyron/src/time/mod.rs:664) cc=11
- pipe_with_flags (src/kyron/src/mio/selector/unix/poll.rs:232) cc=13
- select (src/kyron/src/mio/selector/unix/poll.rs:499) cc=26
- wait_all (src/kyron/src/ipc/iceoryx2/event.rs:99) cc=13
- create_engine_with_worker_and_verify_ids (src/kyron/src/scheduler/execution_engine.rs:543) cc=11
- poll (src/kyron/src/scheduler/join_handle.rs:66) cc=16
- poll_core (src/kyron/src/scheduler/task/async_task.rs:269) cc=23

### High Nesting Functions (depth > 3)
- try_from (src/logging_tracing/src/tracing.rs:29) depth=6
- format_timestamp (src/logging_tracing/src/tracing.rs:244) depth=5
- main (src/xtask/src/main.rs:20) depth=4
- check_license_header (src/xtask/src/main.rs:239) depth=4
- visit_dirs (src/xtask/src/main.rs:260) depth=7
- get_notifier (src/kyron-foundation/src/threading/thread_wait_barrier.rs:67) depth=4
- push (src/kyron-foundation/src/containers/spmc_queue.rs:284) depth=5
- push_local_queue (src/kyron-foundation/src/containers/spmc_queue.rs:297) depth=4
- fetch_from (src/kyron-foundation/src/containers/spmc_queue.rs:321) depth=5
- pop_local (src/kyron-foundation/src/containers/spmc_queue.rs:354) depth=5
- steal_internal (src/kyron-foundation/src/containers/spmc_queue.rs:398) depth=5
- push_to_mpmc (src/kyron-foundation/src/containers/spmc_queue.rs:477) depth=5
- steal_fn (src/kyron-foundation/src/containers/spmc_queue.rs:712) depth=7
- steal_for_pop_fn (src/kyron-foundation/src/containers/spmc_queue.rs:733) depth=6
- test_one_producer_one_stealer_mt_thread (src/kyron-foundation/src/containers/spmc_queue.rs:780) depth=4
- test_one_producer_multi_stealer_mt_thread (src/kyron-foundation/src/containers/spmc_queue.rs:849) depth=4
- test_mt_one_push_mpmc_one_stealer (src/kyron-foundation/src/containers/spmc_queue.rs:974) depth=5
- pop_into_vec (src/kyron-foundation/src/containers/trigger_queue.rs:139) depth=5
- test_concurrent_push_pop (src/kyron-foundation/src/containers/trigger_queue.rs:322) depth=5
- test_pop_into_vec_concurrent (src/kyron-foundation/src/containers/trigger_queue.rs:369) depth=8

### Large Functions (LOC > 100)
- main (src/xtask/src/main.rs:20) loc=123
- test_broadcast_channel_mt_sender_receiver (src/kyron/src/channels/spmc_broadcast.rs:642) loc=157
- build (src/kyron/src/scheduler/execution_engine.rs:378) loc=106
- async_registration_poll_readiness (src/kyron/src/io/async_registration.rs:1144) loc=127
- main (src/kyron/examples/select.rs:21) loc=109
- parse (src/kyron-macros/src/lib.rs:72) loc=105
- main (src/kyron-macros/src/lib.rs:298) loc=177

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 2058 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 234 per-function CFGs (cc > 3)
- `statemachines.json` — 22 state machine patterns
- `metrics.json` — 2058 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 43 external dependencies
