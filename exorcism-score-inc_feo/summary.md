# Project Analysis: score-inc_feo

## Overview
| Item | Value |
|------|-------|
| Languages | C, Rust, C++ |
| Build System | Cargo, Bazel |
| Total Files | 121 |
| Total LOC | 14,329 |
| Total Functions | 664 |
| State Machines | 2 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **C**: 6 files, 181 LOC
- **Rust**: 109 files, 13,966 LOC
- **C++**: 6 files, 182 LOC

## Architecture Overview
Build system: **Cargo, Bazel**

### State Machines Detected
- `feo-com/src/linux_shm/shared_memory.rs:94` — match on `new_state` (2 states)
- `feo-com/src/linux_shm/shared_memory.rs:117` — match on `new_state` (2 states)

## Key Findings

### High Complexity Functions (cc > 10)
- system_time_math (feo-time/src/tests.rs:145) cc=11
- since_epoch (feo-time/src/tests.rs:201) cc=11
- thread_main (feo-tracing/src/subscriber.rs:75) cc=11
- parse (feo-cpp-macros/src/lib.rs:43) cc=12
- decode (feo-logger/src/record.rs:135) cc=14
- color (feo-logger/src/fmt.rs:115) cc=15
- find_composites (examples/rust/cycle-benchmark/src/composites.rs:89) cc=12
- main (examples/rust/mini-adas/src/bin/adas_deserializer.rs:11) cc=12
- encode (feo/src/signalling/common/socket/mod.rs:153) cc=18
- try_decode (feo/src/signalling/common/socket/mod.rs:213) cc=22
- try_from (feo/src/signalling/common/socket/mod.rs:312) cc=29
- receive (feo/src/signalling/common/socket/client.rs:107) cc=13
- connect_senders (feo/src/signalling/common/mpsc/endpoint.rs:116) cc=11
- thread_main (feo/src/signalling/relayed/connectors/relays.rs:210) cc=15
- on_packet (feo-tracer/src/perfetto.rs:85) cc=15
- connection (feo-tracer/src/io.rs:42) cc=16

### High Nesting Functions (depth > 3)
- instant_monotonic (feo-time/src/tests.rs:26) depth=5
- instant_monotonic_concurrent (feo-time/src/tests.rs:39) depth=5
- big_math (feo-time/src/tests.rs:229) depth=4
- now (feo-time/src/lib.rs:146) depth=5
- now (feo-time/src/lib.rs:353) depth=5
- scaled (feo-time/src/lib.rs:523) depth=5
- init_topic_primary (feo-com/src/interface.rs:331) depth=6
- init_topic_secondary (feo-com/src/interface.rs:356) depth=6
- lock_read (feo-com/src/linux_shm/shared_memory.rs:79) depth=4
- unlock_read (feo-com/src/linux_shm/shared_memory.rs:102) depth=4
- service_main (feo-com/src/linux_shm/mod.rs:114) depth=7
- serve_connection (feo-com/src/linux_shm/mod.rs:139) depth=5
- ipc_node (feo-com/src/iox2/mod.rs:247) depth=7
- connection (logd/src/input.rs:89) depth=5
- trunc_len (feo-tracing/src/protocol.rs:133) depth=4
- thread_main (feo-tracing/src/subscriber.rs:75) depth=5
- main (feo-tracing/examples/hello_tracing.rs:14) depth=4
- parse (feo-cpp-macros/src/lib.rs:43) depth=7
- write (feo-logger/src/logd.rs:22) depth=4
- decode (feo-logger/src/record.rs:135) depth=4

### Large Functions (LOC > 100)
- main (feo-tracer/src/main.rs:54) loc=102
- on_packet (feo-tracer/src/perfetto.rs:85) loc=143

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 664 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 111 per-function CFGs (cc > 3)
- `statemachines.json` — 2 state machine patterns
- `metrics.json` — 664 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
