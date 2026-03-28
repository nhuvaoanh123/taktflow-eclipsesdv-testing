# Project Analysis: score-baselibs

## Overview
| Item | Value |
|------|-------|
| Languages | C, C++, Python |
| Build System | Bazel |
| Total Files | 1668 |
| Total LOC | 240,133 |
| Total Functions | 12783 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **C**: 580 files, 60,355 LOC
- **C++**: 1083 files, 179,536 LOC
- **Python**: 5 files, 242 LOC

## Architecture Overview
Build system: **Bazel**

## Key Findings

### High Complexity Functions (cc > 10)
- score (score/bitmanipulation/bit_manipulation.h:20) cc=51
- platform (score/bitmanipulation/bit_manipulation.h:22) cc=38
- Byte (score/bitmanipulation/bit_manipulation.h:53) cc=22
- GetByte (score/bitmanipulation/bit_manipulation.h:232) cc=12
- logging_serializer (score/static_reflection_with_serialization/serialization/include/serialization/for_logging.h:42) cc=86
- serialize (score/static_reflection_with_serialization/serialization/include/serialization/for_logging.h:58) cc=15
- deserialize (score/static_reflection_with_serialization/serialization/include/serialization/for_logging.h:72) cc=60
- deserialize (score/static_reflection_with_serialization/serialization/include/serialization/for_logging.h:82) cc=12
- Typeinfo (score/static_reflection_with_serialization/serialization/include/serialization/for_logging.h:146) cc=28
- copy (score/static_reflection_with_serialization/serialization/include/serialization/for_logging.h:157) cc=21
- score (score/static_reflection_with_serialization/serialization/include/serialization/visit_type_traits.h:20) cc=55
- common (score/static_reflection_with_serialization/serialization/include/serialization/visit_type_traits.h:22) cc=21
- visitor (score/static_reflection_with_serialization/serialization/include/serialization/visit_type_traits.h:24) cc=12
- score (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:36) cc=499
- common (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:39) cc=473
- visitor (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:42) cc=26
- details (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:88) cc=12
- advance (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:152) cc=19
- deserialize (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:464) cc=21
- detail (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:512) cc=17

### High Nesting Functions (depth > 3)
- score (score/static_reflection_with_serialization/visitor/include/visitor/visit_as_struct.h:23) depth=4
- common (score/static_reflection_with_serialization/visitor/include/visitor/visit_as_struct.h:26) depth=4
- visitor (score/static_reflection_with_serialization/visitor/include/visitor/visit_as_struct.h:29) depth=4
- detail (score/static_reflection_with_serialization/visitor/include/visitor/visit_as_struct.h:32) depth=4
- <anonymous> (score/os/capability.cpp:156) depth=5
- NextServiceRequest (score/os/test/qnx/channel_test.cpp:283) depth=5
- parse_safe_headers (score/os/interface/qnx/gen_unsafe_headers.py:25) depth=7
- find_unsafe_headers (score/os/interface/qnx/gen_unsafe_headers.py:35) depth=7
- <anonymous> (score/network/sock_async/socket.cpp:38) depth=4
- <anonymous> (score/network/sock_async/sock_ctrl.cpp:123) depth=4
- <anonymous> (score/memory/shared/memory_region_map.cpp:338) depth=4
- isValidDateTimeFormat (score/datetime_converter/datetime_converter.cpp:46) depth=6
- TEST (score/mw/log/detail/wait_free_stack/wait_free_stack_test.cpp:72) depth=4
- <anonymous> (score/analysis/tracing/common/flexible_circular_allocator/lockless_flexible_circular_allocator.cpp:424) depth=4
- <anonymous> (score/json/internal/parser/nlohmann/json_builder.cpp:87) depth=7
- <anonymous> (score/filesystem/standard_filesystem_fake.cpp:633) depth=6
- <anonymous> (score/filesystem/file_utils/file_test_utils.cpp:20) depth=5
- StatusInternal (score/filesystem/details/standard_filesystem.cpp:88) depth=7
- <anonymous> (score/filesystem/details/standard_filesystem.cpp:211) depth=4
- <anonymous> (score/filesystem/details/standard_filesystem.cpp:520) depth=5

### Large Functions (LOC > 100)
- score (score/bitmanipulation/bit_manipulation.h:20) loc=179
- platform (score/bitmanipulation/bit_manipulation.h:22) loc=149
- logging_serializer (score/static_reflection_with_serialization/serialization/include/serialization/for_logging.h:42) loc=157
- deserialize (score/static_reflection_with_serialization/serialization/include/serialization/for_logging.h:72) loc=126
- score (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:36) loc=995
- common (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:39) loc=948
- serialize (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:610) loc=279
- deserialize (score/static_reflection_with_serialization/serialization/include/serialization/visit_serialize.h:712) loc=160
- common (score/static_reflection_with_serialization/serialization/include/serialization/visit_size.h:30) loc=265
- visitor (score/static_reflection_with_serialization/serialization/include/serialization/visit_size.h:32) loc=262
- out (score/static_reflection_with_serialization/serialization/include/serialization/visit_size.h:50) loc=192
- TEST (score/static_reflection_with_serialization/serialization/test/ut/test_serializer_visitor.cpp:260) loc=247
- score (score/static_reflection_with_serialization/visitor/include/visitor/visit_as_struct.h:23) loc=192
- common (score/static_reflection_with_serialization/visitor/include/visitor/visit_as_struct.h:26) loc=161
- visitor (score/static_reflection_with_serialization/visitor/include/visitor/visit_as_struct.h:29) loc=156
- detail (score/static_reflection_with_serialization/visitor/include/visitor/visit_as_struct.h:32) loc=151
- score (score/static_reflection_with_serialization/visitor/examples/ostream/include/visitor/visit_ostream.h:24) loc=128
- common (score/static_reflection_with_serialization/visitor/examples/ostream/include/visitor/visit_ostream.h:27) loc=123
- visit_as_struct (score/static_reflection_with_serialization/visitor/examples/ostream/include/visitor/visit_ostream.h:47) loc=101
- score (score/os/pthread.h:27) loc=126

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 12783 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 1628 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 12783 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
