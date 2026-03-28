# Project Analysis: eclipse-kuksa-python-sdk

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Unknown |
| Total Files | 18 |
| Total LOC | 6,841 |
| Total Functions | 297 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Python**: 18 files, 6,841 LOC

## Architecture Overview
Build system: **Unknown**

## Key Findings

### High Complexity Functions (cc > 10)
- connect (kuksa-client/kuksa_client/__main__.py:565) cc=18
- setValue (kuksa-client/kuksa_client/cli_backend/ws.py:185) cc=12
- _grpcHandler (kuksa-client/kuksa_client/cli_backend/grpc.py:242) cc=17
- set (kuksa-client/kuksa_client/grpc/aio.py:412) cc=11
- to_message (kuksa-client/kuksa_client/grpc/__init__.py:200) cc=19
- _raise_if_invalid (kuksa-client/kuksa_client/grpc/__init__.py:914) cc=13
- set (kuksa-client/kuksa_client/grpc/__init__.py:1295) cc=11

### High Nesting Functions (depth > 3)
- run (kuksa-client/setup.py:40) depth=5
- run (kuksa-client/setup.py:85) depth=5
- ensure_proto_packages (kuksa-client/setup.py:140) depth=9
- main (kuksa-client/prototagandcopy.py:21) depth=7
- test_get_no_entries_requested (kuksa-client/tests/test_grpc.py:947) depth=5
- test_get_nonexistent_entries (kuksa-client/tests/test_grpc.py:981) depth=5
- test_set_some_updates_v2 (kuksa-client/tests/test_grpc.py:1233) depth=5
- test_set_some_updates_v2_target (kuksa-client/tests/test_grpc.py:1312) depth=5
- test_set_no_updates_provided (kuksa-client/tests/test_grpc.py:1357) depth=5
- test_set_nonexistent_entries_v1 (kuksa-client/tests/test_grpc.py:1398) depth=5
- test_set_nonexistent_entries_v2 (kuksa-client/tests/test_grpc.py:1444) depth=5
- test_authorize_unsuccessful (kuksa-client/tests/test_grpc.py:1530) depth=5
- test_subscribe_some_entries_v1 (kuksa-client/tests/test_grpc.py:1541) depth=5
- test_subscribe_some_entries_v2 (kuksa-client/tests/test_grpc.py:1733) depth=5
- test_subscribe_some_entries_v2_target (kuksa-client/tests/test_grpc.py:1837) depth=7
- test_subscribe_no_entries_requested (kuksa-client/tests/test_grpc.py:1863) depth=7
- test_subscribe_nonexistent_entries (kuksa-client/tests/test_grpc.py:1887) depth=7
- test_get_server_info_unavailable (kuksa-client/tests/test_grpc.py:1923) depth=5
- test_add_subscriber_v1 (kuksa-client/tests/test_grpc.py:1936) depth=5
- test_remove_subscriber_v1 (kuksa-client/tests/test_grpc.py:2021) depth=5

### Large Functions (LOC > 100)
- test_get_some_entries (kuksa-client/tests/test_grpc.py:744) loc=201
- test_set_some_updates_v1 (kuksa-client/tests/test_grpc.py:997) loc=234
- test_subscribe_some_entries_v1 (kuksa-client/tests/test_grpc.py:1541) loc=190
- test_subscribe_some_entries_v2 (kuksa-client/tests/test_grpc.py:1733) loc=102

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 297 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 72 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 297 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
