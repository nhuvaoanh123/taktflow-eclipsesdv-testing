# Project Analysis: sdv-blueprints-service-to-signal

## Overview
| Item | Value |
|------|-------|
| Languages | Rust, C |
| Build System | Unknown |
| Total Files | 18 |
| Total LOC | 1,347 |
| Total Functions | 45 |
| State Machines | 2 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 16 files, 944 LOC
- **C**: 2 files, 403 LOC

## Architecture Overview
Build system: **Unknown**

### State Machines Detected
- `components/horn-service-kuksa/src/request_processor.rs:60` — match on `req.mode.enum_value()` (2 states)
- `components/horn-service-kuksa/src/request_processor.rs:62` — match on `mode` (4 states)

## Key Findings

### High Complexity Functions (cc > 10)
- sample_handler (components/actuator-provider/src/main.c:138) cc=17
- event_handler (components/actuator-provider/src/main.c:193) cc=20
- app_main (components/actuator-provider/src/main.c:260) cc=15

### High Nesting Functions (depth > 3)
- sample_handler (components/actuator-provider/src/main.c:138) depth=5
- main (components/software-horn/src/main.rs:38) depth=6
- send_to_databroker (components/horn-service-kuksa/src/connections.rs:23) depth=4
- horn_request_apply (components/horn-service-kuksa/src/request_processor.rs:56) depth=5

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 45 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 14 per-function CFGs (cc > 3)
- `statemachines.json` — 2 state machine patterns
- `metrics.json` — 45 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
