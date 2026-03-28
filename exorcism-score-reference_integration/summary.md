# Project Analysis: score-reference_integration

## Overview
| Item | Value |
|------|-------|
| Languages | Python, Rust, C++ |
| Build System | Bazel, Python/pyproject |
| Total Files | 51 |
| Total LOC | 5,082 |
| Total Functions | 191 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 45 |

## Language Breakdown
- **Python**: 36 files, 3,896 LOC
- **Rust**: 14 files, 1,148 LOC
- **C++**: 1 files, 38 LOC

## Architecture Overview
Build system: **Bazel, Python/pyproject**

## Key Findings

### High Complexity Functions (cc > 10)
- format_commit_version_cell (scripts/integration_test.py:202) cc=23
- main (scripts/integration_test.py:258) cc=16
- main (scripts/known_good/update_module_latest.py:119) cc=29
- generate_git_override_blocks (scripts/known_good/update_module_from_known_good.py:45) cc=11
- main (scripts/known_good/update_module_from_known_good.py:209) cc=19
- parse_and_apply_overrides (scripts/known_good/override_known_good_repo.py:43) cc=15

### High Nesting Functions (depth > 3)
- pytest_sessionstart (feature_integration_tests/test_cases/conftest.py:65) depth=5
- kvs_instance (feature_integration_tests/test_scenarios/rust/src/internals/persistency/kvs_instance.rs:20) depth=4
- deserialize_defaults (feature_integration_tests/test_scenarios/rust/src/internals/persistency/kvs_parameters.rs:49) depth=4
- deserialize_kvs_load (feature_integration_tests/test_scenarios/rust/src/internals/persistency/kvs_parameters.rs:67) depth=4
- deserialize_scheduler_type (feature_integration_tests/test_scenarios/rust/src/internals/kyron/runtime_helper.rs:21) depth=4
- build (feature_integration_tests/test_scenarios/rust/src/internals/kyron/runtime_helper.rs:105) depth=7
- kvs_save_cycle_number (feature_integration_tests/test_scenarios/rust/src/scenarios/basic/orchestration_with_persistency.rs:61) depth=4
- datarouter_running (feature_integration_tests/itf/test_remote_logging.py:55) depth=5
- get_module_version_gh (scripts/integration_test.py:37) depth=5
- count_pattern (scripts/integration_test.py:103) depth=7
- get_identifier_and_link (scripts/integration_test.py:124) depth=7
- build_group (scripts/integration_test.py:156) depth=7
- format_commit_version_cell (scripts/integration_test.py:202) depth=5
- main (scripts/integration_test.py:258) depth=5
- main (scripts/publish_integration_summary.py:30) depth=9
- run_command (scripts/quality_runners.py:207) depth=11
- main (scripts/quality_runners.py:281) depth=7
- _find_repo_root (scripts/tooling/cli/misc/html_report.py:33) depth=5
- _resolve_path_from_bazel (scripts/tooling/cli/misc/html_report.py:41) depth=5
- _collect_entries (scripts/tooling/cli/misc/html_report.py:49) depth=7

### Large Functions (LOC > 100)
- main (scripts/integration_test.py:258) loc=121
- main (scripts/known_good/update_module_from_known_good.py:209) loc=150

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 191 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 48 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 191 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 45 external dependencies
