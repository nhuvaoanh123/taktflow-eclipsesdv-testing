# Project Analysis: score-toolchains_gcc

## Overview
| Item | Value |
|------|-------|
| Languages | C++ |
| Build System | Bazel |
| Total Files | 2 |
| Total LOC | 55 |
| Total Functions | 3 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **C++**: 2 files, 55 LOC

## Architecture Overview
Build system: **Bazel**

## Key Findings

### High Complexity Functions (cc > 10)
- main (test/main_pthread.cpp:22) cc=11

### High Nesting Functions (depth > 3)
_None_

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 3 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 1 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 3 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
