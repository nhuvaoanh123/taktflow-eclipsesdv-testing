# Project Analysis: score-lifecycle

## Overview
| Item | Value |
|------|-------|
| Languages | C, C++, Rust, Python |
| Build System | Cargo, Bazel, Python/pyproject |
| Total Files | 227 |
| Total LOC | 41,007 |
| Total Functions | 1999 |
| State Machines | 5 |
| Communication Patterns | 0 |
| External Dependencies | 1 |

## Language Breakdown
- **C**: 24 files, 5,452 LOC
- **C++**: 163 files, 26,081 LOC
- **Rust**: 30 files, 7,835 LOC
- **Python**: 10 files, 1,639 LOC

## Architecture Overview
Build system: **Cargo, Bazel, Python/pyproject**

### State Machines Detected
- `src/health_monitoring_lib/rust/health_monitor.rs:232` — match on `monitor_state.take()` (3 states)
- `src/health_monitoring_lib/rust/logic/logic_monitor.rs:143` — match on `initial_state_index_option` (2 states)
- `src/health_monitoring_lib/rust/logic/logic_monitor.rs:232` — match on `self.state_graph.get(state_index)` (2 states)
- `src/health_monitoring_lib/rust/logic/ffi.rs:133` — match on `monitor.transition(target_state)` (2 states)
- `src/health_monitoring_lib/rust/logic/ffi.rs:151` — match on `monitor.state()` (2 states)

## Key Findings

### High Complexity Functions (cc > 10)
- lifecycle (src/lifecycle_client_lib/include/aasapplicationcontainer.h:23) cc=22
- AasApplicationContainer (src/lifecycle_client_lib/include/aasapplicationcontainer.h:31) cc=22
- mw (src/lifecycle_client_lib/include/runapplication.h:25) cc=22
- lifecycle (src/lifecycle_client_lib/include/runapplication.h:27) cc=22
- final (src/lifecycle_client_lib/include/runapplication.h:31) cc=20
- <anonymous> (src/lifecycle_client_lib/src/lifecyclemanager.cpp:69) cc=19
- <anonymous> (src/lifecycle_client_lib/src/lifecyclemanager.cpp:105) cc=13
- <anonymous> (src/lifecycle_client_lib/src/lifecyclemanager.cpp:136) cc=21
- evaluate (src/health_monitoring_lib/rust/heartbeat/heartbeat_monitor.rs:203) cc=21
- logic_monitor_builder_add_state (src/health_monitoring_lib/rust/logic/ffi.rs:57) cc=11
- stop_internal (src/health_monitoring_lib/rust/deadline/deadline_monitor.rs:179) cc=13
- score (src/health_monitoring_lib/cpp/include/score/hm/health_monitor.h:22) cc=33
- HealthMonitorBuilder (src/health_monitoring_lib/cpp/include/score/hm/health_monitor.h:30) cc=18
- HealthMonitor (src/health_monitoring_lib/cpp/include/score/hm/health_monitor.h:72) cc=16
- internal (src/health_monitoring_lib/cpp/include/score/hm/common.h:24) cc=17
- DroppableFFIHandle (src/health_monitoring_lib/cpp/include/score/hm/common.h:52) cc=11
- heartbeat (src/health_monitoring_lib/cpp/include/score/hm/heartbeat/heartbeat_monitor.h:26) cc=17
- score (src/health_monitoring_lib/cpp/include/score/hm/logic/logic_monitor.h:28) cc=23
- LogicMonitor (src/health_monitoring_lib/cpp/include/score/hm/logic/logic_monitor.h:65) cc=12
- deadline (src/health_monitoring_lib/cpp/include/score/hm/deadline/deadline_monitor.h:29) cc=39

