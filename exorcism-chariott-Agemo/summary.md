# Project Analysis: chariott-Agemo

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Cargo |
| Total Files | 37 |
| Total LOC | 4,900 |
| Total Functions | 131 |
| State Machines | 0 |
| Communication Patterns | 24 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 37 files, 4,900 LOC

## Architecture Overview
Build system: **Cargo**

### Communication Protocols
- **MQTT_topic**: 19 occurrence(s)
- **DDS_topic**: 5 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- update_topic (pub-sub-service/src/topic_manager.rs:188) cc=20
- monitor (pub-sub-service/src/topic_manager.rs:383) cc=11

### High Nesting Functions (depth > 3)
- main (pub-sub-service/src/main.rs:40) depth=6
- update_topic (pub-sub-service/src/topic_manager.rs:188) depth=9
- cleanup_topics (pub-sub-service/src/topic_manager.rs:317) depth=5
- handle_topic_action (pub-sub-service/src/topic_manager.rs:354) depth=7
- monitor (pub-sub-service/src/topic_manager.rs:383) depth=12
- load_settings (pub-sub-service/src/load_config.rs:138) depth=5
- connect_to_chariott_with_retry (pub-sub-service/src/connectors/chariott_connector.rs:34) depth=6
- connect_client (pub-sub-service/src/connectors/mosquitto_connector.rs:120) depth=6
- get_config_home_path_from_env (common/src/config_utils.rs:128) depth=4
- connect_to_chariott_with_retry (samples/common/src/chariott_helper.rs:24) depth=6
- get_service_metadata_with_retry (samples/common/src/chariott_helper.rs:65) depth=4
- handle_publish_loop (samples/common/src/publisher_helper.rs:66) depth=5
- handle_ctrlc_shutdown (samples/common/src/subscriber_helper.rs:133) depth=6
- read_from_files (samples/common/src/config_utils.rs:25) depth=4
- main (samples/simple-subscriber/src/main.rs:23) depth=4
- main (samples/chariott-subscriber/src/main.rs:55) depth=4
- on_stop_action (samples/simple-publisher/src/publisher_impl.rs:119) depth=6
- get_subscription_info (samples/simple-publisher/src/publisher_impl.rs:220) depth=4
- on_stop_action (samples/chariott-publisher/src/publisher_impl.rs:119) depth=6
- get_subscription_info (samples/chariott-publisher/src/publisher_impl.rs:220) depth=4

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 131 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 24 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 131 function metrics
- `communication.json` — 24 protocol patterns
- `dependencies.json` — 0 external dependencies
