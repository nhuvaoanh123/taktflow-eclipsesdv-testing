# Project Analysis: score-config_management

## Overview
| Item | Value |
|------|-------|
| Languages | C++, C, Rust, Python |
| Build System | Bazel, Python/pyproject |
| Total Files | 113 |
| Total LOC | 12,195 |
| Total Functions | 529 |
| State Machines | 0 |
| Communication Patterns | 1 |
| External Dependencies | 1 |

## Language Breakdown
- **C++**: 57 files, 8,826 LOC
- **C**: 54 files, 3,309 LOC
- **Rust**: 1 files, 4 LOC
- **Python**: 1 files, 56 LOC

## Architecture Overview
Build system: **Bazel, Python/pyproject**

### Communication Protocols
- **MQTT_topic**: 1 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- <anonymous> (score/config_management/config_provider/code/parameter_set/parameter_set.cpp:51) cc=11
- <anonymous> (score/config_management/config_provider/code/parameter_set/parameter_set.cpp:73) cc=31
- <anonymous> (score/config_management/config_provider/code/parameter_set/parameter_set.cpp:170) cc=14
- score (score/config_management/config_provider/code/parameter_set/parameter_set.h:27) cc=153
- config_management (score/config_management/config_provider/code/parameter_set/parameter_set.h:29) cc=102
- config_provider (score/config_management/config_provider/code/parameter_set/parameter_set.h:31) cc=102
- ParameterSet (score/config_management/config_provider/code/parameter_set/parameter_set.h:34) cc=102
- TYPED_TEST (score/config_management/config_provider/code/parameter_set/parameter_set_test.cpp:898) cc=15
- TYPED_TEST (score/config_management/config_provider/code/parameter_set/parameter_set_test.cpp:940) cc=15
- TYPED_TEST (score/config_management/config_provider/code/parameter_set/parameter_set_test.cpp:982) cc=15
- score (score/config_management/config_provider/code/persistency/persistency.h:24) cc=11
- config_management (score/config_management/config_provider/code/persistency/persistency.h:26) cc=11
- config_provider (score/config_management/config_provider/code/persistency/persistency.h:28) cc=11
- score (score/config_management/config_provider/code/config_provider/config_provider.h:27) cc=25
- config_management (score/config_management/config_provider/code/config_provider/config_provider.h:29) cc=25
- config_provider (score/config_management/config_provider/code/config_provider/config_provider.h:31) cc=25
- ConfigProvider (score/config_management/config_provider/code/config_provider/config_provider.h:37) cc=22
- score (score/config_management/config_provider/code/config_provider/config_provider_mock.h:24) cc=26
- config_management (score/config_management/config_provider/code/config_provider/config_provider_mock.h:26) cc=26
- config_provider (score/config_management/config_provider/code/config_provider/config_provider_mock.h:28) cc=26

### High Nesting Functions (depth > 3)
_None_

### Large Functions (LOC > 100)
- score (score/config_management/config_provider/code/parameter_set/parameter_set.h:27) loc=160
- TEST_F (score/config_management/config_provider/code/parameter_set/parameter_set_test.cpp:1025) loc=128
- score (score/config_management/config_provider/code/config_provider/factory/factory_mw_com.h:29) loc=130
- config_management (score/config_management/config_provider/code/config_provider/factory/factory_mw_com.h:31) loc=127
- config_provider (score/config_management/config_provider/code/config_provider/factory/factory_mw_com.h:33) loc=123
- ConfigProviderFactory (score/config_management/config_provider/code/config_provider/factory/factory_mw_com.h:38) loc=115

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 529 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 132 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 529 function metrics
- `communication.json` — 1 protocol patterns
- `dependencies.json` — 1 external dependencies
