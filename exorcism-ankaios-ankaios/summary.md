# Project Analysis: ankaios-ankaios

## Overview
| Item | Value |
|------|-------|
| Languages | Rust, Python, JavaScript, C++ |
| Build System | Cargo |
| Total Files | 187 |
| Total LOC | 70,631 |
| Total Functions | 2363 |
| State Machines | 30 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 175 files, 68,335 LOC
- **Python**: 10 files, 1,846 LOC
- **JavaScript**: 1 files, 234 LOC
- **C++**: 1 files, 216 LOC

## Architecture Overview
Build system: **Cargo**

### State Machines Detected
- `agent/src/control_interface/authorizer.rs:214` — match on `state_rule.operation` (4 states)
- `agent/src/workload/workload_control_loop.rs:294` — match on `Self::handle_mount_point_creation(&control_loop_state).await` (2 states)
- `agent/src/workload/workload_control_loop.rs:308` — match on `control_loop_state
            .runtime
            .create_workload(
                control_loop_state.workload_named.clone(),
                control_loop_state.workload_id.clone(),
                control_loop_state
                    .control_interface_path
                    .as_ref()
                    .map(|path| path.to_path_buf()),
                control_loop_state
                    .state_checker_workload_state_sender
                    .clone(),
                host_file_path_mount_point_mappings,
            )
            .await` (2 states)
- `agent/src/workload/workload_control_loop.rs:390` — match on `WorkloadFilesCreator::create_files(
                &workload_files_base_path,
                &control_loop_state.workload_named.workload.files.files,
            )
            .await` (2 states)
- `agent/src/runtime_connectors/podman_cli.rs:62` — match on `value.state.to_lowercase().as_str()` (11 states)
- `agent/src/runtime_connectors/podman_cli.rs:86` — match on `value.state.to_lowercase().as_str()` (11 states)
- `agent/src/runtime_connectors/containerd/containerd_runtime.rs:74` — match on `NerdctlCli::list_states_by_id(workload_id.id.as_str()).await` (2 states)
- `agent/src/runtime_connectors/containerd/containerd_runtime.rs:109` — match on `NerdctlCli::list_states_by_id(workload_id).await` (3 states)
- `agent/src/runtime_connectors/containerd/nerdctl_cli.rs:52` — match on `value.state.status.to_lowercase().as_str()` (9 states)
- `agent/src/runtime_connectors/podman/podman_runtime.rs:73` — match on `PodmanCli::list_states_by_id(workload_id.id.as_str()).await` (2 states)

## Key Findings

### High Complexity Functions (cc > 10)
- process_log_entries_response (common/src/message_size.rs:24) cc=13
- generate_paths_from_yaml_node (common/src/state_manipulation/object.rs:159) cc=15
- expand_wildcards (common/src/state_manipulation/object.rs:337) cc=14
- execute_from_server_command (agent/src/agent_manager.rs:103) cc=11
- resume_and_remove_from_added_workloads (agent/src/runtime_manager.rs:200) cc=19
- from_file (agent/src/agent_config.rs:81) cc=17
- eq (agent/src/workload.rs:79) cc=11
- matches (agent/src/control_interface/authorizer/rules.rs:63) cc=15
- utest_max_retry_time (agent/src/workload/retry_manager.rs:316) cc=12
- create_workload_non_blocking (agent/src/runtime_connectors/runtime_facade.rs:167) cc=12
- create_workload (agent/src/runtime_connectors/runtime_connector.rs:382) cc=14
- from (agent/src/runtime_connectors/podman_cli.rs:61) cc=13
- from (agent/src/runtime_connectors/podman_cli.rs:85) cc=15
- from (agent/src/runtime_connectors/containerd/nerdctl_cli.rs:51) cc=13
- next_lines (agent/src/runtime_connectors/log_fetching/generic_log_fetcher.rs:58) cc=11
- next_lines (agent/src/runtime_connectors/log_fetching/generic_log_fetcher.rs:111) cc=18
- next_lines (agent/src/runtime_connectors/log_fetching/log_fetcher.rs:137) cc=12
- from_file (ank/src/ank_config.rs:192) cc=17
- output_update_fn (ank/src/log.rs:123) cc=15
- main (ank/src/main.rs:34) cc=46

