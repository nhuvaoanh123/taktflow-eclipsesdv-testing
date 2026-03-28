# Project Analysis: leda-leda-contrib-self-update-agent

## Overview
| Item | Value |
|------|-------|
| Languages | C, C++ |
| Build System | CMake |
| Total Files | 82 |
| Total LOC | 6,850 |
| Total Functions | 300 |
| State Machines | 0 |
| Communication Patterns | 8 |
| External Dependencies | 0 |

## Language Breakdown
- **C**: 44 files, 1,873 LOC
- **C++**: 38 files, 4,977 LOC

## Architecture Overview
Build system: **CMake**

### Communication Protocols
- **MQTT_topic**: 8 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- main (src/main.cpp:63) cc=133
- sua (src/Logger.h:22) cc=43
- Logger (src/Logger.h:24) cc=43
- <anonymous> (src/FSM/FSM.cpp:59) cc=14
- <anonymous> (src/FSM/States/Installing.cpp:37) cc=19
- <anonymous> (src/FSM/States/Downloading.cpp:47) cc=17
- <anonymous> (src/Install/Installer.cpp:36) cc=16
- on_properties_changed (src/Install/DBusRaucInstaller.cpp:58) cc=19
- <anonymous> (src/Install/DBusRaucInstaller.cpp:291) cc=12
- <anonymous> (src/Mqtt/MqttMessagingProtocolJSON.cpp:35) cc=17
- <anonymous> (src/Mqtt/MqttMessagingProtocolJSON.cpp:64) cc=11
- sua (src/Mqtt/MqttMessagingProtocolJSON.h:22) cc=12
- MqttMessagingProtocolJSON (src/Mqtt/MqttMessagingProtocolJSON.h:24) cc=12
- message_arrived (src/Mqtt/MqttProcessor.cpp:106) cc=15
- download (src/Download/Downloader.cpp:115) cc=18

### High Nesting Functions (depth > 3)
- main (src/main.cpp:63) depth=4
- on_properties_changed (src/Install/DBusRaucInstaller.cpp:58) depth=7
- <anonymous> (src/Install/DBusRaucInstaller.cpp:291) depth=4
- <anonymous> (src/Install/DBusRaucInstaller.cpp:370) depth=4
- <anonymous> (src/Install/DBusRaucInstaller.cpp:418) depth=4
- <anonymous> (src/Mqtt/MqttMessagingProtocolJSON.cpp:35) depth=5
- message_arrived (src/Mqtt/MqttProcessor.cpp:106) depth=4

### Large Functions (LOC > 100)
- main (src/main.cpp:63) loc=188
- <anonymous> (src/Mqtt/MqttMessagingProtocolJSON.cpp:135) loc=110

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 300 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 59 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 300 function metrics
- `communication.json` — 8 protocol patterns
- `dependencies.json` — 0 external dependencies
