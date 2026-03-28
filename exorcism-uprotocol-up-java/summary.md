# Project Analysis: uprotocol-up-java

## Overview
| Item | Value |
|------|-------|
| Languages | Java |
| Build System | Maven |
| Total Files | 68 |
| Total LOC | 10,401 |
| Total Functions | 541 |
| State Machines | 0 |
| Communication Patterns | 4 |
| External Dependencies | 0 |

## Language Breakdown
- **Java**: 68 files, 10,401 LOC

## Architecture Overview
Build system: **Maven**

### Communication Protocols
- **MQTT_topic**: 4 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- handleRequest (src/main/java/org/eclipse/uprotocol/communication/InMemoryRpcServer.java:154) cc=11
- validateAuthority (src/main/java/org/eclipse/uprotocol/uri/validator/UriValidator.java:106) cc=24
- verifyFilterCriteria (src/main/java/org/eclipse/uprotocol/uri/validator/UriValidator.java:326) cc=14
- deserialize (src/main/java/org/eclipse/uprotocol/uri/serializer/UriSerializer.java:126) cc=19

### High Nesting Functions (depth > 3)
- testUnpackOrDefaultInstanceSucceedsForSimpleProtobuf (src/test/java/org/eclipse/uprotocol/communication/UPayloadTest.java:169) depth=4
- testValidate (src/test/java/org/eclipse/uprotocol/uri/validator/UriValidatorTest.java:36) depth=4
- assertBuilderPanics (src/test/java/org/eclipse/uprotocol/transport/builder/UMessageBuilderTest.java:108) depth=5
- testRequestMessageBuilderRejectsInvalidAttributes (src/test/java/org/eclipse/uprotocol/transport/builder/UMessageBuilderTest.java:141) depth=5
- testResponseMessageBuilderRejectsInvalidAttributes (src/test/java/org/eclipse/uprotocol/transport/builder/UMessageBuilderTest.java:183) depth=5
- unpackOrDefaultInstance (src/main/java/org/eclipse/uprotocol/communication/UPayload.java:205) depth=5
- mapResponse (src/main/java/org/eclipse/uprotocol/communication/RpcMapper.java:45) depth=6
- mapResponseToResult (src/main/java/org/eclipse/uprotocol/communication/RpcMapper.java:78) depth=6
- addSubscriptionChangeHandler (src/main/java/org/eclipse/uprotocol/communication/InMemorySubscriber.java:155) depth=7
- subscribe (src/main/java/org/eclipse/uprotocol/communication/InMemorySubscriber.java:186) depth=5
- unsubscribe (src/main/java/org/eclipse/uprotocol/communication/InMemorySubscriber.java:233) depth=5
- handleSubscriptionChangeNotification (src/main/java/org/eclipse/uprotocol/communication/InMemorySubscriber.java:302) depth=5
- registerRequestHandler (src/main/java/org/eclipse/uprotocol/communication/InMemoryRpcServer.java:96) depth=5
- handleRequest (src/main/java/org/eclipse/uprotocol/communication/InMemoryRpcServer.java:154) depth=5
- collectErrors (src/main/java/org/eclipse/uprotocol/validation/ValidationUtils.java:35) depth=4
- validate (src/main/java/org/eclipse/uprotocol/uri/validator/UriValidator.java:60) depth=4
- validateAuthority (src/main/java/org/eclipse/uprotocol/uri/validator/UriValidator.java:106) depth=5
- verifyFilterCriteria (src/main/java/org/eclipse/uprotocol/uri/validator/UriValidator.java:326) depth=4
- matches (src/main/java/org/eclipse/uprotocol/uri/validator/UriFilter.java:46) depth=4

### Large Functions (LOC > 100)
- notificationMessageArgProvider (src/test/java/org/eclipse/uprotocol/transport/validator/UAttributesValidatorTest.java:244) loc=121
- requestMessageArgProvider (src/test/java/org/eclipse/uprotocol/transport/validator/UAttributesValidatorTest.java:405) loc=164
- responseMessageArgProvider (src/test/java/org/eclipse/uprotocol/transport/validator/UAttributesValidatorTest.java:613) loc=172

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 541 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 49 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 541 function metrics
- `communication.json` — 4 protocol patterns
- `dependencies.json` — 0 external dependencies
