# Project Analysis: eclipse-leda-distro

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Unknown |
| Total Files | 4 |
| Total LOC | 573 |
| Total Functions | 26 |
| State Machines | 0 |
| Communication Patterns | 2 |
| External Dependencies | 0 |

## Language Breakdown
- **Python**: 4 files, 573 LOC

## Architecture Overview
Build system: **Unknown**

### Communication Protocols
- **MQTT_topic**: 2 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
_None_

### High Nesting Functions (depth > 3)
- parseContainerState (resources/docker-snapshot/dockerfiles/container-metrics/app.py:102) depth=7
- parseMetrics (resources/docker-snapshot/dockerfiles/container-metrics/app.py:142) depth=7
- on_message (resources/docker-snapshot/dockerfiles/container-metrics/app.py:180) depth=5
- convert_directory (resources/oss-compliance/dependencytrack/sbom-converter.py:89) depth=4
- convert_directory (.github/workflow-scripts/sbom-converter.py:89) depth=4

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 26 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 4 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 26 function metrics
- `communication.json` — 2 protocol patterns
- `dependencies.json` — 0 external dependencies
