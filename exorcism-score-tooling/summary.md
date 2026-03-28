# Project Analysis: score-tooling

## Overview
| Item | Value |
|------|-------|
| Languages | Python, C++ |
| Build System | Bazel |
| Total Files | 23 |
| Total LOC | 2,913 |
| Total Functions | 83 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Python**: 19 files, 2,851 LOC
- **C++**: 4 files, 62 LOC

## Architecture Overview
Build system: **Bazel**

## Key Findings

### High Complexity Functions (cc > 10)
- copy_html_files (bazel/rules/rules_score/src/sphinx_html_merge.py:38) cc=15
- main (bazel/rules/rules_score/test/fixtures/test_unit_test.cc:12) cc=15
- convert_cargo_to_dash_format (dash/tool/formatters/dash_format_converter.py:169) cc=11
- test_starpls_server_initialize_simple (starpls/integration_tests/starpls_test.py:73) cc=12
- process_files (cr_checker/tool/cr_checker.py:530) cc=12
- main (cr_checker/tool/cr_checker.py:711) cc=17

### High Nesting Functions (depth > 3)
- copy_html_files (bazel/rules/rules_score/src/sphinx_html_merge.py:38) depth=8
- process_file (bazel/rules/rules_score/src/sphinx_html_merge.py:75) depth=6
- copy_tree (bazel/rules/rules_score/src/sphinx_html_merge.py:106) depth=7
- main (bazel/rules/rules_score/src/sphinx_html_merge.py:164) depth=5
- build_sphinx_arguments (bazel/rules/rules_score/src/sphinx_wrapper.py:113) depth=5
- main (bazel/rules/rules_score/src/sphinx_wrapper.py:246) depth=5
- find_workspace_root (bazel/rules/rules_score/src/bazel_sphinx_needs.py:29) depth=5
- load_external_needs (bazel/rules/rules_score/src/bazel_sphinx_needs.py:48) depth=5
- convert_to_dash_format (dash/tool/formatters/dash_format_converter.py:144) depth=7
- convert_cargo_to_dash_format (dash/tool/formatters/dash_format_converter.py:169) depth=9
- relativize (coverage/scripts/normalize_symbol_report.py:35) depth=5
- test_starpls_server_initialize_simple (starpls/integration_tests/starpls_test.py:73) depth=9
- __call__ (cr_checker/tool/cr_checker.py:100) depth=5
- load_templates (cr_checker/tool/cr_checker.py:142) depth=7
- load_exclusion (cr_checker/tool/cr_checker.py:191) depth=7
- detect_shebang_offset (cr_checker/tool/cr_checker.py:249) depth=11
- load_text_from_file_with_mmap (cr_checker/tool/cr_checker.py:308) depth=5
- get_files_from_dir (cr_checker/tool/cr_checker.py:381) depth=7
- collect_inputs (cr_checker/tool/cr_checker.py:406) depth=5
- create_temp_file (cr_checker/tool/cr_checker.py:443) depth=7

### Large Functions (LOC > 100)
- parse_arguments (cr_checker/tool/cr_checker.py:607) loc=102

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 83 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 28 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 83 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
