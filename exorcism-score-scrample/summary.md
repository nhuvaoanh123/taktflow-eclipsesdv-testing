# Project Analysis: score-scrample

## Overview
| Item | Value |
|------|-------|
| Languages | C++, C, Go, Python, Rust |
| Build System | Bazel, Python/pyproject |
| Total Files | 43 |
| Total LOC | 3,294 |
| Total Functions | 119 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 1 |

## Language Breakdown
- **C++**: 5 files, 721 LOC
- **C**: 3 files, 385 LOC
- **Go**: 21 files, 1,225 LOC
- **Python**: 3 files, 291 LOC
- **Rust**: 11 files, 672 LOC

## Architecture Overview
Build system: **Bazel, Python/pyproject**

## Key Findings

### High Complexity Functions (cc > 10)
- <anonymous> (src/sample_sender_receiver.cpp:275) cc=53
- <anonymous> (src/sample_sender_receiver.cpp:406) cc=19
- main (src/main.cpp:85) cc=28
- assert_handler (src/assert_handler.cpp:30) cc=30
- EventSenderReceiver (src/sample_sender_receiver.h:30) cc=12
- Run (scorex/internal/service/projectinit/service.go:33) cc=13
- Generate (scorex/internal/service/skeleton/generator.go:62) cc=18
- <anonymous> (scorex/internal/service/skeleton/generator.go:85) cc=12
- Load (scorex/internal/service/knowngood/loader.go:15) cc=14
- ApplicableModulePresets (scorex/internal/config/module_presets.go:62) cc=12
- <anonymous> (scorex/cmd/init.go:51) cc=11
- runInitInteractive (scorex/cmd/init.go:116) cc=31
- applyPresetNonInteractive (scorex/cmd/init.go:218) cc=16
- applyPresetInteractive (scorex/cmd/init.go:240) cc=29
- mergeUnique (scorex/cmd/init.go:297) cc=11
- validateInitOptions (scorex/cmd/init.go:323) cc=17
- promptModules (scorex/cmd/init.go:366) cc=27

### High Nesting Functions (depth > 3)
- <anonymous> (src/sample_sender_receiver.cpp:275) depth=4
- ResolveModules (scorex/internal/service/module/resolver.go:47) depth=5
- undotifyPath (scorex/internal/service/skeleton/generator.go:50) depth=5
- Generate (scorex/internal/service/skeleton/generator.go:62) depth=5
- Load (scorex/internal/service/knowngood/loader.go:15) depth=5
- LoadModulePresets (scorex/internal/config/module_presets.go:26) depth=5
- ApplicableModulePresets (scorex/internal/config/module_presets.go:62) depth=5
- FindModulePreset (scorex/internal/config/module_presets.go:76) depth=5
- dedupeStrings (scorex/internal/config/module_presets.go:97) depth=5
- <anonymous> (scorex/cmd/init.go:51) depth=7
- runInitInteractive (scorex/cmd/init.go:116) depth=5
- mergeUnique (scorex/cmd/init.go:297) depth=5
- validateInitOptions (scorex/cmd/init.go:323) depth=5
- promptModules (scorex/cmd/init.go:366) depth=7
- confirm (scorex/cmd/init.go:433) depth=5
- tcp_listener (feo/ad-demo/lichtblick-com/foxglove_ws_server.py:29) depth=8
- handle_client (feo/ad-demo/lichtblick-com/foxglove_ws_server.py:30) depth=7
- main (feo/ad-demo/lichtblick-com/foxglove_ws_server.py:89) depth=7

### Large Functions (LOC > 100)
- <anonymous> (src/sample_sender_receiver.cpp:275) loc=130
- runInitInteractive (scorex/cmd/init.go:116) loc=101

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 119 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 42 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 119 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 1 external dependencies
