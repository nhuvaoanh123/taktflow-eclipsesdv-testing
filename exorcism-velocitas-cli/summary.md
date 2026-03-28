# Project Analysis: velocitas-cli

## Overview
| Item | Value |
|------|-------|
| Languages | TypeScript, Python |
| Build System | npm/Node |
| Total Files | 70 |
| Total LOC | 7,541 |
| Total Functions | 627 |
| State Machines | 0 |
| Communication Patterns | 0 |
| External Dependencies | 27 |

## Language Breakdown
- **TypeScript**: 64 files, 7,432 LOC
- **Python**: 6 files, 109 LOC

## Architecture Overview
Build system: **npm/Node**

## Key Findings

### High Complexity Functions (cc > 10)
- <anonymous> (src/commands/upgrade/index.ts:47) cc=13
- <anonymous> (src/commands/component/list.ts:35) cc=11
- <anonymous> (src/commands/package/index.ts:46) cc=27
- <anonymous> (src/commands/init/index.ts:219) cc=15
- runExecSpec (src/modules/exec.ts:91) cc=22
- createPythonVenv (src/modules/exec.ts:147) cc=12
- stdOutParser (src/modules/stdout-parser.ts:20) cc=12
- <anonymous> (src/modules/variables.ts:83) cc=24
- verifyGivenVariables (src/modules/variables.ts:190) cc=18
- buildErrorMessageForComponent (src/modules/variables.ts:231) cc=22
- <anonymous> (src/modules/projectConfig/projectConfigFileReader.ts:80) cc=11
- <anonymous> (src/modules/projectConfig/projectConfigFileReader.ts:97) cc=12
- <anonymous> (test/utils/mockfs.ts:56) cc=18

### High Nesting Functions (depth > 3)
- <anonymous> (src/commands/package/index.ts:46) depth=5
- <anonymous> (src/commands/init/index.ts:219) depth=5
- getLatestVersion (src/modules/semver.ts:20) depth=4
- installComponent (src/modules/setup.ts:180) depth=5
- <anonymous> (src/modules/variables.ts:83) depth=4
- verifyGivenVariables (src/modules/variables.ts:190) depth=4

### Large Functions (LOC > 100)
- <anonymous> (test/commands/upgrade/upgrade.test.ts:28) loc=190
- <anonymous> (test/commands/upgrade/upgrade.test.ts:92) loc=125
- <anonymous> (test/commands/init/init.test.ts:24) loc=192
- <anonymous> (test/commands/create/create.test.ts:72) loc=171
- <anonymous> (test/system-test/exec.stest.ts:23) loc=168
- <anonymous> (test/system-test/exec.stest.ts:24) loc=166
- <anonymous> (test/unit/variables.test.ts:46) loc=243
- <anonymous> (test/unit/variables.test.ts:147) loc=141
- <anonymous> (test/unit/projectConfigIO.test.ts:91) loc=152

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 627 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 65 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 627 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 27 external dependencies
