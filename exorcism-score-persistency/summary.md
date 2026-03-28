# Project Analysis: score-persistency

## Overview
| Item | Value |
|------|-------|
| Languages | Rust, C++, Python |
| Build System | Cargo, Bazel, Python/pyproject |
| Total Files | 77 |
| Total LOC | 15,745 |
| Total Functions | 806 |
| State Machines | 1 |
| Communication Patterns | 0 |
| External Dependencies | 48 |

## Language Breakdown
- **Rust**: 29 files, 7,791 LOC
- **C++**: 36 files, 6,152 LOC
- **Python**: 12 files, 1,802 LOC

## Architecture Overview
Build system: **Cargo, Bazel, Python/pyproject**

### State Machines Detected
- `src/rust/rust_kvs_tool/src/kvs_tool.rs:567` — match on `op_mode` (12 states)

## Key Findings

### High Complexity Functions (cc > 10)
- _getkey (src/rust/rust_kvs_tool/src/kvs_tool.rs:120) cc=17
- _setkey (src/rust/rust_kvs_tool/src/kvs_tool.rs:181) cc=18
- main (src/rust/rust_kvs_tool/src/kvs_tool.rs:439) cc=48
- get_value_as (src/rust/rust_kvs/src/kvs.rs:153) cc=11
- compare_parameters (src/rust/rust_kvs/src/kvs_builder.rs:146) cc=12
- build (src/rust/rust_kvs/src/kvs_builder.rs:189) cc=33
- from (src/rust/rust_kvs/src/json_backend.rs:36) cc=17
- from (src/rust/rust_kvs/src/json_backend.rs:70) cc=12
- main (src/rust/rust_kvs/examples/basic.rs:22) cc=16
- compare_kvs_values (src/rust/rust_kvs/tests/common/mod.rs:29) cc=27
- <anonymous> (src/cpp/src/kvs.cpp:136) cc=37
- <anonymous> (src/cpp/src/kvs.cpp:216) cc=19
- <anonymous> (src/cpp/src/kvs.cpp:479) cc=14
- <anonymous> (src/cpp/src/kvs.cpp:587) cc=13
- <anonymous> (src/cpp/src/kvs.cpp:629) cc=42
- <anonymous> (src/cpp/src/kvs.cpp:690) cc=15
- any_to_kvsvalue (src/cpp/src/internal/kvs_helper.cpp:98) cc=65
- prepare_environment (src/cpp/tests/test_kvs_general.cpp:29) cc=21
- TEST (src/cpp/tests/test_kvs.cpp:170) cc=13
- TEST (src/cpp/tests/test_kvs.cpp:598) cc=16

### High Nesting Functions (depth > 3)
- _getkey (src/rust/rust_kvs_tool/src/kvs_tool.rs:120) depth=5
- _setkey (src/rust/rust_kvs_tool/src/kvs_tool.rs:181) depth=6
- _removekey (src/rust/rust_kvs_tool/src/kvs_tool.rs:230) depth=4
- _snapshotrestore (src/rust/rust_kvs_tool/src/kvs_tool.rs:302) depth=4
- _getkvsfilename (src/rust/rust_kvs_tool/src/kvs_tool.rs:338) depth=4
- _gethashfilename (src/rust/rust_kvs_tool/src/kvs_tool.rs:361) depth=4
- main (src/rust/rust_kvs_tool/src/kvs_tool.rs:439) depth=4
- get_value (src/rust/rust_kvs/src/kvs.rs:125) depth=4
- get_value_as (src/rust/rust_kvs/src/kvs.rs:153) depth=6
- is_value_default (src/rust/rust_kvs/src/kvs.rs:217) depth=4
- compare_parameters (src/rust/rust_kvs/src/kvs_builder.rs:146) depth=6
- build (src/rust/rust_kvs/src/kvs_builder.rs:189) depth=7
- from (src/rust/rust_kvs/src/json_backend.rs:36) depth=7
- snapshot_rotate (src/rust/rust_kvs/src/json_backend.rs:216) depth=5
- snapshot_count (src/rust/rust_kvs/src/json_backend.rs:427) depth=4
- main (src/rust/rust_kvs/examples/defaults.rs:50) depth=4
- main (src/rust/rust_kvs/examples/basic.rs:22) depth=5
- from_kvs (src/rust/rust_kvs/examples/custom_types.rs:79) depth=5
- compare_kvs_values (src/rust/rust_kvs/tests/common/mod.rs:29) depth=6
- <anonymous> (src/cpp/src/kvs.cpp:479) depth=4

### Large Functions (LOC > 100)
- main (src/rust/rust_kvs_tool/src/kvs_tool.rs:439) loc=179
- build (src/rust/rust_kvs/src/kvs_builder.rs:189) loc=109
- main (src/rust/rust_kvs/examples/basic.rs:22) loc=134
- any_to_kvsvalue (src/cpp/src/internal/kvs_helper.cpp:98) loc=180
- kvsvalue_to_any (src/cpp/src/internal/kvs_helper.cpp:280) loc=112

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 806 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 109 per-function CFGs (cc > 3)
- `statemachines.json` — 1 state machine patterns
- `metrics.json` — 806 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 48 external dependencies
