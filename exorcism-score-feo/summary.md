# Project Analysis: score-feo

## Overview
| Item | Value |
|------|-------|
| Languages | C, Rust, C++, Python |
| Build System | Cargo, Bazel, Python/pyproject |
| Total Files | 112 |
| Total LOC | 16,085 |
| Total Functions | 723 |
| State Machines | 2 |
| Communication Patterns | 0 |
| External Dependencies | 1 |

## Language Breakdown
- **C**: 5 files, 289 LOC
- **Rust**: 101 files, 15,571 LOC
- **C++**: 5 files, 169 LOC
- **Python**: 1 files, 56 LOC

## Architecture Overview
Build system: **Cargo, Bazel, Python/pyproject**

### State Machines Detected
- `src/feo-com/src/linux_shm/shared_memory.rs:93` — match on `new_state` (2 states)
- `src/feo-com/src/linux_shm/shared_memory.rs:109` — match on `new_state` (2 states)

## Key Findings

### High Complexity Functions (cc > 10)
- system_time_math (src/feo-time/src/tests.rs:145) cc=11
- since_epoch (src/feo-time/src/tests.rs:197) cc=11
- fmt (src/feo-tracing/src/subscriber.rs:73) cc=42
- fmt (src/feo-tracing/src/subscriber.rs:134) cc=19
- thread_main (src/feo-tracing/src/subscriber.rs:191) cc=11
- parse (src/feo-cpp-macros/src/lib.rs:47) cc=12
- fmt (src/feo/src/error.rs:59) cc=12
- shutdown_gracefully (src/feo/src/scheduler.rs:271) cc=13
- fmt (src/feo/src/signalling/common/signals.rs:65) cc=13
- encode (src/feo/src/signalling/common/socket/mod.rs:164) cc=21
- try_decode (src/feo/src/signalling/common/socket/mod.rs:233) cc=25
- try_from (src/feo/src/signalling/common/socket/mod.rs:365) cc=35
- receive (src/feo/src/signalling/common/socket/client.rs:111) cc=13
- receive (src/feo/src/signalling/common/socket/server.rs:61) cc=13
- connect_senders (src/feo/src/signalling/common/mpsc/endpoint.rs:118) cc=11
- thread_main (src/feo/src/signalling/relayed/connectors/relays.rs:65) cc=12
- thread_main (src/feo/src/signalling/relayed/connectors/relays.rs:198) cc=26
- run (src/feo/src/worker/mod.rs:69) cc=13
- handle_activity_signal (src/feo/src/worker/mod.rs:119) cc=15
- on_packet (src/feo-tracer/src/perfetto.rs:86) cc=15

### High Nesting Functions (depth > 3)
- instant_monotonic (src/feo-time/src/tests.rs:35) depth=5
- instant_monotonic_concurrent (src/feo-time/src/tests.rs:48) depth=5
- big_math (src/feo-time/src/tests.rs:223) depth=4
- now (src/feo-time/src/lib.rs:275) depth=5
- now (src/feo-time/src/lib.rs:482) depth=5
- scaled (src/feo-time/src/lib.rs:652) depth=5
- init_topic_primary (src/feo-com/src/interface.rs:458) depth=6
- init_topic_secondary (src/feo-com/src/interface.rs:486) depth=6
- lock_read (src/feo-com/src/linux_shm/shared_memory.rs:85) depth=4
- unlock_read (src/feo-com/src/linux_shm/shared_memory.rs:101) depth=4
- service_main (src/feo-com/src/linux_shm/mod.rs:120) depth=7
- serve_connection (src/feo-com/src/linux_shm/mod.rs:145) depth=5
- ipc_node (src/feo-com/src/iox2/mod.rs:237) depth=7
- trunc_len (src/feo-tracing/src/protocol.rs:139) depth=4
- thread_main (src/feo-tracing/src/subscriber.rs:191) depth=5
- main (src/feo-tracing/examples/hello_tracing.rs:23) depth=4
- parse (src/feo-cpp-macros/src/lib.rs:47) depth=7
- run (src/feo/src/scheduler.rs:110) depth=6
- step_ready_activities (src/feo/src/scheduler.rs:213) depth=4
- shutdown_gracefully (src/feo/src/scheduler.rs:271) depth=8

### Large Functions (LOC > 100)
- run (src/feo/src/scheduler.rs:110) loc=101
- thread_main (src/feo/src/signalling/relayed/connectors/relays.rs:198) loc=125
- main (src/feo-tracer/src/main.rs:63) loc=105
- on_packet (src/feo-tracer/src/perfetto.rs:86) loc=142
- launch_primary (tests/rust/feo_tests/test_agent/src/primary.rs:32) loc=128

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 723 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 111 per-function CFGs (cc > 3)
- `statemachines.json` — 2 state machine patterns
- `metrics.json` — 723 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 1 external dependencies
