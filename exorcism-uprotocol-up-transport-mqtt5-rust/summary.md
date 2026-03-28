# Project Analysis: uprotocol-up-transport-mqtt5-rust

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Cargo |
| Total Files | 10 |
| Total LOC | 4,228 |
| Total Functions | 102 |
| State Machines | 0 |
| Communication Patterns | 5 |
| External Dependencies | 18 |

## Language Breakdown
- **Rust**: 10 files, 4,228 LOC

## Architecture Overview
Build system: **Cargo**

### Communication Protocols
- **MQTT_topic**: 5 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- create_mqtt_properties_from_uattributes (src/mapping.rs:85) cc=17
- create_uattributes_from_mqtt_properties (src/mapping.rs:251) cc=16
- create_mqtt_properties (src/mapping.rs:521) cc=18
- test_send (src/transport.rs:237) cc=12

### High Nesting Functions (depth > 3)
- create_mqtt_properties_from_uattributes (src/mapping.rs:85) depth=6
- create_uattributes_from_mqtt_properties (src/mapping.rs:251) depth=5
- create_mqtt_properties (src/mapping.rs:521) depth=5
- test_send (src/transport.rs:237) depth=6
- test_unregister_listener (src/transport.rs:474) depth=4
- uri_to_authority_topic_segment (src/lib.rs:124) depth=4
- to_mqtt_topic (src/lib.rs:177) depth=5
- process_incoming_message (src/lib.rs:219) depth=7
- create_cb_message_handler (src/lib.rs:432) depth=4
- add_listener (src/lib.rs:531) depth=5
- remove_listener (src/lib.rs:565) depth=5
- add_listener (src/listener_registry.rs:133) depth=5
- process_connack (src/mqtt_client.rs:417) depth=4
- recreate_subscriptions (src/mqtt_client.rs:448) depth=4
- connect (src/mqtt_client.rs:479) depth=4
- reconnect (src/mqtt_client.rs:510) depth=7
- subscribe (src/mqtt_client.rs:613) depth=4
- main (examples/publisher_example.rs:35) depth=5
- connection_established (tests/common/mod.rs:31) depth=4

### Large Functions (LOC > 100)
- create_mqtt_properties_from_uattributes (src/mapping.rs:85) loc=164
- create_uattributes_from_mqtt_properties (src/mapping.rs:251) loc=167
- create_mqtt_properties (src/mapping.rs:521) loc=136
- test_publish_and_subscribe_succeeds_after_reconnect (tests/publish_subscribe.rs:33) loc=111

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 102 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 22 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 102 function metrics
- `communication.json` — 5 protocol patterns
- `dependencies.json` — 18 external dependencies
