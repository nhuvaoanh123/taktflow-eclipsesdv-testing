# Project Analysis: chariott-chariott

## Overview
| Item | Value |
|------|-------|
| Languages | Rust |
| Build System | Cargo |
| Total Files | 59 |
| Total LOC | 7,988 |
| Total Functions | 419 |
| State Machines | 5 |
| Communication Patterns | 0 |
| External Dependencies | 0 |

## Language Breakdown
- **Rust**: 59 files, 7,988 LOC

## Architecture Overview
Build system: **Cargo**

### State Machines Detected
- `intent_brokering/examples/applications/kv-app/src/intent_provider.rs:50` — match on `request
            .into_inner()
            .intent
            .and_then(|i| i.intent)
            .ok_or_else(|| Status::invalid_argument("Intent must be specified."))?` (5 states)
- `intent_brokering/examples/applications/simple-provider/src/intent_provider.rs:36` — match on `request
            .into_inner()
            .intent
            .and_then(|i| i.intent)
            .ok_or_else(|| Status::invalid_argument("Intent must be specified."))?` (2 states)
- `intent_brokering/examples/applications/lt-provider/src/main.rs:98` — match on `request
            .into_inner()
            .intent
            .and_then(|i| i.intent)
            .ok_or_else(|| Status::invalid_argument("Intent must be specified"))?` (2 states)
- `intent_brokering/examples/applications/invoke-command/src/intent_provider.rs:69` — match on `request
            .into_inner()
            .intent
            .and_then(|i| i.intent)
            .ok_or_else(|| Status::invalid_argument("Intent must be specified."))?` (3 states)
- `intent_brokering/tests/provider.rs:57` — match on `request
            .into_inner()
            .intent
            .and_then(|i| i.intent)
            .ok_or_else(|| Status::invalid_argument("Intent must be specified"))?` (2 states)

## Key Findings

### High Complexity Functions (cc > 10)
- refresh (intent_brokering/src/intent_broker.rs:81) cc=19
- execute (intent_brokering/src/execution.rs:60) cc=15
- system_inspect_binding_succeeds (intent_brokering/src/execution.rs:272) cc=14
- test (intent_brokering/src/execution.rs:282) cc=14
- upsert (intent_brokering/src/registry.rs:176) cc=11
- wain (intent_brokering/examples/applications/lt-consumer/src/main.rs:55) cc=18
- evaluate_docker_stats (intent_brokering/examples/applications/lt-consumer/src/main.rs:189) cc=11

### High Nesting Functions (depth > 3)
- register (service_discovery/core/src/service_registry_impl.rs:44) depth=4
- main (service_discovery/samples/simple-discovery/consumer/src/main.rs:31) depth=5
- ctrl_c_cancellation (intent_brokering/common/src/shutdown.rs:13) depth=4
- main (intent_brokering/src/main.rs:30) depth=4
- registry_prune_loop (intent_brokering/src/main.rs:110) depth=4
- refresh (intent_brokering/src/intent_broker.rs:81) depth=7
- assert_remote_fallback_binding (intent_brokering/src/intent_broker.rs:380) depth=5
- execute (intent_brokering/src/execution.rs:60) depth=5
- system_inspect_binding_succeeds (intent_brokering/src/execution.rs:272) depth=4
- prune_by (intent_brokering/src/registry.rs:128) depth=5
- filter_map_change (intent_brokering/src/registry.rs:990) depth=4
- register_subscriptions (intent_brokering/ess/src/ess.rs:169) depth=4
- deregister_subscriptions (intent_brokering/ess/src/ess.rs:243) depth=6
- event_sub_system_bench (intent_brokering/ess/benches/load_bench.rs:38) depth=9
- trace_result (intent_brokering/examples/common/src/intent_brokering/provider.rs:88) depth=4
- inspect (intent_brokering/examples/common/src/intent_brokering/api.rs:229) depth=4
- listen (intent_brokering/examples/common/src/intent_brokering/api.rs:316) depth=4
- set_intent_broker_url (intent_brokering/examples/common/src/intent_brokering/registration.rs:90) depth=5
- register (intent_brokering/examples/common/src/intent_brokering/registration.rs:122) depth=5
- register_once (intent_brokering/examples/common/src/intent_brokering/registration.rs:144) depth=5

### Large Functions (LOC > 100)
- wain (intent_brokering/examples/applications/lt-consumer/src/main.rs:55) loc=133

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 419 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 62 per-function CFGs (cc > 3)
- `statemachines.json` — 5 state machine patterns
- `metrics.json` — 419 function metrics
- `communication.json` — 0 protocol patterns
- `dependencies.json` — 0 external dependencies
