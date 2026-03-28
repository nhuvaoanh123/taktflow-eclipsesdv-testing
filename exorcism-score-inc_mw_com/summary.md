# Project Analysis: score-inc_mw_com

## Overview
| Item | Value |
|------|-------|
| Languages | C++, C, Python |
| Build System | Unknown |
| Total Files | 770 |
| Total LOC | 106,815 |
| Total Functions | 4467 |
| State Machines | 0 |
| Communication Patterns | 3 |
| External Dependencies | 0 |

## Language Breakdown
- **C++**: 425 files, 78,580 LOC
- **C**: 290 files, 26,770 LOC
- **Python**: 55 files, 1,465 LOC

## Architecture Overview
Build system: **Unknown**

### Communication Protocols
- **gRPC_service**: 1 occurrence(s)
- **MQTT_topic**: 2 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- bmw (mw/com/types.h:41) cc=28
- mw (mw/com/types.h:43) cc=28
- com (mw/com/types.h:45) cc=28
- run_service (mw/com/test/service_discovery_offer_and_search/service.cpp:45) cc=14
- main (mw/com/test/reserving_skeleton_slots/reserving_skeleton_slots_application.cpp:111) cc=37
- main (mw/com/test/shared_memory_storage/shared_memory_storage_application.cpp:103) cc=83
- bmw (mw/com/test/shared_memory_storage/test_resources.h:36) cc=15
- run_service (mw/com/test/service_discovery_search_and_offer/service.cpp:44) cc=14
- run_inotify_test (mw/com/test/inotify/inotify_test.cpp:91) cc=100
- DoChildActions (mw/com/test/flock/flock_test.cpp:56) cc=43
- CheckSharedLockedFile (mw/com/test/flock/flock_test.cpp:126) cc=15
- CheckExclusiveLockedFile (mw/com/test/flock/flock_test.cpp:163) cc=12
- LockBothFilesExclusively (mw/com/test/flock/flock_test.cpp:199) cc=17
- WaitForChildFinished (mw/com/test/flock/flock_test.cpp:239) cc=33
- main (mw/com/test/flock/flock_test.cpp:299) cc=37
- message_sender (mw/com/test/separate_reception_threads/separate_reception_threads_application.cpp:57) cc=19
- main (mw/com/test/separate_reception_threads/separate_reception_threads_application.cpp:113) cc=55
- run_sender (mw/com/test/smokeyeyes/smokeyeyes.cpp:153) cc=40
- run_receiver (mw/com/test/smokeyeyes/smokeyeyes.cpp:214) cc=70
- main (mw/com/test/smokeyeyes/smokeyeyes.cpp:378) cc=63

### High Nesting Functions (depth > 3)
- test_service_discovery_offer_and_search (mw/com/test/service_discovery_offer_and_search/service_discovery_offer_and_search_test.py:28) depth=5
- test_service_discovery_search_and_offer_test (mw/com/test/service_discovery_search_and_offer/service_discovery_search_and_offer_test.py:30) depth=5
- run_inotify_test (mw/com/test/inotify/inotify_test.cpp:91) depth=5
- <anonymous> (mw/com/test/partial_restart/provider_restart_max_subscribers/consumer.cpp:255) depth=4
- <anonymous> (mw/com/test/common_test_resources/sample_sender_receiver.cpp:412) depth=4
- <anonymous> (mw/com/test/common_test_resources/timeout_supervisor.cpp:67) depth=4
- <anonymous> (mw/com/test/common_test_resources/sctf_test_runner.cpp:234) depth=8
- test_field_initial_value (mw/com/test/field_initial_value/sct/field_initial_value_test.py:30) depth=5
- test_lola_data_slots_read_only (mw/com/test/data_slots_read_only/sct/data_slots_read_only_test.py:35) depth=7
- test_ara_com_mw_com_coexistence (mw/com/test/twoface/sct/mw_com_coexistence_test.py:33) depth=5
- test_find_all_semantics (mw/com/test/find_any_semantics/sct/find_any_semantics_test.py:29) depth=5
- RegisterPid (mw/com/impl/bindings/lola/uid_pid_mapping.cpp:112) depth=4
- <anonymous> (mw/com/impl/bindings/lola/transaction_log.cpp:156) depth=4
- TEST (mw/com/impl/bindings/lola/event_data_control_composite_test.cpp:464) depth=4
- com (mw/com/impl/bindings/lola/messaging/handler_base.h:32) depth=5
- impl (mw/com/impl/bindings/lola/messaging/handler_base.h:34) depth=5
- lola (mw/com/impl/bindings/lola/messaging/handler_base.h:36) depth=5
- HandlerBase (mw/com/impl/bindings/lola/messaging/handler_base.h:39) depth=5
- further_ids_avail (mw/com/impl/bindings/lola/messaging/handler_base.h:83) depth=5
- test_basic_message_passing_commander_first (mw/com/message_passing/test/sct/test_basic_message_passing.py:40) depth=5

### Large Functions (LOC > 100)
- main (mw/com/test/shared_memory_storage/shared_memory_storage_application.cpp:103) loc=282
- run_inotify_test (mw/com/test/inotify/inotify_test.cpp:91) loc=116
- main (mw/com/test/separate_reception_threads/separate_reception_threads_application.cpp:113) loc=133
- run_receiver (mw/com/test/smokeyeyes/smokeyeyes.cpp:214) loc=157
- main (mw/com/test/smokeyeyes/smokeyeyes.cpp:378) loc=141
- DoConsumerActions (mw/com/test/partial_restart/consumer_restart/consumer.cpp:37) loc=163
- DoConsumerRestart (mw/com/test/partial_restart/consumer_restart/consumer_restart_application.cpp:99) loc=199
- PerformSecondConsumerActions (mw/com/test/partial_restart/proxy_restart_shall_not_affect_other_proxies/consumer.cpp:184) loc=114
- DoControllerActions (mw/com/test/partial_restart/proxy_restart_shall_not_affect_other_proxies/application.cpp:45) loc=250
- <anonymous> (mw/com/test/partial_restart/provider_restart_max_subscribers/consumer.cpp:133) loc=121
- <anonymous> (mw/com/test/partial_restart/provider_restart_max_subscribers/consumer.cpp:255) loc=141
- DoProviderRestart (mw/com/test/partial_restart/provider_restart_max_subscribers/provider_restart_max_subscribers_application.cpp:94) loc=216
- main (mw/com/test/partial_restart/checks_number_of_allocations/application.cpp:100) loc=113
- DoConsumerActionsWithProxy (mw/com/test/partial_restart/provider_restart/consumer.cpp:33) loc=222
- DoConsumerActions (mw/com/test/partial_restart/provider_restart/consumer.cpp:269) loc=109
- DoProviderActions (mw/com/test/partial_restart/provider_restart/provider.cpp:115) loc=107
- DoProviderNormalRestartSubscribedProxy (mw/com/test/partial_restart/provider_restart/controller.cpp:48) loc=255
- DoProviderCrashRestartSubscribedProxy (mw/com/test/partial_restart/provider_restart/controller.cpp:309) loc=231
- main (mw/com/test/check_values_created_from_config/check_values_created_from_config_application.cpp:147) loc=102
- <anonymous> (mw/com/test/common_test_resources/sample_sender_receiver.cpp:412) loc=138

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 4467 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 786 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 4467 function metrics
- `communication.json` — 3 protocol patterns
- `dependencies.json` — 0 external dependencies
