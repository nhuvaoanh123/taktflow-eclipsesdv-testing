# Project Analysis: ibeji-freyja

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Cargo |
| Total Files | 117 |
| Total LOC | 10,395 |
| Total Functions | 327 |
| State Machines | 4 |
| Communication Patterns | 1 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 117 files, 10,395 LOC

## Architecture Overview
Build system: **Cargo**

### State Machines Detected
- `mocks/mock_digital_twin/src/mock_provider.rs:47` — match on `find_entity(&state, &request.entity_id)` (2 states)
- `mocks/mock_digital_twin/src/mock_provider.rs:69` — match on `get_entity_value(&mut state, &request.entity_id)` (2 states)
- `mocks/mock_digital_twin/src/mock_provider.rs:77` — match on `state
                    .response_channel_sender
                    .send((request.consumer_uri, publish_request))` (2 states)
- `freyja/src/data_adapter_selector_impl.rs:208` — match on `state.data_adapters.entry(provider_uri)` (2 states)

### Communication Protocols
- **MQTT_topic**: 1 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- serialize (proto/cloud_connector/src/lib.rs:20) cc=16
- parse_value (common/src/message_utils.rs:29) cc=16
- f32_close_enough (common/src/conversion.rs:83) cc=15
- get_service_uri (adapters/service_discovery/grpc_service_discovery_adapter/src/grpc_service_discovery_adapter.rs:71) cc=12
- start (adapters/data/mqtt_data_adapter/src/mqtt_data_adapter.rs:79) cc=12
- get_nth (adapters/data/in_memory_mock_data_adapter/src/config.rs:43) cc=18
- f32_approx_eq (adapters/data/in_memory_mock_data_adapter/src/config.rs:60) cc=15
- main (mocks/mock_digital_twin/src/main.rs:65) cc=21
- within_bounds (mocks/mock_digital_twin/src/main.rs:238) cc=11
- get_nth (mocks/mock_digital_twin/src/config.rs:50) cc=18
- f32_close_enough (mocks/mock_digital_twin/src/config.rs:67) cc=15
- check_for_work (mocks/mock_mapping_service/src/main.rs:140) cc=16
- get_mapping (mocks/mock_mapping_service/src/mock_mapping_service_impl.rs:50) cc=12
- emit_data (freyja/src/emitter.rs:78) cc=15

### High Nesting Functions (depth > 3)
- serialize (proto/cloud_connector/src/lib.rs:20) depth=4
- parse_value (common/src/message_utils.rs:29) depth=6
- execute_with_retry (common/src/retry_utils.rs:17) depth=5
- parse_args (common/src/cmd_utils.rs:21) depth=4
- read_from_files (common/src/config_utils.rs:28) depth=4
- is_supported (common/src/entity.rs:47) depth=7
- get_service_uri (adapters/service_discovery/grpc_service_discovery_adapter/src/grpc_service_discovery_adapter.rs:71) depth=5
- start (adapters/data/mqtt_data_adapter/src/mqtt_data_adapter.rs:79) depth=12
- start (adapters/data/in_memory_mock_data_adapter/src/in_memory_mock_data_adapter.rs:117) depth=8
- register_entity (adapters/data/in_memory_mock_data_adapter/src/in_memory_mock_data_adapter.rs:192) depth=6
- register_entity (adapters/data/sample_grpc_data_adapter/src/sample_grpc_data_adapter.rs:145) depth=6
- verify_attribute_macro_argument_list (proc_macros/src/error/generate.rs:234) depth=5
- main (mocks/mock_digital_twin/src/main.rs:65) depth=8
- get_active_entity_names (mocks/mock_digital_twin/src/main.rs:250) depth=4
- subscribe (mocks/mock_digital_twin/src/mock_provider.rs:39) depth=4
- get (mocks/mock_digital_twin/src/mock_provider.rs:65) depth=4
- main (mocks/mock_mapping_service/src/main.rs:47) depth=8
- check_for_work (mocks/mock_mapping_service/src/main.rs:140) depth=6
- get_mapping (mocks/mock_mapping_service/src/mock_mapping_service_impl.rs:50) depth=6
- emit_data (freyja/src/emitter.rs:78) depth=6

### Large Functions (LOC > 100)
- sync_updates_correct_properties (common/src/signal_store.rs:300) loc=104
- get_signal_value_returns_correct_values (adapters/data/in_memory_mock_data_adapter/src/in_memory_mock_data_adapter.rs:251) loc=107
- main (mocks/mock_digital_twin/src/main.rs:65) loc=165
- create_or_update_adapter (freyja/src/data_adapter_selector_impl.rs:83) loc=109

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 327 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 62 per-function CFGs (cc > 3)
- `statemachines.json` — 4 state machine patterns
- `metrics.json` — 327 function metrics
- `communication.json` — 1 protocol patterns
- `dependencies.json` — 0 external dependencies
