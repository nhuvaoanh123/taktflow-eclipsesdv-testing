# Project Analysis: sdv-blueprints-insurance

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Unknown |
| Total Files | 13 |
| Total LOC | 1,821 |
| Total Functions | 61 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 10 |

## Language Breakdown
- **Python**: 13 files, 1,821 LOC

## Architecture Overview
Build system: **Unknown**

## Key Findings

### High Complexity Functions (cc > 10)
- check_condition (edge/applications/insurance_event_detector/event_definitions.py:84) cc=19

### High Nesting Functions (depth > 3)
- process_sample_file (edge/applications/insurance_event_detector/main.py:99) depth=7
- process_signal_data (edge/applications/insurance_event_detector/event_definitions.py:4) depth=5
- get_signal_value (edge/applications/insurance_event_detector/event_definitions.py:31) depth=5
- check_condition (edge/applications/insurance_event_detector/event_definitions.py:84) depth=7
- collect_callback_data (edge/applications/insurance_event_detector/event_definitions.py:125) depth=5
- generate_sample_data (edge/applications/insurance_event_detector/dummy_data_gen.py:47) depth=5
- risk_event_detector (edge/applications/insurance_event_detector/event_detector.py:12) depth=9
- findSignalByID (edge/proto_build/consumer.py:48) depth=5
- registerSignals (edge/digital_twin_providers/vehicle_properties_provider/main.py:50) depth=7
- sendData (edge/digital_twin_providers/vehicle_properties_provider/main.py:98) depth=5

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 61 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 5 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 61 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 10 external dependencies
