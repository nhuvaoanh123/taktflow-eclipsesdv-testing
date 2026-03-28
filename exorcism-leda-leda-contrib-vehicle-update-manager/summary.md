# Project Analysis: leda-leda-contrib-vehicle-update-manager

## Overview
| Item | Value |
|------|-------|
| Languages | Go |
| Build System | Go modules |
| Total Files | 87 |
| Total LOC | 10,459 |
| Total Functions | 676 |
| State Machines | 0 |
| Communication Patterns | 3 |
| External Dependencies | 84 |

## Language Breakdown
- **Go**: 87 files, 10,459 LOC

## Architecture Overview
Build system: **Go modules**

### Communication Protocols
- **MQTT_topic**: 3 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- handleResourceEvent (updatem/things/features_update_orchestrator_event_handler.go:105) cc=11
- run (updatem/events/events_sinks_dispatcher.go:101) cc=21
- TestSubscribe (updatem/events/events_test.go:62) cc=12
- assertSelfUpdateOperationResult (updatem/orchestration/selfupdate/self_update_operation_test.go:644) cc=11
- assertSelfUpdateResult (updatem/orchestration/selfupdate/self_update_mgr_test.go:253) cc=15
- Apply (updatem/orchestration/selfupdate/self_update_mgr.go:48) cc=13
- handleSelfUpdateDesiredStateFeedback (updatem/orchestration/selfupdate/self_update_operation.go:78) cc=26
- isStateTechCodeSupported (updatem/orchestration/selfupdate/self_update_operation.go:157) cc=15
- createApplyOptions (updatem/orchestration/k8s/k8s_orchestration_mgr_apply.go:61) cc=13
- registryInit (updatem/orchestration/updateorchestrator/update_orchestrator_mgr_init.go:49) cc=15
- Apply (updatem/orchestration/updateorchestrator/update_orchestrator_mgr.go:40) cc=22
- TestRunLock (updatem/daemon/daemon_test.go:243) cc=12
- loadLocalConfig (updatem/daemon/daemon_config_util.go:104) cc=11
- runDaemon (updatem/daemon/daemon_start.go:62) cc=11

### High Nesting Functions (depth > 3)
- AssertError (updatem/pkg/testutil/assertions.go:23) depth=7
- handleEvents (updatem/things/features_update_orchestrator_event_handler.go:24) depth=4
- handleResourceEvent (updatem/things/features_update_orchestrator_event_handler.go:105) depth=5
- TestValdiateHash (updatem/things/features_rollouts_util_test.go:70) depth=4
- handleOrchestrationEvents (updatem/things/features_rollouts_software_updatable_manifests_event_handler.go:23) depth=8
- <anonymous> (updatem/things/features_rollouts_software_updatable_manifests_event_handler.go:28) depth=7
- TestUpdateOrchestratorOperationsHandlerNegative (updatem/things/features_update_orchestrator_test.go:86) depth=4
- TestUpdateOrchestratorOperationsHandlerProcessApply (updatem/things/features_update_orchestrator_test.go:165) depth=4
- TestUpdateOrchestratorHandleOrchestrationEvents (updatem/things/features_update_orchestrator_event_handler_test.go:30) depth=4
- TestUpdateOrchestratorHandleResourceEvents (updatem/things/features_update_orchestrator_event_handler_test.go:181) depth=4
- TestSoftwareUpdatableManifestsHandleEvents (updatem/things/features_rollouts_software_updatable_manifests_event_handler_test.go:28) depth=6
- TestSetSUInstallContext (updatem/things/features_rollouts_software_updatable_manifests_context_test.go:23) depth=6
- TestValidateSUInstallContext (updatem/things/features_rollouts_software_updatable_manifests_context_test.go:65) depth=4
- TestGetSUInstallContext (updatem/things/features_rollouts_software_updatable_manifests_context_test.go:109) depth=6
- TestProcessUpdateThingDefault (updatem/things/things_update_service_internal_test.go:22) depth=8
- <anonymous> (updatem/things/things_update_service_internal_test.go:72) depth=5
- featureOperationsHandler (updatem/things/features_update_orchestrator.go:87) depth=5
- parseMultiYAML (updatem/things/features_rollouts_util.go:62) depth=5
- readResources (updatem/things/features_rollouts_util.go:86) depth=7
- validateSoftareArtifactHash (updatem/things/features_rollouts_util.go:122) depth=5

### Large Functions (LOC > 100)
- TestUpdateOrchestratorHandleOrchestrationEvents (updatem/things/features_update_orchestrator_event_handler_test.go:30) loc=150
- TestUpdateOrchestratorHandleResourceEvents (updatem/things/features_update_orchestrator_event_handler_test.go:181) loc=126
- TestSoftwareUpdatableManifestsHandleEvents (updatem/things/features_rollouts_software_updatable_manifests_event_handler_test.go:28) loc=201
- TestSUMfFeatureOperationsHandler (updatem/things/features_rollouts_software_updatable_manifests_test.go:64) loc=435
- TestMalformedSelfUpdateDesiredStateFeedback (updatem/orchestration/selfupdate/self_update_operation_test.go:21) loc=132
- TestSelfUpdateStateFailed (updatem/orchestration/selfupdate/self_update_operation_test.go:154) loc=118
- TestSelfUpdateDesiredState (updatem/orchestration/selfupdate/self_update_operation_test.go:273) loc=135
- TestApply (updatem/orchestration/selfupdate/self_update_mgr_test.go:39) loc=166
- TestApply (updatem/orchestration/updateorchestrator/update_orchestrator_mgr_test.go:130) loc=114
- TestHandleConnectionStatus (updatem/orchestration/updateorchestrator/update_orchestrator_mgr_internal_test.go:61) loc=130
- TestSetCommandFlags (updatem/daemon/daemon_test.go:131) loc=111

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 676 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 113 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 676 function metrics
- `communication.json` — 3 protocol patterns
- `dependencies.json` — 84 external dependencies
