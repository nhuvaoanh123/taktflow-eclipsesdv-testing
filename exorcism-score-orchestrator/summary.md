# Project Analysis: score-orchestrator

## Overview
| Item | Value |
|------|-------|
| Languages | Rust, C, C++, Python |
| Build System | Cargo, Bazel, Python/pyproject |
| Total Files | 102 |
| Total LOC | 19,003 |
| Total Functions | 1122 |
| State Machines | 2 |
| Communication Patterns | 0 |
| External Dependencies | 43 |

## Language Breakdown
- **Rust**: 77 files, 15,769 LOC
- **C**: 3 files, 178 LOC
- **C++**: 1 files, 53 LOC
- **Python**: 21 files, 3,003 LOC

## Architecture Overview
Build system: **Cargo, Bazel, Python/pyproject**

### State Machines Detected
- `src/orchestration/src/actions/graph.rs:378` — match on `self.state` (2 states)
- `src/orchestration/src/actions/concurrency.rs:177` — match on `self.state` (2 states)

## Key Findings

### High Complexity Functions (cc > 10)
- main (src/xtask/src/main.rs:20) cc=18
- internal_run (src/orchestration/src/program.rs:191) cc=15
- poll (src/orchestration/src/program.rs:296) cc=14
- create_polling_thread (src/orchestration/src/events/iceoryx/event.rs:187) cc=27
- poll_node_handles (src/orchestration/src/actions/graph.rs:377) cc=25
- join_result (src/orchestration/src/actions/concurrency.rs:176) cc=25
- mock_action_with_input (src/orchestration/src/testing/mod.rs:458) cc=11
- choose_graph (tests/test_scenarios/rust/src/scenarios/orchestration/orchestration_graph.rs:381) cc=20
- run (tests/test_scenarios/rust/src/scenarios/taktflow/proc_macro_safety.rs:17) cc=13

### High Nesting Functions (depth > 3)
- main (src/xtask/src/main.rs:20) depth=4
- check_license_header (src/xtask/src/main.rs:239) depth=4
- visit_dirs (src/xtask/src/main.rs:260) depth=7
- build (src/orchestration/src/program.rs:107) depth=5
- internal_run (src/orchestration/src/program.rs:191) depth=6
- run_start_action (src/orchestration/src/program.rs:243) depth=5
- run_stop_action (src/orchestration/src/program.rs:257) depth=5
- create_shutdown_handle (src/orchestration/src/program.rs:271) depth=4
- poll (src/orchestration/src/program.rs:296) depth=5
- set_invoke_worker_id (src/orchestration/src/program_database.rs:292) depth=7
- set_creator_for_events (src/orchestration/src/program_database.rs:314) depth=5
- loom_try_lock (src/orchestration/src/core/orch_locks.rs:167) depth=5
- execute_impl (src/orchestration/src/events/local_events.rs:100) depth=5
- next (src/orchestration/src/events/timer_events.rs:41) depth=4
- check_event (src/orchestration/src/events/iceoryx/event.rs:160) depth=5
- wake_on_event (src/orchestration/src/events/iceoryx/event.rs:173) depth=5
- create_polling_thread (src/orchestration/src/events/iceoryx/event.rs:187) depth=20
- execute_impl (src/orchestration/src/events/iceoryx/global_events.rs:89) depth=4
- sort (src/orchestration/src/actions/graph.rs:138) depth=7
- build_edges (src/orchestration/src/actions/graph.rs:205) depth=4

### Large Functions (LOC > 100)
- main (src/xtask/src/main.rs:20) loc=123
- create_polling_thread (src/orchestration/src/events/iceoryx/event.rs:187) loc=103
- graph_action_with_multiple_roots_and_sequence (src/orchestration/src/actions/graph.rs:1011) loc=147

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 1122 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 86 per-function CFGs (cc > 3)
- `statemachines.json` — 2 state machine patterns
- `metrics.json` — 1122 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 43 external dependencies
