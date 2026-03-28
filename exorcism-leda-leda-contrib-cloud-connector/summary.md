# Project Analysis: leda-leda-contrib-cloud-connector

## Overview
| Item | Value |
|------|-------|
| Languages | Go |
| Build System | Go modules |
| Total Files | 14 |
| Total LOC | 3,175 |
| Total Functions | 133 |
| State Machines | 0 |
| Communication Patterns | 2 |
| External Dependencies | 31 |

## Language Breakdown
- **Go**: 14 files, 3,175 LOC

## Architecture Overview
Build system: **Go modules**

### Communication Protocols
- **MQTT_topic**: 2 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- HandleMessage (routing/message/handlers/command/things_handler.go:65) cc=20
- HandleMessage (routing/message/handlers/telemetry/things_handler.go:71) cc=26
- getTelemetryMapping (routing/message/handlers/telemetry/things_handler.go:146) cc=18
- convertDittoValueInternal (routing/message/handlers/telemetry/things_handler.go:199) cc=12
- Marshal (routing/message/protobuf/marshaller.go:50) cc=16
- getTelemetryMessageDescriptor (routing/message/protobuf/marshaller.go:112) cc=11
- loadMessageDescriptor (routing/message/protobuf/marshaller.go:159) cc=18
- main (cmd/main.go:42) cc=14

### High Nesting Functions (depth > 3)
- HandleMessage (routing/message/handlers/command/things_handler.go:65) depth=7
- wrapDittoPayload (routing/message/handlers/command/things_handler.go:135) depth=5
- TestHandleC2DMessageCorrectly (routing/message/handlers/command/things_handler_test.go:39) depth=4
- TestValidC2DMessageWithTypeSimpleMessage (routing/message/handlers/command/things_handler_test.go:99) depth=4
- HandleMessage (routing/message/handlers/telemetry/things_handler.go:71) depth=7
- getTelemetryMapping (routing/message/handlers/telemetry/things_handler.go:146) depth=11
- convertDittoValueInternal (routing/message/handlers/telemetry/things_handler.go:199) depth=7
- getFieldMappingValue (routing/message/handlers/telemetry/things_handler.go:234) depth=5
- TestHandleContainerMessageTypes (routing/message/handlers/telemetry/things_handler_test.go:43) depth=4
- TestOptimizeDittoPayload (routing/message/handlers/telemetry/things_handler_test.go:216) depth=4
- TestConvertDittoValue (routing/message/handlers/telemetry/things_handler_test.go:321) depth=4
- TestIgnoreConvertDittoValue (routing/message/handlers/telemetry/things_handler_test.go:606) depth=4
- TestMessageTypeMappingWithoutSpecificDescriptorMappingFields (routing/message/handlers/telemetry/things_handler_test.go:797) depth=4
- getTelemetryMessageDescriptor (routing/message/protobuf/marshaller.go:112) depth=5
- loadMessageDescriptor (routing/message/protobuf/marshaller.go:159) depth=5
- TestMarshalValidPayloadAndMessageSubType (routing/message/protobuf/marshaller_test.go:281) depth=4
- TestUnmarshalValidPayloadAndMessageSubType (routing/message/protobuf/marshaller_test.go:359) depth=4
- main (cmd/main.go:42) depth=5

### Large Functions (LOC > 100)
- TestHandleContainerMessageTypes (routing/message/handlers/telemetry/things_handler_test.go:43) loc=172
- TestOptimizeDittoPayload (routing/message/handlers/telemetry/things_handler_test.go:216) loc=104
- TestConvertDittoValue (routing/message/handlers/telemetry/things_handler_test.go:321) loc=284

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 133 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 22 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 133 function metrics
- `communication.json` — 2 protocol patterns
- `dependencies.json` — 31 external dependencies
