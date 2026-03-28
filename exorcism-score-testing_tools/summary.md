# Project Analysis: score-testing_tools

## Overview
| Item | Value |
|------|-------|
| Languages | Python, Rust, C++ |
| Build System | Bazel, Python/pyproject |
| Total Files | 36 |
| Total LOC | 5,732 |
| Total Functions | 345 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 53 |

## Language Breakdown
- **Python**: 15 files, 3,669 LOC
- **Rust**: 5 files, 853 LOC
- **C++**: 16 files, 1,210 LOC

## Architecture Overview
Build system: **Bazel, Python/pyproject**

## Key Findings

### High Complexity Functions (cc > 10)
- parse_cli_arguments (test_scenarios_rust/src/cli.rs:58) cc=11
- run_cli_app (test_scenarios_rust/src/cli.rs:113) cc=11
- minify_json (test_scenarios_cpp/src/tracing.cpp:25) cc=26
- <anonymous> (test_scenarios_cpp/src/tracing.cpp:67) cc=13
- <anonymous> (test_scenarios_cpp/src/scenario.cpp:34) cc=11
- parse_cli_arguments (test_scenarios_cpp/src/cli.cpp:21) cc=33
- run_cli_app (test_scenarios_cpp/src/cli.cpp:53) cc=22

### High Nesting Functions (depth > 3)
- __init__ (testing_utils/result_entry.py:34) depth=7
- select_target_path (testing_utils/build_tools.py:112) depth=5
- metadata (testing_utils/build_tools.py:193) depth=5
- build (testing_utils/build_tools.py:236) depth=5
- query (testing_utils/build_tools.py:312) depth=5
- find_target_path (testing_utils/build_tools.py:333) depth=5
- build (testing_utils/build_tools.py:379) depth=5
- __repr__ (testing_utils/scenario.py:48) depth=5
- _run_command (testing_utils/scenario.py:135) depth=5
- get_caps (testing_utils/cap_utils.py:16) depth=5
- set_caps (testing_utils/cap_utils.py:53) depth=5
- _logs_by_field_field_only (testing_utils/log_container.py:83) depth=7
- _logs_by_field_regex_match (testing_utils/log_container.py:107) depth=7
- _logs_by_field_exact_match (testing_utils/log_container.py:141) depth=7
- get_logs (testing_utils/log_container.py:220) depth=5
- _find_visibility (scripts/coverage_checker/coverage_checker.py:130) depth=5
- _find_name (scripts/coverage_checker/coverage_checker.py:153) depth=5
- __init__ (scripts/coverage_checker/coverage_checker.py:239) depth=7
- filter_visibility (scripts/coverage_checker/coverage_checker.py:325) depth=7
- filter_item_type (scripts/coverage_checker/coverage_checker.py:343) depth=9

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 345 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 38 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 345 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 53 external dependencies
