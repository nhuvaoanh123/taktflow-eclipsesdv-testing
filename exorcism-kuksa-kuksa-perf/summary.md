# Project Analysis: kuksa-kuksa-perf

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Cargo |
| Total Files | 24 |
| Total LOC | 4,526 |
| Total Functions | 54 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 17 |

## Language Breakdown
- **Rust**: 24 files, 4,526 LOC

## Architecture Overview
Build system: **Cargo**

## Key Findings

### High Complexity Functions (cc > 10)
- main (src/main.rs:113) cc=29
- perform_measurement (src/measure.rs:215) cc=38
- measurement_loop (src/measure.rs:405) cc=16
- write_global_output (src/utils.rs:132) cc=16
- write_output (src/utils.rs:220) cc=14
- from (src/triggering_ends/kuksa_val_v2/conversions.rs:18) cc=22
- open_provider_stream (src/triggering_ends/kuksa_val_v2/triggering_end.rs:85) cc=14
- trigger (src/triggering_ends/kuksa_val_v2/triggering_end.rs:133) cc=23
- validate_signals_metadata (src/triggering_ends/kuksa_val_v2/triggering_end.rs:227) cc=16
- n_to_value (src/triggering_ends/kuksa_val_v2/triggering_end.rs:313) cc=239
- n_to_value (src/triggering_ends/sdv_databroker_v1/triggering_end.rs:182) cc=175
- from (src/triggering_ends/kuksa_val_v1/conversions.rs:18) cc=21
- n_to_value (src/triggering_ends/kuksa_val_v1/triggering_end.rs:214) cc=428
- handle_kuksa_val_v2 (src/receiving_ends/kuksa_val_v2/receiving_end.rs:90) cc=28

### High Nesting Functions (depth > 3)
- check_if_duplicate_paths (src/main.rs:98) depth=5
- main (src/main.rs:113) depth=8
- create_receiving_end (src/measure.rs:113) depth=4
- create_triggering_end (src/measure.rs:189) depth=4
- perform_measurement (src/measure.rs:215) depth=6
- measurement_loop (src/measure.rs:405) depth=8
- setup_shutdown_handler (src/shutdown.rs:47) depth=4
- from (src/triggering_ends/kuksa_val_v2/conversions.rs:18) depth=4
- open_provider_stream (src/triggering_ends/kuksa_val_v2/triggering_end.rs:85) depth=11
- trigger (src/triggering_ends/kuksa_val_v2/triggering_end.rs:133) depth=10
- validate_signals_metadata (src/triggering_ends/kuksa_val_v2/triggering_end.rs:227) depth=7
- n_to_value (src/triggering_ends/kuksa_val_v2/triggering_end.rs:313) depth=9
- run (src/triggering_ends/sdv_databroker_v1/triggering_end.rs:57) depth=7
- n_to_value (src/triggering_ends/sdv_databroker_v1/triggering_end.rs:182) depth=9
- from (src/triggering_ends/kuksa_val_v1/conversions.rs:18) depth=4
- run (src/triggering_ends/kuksa_val_v1/triggering_end.rs:55) depth=7
- trigger (src/triggering_ends/kuksa_val_v1/triggering_end.rs:92) depth=8
- validate_signals_metadata (src/triggering_ends/kuksa_val_v1/triggering_end.rs:147) depth=4
- n_to_value (src/triggering_ends/kuksa_val_v1/triggering_end.rs:214) depth=11
- handle_kuksa_val_v2 (src/receiving_ends/kuksa_val_v2/receiving_end.rs:90) depth=17

### Large Functions (LOC > 100)
- perform_measurement (src/measure.rs:215) loc=189
- measurement_loop (src/measure.rs:405) loc=105
- n_to_value (src/triggering_ends/kuksa_val_v2/triggering_end.rs:313) loc=602
- n_to_value (src/triggering_ends/sdv_databroker_v1/triggering_end.rs:182) loc=484
- n_to_value (src/triggering_ends/kuksa_val_v1/triggering_end.rs:214) loc=646
- handle_kuksa_val_v2 (src/receiving_ends/kuksa_val_v2/receiving_end.rs:90) loc=148

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 54 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 30 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 54 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 17 external dependencies
