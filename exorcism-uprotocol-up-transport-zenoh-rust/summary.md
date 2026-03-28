# Project Analysis: uprotocol-up-transport-zenoh-rust

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Cargo |
| Total Files | 15 |
| Total LOC | 2,601 |
| Total Functions | 67 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 14 |

## Language Breakdown
- **Rust**: 15 files, 2,601 LOC

## Architecture Overview
Build system: **Cargo**

## Key Findings

### High Complexity Functions (cc > 10)
- uri_to_zenoh_key (src/utransport.rs:54) cc=11
- register_subscriber (src/listener_registry.rs:76) cc=15

### High Nesting Functions (depth > 3)
- register_subscriber (src/listener_registry.rs:76) depth=9
- on_receive (tests/blocking_callback.rs:28) depth=7

### Large Functions (LOC > 100)
- register_subscriber (src/listener_registry.rs:76) loc=101

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 67 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 9 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 67 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 14 external dependencies
