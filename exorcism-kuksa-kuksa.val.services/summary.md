# Project Analysis: kuksa-kuksa.val.services

## Overview
| Item | Value |
|------|-------|
| Languages | C, C++, Python |
| Build System | Unknown |
| Total Files | 107 |
| Total LOC | 14,040 |
| Total Functions | 484 |
| State Machines | 1 |
| Communication Patterns | 9 |
| External Dependencies | 0 |

## Language Breakdown
- **C**: 16 files, 2,422 LOC
- **C++**: 18 files, 5,033 LOC
- **Python**: 73 files, 6,585 LOC

## Architecture Overview
Build system: **Unknown**

### State Machines Detected
- `seat_service/src/lib/seat_adjuster/seat_controller/tests/cansim/seatadjuster_engine.c:62` — switch on `state` (9 states)

### Communication Protocols
- **CAN_message_id**: 4 occurrence(s)
- **MQTT_topic**: 4 occurrence(s)
- **gRPC_service**: 1 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- sdv (seat_service/src/lib/broker_feeder/kuksa_client.h:27) cc=21
- broker_feeder (seat_service/src/lib/broker_feeder/kuksa_client.h:36) cc=20
- KuksaClient (seat_service/src/lib/broker_feeder/kuksa_client.h:40) cc=19
- toString (seat_service/src/lib/broker_feeder/kuksa_client.cc:82) cc=16
- Run (seat_service/src/lib/broker_feeder/data_broker_feeder.cc:72) cc=64
- registerDatapoints (seat_service/src/lib/broker_feeder/data_broker_feeder.cc:238) cc=43
- getMetadata (seat_service/src/lib/broker_feeder/data_broker_feeder.cc:302) cc=47
- checkDatapoints (seat_service/src/lib/broker_feeder/data_broker_feeder.cc:355) cc=24
- feedToBroker (seat_service/src/lib/broker_feeder/data_broker_feeder.cc:411) cc=54
- handleError (seat_service/src/lib/broker_feeder/data_broker_feeder.cc:488) cc=26
- <anonymous> (seat_service/src/lib/seat_adjuster/seat_adjuster.cc:79) cc=26
- <anonymous> (seat_service/src/lib/seat_adjuster/seat_adjuster.cc:135) cc=11
- <anonymous> (seat_service/src/lib/seat_adjuster/seat_adjuster.cc:153) cc=13
- <anonymous> (seat_service/src/lib/seat_adjuster/seat_adjuster.cc:185) cc=35
- main (seat_service/src/lib/seat_adjuster/seat_controller/main.cc:69) cc=27
- handle_secu_stat (seat_service/src/lib/seat_adjuster/seat_controller/seat_controller.cc:226) cc=35
- is_ctl_running (seat_service/src/lib/seat_adjuster/seat_controller/seat_controller.cc:292) cc=12
- seatctrl_control_loop (seat_service/src/lib/seat_adjuster/seat_controller/seat_controller.cc:333) cc=63
- <anonymous> (seat_service/src/lib/seat_adjuster/seat_controller/seat_controller.cc:447) cc=36
- seatctrl_set_position (seat_service/src/lib/seat_adjuster/seat_controller/seat_controller.cc:591) cc=44

### High Nesting Functions (depth > 3)
- Run (seat_service/src/lib/broker_feeder/data_broker_feeder.cc:72) depth=7
- <anonymous> (seat_service/src/lib/seat_adjuster/seat_adjuster.cc:185) depth=4
- seatctrl_control_loop (seat_service/src/lib/seat_adjuster/seat_controller/seat_controller.cc:333) depth=5
- <anonymous> (seat_service/src/lib/seat_adjuster/seat_controller/seat_controller.cc:447) depth=4
- TEST_F (seat_service/src/lib/seat_adjuster/seat_controller/tests/test_seatctrl_api.cc:420) depth=5
- TEST_F (seat_service/src/lib/seat_adjuster/seat_controller/tests/test_seatctrl_api.cc:509) depth=5
- <anonymous> (seat_service/src/lib/seat_adjuster/seat_controller/tests/mock/mock_unix_socket.cc:218) depth=4
- ioctl (seat_service/src/lib/seat_adjuster/seat_controller/tests/cansim/cansim_lib.c:324) depth=4
- write (seat_service/src/lib/seat_adjuster/seat_controller/tests/cansim/cansim_lib.c:362) depth=4
- read (seat_service/src/lib/seat_adjuster/seat_controller/tests/cansim/cansim_lib.c:404) depth=4
- sae_write_cb (seat_service/src/lib/seat_adjuster/seat_controller/tests/cansim/seatadjuster_engine.c:384) depth=5
- main (seat_service/src/examples/broker_feeder/broker_feeder.cc:39) depth=4
- <anonymous> (seat_service/src/bin/seat_service/seat_position_subscriber.cc:46) depth=5
- main (hvac_service/testclient.py:66) depth=7
- on_broker_connectivity_change (hvac_service/hvacservice.py:107) depth=7
- _run (hvac_service/hvacservice.py:137) depth=7
- test_hvac_events (integration_test/test_hvac.py:145) depth=6
- client_thread_runner (integration_test/test_hvac.py:162) depth=5
- __initialize_metadata (integration_test/vdb_helper.py:206) depth=5
- subscribe_datapoints (integration_test/vdb_helper.py:282) depth=9

### Large Functions (LOC > 100)
- seatctrl_control_loop (seat_service/src/lib/seat_adjuster/seat_controller/seat_controller.cc:333) loc=107
- TEST_F (seat_service/src/lib/seat_adjuster/seat_controller/tests/integration_seatctrl.cc:257) loc=146
- main (seat_service/src/lib/seat_adjuster/seat_controller/tests/cansim/main.c:40) loc=101
- sae_read_cb (seat_service/src/lib/seat_adjuster/seat_controller/tests/cansim/seatadjuster_engine.c:235) loc=147
- main (seat_service/src/examples/seat_svc_client/seat_svc_client.cc:228) loc=131
- _parse_datapoint (integration_test/broker_subscribe.py:124) loc=108
- create_mock_behavior (mock_service/showcase_gui/GUI.py:106) loc=113
- show_mock_popup (mock_service/showcase_gui/GUI.py:327) loc=108

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 484 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 171 per-function CFGs (cc > 3)
- `statemachines.json` — 1 state machine patterns
- `metrics.json` — 484 function metrics
- `communication.json` — 9 protocol patterns
- `dependencies.json` — 0 external dependencies