### High Nesting Functions (depth > 3)
- collect_given_monitors (src/health_monitoring_lib/rust/health_monitor.rs:276) depth=6
- run (src/health_monitoring_lib/rust/worker.rs:48) depth=5
- start (src/health_monitoring_lib/rust/worker.rs:108) depth=6
- health_monitor_builder_build (src/health_monitoring_lib/rust/ffi.rs:110) depth=4
- health_monitor_get_deadline_monitor (src/health_monitoring_lib/rust/ffi.rs:244) depth=4
- health_monitor_get_heartbeat_monitor (src/health_monitoring_lib/rust/ffi.rs:275) depth=4
- health_monitor_get_logic_monitor (src/health_monitoring_lib/rust/ffi.rs:306) depth=4
- evaluate (src/health_monitoring_lib/rust/heartbeat/heartbeat_monitor.rs:203) depth=6
- build (src/health_monitoring_lib/rust/logic/logic_monitor.rs:102) depth=5
- find_index_by_tag (src/health_monitoring_lib/rust/logic/logic_monitor.rs:238) depth=4
- logic_monitor_builder_add_state (src/health_monitoring_lib/rust/logic/ffi.rs:57) depth=4
- logic_monitor_state (src/health_monitoring_lib/rust/logic/ffi.rs:140) depth=4
- start_internal (src/health_monitoring_lib/rust/deadline/deadline_monitor.rs:154) depth=4
- stop_internal (src/health_monitoring_lib/rust/deadline/deadline_monitor.rs:179) depth=4
- evaluate (src/health_monitoring_lib/rust/deadline/deadline_monitor.rs:262) depth=7
- get_deadline (src/health_monitoring_lib/rust/deadline/deadline_monitor.rs:323) depth=4
- deadline_monitor_get_deadline (src/health_monitoring_lib/rust/deadline/ffi.rs:109) depth=4
- setSchedulingParameters (src/launch_manager_daemon/src/configuration_manager/configurationmanager.cpp:383) depth=4
- <anonymous> (src/launch_manager_daemon/src/process_group_manager/graph.cpp:292) depth=4
- <anonymous> (src/launch_manager_daemon/src/process_group_manager/processlauncher.cpp:219) depth=4

### Large Functions (LOC > 100)
- deadline (src/health_monitoring_lib/cpp/include/score/hm/deadline/deadline_monitor.h:29) loc=114
- LocalSupervisionStatus (src/launch_manager_daemon/health_monitor_lib/include/score/lcm/Monitor.h:43) loc=123
- GlobalSupervisionStatus (src/launch_manager_daemon/health_monitor_lib/include/score/lcm/Monitor.h:56) loc=109
- <anonymous> (src/launch_manager_daemon/health_monitor_lib/src/score/lcm/saf/factory/FlatCfgFactory.cpp:102) loc=114
- <anonymous> (src/launch_manager_daemon/health_monitor_lib/src/score/lcm/saf/factory/FlatCfgFactory.cpp:500) loc=121
- <anonymous> (src/launch_manager_daemon/health_monitor_lib/src/score/lcm/saf/factory/FlatCfgFactory.cpp:622) loc=126
- <anonymous> (src/launch_manager_daemon/health_monitor_lib/src/score/lcm/saf/factory/FlatCfgFactory.cpp:841) loc=107
- HMFlatBuffer (src/launch_manager_daemon/health_monitor_lib/config/hm_flatcfg_generated.h:28) loc=256
- FLATBUFFERS_FINAL_CLASS (src/launch_manager_daemon/health_monitor_lib/config/hm_flatcfg_generated.h:126) loc=130
- FLATBUFFERS_FINAL_CLASS (src/launch_manager_daemon/health_monitor_lib/config/hm_flatcfg_generated.h:839) loc=107
- LMFlatBuffer (src/launch_manager_daemon/config/lm_flatcfg_generated.h:28) loc=166
- FLATBUFFERS_FINAL_CLASS (src/launch_manager_daemon/config/lm_flatcfg_generated.h:370) loc=121
- FLATBUFFERS_FINAL_CLASS (src/launch_manager_daemon/config/lm_flatcfg_generated.h:555) loc=132
- score (src/control_client_lib/include/score/lcm/control_client.h:25) loc=111
- lcm (src/control_client_lib/include/score/lcm/control_client.h:27) loc=107
- <anonymous> (src/control_client_lib/src/control_client_impl.cpp:110) loc=123
- generate_json (examples/config/gen_launch_manager_cfg.py:25) loc=155

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 1999 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 569 per-function CFGs (cc > 3)
- `statemachines.json` — 5 state machine patterns
- `metrics.json` — 1999 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 1 external dependencies
