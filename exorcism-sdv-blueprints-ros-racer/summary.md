# Project Analysis: sdv-blueprints-ros-racer

## Overview
| Item | Value |
|------|-------|
| Languages | C++, Python |
| Build System | Unknown |
| Total Files | 23 |
| Total LOC | 2,952 |
| Total Functions | 71 |
| State Machines | 0 |
| Communication Patterns | 3 |
| External Dependencies | 0 |

## Language Breakdown
- **C++**: 3 files, 621 LOC
- **Python**: 20 files, 2,331 LOC

## Architecture Overview
Build system: **Unknown**

### Communication Protocols
- **MQTT_topic**: 3 occurrence(s)

## Key Findings

### High Complexity Functions (cc > 10)
- <anonymous> (src/multiagent_plugin/src/multiagent_plugin.cpp:34) cc=12
- <anonymous> (src/multiagent_plugin/src/multiagent_plugin.cpp:250) cc=20
- <anonymous> (src/multiagent_plugin/src/multiagent_plugin.cpp:330) cc=41
- <anonymous> (src/multiagent_plugin/src/multiagent_plugin.cpp:401) cc=37
- cb (src/gap_follower/gap_follower/gap_follower.py:290) cc=12
- __init__ (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:59) cc=11

### High Nesting Functions (depth > 3)
- <anonymous> (src/multiagent_plugin/src/multiagent_plugin.cpp:330) depth=4
- <anonymous> (src/multiagent_plugin/src/multiagent_plugin.cpp:401) depth=4
- apply_disparity_extender (src/gap_follower/gap_follower/gap_follower.py:108) depth=11
- find_best_gap_index (src/gap_follower/gap_follower/gap_follower.py:137) depth=5
- cb (src/gap_follower/gap_follower/gap_follower.py:290) depth=7
- publish_visualization (src/gap_follower/gap_follower/gap_follower.py:390) depth=7
- handle_collision (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:297) depth=5
- pause_callback (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:332) depth=5
- drive_callback (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:351) depth=5
- drive_timer_callback (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:379) depth=9
- _apply_pending_pose_updates (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:403) depth=5
- timer_callback (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:459) depth=5
- pose_reset_callback (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:483) depth=7
- _publish_speed_markers (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:571) depth=5
- _publish_trajectories (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:625) depth=5
- main (demo/scripts/deploy-stack.py:89) depth=5
- main (demo/scripts/deploy-stack-fleet.py:19) depth=5
- main (scripts/generate-gap-follower-stacks.py:53) depth=5

### Large Functions (LOC > 100)
- <anonymous> (src/multiagent_plugin/src/multiagent_plugin.cpp:34) loc=196
- publish_visualization (src/gap_follower/gap_follower/gap_follower.py:390) loc=119
- __init__ (src/f1tenth_gym_ros/f1tenth_gym_ros/gym_bridge.py:59) loc=223
- launch_setup (src/f1tenth_gym_ros/launch/gym_bridge_launch.py:45) loc=110
- generate_launch_description (launch/muto.launch.py:8) loc=221

## Files Generated
- `inventory.json` — file/LOC/function counts, build system
- `callgraph.json` — 71 call relationships
- `callgraph.dot` — Graphviz DOT call graph
- `cfg/` — 24 per-function CFGs (cc > 3)
- `statemachines.json` — 0 state machine patterns
- `metrics.json` — 71 function metrics
- `communication.json` — 3 protocol patterns
- `dependencies.json` — 0 external dependencies
