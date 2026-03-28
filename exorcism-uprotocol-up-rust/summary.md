# Project Analysis: uprotocol-up-rust

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Cargo |
| Total Files | 37 |
| Total LOC | 13,566 |
| Total Functions | 515 |
| State Machines | 3 |
| Communication Patterns | 3 |
| External Dependencies | 22 |

## Language Breakdown
- **Rust**: 37 files, 13,566 LOC

## Architecture Overview
Build system: **Cargo**

### State Machines Detected
- `src/communication/default_pubsub.rs:341` — match on `response.status.state.enum_value()` (2 states)
- `src/communication/in_memory_rpc_client.rs:36` — match on `response.commstatus()` (2 states)
- `src/uattributes/uattributesvalidator.rs:509` — match on `status.enum_value()` (2 states)

### Communication Protocols
- **MQTT_topic**: 3 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- verify_filter_criteria (src/utransport.rs:35) cc=14
- try_from (src/cloudevents.rs:240) cc=24
- from_str (src/uri.rs:144) cc=12
- verify_parsed_authority (src/uri.rs:508) cc=13
- is_remote_authority (src/uri.rs:656) cc=11
- verify_no_wildcards (src/uri.rs:768) cc=11
- invoke_subscribe (src/communication/default_pubsub.rs:331) cc=12
- test_publish_succeeds (src/communication/default_pubsub.rs:524) cc=13
- test_publish_succeeds (src/communication/default_notifier.rs:188) cc=19
- test_request_listener_invokes_operation_successfully (src/communication/in_memory_rpc_server.rs:376) cc=19
- test_request_listener_invokes_operation_erroneously (src/communication/in_memory_rpc_server.rs:447) cc=11
- test_invoke_method_succeeds (src/communication/in_memory_rpc_client.rs:358) cc=11
- from (src/communication/rpc.rs:71) cc=14
- from (src/communication/rpc.rs:98) cc=14

### High Nesting Functions (depth > 3)
- priority (src/uattributes.rs:233) depth=4
- check_expired (src/uattributes.rs:563) depth=5
- check_expired_for_reference (src/uattributes.rs:589) depth=5
- verify_filter_criteria (src/utransport.rs:35) depth=5
- deserialize_protobuf_bytes (src/umessage.rs:358) depth=4
- dispatch (src/local_transport.rs:75) depth=4
- try_from (src/cloudevents.rs:240) depth=6
- try_from (src/cloudevents.rs:347) depth=5
- from_str (src/uri.rs:144) depth=5
- verify_parsed_authority (src/uri.rs:508) depth=8
- verify_no_wildcards (src/uri.rs:768) depth=7
- add_handler (src/communication/default_pubsub.rs:85) depth=5
- invoke_subscribe (src/communication/default_pubsub.rs:331) depth=6
- process_valid_request (src/communication/in_memory_rpc_server.rs:37) depth=5
- validate_origin_filter (src/communication/in_memory_rpc_server.rs:145) depth=5
- register_endpoint (src/communication/in_memory_rpc_server.rs:165) depth=4
- unregister_endpoint (src/communication/in_memory_rpc_server.rs:199) depth=4
- test_request_listener_invokes_operation_successfully (src/communication/in_memory_rpc_server.rs:376) depth=4
- handle_response_message (src/communication/in_memory_rpc_client.rs:35) depth=4
- handle_response (src/communication/in_memory_rpc_client.rs:81) depth=5

### Large Functions (LOC > 100)
- handle_request (src/symphony.rs:258) loc=115

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 515 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 85 per-function CFGs (cc > 3)
- `statemachines.json` — 3 state machine patterns
- `metrics.json` — 515 function metrics
- `communication.json` — 3 protocol patterns
- `dependencies.json` — 22 external dependencies
