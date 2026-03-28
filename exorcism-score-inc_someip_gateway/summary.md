# Project Analysis: score-inc_someip_gateway

## Overview
| Item | Value |
|------|-------|
| Languages | C, C++, Python, Rust |
| Build System | Bazel, Python/pyproject |
| Total Files | 24 |
| Total LOC | 2,947 |
| Total Functions | 84 |
| State Machines | 3 |
| Communication Patterns | 0 |
| External Dependencies | 7 |

## Language Breakdown
- **C**: 5 files, 384 LOC
- **C++**: 10 files, 1,880 LOC
- **Python**: 5 files, 354 LOC
- **Rust**: 4 files, 329 LOC

## Architecture Overview
Build system: **Bazel, Python/pyproject**

### State Machines Detected
- `examples/car_window_sim/src/car_window.rs:46` — match on `window_state` (5 states)
- `examples/car_window_sim/src/car_window.rs:65` — match on `window_state` (5 states)
- `examples/car_window_sim/src/car_window.rs:87` — match on `window_state` (5 states)

## Key Findings

### High Complexity Functions (cc > 10)
- main (src/someipd/main.cpp:64) cc=22
- gatewayd (src/gatewayd/remote_service_instance.h:25) cc=13
- RemoteServiceInstance (src/gatewayd/remote_service_instance.h:27) cc=13
- gatewayd (src/gatewayd/local_service_instance.h:24) cc=15
- LocalServiceInstance (src/gatewayd/local_service_instance.h:26) cc=15
- main (src/gatewayd/main.cpp:42) cc=23
- <anonymous> (src/gatewayd/local_service_instance.cpp:31) cc=20
- <anonymous> (src/gatewayd/local_service_instance.cpp:134) cc=15
- <anonymous> (src/gatewayd/remote_service_instance.cpp:31) cc=12
- <anonymous> (src/gatewayd/remote_service_instance.cpp:90) cc=17
- main (examples/car_window_sim/src/car_window_controller.rs:23) cc=14
- WindowCommand (examples/car_window_sim/src/car_window_types.h:28) cc=15
- update_state_machine (examples/car_window_sim/src/car_window.rs:26) cc=34
- Initialize (tests/performance_benchmarks/ipc_benchmarks.cpp:60) cc=50
- SendEchoRequestSyncWithPolling (tests/performance_benchmarks/ipc_benchmarks.cpp:232) cc=16
- Percentile (tests/performance_benchmarks/ipc_benchmarks.cpp:531) cc=12
- main (tests/performance_benchmarks/ipc_benchmarks.cpp:635) cc=16
- ProcessSingleEchoRequestTiny (tests/performance_benchmarks/echo_server.cpp:62) cc=13
- ProcessSingleEchoRequestSmall (tests/performance_benchmarks/echo_server.cpp:95) cc=13
- ProcessSingleEchoRequestMedium (tests/performance_benchmarks/echo_server.cpp:128) cc=13

### High Nesting Functions (depth > 3)
- main (examples/car_window_sim/src/car_window_controller.rs:23) depth=7
- update_state_machine (examples/car_window_sim/src/car_window.rs:26) depth=7
- main (examples/car_window_sim/src/car_window.rs:121) depth=7
- run (tests/integration/client.py:60) depth=5
- main (tests/performance_benchmarks/echo_server.cpp:313) depth=4

### Large Functions (LOC > 100)
- main (src/someipd/main.cpp:64) loc=109
- main (tests/performance_benchmarks/echo_server.cpp:313) loc=129
- echo_service (tests/performance_benchmarks/echo_service.h:23) loc=132
- PayloadSize (tests/performance_benchmarks/echo_service.h:25) loc=110

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 84 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 40 per-function CFGs (cc > 3)
- `statemachines.json` — 3 state machine patterns
- `metrics.json` — 84 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 7 external dependencies
