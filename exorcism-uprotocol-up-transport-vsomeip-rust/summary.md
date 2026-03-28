# Project Analysis: uprotocol-up-transport-vsomeip-rust

## Overview
| Item | Value |
|------|-------|
| Languages | Rust, C, C++ |
| Build System | Cargo |
| Total Files | 38 |
| Total LOC | 8,302 |
| Total Functions | 236 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 31 files, 7,842 LOC
- **C**: 5 files, 348 LOC
- **C++**: 2 files, 112 LOC

## Architecture Overview
Build system: **Cargo**

## Key Findings

### High Complexity Functions (cc > 10)
- test_available_state_handler (vsomeip-sys/src/lib.rs:159) cc=11
- glue (vsomeip-sys/src/glue/include/payload_wrapper.h:20) cc=31
- glue (vsomeip-sys/src/glue/include/message_wrapper.h:20) cc=11
- determine_type (up-transport-vsomeip/src/determine_message_type.rs:28) cc=25
- register_for_returning_response_if_point_to_point_listener_and_sending_request (up-transport-vsomeip/src/lib.rs:362) cc=12
- ucode_to_vsomeip_err_code (up-transport-vsomeip/src/message_conversions.rs:264) cc=12
- vsomeip_err_code_to_ucode (up-transport-vsomeip/src/message_conversions.rs:582) cc=12
- publisher_subscriber (up-transport-vsomeip/tests/publisher_subscriber.rs:70) cc=11
- on_receive (up-transport-vsomeip/tests/point_to_point.rs:112) cc=16
- point_to_point (up-transport-vsomeip/tests/point_to_point.rs:328) cc=13

### High Nesting Functions (depth > 3)
- get_and_build_protos (example-utils/hello-world-protos/build.rs:43) depth=4
- download_and_write_file (example-utils/hello-world-protos/build.rs:100) depth=4
- copy_dir_all (vsomeip-sys/build.rs:341) depth=4
- get_message_base_pinned (vsomeip-sys/src/glue_additions.rs:300) depth=4
- test_available_state_handler (vsomeip-sys/src/lib.rs:159) depth=7
- main (vsomeip-sys/examples/publisher_example.rs:30) depth=4
- main (vsomeip-sys/examples/service_example.rs:32) depth=4
- create_app (up-transport-vsomeip/src/transport_engine.rs:130) depth=4
- event_loop (up-transport-vsomeip/src/transport_engine.rs:239) depth=5
- register_listener_internal (up-transport-vsomeip/src/transport_engine.rs:412) depth=5
- unregister_listener_internal (up-transport-vsomeip/src/transport_engine.rs:618) depth=4
- send_internal (up-transport-vsomeip/src/transport_engine.rs:726) depth=4
- determine_type (up-transport-vsomeip/src/determine_message_type.rs:28) depth=5
- get_callback_runtime_handle (up-transport-vsomeip/src/lib.rs:75) depth=4
- register_for_returning_response_if_point_to_point_listener_and_sending_request (up-transport-vsomeip/src/lib.rs:362) depth=5
- register_point_to_point_listener (up-transport-vsomeip/src/lib.rs:452) depth=4
- unregister_point_to_point_listener (up-transport-vsomeip/src/lib.rs:532) depth=5
- drop (up-transport-vsomeip/src/lib.rs:684) depth=4
- umsg_response_to_vsomeip_message (up-transport-vsomeip/src/message_conversions.rs:170) depth=4
- get_message_handler (up-transport-vsomeip/src/storage/message_handler_registry.rs:157) depth=5

### Large Functions (LOC > 100)
- test_available_state_handler (vsomeip-sys/src/lib.rs:159) loc=101
- test_service_availability_handler (vsomeip-sys/src/lib.rs:262) loc=177
- generate_message_handler_extern_c_fns (vsomeip-proc-macro/src/lib.rs:30) loc=154
- generate_available_state_handler_extern_c_fns (vsomeip-proc-macro/src/lib.rs:186) loc=122
- create_app (up-transport-vsomeip/src/transport_engine.rs:130) loc=108
- event_loop (up-transport-vsomeip/src/transport_engine.rs:239) loc=172
- register_listener_internal (up-transport-vsomeip/src/transport_engine.rs:412) loc=205
- unregister_listener_internal (up-transport-vsomeip/src/transport_engine.rs:618) loc=107
- publisher_subscriber (up-transport-vsomeip/tests/publisher_subscriber.rs:70) loc=119
- on_receive (up-transport-vsomeip/tests/point_to_point.rs:112) loc=117
- point_to_point (up-transport-vsomeip/tests/point_to_point.rs:328) loc=181
- client_service (up-transport-vsomeip/tests/client_service.rs:128) loc=160

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 236 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 44 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 236 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
