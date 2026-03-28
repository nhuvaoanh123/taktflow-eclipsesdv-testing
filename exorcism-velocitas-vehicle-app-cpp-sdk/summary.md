# Project Analysis: velocitas-vehicle-app-cpp-sdk

## Overview
| Item | Value |
|------|-------|
| Languages | Python, C, C++ |
| Build System | CMake |
| Total Files | 98 |
| Total LOC | 10,061 |
| Total Functions | 580 |
| State Machines | 0 |
| Communication Patterns | 4 |
| External Dependencies | 4 |

## Language Breakdown
- **Python**: 2 files, 184 LOC
- **C**: 42 files, 3,854 LOC
- **C++**: 54 files, 6,023 LOC

## Architecture Overview
Build system: **CMake**

### Communication Protocols
- **MQTT_topic**: 4 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- velocitas (sdk/include/sdk/VehicleApp.h:29) cc=36
- VehicleApp (sdk/include/sdk/VehicleApp.h:39) cc=22
- velocitas (sdk/include/sdk/DataPoint.h:30) cc=13
- velocitas (sdk/include/sdk/DataPointReply.h:29) cc=22
- QueryBuilder (sdk/include/sdk/QueryBuilder.h:33) cc=12
- velocitas (sdk/include/sdk/DataPointBatch.h:26) cc=14
- DataPointBatch (sdk/include/sdk/DataPointBatch.h:33) cc=14
- velocitas (sdk/include/sdk/Logger.h:24) cc=19
- velocitas (sdk/include/sdk/grpc/GrpcCall.h:27) cc=22
- GrpcCall (sdk/include/sdk/grpc/GrpcCall.h:33) cc=18
- velocitas (sdk/include/sdk/middleware/Middleware.h:24) cc=11
- Middleware (sdk/include/sdk/middleware/Middleware.h:31) cc=11
- <anonymous> (sdk/src/sdk/Utils.cpp:62) cc=11
- velocitas (sdk/src/sdk/vdb/grpc/kuksa_val_v2/BrokerClient.h:27) cc=27
- kuksa_val_v2 (sdk/src/sdk/vdb/grpc/kuksa_val_v2/BrokerClient.h:31) cc=27
- IVehicleDataBrokerClient (sdk/src/sdk/vdb/grpc/kuksa_val_v2/BrokerClient.h:36) cc=27
- kuksa_val_v2 (sdk/src/sdk/vdb/grpc/kuksa_val_v2/TypeConversions.h:28) cc=13
- parseQuery (sdk/src/sdk/vdb/grpc/kuksa_val_v2/TypeConversions.cpp:234) cc=13
- sdv_databroker_v1 (sdk/src/sdk/vdb/grpc/sdv_databroker_v1/GrpcDataPointValueProvider.h:20) cc=26
- GrpcDataPointValueProvider (sdk/src/sdk/vdb/grpc/sdv_databroker_v1/GrpcDataPointValueProvider.h:26) cc=26

### High Nesting Functions (depth > 3)
- set_version (conanfile.py:45) depth=7
- getChannelArguments (sdk/src/sdk/vdb/grpc/common/ChannelConfiguration.cpp:36) depth=5

### Large Functions (LOC > 100)
- velocitas (sdk/include/sdk/VehicleApp.h:29) loc=129
- velocitas (sdk/include/sdk/Utils.h:23) loc=105
- velocitas (sdk/include/sdk/IPubSubClient.h:25) loc=122
- IPubSubClient (sdk/include/sdk/IPubSubClient.h:31) loc=114
- velocitas (sdk/include/sdk/middleware/Middleware.h:24) loc=101
- convertToGrpcValue (sdk/src/sdk/vdb/grpc/kuksa_val_v2/TypeConversions.cpp:27) loc=136
- convertToGrpcDataPoint (sdk/src/sdk/vdb/grpc/sdv_databroker_v1/BrokerClient.cpp:74) loc=146

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 580 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 96 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 580 function metrics
- `communication.json` — 4 protocol patterns
- `dependencies.json` — 4 external dependencies
