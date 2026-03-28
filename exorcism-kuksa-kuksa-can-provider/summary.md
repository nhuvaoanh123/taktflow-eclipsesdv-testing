# Project Analysis: kuksa-kuksa-can-provider

## Overview
| Item | Value |
|------|-------|
| Languages | Python |
| Build System | Unknown |
| Total Files | 27 |
| Total LOC | 3,458 |
| Total Functions | 161 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 35 |

## Language Breakdown
- **Python**: 27 files, 3,458 LOC

## Architecture Overview
Build system: **Unknown**

## Key Findings

### High Complexity Functions (cc > 10)
- start (dbcfeeder.py:104) cc=13
- _run_receiver (dbcfeeder.py:210) cc=17
- _get_kuksa_val_client (dbcfeeder.py:357) cc=17
- main (dbcfeeder.py:477) cc=40
- _serial_procesor (dbcfeederlib/elm2canbridge.py:104) cc=11
- transform_value (dbcfeederlib/dbc2vssmapper.py:136) cc=17
- _extract_verify_transform (dbcfeederlib/dbc2vssmapper.py:289) cc=12
- _analyze_dbc2vss (dbcfeederlib/dbc2vssmapper.py:330) cc=12
- _analyze_vss2dbc (dbcfeederlib/dbc2vssmapper.py:377) cc=12

### High Nesting Functions (depth > 3)
- start (dbcfeeder.py:104) depth=7
- _register_datapoints (dbcfeeder.py:192) depth=5
- _run_receiver (dbcfeeder.py:210) depth=11
- _vss_update (dbcfeeder.py:272) depth=7
- _parse_config (dbcfeeder.py:328) depth=7
- main (dbcfeeder.py:477) depth=5
- _serial_reader (dbcfeederlib/elm2canbridge.py:72) depth=5
- _serial_procesor (dbcfeederlib/elm2canbridge.py:104) depth=7
- _init_elm (dbcfeederlib/elm2canbridge.py:153) depth=7
- _read_response (dbcfeederlib/elm2canbridge.py:218) depth=5
- __init__ (dbcfeederlib/dbcparser.py:40) depth=7
- _populate_signal_to_message_map (dbcfeederlib/dbcparser.py:80) depth=9
- get_signals_by_frame_id (dbcfeederlib/dbcparser.py:150) depth=5
- _rx_worker (dbcfeederlib/dbcreader.py:39) depth=5
- _process_log (dbcfeederlib/canplayer.py:48) depth=7
- recv (dbcfeederlib/canclient.py:37) depth=5
- send (dbcfeederlib/canclient.py:54) depth=5
- start (dbcfeederlib/databrokerclientwrapper.py:71) depth=5
- on_broker_connectivity_change (dbcfeederlib/databrokerclientwrapper.py:113) depth=7
- is_signal_defined (dbcfeederlib/databrokerclientwrapper.py:132) depth=5

### Large Functions (LOC > 100)
- main (dbcfeeder.py:477) loc=125

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 161 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 40 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 161 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 35 external dependencies
