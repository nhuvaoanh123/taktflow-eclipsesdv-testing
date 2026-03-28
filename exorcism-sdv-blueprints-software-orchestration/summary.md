# Project Analysis: sdv-blueprints-software-orchestration

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Unknown |
| Total Files | 14 |
| Total LOC | 1,119 |
| Total Functions | 20 |
| State Machines | 0 |
| Communication Patterns | 2 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 14 files, 1,119 LOC

## Architecture Overview
Build system: **Unknown**

### Communication Protocols
- **MQTT_topic**: 2 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- main (scenarios/smart_trailer/applications/smart_trailer_application/src/main.rs:160) cc=11

### High Nesting Functions (depth > 3)
- receive_trailer_weight_updates (scenarios/smart_trailer/applications/smart_trailer_application/src/main.rs:75) depth=9
- main (scenarios/smart_trailer/applications/smart_trailer_application/src/main.rs:160) depth=4
- start_trailer_weight_data_stream (scenarios/smart_trailer/digital_twin_providers/trailer_properties_provider/src/main.rs:81) depth=7
- handle_publish_action (scenarios/smart_trailer/digital_twin_providers/trailer_properties_provider/src/trailer_properties_provider_impl.rs:135) depth=6

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 20 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 8 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 20 function metrics
- `communication.json` — 2 protocol patterns
- `dependencies.json` — 0 external dependencies
