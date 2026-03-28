# Project Analysis: kuksa-kuksa-common

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Unknown |
| Total Files | 6 |
| Total LOC | 301 |
| Total Functions | 9 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Python**: 6 files, 301 LOC

## Architecture Overview
Build system: **Unknown**

## Key Findings

### High Complexity Functions (cc > 10)
_None_

### High Nesting Functions (depth > 3)
- collect_license_id_from_expression (sbom-tools/src/kuksa_sbom_utils/collectlicensefiles.py:66) depth=5
- collect (sbom-tools/src/kuksa_sbom_utils/collectlicensefiles.py:84) depth=5
- main (sbom-tools/src/kuksa_sbom_utils/collectlicensefiles.py:130) depth=7

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 9 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 3 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 9 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
