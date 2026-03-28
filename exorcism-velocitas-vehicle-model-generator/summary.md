# Project Analysis: velocitas-vehicle-model-generator

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Python/pyproject |
| Total Files | 17 |
| Total LOC | 1,737 |
| Total Functions | 65 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 11 |

## Language Breakdown
- **Python**: 17 files, 1,737 LOC

## Architecture Overview
Build system: **Python/pyproject**

## Key Findings

### High Complexity Functions (cc > 10)
- write (src/velocitas/model_generator/utils.py:61) cc=12
- __gen_model (src/velocitas/model_generator/python/python_generator.py:161) cc=12
- __gen_collection (src/velocitas/model_generator/python/vss_collection.py:59) cc=12
- __gen_nested_class (src/velocitas/model_generator/cpp/cpp_generator.py:201) cc=16

### High Nesting Functions (depth > 3)
- write (src/velocitas/model_generator/utils.py:61) depth=9
- generate_model (src/velocitas/model_generator/__init__.py:35) depth=5
- __visit_nodes (src/velocitas/model_generator/python/python_generator.py:81) depth=7
- __gen_imports (src/velocitas/model_generator/python/python_generator.py:103) depth=5
- __gen_model_docstring (src/velocitas/model_generator/python/python_generator.py:133) depth=7
- __gen_model (src/velocitas/model_generator/python/python_generator.py:161) depth=7
- __gen_collection (src/velocitas/model_generator/python/vss_collection.py:59) depth=9
- __gen_collection_types (src/velocitas/model_generator/python/vss_collection.py:137) depth=9
- __gen_getter (src/velocitas/model_generator/python/vss_collection.py:153) depth=5
- __parse_instances (src/velocitas/model_generator/python/vss_collection.py:174) depth=7
- __get_format_implementation (src/velocitas/model_generator/tree_generator/file_import.py:51) depth=5
- __extend_fields (src/velocitas/model_generator/tree_generator/file_formats.py:88) depth=5
- __visit_nodes (src/velocitas/model_generator/cpp/cpp_generator.py:98) depth=7
- __gen_imports (src/velocitas/model_generator/cpp/cpp_generator.py:151) depth=5
- __gen_nested_class (src/velocitas/model_generator/cpp/cpp_generator.py:201) depth=9
- __gen_collection_types (src/velocitas/model_generator/cpp/cpp_generator.py:311) depth=9
- __gen_model (src/velocitas/model_generator/cpp/cpp_generator.py:342) depth=9
- __gen_instances (src/velocitas/model_generator/cpp/cpp_generator.py:420) depth=5
- __parse_instances (src/velocitas/model_generator/cpp/cpp_generator.py:441) depth=5

### Large Functions (LOC > 100)
- __gen_nested_class (src/velocitas/model_generator/cpp/cpp_generator.py:201) loc=109

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 65 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 19 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 65 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 11 external dependencies
