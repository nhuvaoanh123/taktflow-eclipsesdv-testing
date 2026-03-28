# Project Analysis: score-inc_time

## Overview
| Item | Value |
|------|-------|
| Languages | C, C++, Python |
| Build System | Bazel, Python/pyproject |
| Total Files | 148 |
| Total LOC | 12,250 |
| Total Functions | 558 |
| State Machines | 0 |
| Communication Patterns | 17 |
| External Dependencies | 1 |

## Language Breakdown
- **C**: 67 files, 5,217 LOC
- **C++**: 79 files, 6,896 LOC
- **Python**: 2 files, 137 LOC

## Architecture Overview
Build system: **Bazel, Python/pyproject**

### Communication Protocols
- **MQTT_topic**: 17 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- flag_position (score/time/common/time_base_status.h:75) cc=11
- kCallbackCapacity (score/time/SynchronizedVehicleTime/synchronized_vehicle_time.h:62) cc=30
- TimeStatus (score/time/SynchronizedVehicleTime/synchronized_vehicle_time.h:74) cc=19
- score (score/time/SynchronizedVehicleTime/slave_timebase_notification_types.h:20) cc=90
- time (score/time/SynchronizedVehicleTime/slave_timebase_notification_types.h:22) cc=12
- score (score/time/SynchronizedVehicleTime/details/factory_shm_impl.h:21) cc=12
- time (score/time/SynchronizedVehicleTime/details/factory_shm_impl.h:23) cc=12
- Factory (score/time/SynchronizedVehicleTime/details/factory_shm_impl.h:31) cc=12
- score (score/time/SynchronizedVehicleTime/details/factory_impl.h:21) cc=12
- time (score/time/SynchronizedVehicleTime/details/factory_impl.h:23) cc=12
- Factory (score/time/SynchronizedVehicleTime/details/factory_impl.h:31) cc=12
- score (score/time/SynchronizedVehicleTime/details/tdr/receiver.h:26) cc=12
- time (score/time/SynchronizedVehicleTime/details/tdr/receiver.h:28) cc=12
- details (score/time/SynchronizedVehicleTime/details/tdr/receiver.h:30) cc=12
- tdr (score/time/SynchronizedVehicleTime/details/tdr/receiver.h:32) cc=12
- <anonymous> (score/time/HighPrecisionLocalSteadyClock/details/qtime/qclock.cpp:34) cc=15
- score (score/TimeDaemon/code/common/data_types/ptp_time_info.h:22) cc=120
- td (score/TimeDaemon/code/common/data_types/ptp_time_info.h:24) cc=120
- <anonymous> (score/TimeDaemon/code/common/data_types/ptp_time_info.cpp:38) cc=14
- <anonymous> (score/TimeDaemon/code/common/data_types/ptp_time_info.cpp:49) cc=26

### High Nesting Functions (depth > 3)
- <anonymous> (score/TimeDaemon/code/application/job_runner/job_runner.cpp:52) depth=4
- <anonymous> (score/TimeDaemon/code/verification_machine/svt/validators/time_jumps_validator.cpp:56) depth=4

### Large Functions (LOC > 100)
- kCallbackCapacity (score/time/SynchronizedVehicleTime/synchronized_vehicle_time.h:62) loc=132
- TimeStatus (score/time/SynchronizedVehicleTime/synchronized_vehicle_time.h:74) loc=119
- score (score/time/SynchronizedVehicleTime/slave_timebase_notification_types.h:20) loc=197
- score (score/TimeDaemon/code/common/data_types/ptp_time_info.h:22) loc=146
- td (score/TimeDaemon/code/common/data_types/ptp_time_info.h:24) loc=143
- score (score/TimeDaemon/code/control_flow_divider/core/control_flow_divider.h:30) loc=112
- score (score/TimeDaemon/code/verification_machine/core/verification_machine.h:27) loc=107
- score (score/TimeDaemon/code/ptp_machine/core/ptp_machine.h:25) loc=106
- score (score/TimeDaemon/code/ipc/core/shared_memory_handler.h:25) loc=161
- td (score/TimeDaemon/code/ipc/core/shared_memory_handler.h:27) loc=158
- score (score/TimeDaemon/code/ipc/svt/svt_time_info.h:25) loc=164
- td (score/TimeDaemon/code/ipc/svt/svt_time_info.h:27) loc=161
- svt (score/TimeDaemon/code/ipc/svt/svt_time_info.h:29) loc=143

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 558 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 115 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 558 function metrics
- `communication.json` — 17 protocol patterns
- `dependencies.json` — 1 external dependencies