### High Nesting Functions (depth > 3)
- process_log_entries_response (common/src/message_size.rs:24) depth=7
- truncate_log_entry (common/src/message_size.rs:70) depth=4
- check_version_compatibility (common/src/helpers.rs:23) depth=5
- handle_config (common/src/config.rs:62) depth=6
- generate_paths_from_yaml_node (common/src/state_manipulation/object.rs:159) depth=6
- get (common/src/state_manipulation/object.rs:293) depth=6
- get_mut (common/src/state_manipulation/object.rs:313) depth=4
- expand_wildcards (common/src/state_manipulation/object.rs:337) depth=9
- execute_from_server_command (agent/src/agent_manager.rs:103) depth=6
- forward_response (agent/src/runtime_manager.rs:185) depth=5
- resume_and_remove_from_added_workloads (agent/src/runtime_manager.rs:200) depth=12
- transform_into_workload_operations (agent/src/runtime_manager.rs:412) depth=4
- execute_workload_operations (agent/src/runtime_manager.rs:479) depth=4
- delete_workload (agent/src/runtime_manager.rs:547) depth=5
- update_workload (agent/src/runtime_manager.rs:578) depth=5
- validate_runtimes (agent/src/main.rs:87) depth=6
- main (agent/src/main.rs:131) depth=4
- consume_futures_and_forward_logs_until_stop (agent/src/workload_log_facade.rs:124) depth=5
- get_log_responses (agent/src/workload_log_facade.rs:199) depth=5
- start_checker (agent/src/generic_polling_state_checker.rs:40) depth=8

### Large Functions (LOC > 100)
- execute_from_server_command (agent/src/agent_manager.rs:103) loc=117
- resume_and_remove_from_added_workloads (agent/src/runtime_manager.rs:200) loc=184
- utest_forward_complete_state_fails (agent/src/runtime_manager.rs:2306) loc=123
- main (agent/src/main.rs:131) loc=132
- utest_workload_log_facade_spawn_log_collection (agent/src/workload_log_facade.rs:244) loc=146
- run (agent/src/workload/workload_control_loop.rs:45) loc=127
- utest_workload_obj_run_update_success (agent/src/workload/workload_control_loop.rs:804) loc=114
- utest_workload_obj_run_update_after_update_delete_only (agent/src/workload/workload_control_loop.rs:1009) loc=118
- utest_workload_obj_run_update_broken_allowed (agent/src/workload/workload_control_loop.rs:1130) loc=106
- utest_restart_workload (agent/src/workload/workload_control_loop.rs:1860) loc=103
- utest_restart_workload_with_bundle_reuse (agent/src/workload/workload_control_loop.rs:1968) loc=101
- utest_workload_obj_update_create_failed_send_retry (agent/src/workload/workload_control_loop.rs:2484) loc=103
- create_workload (agent/src/runtime_connectors/podman_kube/podman_kube_runtime.rs:139) loc=110
- main (ank/src/main.rs:34) loc=230
- utest_apply_manifests_workloads_updated_ok (ank/src/cli_commands/apply_manifests.rs:883) loc=118
- utest_apply_manifest_invalid_names (ank/src/cli_commands/apply_manifests.rs:1113) loc=106
- utest_get_events_multiple_events (ank/src/cli_commands/get_events.rs:362) loc=109
- listen_to_agents (server/src/ankaios_server.rs:131) loc=565
- utest_server_update_state_continues_on_invalid_new_state (server/src/ankaios_server.rs:1022) loc=153
- utest_server_sends_workloads_and_workload_states (server/src/ankaios_server.rs:1255) loc=156

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 2363 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 351 per-function CFGs (cc > 3)
- `statemachines.json` — 30 state machine patterns
- `metrics.json` — 2363 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
