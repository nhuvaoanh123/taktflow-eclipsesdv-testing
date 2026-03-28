# Project Analysis: score-bazel_registry

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Python/pyproject |
| Total Files | 18 |
| Total LOC | 1,872 |
| Total Functions | 93 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 43 |

## Language Breakdown
- **Python**: 18 files, 1,872 LOC

## Architecture Overview
Build system: **Python/pyproject**

## Key Findings

### High Complexity Functions (cc > 10)
- plan_module_updates (src/registry_manager/main.py:144) cc=14
- read_modules (src/registry_manager/bazel_wrapper.py:54) cc=11
- try_parse_metadata_json (src/registry_manager/bazel_wrapper.py:76) cc=11

### High Nesting Functions (depth > 3)
- _loc (src/registry_manager/gh_logging.py:35) depth=5
- get_token (src/registry_manager/main.py:55) depth=5
- is_release_semver_acceptable (src/registry_manager/main.py:81) depth=5
- plan_module_updates (src/registry_manager/main.py:144) depth=7
- main (src/registry_manager/main.py:215) depth=5
- read_modules (src/registry_manager/bazel_wrapper.py:54) depth=9
- try_parse_metadata_json (src/registry_manager/bazel_wrapper.py:76) depth=5
- sha256_from_url (src/registry_manager/bazel_wrapper.py:160) depth=6
- _add_version_to_metadata (src/registry_manager/bazel_wrapper.py:225) depth=5
- _write_files (src/registry_manager/bazel_wrapper.py:248) depth=5
- get_latest_release (src/registry_manager/github_wrapper.py:46) depth=7
- try_get_module_file_content (src/registry_manager/github_wrapper.py:91) depth=5
- build_fake_filesystem (tests/conftest.py:56) depth=6
- _build (tests/conftest.py:59) depth=5
- setup_module_metadata (tests/conftest.py:176) depth=4
- test_token_fallback_when_unavailable (tests/test_token.py:34) depth=5
- test_all_correct (tests/test_noop.py:23) depth=5

### Large Functions (LOC > 100)
_None_

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 93 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 19 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 93 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 43 external dependencies
