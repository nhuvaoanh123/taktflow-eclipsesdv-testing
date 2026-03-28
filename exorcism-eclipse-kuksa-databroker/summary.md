# Project Analysis: eclipse-kuksa-databroker

## Overview
| Item | Value |
|------|-------|
| Languages | Rust, Python |
| Build System | Cargo |
| Total Files | 83 |
| Total LOC | 37,065 |
| Total Functions | 1058 |
| State Machines | 5 |
| Communication Patterns | 15 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 57 files, 32,434 LOC
- **Python**: 26 files, 4,631 LOC

## Architecture Overview
Build system: **Cargo**

### State Machines Detected
- `lib/common/src/lib.rs:361` — match on `&self.connection_state_subs` (2 states)
- `databroker-cli/src/kuksa_cli.rs:284` — match on `state` (2 states)
- `databroker-cli/src/kuksa_cli.rs:285` — match on `state` (2 states)
- `databroker-cli/src/sdv_cli.rs:134` — match on `state` (2 states)
- `databroker-cli/src/sdv_cli.rs:135` — match on `state` (2 states)

### Communication Protocols
- **MQTT_topic**: 15 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- to_regex_string (databroker/src/glob.rs:88) cc=14
- from (databroker/src/vss.rs:176) cc=26
- try_from_json_array (databroker/src/vss.rs:210) cc=18
- try_from_json_value (databroker/src/vss.rs:263) cc=29
- try_from_json_single_value (databroker/src/vss.rs:368) cc=15
- add_entry (databroker/src/vss.rs:409) cc=18
- determine_change_type (databroker/src/vss.rs:513) cc=11
- test_parse_vss (databroker/src/vss.rs:549) cc=28
- main (databroker/src/main.rs:194) cc=31
- fmt (databroker/src/types.rs:45) cc=26
- fmt (databroker/src/types.rs:113) cc=19
- greater_than (databroker/src/types.rs:137) cc=123
- equals (databroker/src/types.rs:308) cc=149
- validate_allowed_type (databroker/src/broker.rs:326) cc=29
- validate_allowed (databroker/src/broker.rs:366) cc=69
- validate_value (databroker/src/broker.rs:519) cc=160
- notify (databroker/src/broker.rs:830) cc=17
- notify (databroker/src/broker.rs:952) cc=37
- notify (databroker/src/broker.rs:1193) cc=13
- update (databroker/src/broker.rs:1376) cc=22

### High Nesting Functions (depth > 3)
- to_regex_string (databroker/src/glob.rs:88) depth=6
- should_match_signals (databroker/src/glob.rs:1141) depth=6
- should_match_signals (databroker/src/glob.rs:2546) depth=4
- try_from_json_array (databroker/src/vss.rs:210) depth=5
- try_from_json_value (databroker/src/vss.rs:263) depth=4
- add_entry (databroker/src/vss.rs:409) depth=5
- determine_change_type (databroker/src/vss.rs:513) depth=4
- test_parse_vss (databroker/src/vss.rs:549) depth=8
- add_kuksa_attribute (databroker/src/main.rs:54) depth=7
- read_metadata_file (databroker/src/main.rs:115) depth=10
- unlink_unix_domain_socket (databroker/src/main.rs:185) depth=5
- main (databroker/src/main.rs:194) depth=8
- greater_than (databroker/src/types.rs:137) depth=6
- equals (databroker/src/types.rs:308) depth=6
- is_expired (databroker/src/permissions.rs:228) depth=5
- extend_with (databroker/src/permissions.rs:250) depth=4
- build (databroker/src/permissions.rs:290) depth=4
- diff (databroker/src/broker.rs:278) depth=7
- validate (databroker/src/broker.rs:304) depth=5
- validate_allowed_type (databroker/src/broker.rs:326) depth=5

### Large Functions (LOC > 100)
- add_entry (databroker/src/vss.rs:409) loc=103
- test_parse_vss (databroker/src/vss.rs:549) loc=150
- main (databroker/src/main.rs:194) loc=391
- greater_than (databroker/src/types.rs:137) loc=152
- equals (databroker/src/types.rs:308) loc=180
- test_float_equals (databroker/src/types.rs:977) loc=111
- validate_allowed (databroker/src/broker.rs:366) loc=130
- validate_value (databroker/src/broker.rs:519) loc=234
- notify (databroker/src/broker.rs:952) loc=136
- test_get_set_datapoint (databroker/src/broker.rs:2749) loc=166
- test_get_set_allowed_values (databroker/src/broker.rs:2917) loc=128
- test_multi_subscribe (databroker/src/broker.rs:3824) loc=104
- test_subscribe_after_new_registration (databroker/src/broker.rs:3930) loc=146
- test_subscribe_set_multiple (databroker/src/broker.rs:4078) loc=120
- test_string_array_allowed_values (databroker/src/broker.rs:4346) loc=172
- test_subscribe_and_get_buffer_size (databroker/src/broker.rs:4772) loc=104
- handle_viss_v2 (databroker/src/viss/server.rs:115) loc=139
- get (databroker/src/viss/v2/server.rs:92) loc=149
- set (databroker/src/viss/v2/server.rs:242) loc=103
- open_provider_stream (databroker/src/grpc/kuksa_val_v2/val.rs:841) loc=163

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 1058 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 400 per-function CFGs (cc > 3)
- `statemachines.json` — 5 state machine patterns
- `metrics.json` — 1058 function metrics
- `communication.json` — 15 protocol patterns
- `dependencies.json` — 0 external dependencies
