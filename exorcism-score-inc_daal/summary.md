# Project Analysis: score-inc_daal

## Overview
| Item | Value |
|------|-------|
| Languages | C++, C, Python |
| Build System | Bazel, Python/pyproject |
| Total Files | 145 |
| Total LOC | 11,255 |
| Total Functions | 649 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 1 |

## Language Breakdown
- **C++**: 141 files, 11,085 LOC
- **C**: 3 files, 116 LOC
- **Python**: 1 files, 54 LOC

## Architecture Overview
Build system: **Bazel, Python/pyproject**

## Key Findings

### High Complexity Functions (cc > 10)
- <anonymous> (src/daal/af/os/details/posix_helper_impl.cpp:33) cc=19
- <anonymous> (src/daal/af/runtime_statistics/runtime_statistics.cpp:22) cc=12
- <anonymous> (src/daal/af/runtime_statistics/details/console_backend.cpp:23) cc=62
- <anonymous> (src/daal/af/runtime_statistics/details/file_backend.cpp:27) cc=66
- <anonymous> (src/daal/af/checkpoint/details/checkpoint_container.cpp:29) cc=15
- <anonymous> (src/daal/af/app_handler/details/fork_join_module_handler.cpp:52) cc=14
- <anonymous> (src/daal/af/trigger/details/trigger_activation_impl.cpp:35) cc=13
- <anonymous> (src/daal/af/exe/details/executor_impl.cpp:93) cc=18
- <anonymous> (src/daal/af/env/details/simple_signal_handler.cpp:28) cc=21
- <anonymous> (src/daal/af/env/details/simple_signal_handler.cpp:53) cc=15
- <anonymous> (examples/iohandler-score-mw-com/adas-vehicle-control/io/impl/steering_wheel_client_score.cpp:29) cc=15
- <anonymous> (examples/iohandler-score-mw-com/steering-wheel/io/impl/steering_wheel_server_score.cpp:32) cc=11

### High Nesting Functions (depth > 3)
- <anonymous> (src/daal/af/os/details/posix_helper_impl.cpp:33) depth=4

### Large Functions (LOC > 100)
- <anonymous> (src/daal/af/exe/details/executor_impl.cpp:93) loc=101

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 649 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 52 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 649 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 1 external dependencies
