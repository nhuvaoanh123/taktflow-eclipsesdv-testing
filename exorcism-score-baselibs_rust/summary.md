# Project Analysis: score-baselibs_rust

## Overview
| Item | Value |
|------|-------|
| Languages | Rust, C++, C, Python |
| Build System | Cargo, Bazel |
| Total Files | 55 |
| Total LOC | 10,496 |
| Total Functions | 711 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 50 files, 10,146 LOC
- **C++**: 2 files, 113 LOC
- **C**: 1 files, 91 LOC
- **Python**: 2 files, 146 LOC

## Architecture Overview
Build system: **Cargo, Bazel**

## Key Findings

### High Complexity Functions (cc > 10)
- get_date (src/log/stdout_logger/timestamp.rs:49) cc=12
- log (src/log/stdout_logger/lib.rs:289) cc=12
- parse_spec (src/log/score_log_fmt_macro/format_args.rs:63) cc=43
- tokenize_spec (src/log/score_log_fmt_macro/format_args.rs:218) cc=33
- tokenize_display_hint (src/log/score_log_fmt_macro/format_args.rs:220) cc=11
- process_format_string (src/log/score_log_fmt_macro/format_args.rs:349) cc=34
- select_arg_with_name (src/log/score_log_fmt_macro/format_args.rs:512) cc=13
- parse_fragments (src/log/score_log_fmt_macro/format_args.rs:573) cc=15
- score (src/log/stdout_logger_cpp_init/stdout_logger_init.h:19) cc=20
- LogLevel (src/log/stdout_logger_cpp_init/stdout_logger_init.h:23) cc=20
- StdoutLoggerBuilder (src/log/stdout_logger_cpp_init/stdout_logger_init.h:40) cc=20

### High Nesting Functions (depth > 3)
- get_date (src/log/stdout_logger/timestamp.rs:49) depth=5
- log (src/log/stdout_logger/lib.rs:289) depth=7
- test_level_partial_cmp_with_level_filter (src/log/score_log/lib.rs:484) depth=6
- test_level_filter_partial_cmp_with_level (src/log/score_log/lib.rs:609) depth=6
- test_filter (src/log/score_log/tests/integration.rs:43) depth=4
- parse_argument (src/log/score_log_fmt_macro/format_args.rs:32) depth=4
- parse_spec (src/log/score_log_fmt_macro/format_args.rs:63) depth=9
- tokenize_spec (src/log/score_log_fmt_macro/format_args.rs:218) depth=4
- process_format_string (src/log/score_log_fmt_macro/format_args.rs:349) depth=7
- validate_args (src/log/score_log_fmt_macro/format_args.rs:457) depth=6
- select_arg_with_name (src/log/score_log_fmt_macro/format_args.rs:512) depth=6
- parse_fragments (src/log/score_log_fmt_macro/format_args.rs:573) depth=7
- generate_for_struct (src/log/score_log_fmt_macro/score_debug.rs:20) depth=5
- generate_for_enum (src/log/score_log_fmt_macro/score_debug.rs:87) depth=6
- field_with (src/log/score_log_fmt/builders.rs:49) depth=4
- finish_non_exhaustive (src/log/score_log_fmt/builders.rs:67) depth=4
- field_with (src/log/score_log_fmt/builders.rs:122) depth=4
- finish_non_exhaustive (src/log/score_log_fmt/builders.rs:138) depth=4
- finish (src/log/score_log_fmt/builders.rs:151) depth=6
- entry_with (src/log/score_log_fmt/builders.rs:174) depth=4

### Large Functions (LOC > 100)
- parse_spec (src/log/score_log_fmt_macro/format_args.rs:63) loc=153
- process_format_string (src/log/score_log_fmt_macro/format_args.rs:349) loc=105

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 711 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 103 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 711 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
