# Project Analysis: score-bazel_cpp_toolchains

## Overview
| Item | Value |
|------|-------|
| Languages | C++, C, Python |
| Build System | Bazel |
| Total Files | 11 |
| Total LOC | 352 |
| Total Functions | 16 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **C++**: 8 files, 236 LOC
- **C**: 1 files, 16 LOC
- **Python**: 2 files, 100 LOC

## Architecture Overview
Build system: **Bazel**

## Key Findings

### High Complexity Functions (cc > 10)
- main (examples/main_pthread.cpp:21) cc=11

### High Nesting Functions (depth > 3)
_None_

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 16 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 4 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 16 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
