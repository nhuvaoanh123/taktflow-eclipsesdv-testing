# Project Analysis: score-docs-as-code

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Bazel, Python/pyproject |
| Total Files | 61 |
| Total LOC | 11,314 |
| Total Functions | 419 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 10 |

## Language Breakdown
- **Python**: 61 files, 11,314 LOC

## Architecture Overview
Build system: **Bazel, Python/pyproject**

## Key Findings

### High Complexity Functions (cc > 10)
- id_contains_feature (src/extensions/score_metamodel/checks/id_contains_feature.py:25) cc=13
- filter_needs_by_criteria (src/extensions/score_metamodel/checks/graph_checks.py:103) cc=13

### High Nesting Functions (depth > 3)
- _extract_github_data (src/extensions/score_header_service/header_service.py:178) depth=5
- load_source_code_links_json (src/extensions/score_source_code_linker/needlinks.py:83) depth=5
- _extract_references_from_line (src/extensions/score_source_code_linker/generate_source_code_links_json.py:34) depth=7
- _extract_references_from_file (src/extensions/score_source_code_linker/generate_source_code_links_json.py:46) depth=9
- iterate_files_recursively (src/extensions/score_source_code_linker/generate_source_code_links_json.py:79) depth=7
- is_valid (src/extensions/score_source_code_linker/testlink.py:148) depth=5
- get_test_links (src/extensions/score_source_code_linker/testlink.py:178) depth=4
- parse_properties (src/extensions/score_source_code_linker/xml_parser.py:77) depth=5
- read_test_xml_file (src/extensions/score_source_code_linker/xml_parser.py:90) depth=7
- find_xml_files (src/extensions/score_source_code_linker/xml_parser.py:172) depth=5
- build_test_needs_from_files (src/extensions/score_source_code_linker/xml_parser.py:224) depth=5
- group_by_need (src/extensions/score_source_code_linker/__init__.py:74) depth=5
- setup_test_code_linker (src/extensions/score_source_code_linker/__init__.py:215) depth=5
- inject_links_into_needs (src/extensions/score_source_code_linker/__init__.py:323) depth=7
- test_group_by_need (src/extensions/score_source_code_linker/tests/test_codelink.py:302) depth=5
- test_group_by_need_and_find_need_integration (src/extensions/score_source_code_linker/tests/test_codelink.py:437) depth=5
- test_source_linker_end_to_end_with_real_files (src/extensions/score_source_code_linker/tests/test_codelink.py:465) depth=5
- _write_test_xml (src/extensions/score_source_code_linker/tests/test_xml_parser.py:34) depth=5
- tmp_xml_dirs (src/extensions/score_source_code_linker/tests/test_xml_parser.py:71) depth=4
- sphinx_app_setup (src/extensions/score_source_code_linker/tests/test_source_code_link_integration.py:221) depth=8

### Large Functions (LOC > 100)
- draw_module (src/extensions/score_draw_uml_funcs/__init__.py:288) loc=105
- test_my_pie_workproducts_contained_in_exactly_one_workflow (src/extensions/score_metamodel/tests/test_standards.py:513) loc=122

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 419 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 94 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 419 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 10 external dependencies
