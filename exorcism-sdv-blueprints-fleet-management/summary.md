# Project Analysis: sdv-blueprints-fleet-management

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Unknown |
| Total Files | 22 |
| Total LOC | 4,405 |
| Total Functions | 80 |
| State Machines | 6 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 22 files, 4,405 LOC

## Architecture Overview
Build system: **Unknown**

### State Machines Detected
- `components/fms-server/src/influx_reader.rs:80` — match on `state.as_str()` (7 states)
- `components/fms-forwarder/src/main.rs:87` — match on `UPayload::try_from_protobuf(vehicle_status)` (2 states)
- `components/fms-forwarder/src/vehicle_abstraction.rs:400` — match on `databroker.get_vehicle_status().await` (2 states)
- `components/fms-forwarder/src/vehicle_abstraction.rs:474` — match on `status_publisher.send(new_vehicle_status).await` (2 states)
- `components/influx-client/src/writer.rs:255` — match on `vehicle_status.created.clone().into_option()` (2 states)
- `components/influx-client/src/writer.rs:265` — match on `vehicle_status.trigger.clone().into_option()` (2 states)

## Key Findings

### High Complexity Functions (cc > 10)
- get_vehicleposition (components/fms-server/src/influx_reader.rs:124) cc=15
- get_vehiclesstatuses (components/fms-server/src/influx_reader.rs:226) cc=15
- as_trigger (components/fms-forwarder/src/vehicle_abstraction.rs:152) cc=13
- try_from (components/fms-forwarder/src/vehicle_abstraction.rs:208) cc=20
- init (components/fms-forwarder/src/vehicle_abstraction.rs:386) cc=20
- new_vehicle_status (components/fms-forwarder/src/vehicle_abstraction/kuksa.rs:31) cc=28
- build_snapshot_measurement (components/influx-client/src/writer.rs:82) cc=25
- write_vehicle_status (components/influx-client/src/writer.rs:250) cc=15
- new (components/up-transport-hono-kafka/src/lib.rs:194) cc=11

### High Nesting Functions (depth > 3)
- parse_latest_only (components/fms-server/src/query_parser.rs:75) depth=5
- parse_time (components/fms-server/src/query_parser.rs:87) depth=5
- unpack_driver_working_state (components/fms-server/src/influx_reader.rs:78) depth=4
- get_vehicleposition (components/fms-server/src/influx_reader.rs:124) depth=7
- get_vehiclesstatuses (components/fms-server/src/influx_reader.rs:226) depth=7
- main (components/fms-forwarder/src/main.rs:64) depth=6
- try_from (components/fms-forwarder/src/vehicle_abstraction.rs:208) depth=6
- get_vehicle_status (components/fms-forwarder/src/vehicle_abstraction.rs:297) depth=6
- register_triggers (components/fms-forwarder/src/vehicle_abstraction.rs:343) depth=12
- init (components/fms-forwarder/src/vehicle_abstraction.rs:386) depth=7
- new_vehicle_status (components/fms-forwarder/src/vehicle_abstraction/kuksa.rs:31) depth=5
- token (components/influx-client/src/connection.rs:83) depth=5
- build_snapshot_measurement (components/influx-client/src/writer.rs:82) depth=7
- write_vehicle_status (components/influx-client/src/writer.rs:250) depth=5
- add_property_bag_to_map (components/up-transport-hono-kafka/src/lib.rs:53) depth=6
- get_headers_as_map (components/up-transport-hono-kafka/src/lib.rs:67) depth=6
- extract_umessage_from_cloudevent (components/up-transport-hono-kafka/src/lib.rs:94) depth=4
- extract_umessage_from_kafka_message (components/up-transport-hono-kafka/src/lib.rs:110) depth=5
- get_kafka_client_config (components/up-transport-hono-kafka/src/lib.rs:164) depth=6
- new (components/up-transport-hono-kafka/src/lib.rs:194) depth=7

### Large Functions (LOC > 100)
- get_vehicleposition (components/fms-server/src/influx_reader.rs:124) loc=101
- get_vehiclesstatuses (components/fms-server/src/influx_reader.rs:226) loc=169
- init (components/fms-forwarder/src/vehicle_abstraction.rs:386) loc=108
- new_vehicle_status (components/fms-forwarder/src/vehicle_abstraction/kuksa.rs:31) loc=193
- build_snapshot_measurement (components/influx-client/src/writer.rs:82) loc=103

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 80 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 29 per-function CFGs (cc > 3)
- `statemachines.json` — 6 state machine patterns
- `metrics.json` — 80 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
