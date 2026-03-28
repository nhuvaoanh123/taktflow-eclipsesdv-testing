# Project Analysis: kuksa-kuksa-gps-provider

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Unknown |
| Total Files | 1 |
| Total LOC | 328 |
| Total Functions | 11 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 2 |

## Language Breakdown
- **Python**: 1 files, 328 LOC

## Architecture Overview
Build system: **Unknown**

## Key Findings

### High Complexity Functions (cc > 10)
- parse_env_log (gpsd_feeder.py:82) cc=11

### High Nesting Functions (depth > 3)
- parse_env_log (gpsd_feeder.py:82) depth=9
- parse_level (gpsd_feeder.py:83) depth=5
- setData (gpsd_feeder.py:147) depth=9
- run (gpsd_feeder.py:190) depth=7

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 11 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 5 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 11 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 2 external dependencies
