# Project Analysis: eclipse-velocitas-sdk

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Python/setuptools |
| Total Files | 103 |
| Total LOC | 8,564 |
| Total Functions | 572 |
| State Machines | 0 |
| Communication Patterns | 14 |
| External Dependencies | 64 |

## Language Breakdown
- **Python**: 103 files, 8,564 LOC

## Architecture Overview
Build system: **Python/setuptools**

### Communication Protocols
- **MQTT_topic**: 14 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- get_sample_datapoint (tests/unit/model_test.py:1618) cc=18

### High Nesting Functions (depth > 3)
- run (velocitas_sdk/vehicle_app.py:84) depth=7
- _set (velocitas_sdk/model.py:134) depth=5
- apply (velocitas_sdk/model.py:793) depth=5
- getNode (velocitas_sdk/model.py:819) depth=7
- remove_all_subscriptions (velocitas_sdk/vdb/subscriptions.py:31) depth=5
- list_all_subscription (velocitas_sdk/vdb/subscriptions.py:39) depth=5
- _remove_subscription (velocitas_sdk/vdb/subscriptions.py:47) depth=5
- _subscribe_to_data_points (velocitas_sdk/vdb/subscriptions.py:80) depth=7
- _subscribe_to_data_points_forever (velocitas_sdk/vdb/subscriptions.py:95) depth=9
- subscribe (velocitas_sdk/vdb/subscriptions.py:129) depth=5
- __new__ (velocitas_sdk/vdb/client.py:40) depth=5
- get_service_location (velocitas_sdk/native/locator.py:33) depth=5
- on_connect (velocitas_sdk/native/mqtt.py:47) depth=5
- subscribe_topic (velocitas_sdk/native/mqtt.py:72) depth=4
- __init__ (velocitas_sdk/test/inttesthelper.py:35) depth=5
- __initialize_metadata (velocitas_sdk/test/inttesthelper.py:77) depth=5
- __call__ (velocitas_sdk/test/mqtt_util.py:46) depth=5
- __init__ (velocitas_sdk/test/mqtt_util.py:61) depth=5
- on_connect_callback (velocitas_sdk/test/mqtt_util.py:85) depth=4
- get_log_level (velocitas_sdk/util/log.py:52) depth=5

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 572 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 26 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 572 function metrics
- `communication.json` — 14 protocol patterns
- `dependencies.json` — 64 external dependencies
