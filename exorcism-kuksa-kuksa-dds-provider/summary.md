# Project Analysis: kuksa-kuksa-dds-provider

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Unknown |
| Total Files | 14 |
| Total LOC | 1,171 |
| Total Functions | 59 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Python**: 14 files, 1,171 LOC

## Architecture Overview
Build system: **Unknown**

## Key Findings

### High Complexity Functions (cc > 10)
- main (ddsprovider.py:26) cc=11

### High Nesting Functions (depth > 3)
- on_data_available (ddsproviderlib/helper.py:55) depth=5
- register_datapoints (ddsproviderlib/helper.py:81) depth=5
- _run (ddsproviderlib/helper.py:154) depth=5
- _on_broker_connectivity_change (ddsproviderlib/helper.py:190) depth=7
- transform (ddsproviderlib/vss2ddsmapper.py:49) depth=5
- _createdict (ddsproviderlib/vss2ddsmapper.py:61) depth=5
- register (ddsproviderlib/databroker.py:43) depth=5
- test_ddsprovider_start (tests/integration/test_ddsprovider_int.py:46) depth=7

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 59 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 8 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 59 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
