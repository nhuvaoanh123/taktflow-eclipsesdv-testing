# Project Analysis: leda-leda-utils

## Overview
| Item | Value |
|------|-------|
| Languages | Python, Rust |
| Build System | Unknown |
| Total Files | 16 |
| Total LOC | 2,264 |
| Total Functions | 94 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Python**: 1 files, 213 LOC
- **Rust**: 15 files, 2,051 LOC

## Architecture Overview
Build system: **Unknown**

## Key Findings

### High Complexity Functions (cc > 10)
- update_containers (src/python/kantocm-zeroconf/kantocm_zeroconf.py:65) cc=16
- process_request (src/rust/kanto-tui/src/io.rs:19) cc=13

### High Nesting Functions (depth > 3)
- update_containers (src/python/kantocm-zeroconf/kantocm_zeroconf.py:65) depth=13
- update_service (src/python/kantocm-zeroconf/kantocm_zeroconf.py:119) depth=5
- handle_existing (src/rust/kanto-auto-deployer/src/main.rs:208) depth=5
- deploy (src/rust/kanto-auto-deployer/src/main.rs:250) depth=5
- redeploy_on_change (src/rust/kanto-auto-deployer/src/main.rs:311) depth=6
- main (src/rust/kanto-auto-deployer/src/main.rs:327) depth=6
- mqtt_main (src/rust/kanto-auto-deployer/src/mqtt_listener.rs:117) depth=8
- try_parse_manifest (src/rust/kanto-auto-deployer/src/manifest_parser.rs:121) depth=5
- publish_blueprint (src/rust/blueprint-selector/src/main.rs:127) depth=4
- copy_dir_recursive (src/rust/blueprint-selector/src/blueprint_fetchers.rs:47) depth=6
- process_request (src/rust/kanto-tui/src/io.rs:19) depth=4
- async_io_thread (src/rust/kanto-tui/src/io.rs:80) depth=5
- get_current_container (src/rust/kanto-tui/src/ui/containers_table_view.rs:116) depth=5
- run (src/rust/kanto-tui/src/ui/mod.rs:24) depth=6

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 94 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 24 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 94 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
