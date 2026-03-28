# Project Analysis: score-communication-patches

## Overview
| Item | Value |
|------|-------|
| Languages | C++, C |
| Build System | Unknown |
| Total Files | 4 |
| Total LOC | 618 |
| Total Functions | 17 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **C++**: 3 files, 615 LOC
- **C**: 1 files, 3 LOC

## Architecture Overview
Build system: **Unknown**

## Key Findings

### High Complexity Functions (cc > 10)
- open_can (can_bridge_main.cpp:29) cc=15
- decode (can_bridge_main.cpp:40) cc=52
- run_skeleton (can_bridge_main.cpp:62) cc=35
- run_proxy (can_bridge_main.cpp:95) cc=25
- main (can_bridge_main.cpp:121) cc=16
- open_can (can_bridge_main_v3.cpp:31) cc=15
- decode (can_bridge_main_v3.cpp:57) cc=32
- run_skeleton (can_bridge_main_v3.cpp:146) cc=55
- run_proxy (can_bridge_main_v3.cpp:193) cc=35
- main (can_bridge_main_v3.cpp:227) cc=16
- open_can (can_bridge_main_v2.cpp:31) cc=15
- decode (can_bridge_main_v2.cpp:57) cc=20
- run_skeleton (can_bridge_main_v2.cpp:117) cc=55
- run_proxy (can_bridge_main_v2.cpp:164) cc=35
- main (can_bridge_main_v2.cpp:198) cc=16

### High Nesting Functions (depth > 3)
- decode (can_bridge_main.cpp:40) depth=7

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 17 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 14 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 17 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
