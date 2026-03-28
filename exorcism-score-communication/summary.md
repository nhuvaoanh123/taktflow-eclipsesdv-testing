# Project Analysis: score-communication

## Overview
| Item | Value |
|------|-------|
| Languages | C, C++, Python, Rust |
| Build System | Bazel |
| Total Files | 1126 |
| Total LOC | 168,550 |
| Total Functions | 6414 |
| State Machines | 1 |
| Communication Patterns | 3 |
| External Dependencies | 0 |

## Language Breakdown
- **C**: 435 files, 39,359 LOC
- **C++**: 618 files, 117,303 LOC
- **Python**: 43 files, 3,133 LOC
- **Rust**: 30 files, 8,755 LOC

## Architecture Overview
Build system: **Bazel**

### State Machines Detected
- `score/mw/com/example/ipc_bridge/ipc_bridge.rs:158` — match on `args.mode` (2 states)

### Communication Protocols
- **gRPC_service**: 1 occurrence(s)
- **MQTT_topic**: 2 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- score (score/mw/service/provided_service_container.h:24) cc=46
- mw (score/mw/service/provided_service_container.h:26) cc=38
- service (score/mw/service/provided_service_container.h:28) cc=30
- ProvidedServicesBase (score/mw/service/provided_service_container.h:31) cc=24
- Count (score/mw/service/provided_service_container.h:41) cc=16
- ProvidedServiceContainer (score/mw/service/provided_service_container.h:184) cc=42
- mw (score/mw/service/proxy_needs.h:29) cc=45
- service (score/mw/service/proxy_needs.h:31) cc=45
- score (score/mw/service/backend/mw_com/provided_service_builder.h:22) cc=20
- mw (score/mw/service/backend/mw_com/provided_service_builder.h:24) cc=20
- service (score/mw/service/backend/mw_com/provided_service_builder.h:26) cc=20
- backend (score/mw/service/backend/mw_com/provided_service_builder.h:36) cc=18
- mw_com (score/mw/service/backend/mw_com/provided_service_builder.h:38) cc=18
- ProvidedServiceBuilder (score/mw/service/backend/mw_com/provided_service_builder.h:42) cc=17
- score (score/mw/service/backend/mw_com/provided_service_decorator.h:22) cc=31
- mw (score/mw/service/backend/mw_com/provided_service_decorator.h:24) cc=31
- service (score/mw/service/backend/mw_com/provided_service_decorator.h:26) cc=31
- backend (score/mw/service/backend/mw_com/provided_service_decorator.h:28) cc=31
- mw_com (score/mw/service/backend/mw_com/provided_service_decorator.h:30) cc=31
- score (score/mw/service/backend/mw_com/single_instantiation_strategy.h:21) cc=21

