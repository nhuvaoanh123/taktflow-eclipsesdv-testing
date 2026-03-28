# Project Analysis: kuksa-kuksa-incubation

## Overview
| Item | Value |
|------|-------|
| Languages | Rust, Python, JavaScript, Go, C, C++ |
| Build System | Unknown |
| Total Files | 147 |
| Total LOC | 20,386 |
| Total Functions | 677 |
| State Machines | 2 |
| Communication Patterns | 11 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 20 files, 2,619 LOC
- **Python**: 73 files, 6,276 LOC
- **JavaScript**: 1 files, 159 LOC
- **Go**: 8 files, 1,581 LOC
- **C**: 24 files, 4,028 LOC
- **C++**: 21 files, 5,723 LOC

## Architecture Overview
Build system: **Unknown**

### State Machines Detected
- `kuksa-persistence-provider/src/main.rs:103` — match on `parsed_cfg_hash["state-storage"]` (2 states)
- `seat_service/src/lib/seat_adjuster/seat_controller/tests/cansim/seatadjuster_engine.c:62` — switch on `state` (9 states)

### Communication Protocols
- **CAN_message_id**: 4 occurrence(s)
- **MQTT_topic**: 6 occurrence(s)
- **gRPC_service**: 1 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- new_datapoint (zenoh-kuksa-provider/src/utils/kuksa_utils.rs:50) cc=11
- datapoint_to_string (zenoh-kuksa-provider/src/utils/kuksa_utils.rs:100) cc=18
- initWebsocket (kuksademo/driver-ui/webapp/com.js:35) cc=27
- tempTostr (kuksademo/driver-ui/webapp/com.js:116) cc=17
- parseData (kuksademo/driver-ui/webapp/com.js:135) cc=17
- TestQuotesInStringValues (kuksa_go_client/client_test.go:168) cc=11
- main (kuksa_go_client/main.go:28) cc=60
- UnzipSource (kuksa_go_client/protocInstall/protocInstall.go:53) cc=16
- startCommunication (kuksa_go_client/kuksa_client/commn.go:79) cc=29
- GetArrayFromInput (kuksa_go_client/kuksa_client/grpc.go:80) cc=26
- parseValue (kuksa_go_client/kuksa_client/grpc.go:120) cc=15
- SetValueFromKuksaVal (kuksa_go_client/kuksa_client/grpc.go:188) cc=54
- AuthorizeKuksaValConn (kuksa_go_client/kuksa_client/grpc.go:432) cc=11
- String (kuksa_go_client/kuksa_client/config.go:53) cc=13
- create_storage_from_cfg (kuksa-persistence-provider/src/main.rs:93) cc=16
- collect_vss_paths (kuksa-persistence-provider/src/main.rs:150) cc=14
- get_from_storage_and_set (kuksa-persistence-provider/src/kuksaconnector.rs:50) cc=20
- watch_values (kuksa-persistence-provider/src/kuksaconnector.rs:173) cc=20
- try_into_data_value (kuksa-persistence-provider/src/kuksaconnector.rs:259) cc=98
- fmt (kuksa-persistence-provider/src/kuksaconnector.rs:433) cc=21

### High Nesting Functions (depth > 3)
- handling_zenoh_subscription (zenoh-kuksa-provider/src/main.rs:56) depth=8
- publish_to_zenoh (zenoh-kuksa-provider/src/main.rs:89) depth=15
- chooseValue (kuksademo/data-provider.py:34) depth=5
- initWebsocket (kuksademo/driver-ui/webapp/com.js:35) depth=7
- parseData (kuksademo/driver-ui/webapp/com.js:135) depth=6
- main (kuksa_go_client/main.go:28) depth=9
- UnzipSource (kuksa_go_client/protocInstall/protocInstall.go:53) depth=7
- ProtoExists (kuksa_go_client/protocInstall/protocInstall.go:165) depth=5
- main (kuksa_go_client/protocInstall/protocInstall.go:175) depth=5
- startCommunication (kuksa_go_client/kuksa_client/commn.go:79) depth=9
- <anonymous> (kuksa_go_client/kuksa_client/commn.go:130) depth=7
- <anonymous> (kuksa_go_client/kuksa_client/commn.go:145) depth=8
- GetArrayFromInput (kuksa_go_client/kuksa_client/grpc.go:80) depth=7
- SetValueFromKuksaVal (kuksa_go_client/kuksa_client/grpc.go:188) depth=4
- PrintSubscriptionMessages (kuksa_go_client/kuksa_client/grpc.go:369) depth=5
- AuthorizeKuksaValConn (kuksa_go_client/kuksa_client/grpc.go:432) depth=6
- AuthorizeKuksaValConn (kuksa_go_client/kuksa_client/ws.go:129) depth=6
- create_storage_from_cfg (kuksa-persistence-provider/src/main.rs:93) depth=7
- collect_vss_paths (kuksa-persistence-provider/src/main.rs:150) depth=9
- get_from_storage_and_set (kuksa-persistence-provider/src/kuksaconnector.rs:50) depth=8

### Large Functions (LOC > 100)
- main (kuksa_go_client/main.go:28) loc=159
- startCommunication (kuksa_go_client/kuksa_client/commn.go:79) loc=105
- SetValueFromKuksaVal (kuksa_go_client/kuksa_client/grpc.go:188) loc=180
- get_from_storage_and_set (kuksa-persistence-provider/src/kuksaconnector.rs:50) loc=122
- try_into_data_value (kuksa-persistence-provider/src/kuksaconnector.rs:259) loc=129
- seatctrl_control_loop (seat_service/src/lib/seat_adjuster/seat_controller/seat_controller.cc:333) loc=107
- TEST_F (seat_service/src/lib/seat_adjuster/seat_controller/tests/integration_seatctrl.cc:257) loc=146
- main (seat_service/src/lib/seat_adjuster/seat_controller/tests/cansim/main.c:40) loc=101
- sae_read_cb (seat_service/src/lib/seat_adjuster/seat_controller/tests/cansim/seatadjuster_engine.c:235) loc=147
- main (seat_service/src/examples/seat_svc_client/seat_svc_client.cc:228) loc=131
- _parse_datapoint (seat_service/integration_test/broker_subscribe.py:124) loc=108
- app_main (gRPC-on-ESP32/main/main.c:49) loc=148
- kuksa (kuksa-cpp-client/include/kuksaclient.h:23) loc=107
- _parse_datapoint (hvac_service/integration_test/broker_subscribe.py:124) loc=108
- main (can-protocol-adapter/src/main.rs:38) loc=114

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 677 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 243 per-function CFGs (cc > 3)
- `statemachines.json` — 2 state machine patterns
- `metrics.json` — 677 function metrics
- `communication.json` — 11 protocol patterns
- `dependencies.json` — 0 external dependencies
