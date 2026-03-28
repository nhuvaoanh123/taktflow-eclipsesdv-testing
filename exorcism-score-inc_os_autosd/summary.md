# Project Analysis: score-inc_os_autosd

## Overview
| Item | Value |
|------|-------|
| Languages | Rust, C++, C, Python |
| Build System | Bazel, Python/pyproject |
| Total Files | 7 |
| Total LOC | 1,797 |
| Total Functions | 47 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 1 |

## Language Breakdown
- **Rust**: 1 files, 432 LOC
- **C++**: 1 files, 527 LOC
- **C**: 4 files, 782 LOC
- **Python**: 1 files, 56 LOC

## Architecture Overview
Build system: **Bazel, Python/pyproject**

## Key Findings

### High Complexity Functions (cc > 10)
- print_kvs_value (reference_integration/demos/persistency/rust_demo.rs:65) cc=12
- printHeader (reference_integration/demos/persistency/kvs_demo.cpp:52) cc=22
- printKvsValue (reference_integration/demos/persistency/kvs_demo.cpp:74) cc=56
- demonstrateBasicOperations (reference_integration/demos/persistency/kvs_demo.cpp:119) cc=17
- demonstrateSnapshots (reference_integration/demos/persistency/kvs_demo.cpp:249) cc=21
- demonstrateReset (reference_integration/demos/persistency/kvs_demo.cpp:435) cc=11
- run (reference_integration/demos/persistency/kvs_demo.cpp:474) cc=30
- spawn_agent_process (reference_integration/demos/holden/orchestrator.c:133) cc=20
- main (reference_integration/demos/holden/orchestrator.c:208) cc=41
- start_process (reference_integration/demos/holden/agent.c:69) cc=21
- main (reference_integration/demos/holden/agent.c:193) cc=28
- send_message (reference_integration/demos/holden/protocol.c:18) cc=13
- recv_message (reference_integration/demos/holden/protocol.c:37) cc=27

### High Nesting Functions (depth > 3)
- demonstrate_basic_operations (reference_integration/demos/persistency/rust_demo.rs:82) depth=4
- demonstrate_defaults (reference_integration/demos/persistency/rust_demo.rs:273) depth=6
- recv_message (reference_integration/demos/holden/protocol.c:37) depth=4

### Large Functions (LOC > 100)
- main (reference_integration/demos/holden/orchestrator.c:208) loc=133

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 47 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 26 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 47 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 1 external dependencies
