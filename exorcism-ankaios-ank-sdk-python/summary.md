# Project Analysis: ankaios-ank-sdk-python

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Python/setuptools, Python/pyproject |
| Total Files | 55 |
| Total LOC | 11,210 |
| Total Functions | 333 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 2 |

## Language Breakdown
- **Python**: 55 files, 11,210 LOC

## Architecture Overview
Build system: **Python/setuptools, Python/pyproject**

## Key Findings

### High Complexity Functions (cc > 10)
- _read_from_control_interface (ankaios_sdk/_components/control_interface.py:275) cc=15
- _handle_response (ankaios_sdk/_components/control_interface.py:359) cc=11
- build (ankaios_sdk/_components/workload_builder.py:312) cc=12
- _from_proto (ankaios_sdk/_components/response.py:155) cc=15
- to_dict (ankaios_sdk/_components/workload.py:413) cc=13
- _from_dict (ankaios_sdk/_components/workload.py:467) cc=18

### High Nesting Functions (depth > 3)
- run_pylint (run_checks.py:77) depth=5
- extract_the_proto_files (setup.py:29) depth=7
- generate_protos (setup.py:77) depth=9
- test_read_thread_general (tests/test_control_interface.py:161) depth=5
- test_connect_disconnect (tests/test_ankaios.py:102) depth=5
- test_connection_timeout (tests/test_ankaios.py:121) depth=5
- test_send_request (tests/test_ankaios.py:227) depth=5
- test_apply_manifest (tests/test_ankaios.py:256) depth=5
- test_delete_manifest (tests/test_ankaios.py:301) depth=5
- test_apply_workload (tests/test_ankaios.py:346) depth=5
- test_delete_workload (tests/test_ankaios.py:426) depth=5
- test_update_configs (tests/test_ankaios.py:470) depth=5
- test_add_config (tests/test_ankaios.py:513) depth=5
- test_delete_all_configs (tests/test_ankaios.py:590) depth=5
- test_delete_config (tests/test_ankaios.py:633) depth=5
- test_get_state (tests/test_ankaios.py:676) depth=5
- test_set_agent_tags (tests/test_ankaios.py:719) depth=5
- test_get_agent (tests/test_ankaios.py:779) depth=5
- test_get_execution_state_for_instance_name (tests/test_ankaios.py:838) depth=5
- test_wait_for_workload_to_reach_state (tests/test_ankaios.py:919) depth=5

### Large Functions (LOC > 100)
- test_to_dict (tests/test_complete_state.py:188) loc=102

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 333 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 44 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 333 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 2 external dependencies