### High Nesting Functions (depth > 3)
- test_service_discovery_offer_and_search (score/mw/com/test/service_discovery_offer_and_search/service_discovery_offer_and_search_test.py:28) depth=5
- test_service_discovery_offer_and_search (score/mw/com/test/service_discovery_offer_and_search/integration_test/test_service_discovery_offer_and_search.py:17) depth=5
- test_shared_memory_storage (score/mw/com/test/shared_memory_storage/integration_test/test_shared_memory_storage.py:17) depth=5
- test_service_discovery_search_and_offer_test (score/mw/com/test/service_discovery_search_and_offer/service_discovery_search_and_offer_test.py:30) depth=5
- test_service_discovery_search_and_offer (score/mw/com/test/service_discovery_search_and_offer/integration_test/test_service_discovery_search_and_offer.py:17) depth=5
- run_inotify_test (score/mw/com/test/inotify/inotify_test.cpp:84) depth=5
- test_subscribe_handler (score/mw/com/test/subscribe_handler/integration_test/test_subscribe_handler.py:17) depth=5
- <anonymous> (score/mw/com/test/partial_restart/provider_restart_max_subscribers/consumer.cpp:223) depth=4
- test_check_values_created_from_config (score/mw/com/test/check_values_created_from_config/integration_test/test_check_values_created_from_config.py:15) depth=5
- <anonymous> (score/mw/com/test/common_test_resources/sample_sender_receiver.cpp:424) depth=4
- <anonymous> (score/mw/com/test/common_test_resources/sample_sender_receiver.cpp:661) depth=4
- <anonymous> (score/mw/com/test/common_test_resources/sctf_test_runner.cpp:228) depth=8
- test_generic_proxy (score/mw/com/test/generic_proxy/integration_test/test_generic_proxy.py:17) depth=5
- main (score/mw/com/test/bigdata/bigdata.rs:34) depth=5
- test_bigdata_exchange (score/mw/com/test/bigdata/integration_test/test_bigdata.py:15) depth=5
- test_hello_world_via_binary_execution (score/mw/com/test/field_initial_value/integration_test/test_field_initial_value.py:15) depth=5
- test_data_slots_read_only_basic (score/mw/com/test/data_slots_read_only/integration_test/test_data_slots_read_only.py:17) depth=5
- test_find_any_semantics (score/mw/com/test/find_any_semantics/integration_test/test_find_any_semantics.py:17) depth=5
- test_multiple_proxies (score/mw/com/test/multiple_proxies/integration_test/test_multiple_proxies.py:17) depth=5
- subscribe (score/mw/com/impl/rust/proxy_bridge.rs:415) depth=4

### Large Functions (LOC > 100)
- mw (score/mw/service/proxy_needs.h:29) loc=125
- service (score/mw/service/proxy_needs.h:31) loc=122
- score (score/mw/service/backend/mw_com/provided_services.h:25) loc=105
- mw (score/mw/service/backend/mw_com/provided_services.h:27) loc=102
- main (score/mw/com/test/unsubscribe_deadlock/unsubscribe_deadlock_application.cpp:105) loc=110
- main (score/mw/com/test/shared_memory_storage/shared_memory_storage_application.cpp:102) loc=287
- run_inotify_test (score/mw/com/test/inotify/inotify_test.cpp:84) loc=116
- DoConsumerCrash (score/mw/com/test/service_discovery_during_provider_crash/service_discovery_during_provider_crash_application.cpp:91) loc=144
- main (score/mw/com/test/separate_reception_threads/separate_reception_threads_application.cpp:112) loc=117
- run_receiver (score/mw/com/test/smokeyeyes/smokeyeyes.cpp:218) loc=162
- main (score/mw/com/test/smokeyeyes/smokeyeyes.cpp:384) loc=129
- DoConsumerActions (score/mw/com/test/partial_restart/consumer_restart/consumer.cpp:46) loc=172
- DoConsumerRestart (score/mw/com/test/partial_restart/consumer_restart/consumer_restart_application.cpp:98) loc=213
- PerformSecondConsumerActions (score/mw/com/test/partial_restart/proxy_restart_shall_not_affect_other_proxies/consumer.cpp:187) loc=117
- DoControllerActions (score/mw/com/test/partial_restart/proxy_restart_shall_not_affect_other_proxies/application.cpp:46) loc=250
- <anonymous> (score/mw/com/test/partial_restart/provider_restart_max_subscribers/consumer.cpp:110) loc=112
- <anonymous> (score/mw/com/test/partial_restart/provider_restart_max_subscribers/consumer.cpp:223) loc=122
- DoProviderRestart (score/mw/com/test/partial_restart/provider_restart_max_subscribers/provider_restart_max_subscribers_application.cpp:94) loc=243
- main (score/mw/com/test/partial_restart/checks_number_of_allocations/application.cpp:101) loc=113
- DoConsumerActionsWithProxy (score/mw/com/test/partial_restart/provider_restart/consumer.cpp:37) loc=219

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 6414 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 1054 per-function CFGs (cc > 3)
- `statemachines.json` — 1 state machine patterns
- `metrics.json` — 6414 function metrics
- `communication.json` — 3 protocol patterns
- `dependencies.json` — 0 external dependencies
