# Project Analysis: kuksa-kuksa-someip-provider

## Overview
| Item | Value |
|------|-------|
| Languages | C++, C |
| Build System | CMake |
| Total Files | 21 |
| Total LOC | 4,496 |
| Total Functions | 142 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **C++**: 10 files, 3,436 LOC
- **C**: 11 files, 1,060 LOC

## Architecture Overview
Build system: **CMake**

## Key Findings

### High Complexity Functions (cc > 10)
- <anonymous> (src/lib/broker_feeder/actuator_subscriber.cc:77) cc=66
- sdv (src/lib/broker_feeder/actuator_subscriber.h:23) cc=12
- broker_feeder (src/lib/broker_feeder/actuator_subscriber.h:24) cc=12
- kuksa (src/lib/broker_feeder/actuator_subscriber.h:25) cc=12
- ActuatorSubscriber (src/lib/broker_feeder/actuator_subscriber.h:31) cc=12
- Run (src/lib/broker_feeder/data_broker_feeder.cc:70) cc=21
- registerDatapoints (src/lib/broker_feeder/data_broker_feeder.cc:168) cc=15
- feedToBroker (src/lib/broker_feeder/data_broker_feeder.cc:217) cc=25
- <anonymous> (src/lib/broker_feeder/collector_client.cc:71) cc=11
- <anonymous> (src/lib/broker_feeder/collector_client.cc:130) cc=22
- sdv (src/lib/broker_feeder/collector_client.h:23) cc=20
- broker_feeder (src/lib/broker_feeder/collector_client.h:24) cc=20
- CollectorClient (src/lib/broker_feeder/collector_client.h:30) cc=18
- <anonymous> (src/lib/someip_client/someip_client.cc:87) cc=36
- <anonymous> (src/lib/someip_client/someip_client.cc:127) cc=48
- <anonymous> (src/lib/someip_client/someip_client.cc:202) cc=20
- <anonymous> (src/lib/someip_client/someip_client.cc:235) cc=45
- <anonymous> (src/lib/someip_client/someip_client.cc:267) cc=22
- <anonymous> (src/lib/someip_client/someip_client.cc:284) cc=53
- <anonymous> (src/lib/someip_client/someip_client.cc:327) cc=35

### High Nesting Functions (depth > 3)
- <anonymous> (src/lib/broker_feeder/actuator_subscriber.cc:77) depth=5
- Run (src/lib/broker_feeder/data_broker_feeder.cc:70) depth=4
- wiper_mode_parse (src/lib/wiper_poc/wiper_poc.cc:276) depth=4
- main (src/someip_feeder/main.cc:160) depth=7
- notify_th (src/examples/wiper_service/wiper_server.cc:301) depth=5
- notify_th_random (src/examples/wiper_service/wiper_server.cc:365) depth=5
- main (src/examples/wiper_service/wiper_server.cc:525) depth=5
- <anonymous> (src/examples/wiper_service/wiper_sim.cc:71) depth=4
- main (src/examples/wiper_service/wiper_client.cc:388) depth=8

### Large Functions (LOC > 100)
- notify_th_random (src/examples/wiper_service/wiper_server.cc:365) loc=122

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 142 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 84 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 142 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
