# Project Analysis: ankaios-ank-sdk-rust

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Cargo |
| Total Files | 36 |
| Total LOC | 14,801 |
| Total Functions | 401 |
| State Machines | 22 |
| Communication Patterns | 0 |
| External Dependencies | 16 |

## Language Breakdown
- **Rust**: 36 files, 14,801 LOC

## Architecture Overview
Build system: **Cargo**

### State Machines Detected
- `src/ankaios.rs:995` — match on `workload_states.first()` (2 states)
- `src/components/control_interface.rs:503` — match on `state_value` (3 states)
- `src/components/complete_state.rs:273` — match on `self.complete_state.desired_state.as_mut()` (2 states)
- `src/components/complete_state.rs:509` — match on `status.cpu_usage` (2 states)
- `src/components/complete_state.rs:516` — match on `status.free_memory` (2 states)
- `src/components/workload_state_mod/workload_execution_state.rs:44` — match on `exec_state.execution_state_enum` (2 states)
- `src/components/workload_state_mod/workload_execution_state.rs:97` — match on `exec_state` (8 states)
- `src/components/workload_state_mod/workload_state_enums.rs:153` — match on `state` (8 states)
- `src/components/workload_state_mod/workload_state_enums.rs:155` — match on `substate` (1 states)
- `src/components/workload_state_mod/workload_state_enums.rs:162` — match on `substate` (4 states)

## Key Findings

### High Complexity Functions (cc > 10)
- itest_set_agent_tags_ok (src/ankaios.rs:2957) cc=11
- from (src/components/response.rs:157) cc=18
- read_from_control_interface (src/components/control_interface.rs:389) cc=18
- handle_decoded_response (src/components/control_interface.rs:493) cc=13
- try_from (src/components/manifest.rs:166) cc=22
- new_from_str (src/components/workload_state_mod/workload_state_enums.rs:94) cc=11
- from_str (src/components/workload_state_mod/workload_state_enums.rs:122) cc=11
- new (src/components/workload_state_mod/workload_state_enums.rs:152) cc=34
- to_i32 (src/components/workload_state_mod/workload_state_enums.rs:221) cc=18
- from_str (src/components/workload_state_mod/workload_state_enums.rs:250) cc=19
- build (src/components/workload_mod/workload_builder.rs:295) cc=12
- new_from_dict (src/components/workload_mod/workload.rs:235) cc=18
- to_dict (src/components/workload_mod/workload.rs:479) cc=22
- add_mask (src/components/workload_mod/workload.rs:1160) cc=13
- main (examples/apps/test_workload.rs:37) cc=20

### High Nesting Functions (depth > 3)
- send_request (src/ankaios.rs:316) depth=7
- get_workload_states_for_name (src/ankaios.rs:1047) depth=4
- wait_for_workload_to_reach_state (src/ankaios.rs:1077) depth=6
- register_event (src/ankaios.rs:1213) depth=4
- itest_set_agent_tags_ok (src/ankaios.rs:2957) depth=7
- from (src/components/response.rs:157) depth=8
- read_varint_data (src/components/control_interface.rs:171) depth=4
- connect (src/components/control_interface.rs:235) depth=4
- prepare_writer (src/components/control_interface.rs:332) depth=9
- read_from_control_interface (src/components/control_interface.rs:389) depth=10
- handle_decoded_response (src/components/control_interface.rs:493) depth=5
- write_request (src/components/control_interface.rs:560) depth=4
- forward_log_entries (src/components/control_interface.rs:649) depth=4
- forward_logs_stop_response (src/components/control_interface.rs:682) depth=4
- forward_event_response (src/components/control_interface.rs:714) depth=4
- utest_control_interface_connect (src/components/control_interface.rs:855) depth=6
- utest_control_interface_send_request (src/components/control_interface.rs:963) depth=6
- utest_control_interface_agent_disconnected (src/components/control_interface.rs:1066) depth=6
- calculate_masks (src/components/manifest.rs:137) depth=4
- try_from (src/components/manifest.rs:166) depth=10

### Large Functions (LOC > 100)
- utest_control_interface_send_request (src/components/control_interface.rs:963) loc=101
- utest_control_interface_agent_disconnected (src/components/control_interface.rs:1066) loc=117
- new_from_dict (src/components/workload_mod/workload.rs:235) loc=226
- to_dict (src/components/workload_mod/workload.rs:479) loc=157
- main (examples/apps/test_workload.rs:37) loc=121
- main (examples/apps/test_files.rs:32) loc=141

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 401 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 114 per-function CFGs (cc > 3)
- `statemachines.json` — 22 state machine patterns
- `metrics.json` — 401 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 16 external dependencies
