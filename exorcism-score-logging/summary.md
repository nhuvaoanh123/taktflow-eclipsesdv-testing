# Project Analysis: score-logging

## Overview
| Item | Value |
|------|-------|
| Languages | Python, C, C++, Rust |
| Build System | Bazel, Python/pyproject |
| Total Files | 289 |
| Total LOC | 42,142 |
| Total Functions | 2184 |
| State Machines | 0 |
| Communication Patterns | 1 |
| External Dependencies | 1 |

## Language Breakdown
- **Python**: 3 files, 263 LOC
- **C**: 135 files, 11,214 LOC
- **C++**: 144 files, 29,504 LOC
- **Rust**: 7 files, 1,161 LOC

## Architecture Overview
Build system: **Bazel, Python/pyproject**

### Communication Protocols
- **MQTT_topic**: 1 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- score (score/mw/log/rust/score_log_bridge_cpp_init/score_log_bridge_init.h:19) cc=14
- ScoreLogBridgeBuilder (score/mw/log/rust/score_log_bridge_cpp_init/score_log_bridge_init.h:29) cc=14
- log (score/mw/log/rust/score_log_bridge/src/score_log_bridge.rs:182) cc=13
- mw (score/mw/log/test/fake_recorder/fake_recorder.h:29) cc=17
- log (score/mw/log/test/fake_recorder/fake_recorder.h:31) cc=17
- test (score/mw/log/test/fake_recorder/fake_recorder.h:33) cc=17
- helper (score/mw/log/detail/common/helper_functions.h:22) cc=37
- Sum (score/mw/log/detail/common/helper_functions.h:32) cc=11
- ClampTo (score/mw/log/detail/common/helper_functions.h:47) cc=14
- score (score/mw/log/detail/common/recorder_factory.h:23) cc=21
- mw (score/mw/log/detail/common/recorder_factory.h:25) cc=21
- log (score/mw/log/detail/common/recorder_factory.h:27) cc=21
- detail (score/mw/log/detail/common/recorder_factory.h:29) cc=21
- IRecorderFactory (score/mw/log/detail/common/recorder_factory.h:38) cc=21
- <anonymous> (score/mw/log/detail/file_recorder/file_recorder_factory.cpp:37) cc=11
- kDltHtypWEID (score/mw/log/detail/file_recorder/dlt_message_builder_types.h:50) cc=16
- kDltHtypWTMS (score/mw/log/detail/file_recorder/dlt_message_builder_types.h:51) cc=16
- kDltHtypVERS (score/mw/log/detail/file_recorder/dlt_message_builder_types.h:52) cc=16
- mw (score/mw/log/detail/file_recorder/file_recorder_factory.h:24) cc=11
- log (score/mw/log/detail/file_recorder/file_recorder_factory.h:26) cc=11

### High Nesting Functions (depth > 3)
- _module_root (score/mw/log/taktflow_tests/test_module_contracts.py:15) depth=5
- test_unsafe_blocks_have_safety_justification (score/mw/log/taktflow_tests/test_module_contracts.py:99) depth=9
- set_default_logger (score/mw/log/rust/score_log_bridge_cpp_init/ffi.rs:18) depth=4
- set_as_default_logger (score/mw/log/rust/score_log_bridge/src/score_log_bridge.rs:98) depth=9
- log (score/mw/log/rust/score_log_bridge/src/score_log_bridge.rs:182) depth=5
- write_i8 (score/mw/log/rust/score_log_bridge/src/ffi.rs:278) depth=4
- write_i16 (score/mw/log/rust/score_log_bridge/src/ffi.rs:302) depth=4
- write_i32 (score/mw/log/rust/score_log_bridge/src/ffi.rs:326) depth=4
- write_i64 (score/mw/log/rust/score_log_bridge/src/ffi.rs:350) depth=4
- <anonymous> (score/datarouter/src/applications/options.cpp:79) depth=6
- <anonymous> (score/datarouter/src/daemon/udp_stream_output.cpp:25) depth=4
- <anonymous> (score/datarouter/src/daemon/message_passing_server.cpp:214) depth=5
- <anonymous> (score/datarouter/src/unix_domain/unix_domain_server.cpp:280) depth=6
- <anonymous> (score/datarouter/src/unix_domain/unix_domain_server.cpp:336) depth=6
- <anonymous> (score/datarouter/src/unix_domain/unix_domain_server.cpp:386) depth=4
- <anonymous> (score/datarouter/src/unix_domain/unix_domain_server.cpp:418) depth=4
- RecvSocketMessage (score/datarouter/src/unix_domain/unix_domain_common.cpp:281) depth=6
- <anonymous> (score/datarouter/src/unix_domain/unix_domain_client.cpp:70) depth=5
- <anonymous> (score/datarouter/datarouter/data_router.cpp:209) depth=4

### Large Functions (LOC > 100)
- score (score/mw/log/detail/data_router/data_router_message_client_impl.h:32) loc=115
- mw (score/mw/log/detail/data_router/data_router_message_client_impl.h:34) loc=112
- log (score/mw/log/detail/data_router/data_router_message_client_impl.h:36) loc=109
- detail (score/mw/log/detail/data_router/data_router_message_client_impl.h:38) loc=106
- <anonymous> (score/mw/log/detail/data_router/shared_memory/reader_factory_impl.cpp:40) loc=101
- detail (score/mw/log/detail/data_router/shared_memory/shared_memory_writer.h:32) loc=177
- score (score/datarouter/include/daemon/diagnostic_job_handler.h:21) loc=160
- logging (score/datarouter/include/daemon/diagnostic_job_handler.h:23) loc=157
- dltserver (score/datarouter/include/daemon/diagnostic_job_handler.h:25) loc=154
- score (score/datarouter/include/daemon/dlt_log_server.h:43) loc=306
- logging (score/datarouter/include/daemon/dlt_log_server.h:45) loc=144
- dltserver (score/datarouter/include/daemon/dlt_log_server.h:47) loc=141
- kLogEntryTypeName (score/datarouter/include/daemon/dlt_log_server.h:50) loc=128
- kPersistentRequestTypeName (score/datarouter/include/daemon/dlt_log_server.h:51) loc=102
- score (score/datarouter/include/daemon/message_passing_server.h:39) loc=162
- platform (score/datarouter/include/daemon/message_passing_server.h:41) loc=159
- internal (score/datarouter/include/daemon/message_passing_server.h:43) loc=155
- IMessagePassingServerSessionWrapper (score/datarouter/include/daemon/message_passing_server.h:68) loc=106
- UnixDomainServer (score/datarouter/include/unix_domain/unix_domain_server.h:41) loc=172
- SessionWrapper (score/datarouter/include/unix_domain/unix_domain_server.h:62) loc=150

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 2184 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 412 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 2184 function metrics
- `communication.json` — 1 protocol patterns
- `dependencies.json` — 1 external dependencies
