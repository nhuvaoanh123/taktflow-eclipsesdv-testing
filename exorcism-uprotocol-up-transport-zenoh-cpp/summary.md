# Project Analysis: uprotocol-up-transport-zenoh-cpp

## Overview
| Item | Value |
|------|-------|
| Languages | C, C++ |
| Build System | CMake |
| Total Files | 7 |
| Total LOC | 1,200 |
| Total Functions | 67 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **C**: 2 files, 190 LOC
- **C++**: 5 files, 1,010 LOC

## Architecture Overview
Build system: **CMake**

## Key Findings

### High Complexity Functions (cc > 10)
- uprotocol (include/up-transport-zenoh-cpp/ZenohUTransport.h:25) cc=15
- UTransport (include/up-transport-zenoh-cpp/ZenohUTransport.h:44) cc=15
- <anonymous> (src/ZenohUTransport.cpp:36) cc=41

### High Nesting Functions (depth > 3)
_None_

### Large Functions (LOC > 100)
- uprotocol (include/up-transport-zenoh-cpp/ZenohUTransport.h:25) loc=103

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 67 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 14 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 67 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
