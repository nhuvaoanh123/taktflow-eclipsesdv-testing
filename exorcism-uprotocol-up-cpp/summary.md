# Project Analysis: uprotocol-up-cpp

## Overview
| Item | Value |
|------|-------|
| Languages | Python, C, C++ |
| Build System | CMake |
| Total Files | 76 |
| Total LOC | 17,716 |
| Total Functions | 824 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Python**: 1 files, 32 LOC
- **C**: 27 files, 3,936 LOC
- **C++**: 48 files, 13,748 LOC

## Architecture Overview
Build system: **CMake**

## Key Findings

### High Complexity Functions (cc > 10)
- communication (include/up-cpp/communication/NotificationSink.h:25) cc=24
- communication (include/up-cpp/communication/Subscriber.h:22) cc=21
- communication (include/up-cpp/communication/RpcServer.h:30) cc=34
- communication (include/up-cpp/communication/RpcClient.h:30) cc=34
- get (include/up-cpp/communication/RpcClient.h:40) cc=18
- v3 (include/up-cpp/client/usubscription/v3/USubscription.h:20) cc=20
- v3 (include/up-cpp/client/usubscription/v3/Consumer.h:24) cc=22
- v3 (include/up-cpp/client/usubscription/v3/RpcClientUSubscription.h:44) cc=25
- USubscription (include/up-cpp/client/usubscription/v3/RpcClientUSubscription.h:54) cc=25
- v3 (include/up-cpp/client/usubscription/v3/RequestBuilder.h:19) cc=11
- uprotocol (include/up-cpp/utils/Expected.h:20) cc=44
- operator (include/up-cpp/utils/CallbackConnection.h:150) cc=16
- detail (include/up-cpp/utils/CallbackConnection.h:439) cc=11
- uprotocol (include/up-cpp/utils/ProtoConverter.h:15) cc=24
- uprotocol (include/up-cpp/datamodel/validator/Uuid.h:24) cc=11
- Reason (include/up-cpp/datamodel/validator/Uuid.h:26) cc=11
- Reason (include/up-cpp/datamodel/validator/UUri.h:22) cc=14
- uprotocol (include/up-cpp/datamodel/builder/UMessage.h:33) cc=25
- UTransport (include/up-cpp/transport/UTransport.h:43) cc=24
- getEntityUri (include/up-cpp/transport/UTransport.h:204) cc=16

### High Nesting Functions (depth > 3)
- <anonymous> (src/communication/RpcClient.cpp:354) depth=4

### Large Functions (LOC > 100)
- communication (include/up-cpp/communication/RpcServer.h:30) loc=108
- v3 (include/up-cpp/client/usubscription/v3/Consumer.h:24) loc=113
- uprotocol (include/up-cpp/utils/ProtoConverter.h:15) loc=103
- uprotocol (include/up-cpp/datamodel/validator/UMessage.h:25) loc=141
- Reason (include/up-cpp/datamodel/validator/UMessage.h:27) loc=137
- Reason (include/up-cpp/datamodel/validator/UUri.h:22) loc=180
- uprotocol (include/up-cpp/datamodel/builder/UMessage.h:33) loc=271
- UTransport (include/up-cpp/transport/UTransport.h:43) loc=247
- TEST_F (test/coverage/communication/RpcClientTest.cpp:1176) loc=156
- TEST_F (test/coverage/communication/RpcClientTest.cpp:1375) loc=114
- TEST_F (test/coverage/utils/CallbackConnectionTest.cpp:553) loc=115
- TEST_F (test/coverage/datamodel/UMessageValidatorTest.cpp:243) loc=158
- TEST_F (test/coverage/datamodel/UMessageValidatorTest.cpp:402) loc=195
- TEST_F (test/coverage/datamodel/UMessageValidatorTest.cpp:598) loc=107
- TEST_F (test/coverage/datamodel/UMessageValidatorTest.cpp:706) loc=122
- TEST_F (test/coverage/datamodel/UMessageValidatorTest.cpp:829) loc=150
- TEST_F (test/coverage/datamodel/UMessageValidatorTest.cpp:980) loc=141

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 824 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 132 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 824 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
