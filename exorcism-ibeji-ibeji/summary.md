# Project Analysis: ibeji-ibeji

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Cargo |
| Total Files | 68 |
| Total LOC | 9,598 |
| Total Functions | 216 |
| State Machines | 2 |
| Communication Patterns | 5 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 68 files, 9,598 LOC

## Architecture Overview
Build system: **Cargo**

### State Machines Detected
- `samples/common/src/utils.rs:210` — match on `retry_async_based_on_status(
                        30,
                        Duration::from_secs(1),
                        || discover_service_using_chariott(
                            &value,
                            INVEHICLE_DIGITAL_TWIN_SERVICE_NAMESPACE,
                            INVEHICLE_DIGITAL_TWIN_SERVICE_NAME,
                            INVEHICLE_DIGITAL_TWIN_SERVICE_VERSION,
                            INVEHICLE_DIGITAL_TWIN_SERVICE_COMMUNICATION_KIND,
                            INVEHICLE_DIGITAL_TWIN_SERVICE_COMMUNICATION_REFERENCE)
                    ).await` (2 states)
- `samples/streaming/provider/src/provider_impl.rs:203` — match on `tx.send(Result::<_, Status>::Ok(item)).await` (2 states)

### Communication Protocols
- **DDS_topic**: 1 occurrence(s)
- **MQTT_topic**: 4 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- call (core/common/src/grpc_interceptor.rs:151) cc=23
- retry_async_based_on_status (samples/common/src/utils.rs:62) cc=14
- start_ambient_air_temperature_data_stream (samples/property/provider/src/main.rs:83) cc=11
- start_seat_massage_steps (samples/seat_massager/consumer/src/main.rs:37) cc=12
- start_ambient_air_temperature_data_stream (samples/managed_subscribe/provider/src/main.rs:65) cc=11
- execute_epoch (samples/mixed/provider/src/vehicle.rs:24) cc=13
- invoke (samples/digital_twin_graph/seat_massager_provider/src/request_impl.rs:128) cc=14

### High Nesting Functions (depth > 3)
- retrieve_grpc_names_from_uri (core/common/src/grpc_interceptor.rs:105) depth=7
- call (core/common/src/grpc_interceptor.rs:151) depth=6
- execute_with_retry (core/common/src/utils.rs:68) depth=5
- get_service_uri (core/common/src/utils.rs:150) depth=4
- main (core/invehicle-digital-twin/src/main.rs:177) depth=5
- register_entity (core/invehicle-digital-twin/src/invehicle_digital_twin_impl.rs:87) depth=4
- find_by_instance_id (core/module/digital_twin_registry/src/digital_twin_registry_impl.rs:64) depth=6
- register_entity (core/module/digital_twin_registry/src/digital_twin_registry_impl.rs:135) depth=4
- get_subscription_info (core/module/managed_subscribe/src/managed_subscribe_module.rs:220) depth=4
- manage_topic_callback (core/module/managed_subscribe/src/managed_subscribe_module.rs:284) depth=4
- remove_topic (core/module/managed_subscribe/src/managed_subscribe_store.rs:102) depth=5
- handle_request (core/module/managed_subscribe/src/managed_subscribe_interceptor.rs:60) depth=6
- wait_for_answer (core/module/digital_twin_graph/src/digital_twin_graph_impl.rs:189) depth=6
- find (core/module/digital_twin_graph/src/digital_twin_graph_impl.rs:235) depth=4
- retry_async_based_on_status (samples/common/src/utils.rs:62) depth=7
- retrieve_invehicle_digital_twin_uri (samples/common/src/utils.rs:194) depth=6
- start_get_signals_repeater (samples/tutorial/consumer/src/main.rs:34) depth=5
- start_show_notification_repeater (samples/tutorial/consumer/src/main.rs:59) depth=5
- receive_ambient_air_temperature_updates (samples/property/consumer/src/main.rs:24) depth=8
- start_ambient_air_temperature_data_stream (samples/property/provider/src/main.rs:83) depth=8

### Large Functions (LOC > 100)
- start_seat_massage_steps (samples/seat_massager/consumer/src/main.rs:37) loc=108
- main (samples/mixed/consumer/src/main.rs:164) loc=118
- create_provider_state (samples/digital_twin_graph/vehicle_core_provider/src/main.rs:61) loc=150

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 216 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 58 per-function CFGs (cc > 3)
- `statemachines.json` — 2 state machine patterns
- `metrics.json` — 216 function metrics
- `communication.json` — 5 protocol patterns
- `dependencies.json` — 0 external dependencies
