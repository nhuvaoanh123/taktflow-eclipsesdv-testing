---
document_id: INTEG-LC
title: "Upstream Integration Map — score-lifecycle (Health Monitor + Launch Manager)"
version: "1.0"
status: active
date: 2026-03-20
---

# Upstream S-CORE ↔ Taktflow ASPICE Integration Map — Lifecycle

## Upstream Status

| Aspect | Status |
|---|---|
| Requirements (comp_req) | **Template** — dummy placeholders, not yet populated |
| Architecture (health_monitor) | **Complete** — 21 architecture docs with PlantUML diagrams |
| FMEA | **Partially populated** — 3+ failure modes defined |
| DFA | **Template** — structure defined, not populated |
| Safety Plan | Not yet created for lifecycle module |

## FMEA Failure Modes (Upstream Data)

Source: `docs/module/health_monitor/safety_analysis/fmea.rst`

| ID | Title | Failure Effect | Detection | Mitigation | Taktflow Mapping |
|---|---|---|---|---|---|
| HM_FMEA_001 | Missing processing time | Background thread misses CPU → missed alive notification to Launch Daemon | Launch Daemon detects missing notification → safety reaction | AoU: integrator ensures scheduling params give sufficient CPU time. ASIL-B dev process. | **SG-LC-001** → FSR-LC-001 (Alive Supervision) |
| HM_FMEA_002 | Loss of execution | Deadlock/infinite loop → missed alive notification to Launch Daemon | Launch Daemon detects missing notification → safety reaction | ASIL-B development process | **SG-LC-001** → FSR-LC-001 |
| HM_FMEA_003 | Memory corruption of monitoring data | Corrupted supervision state → incorrect health verdict | (to be defined) | ASIL-B development process, memory protection | **SG-LC-001** → FSR-LC-002 (Deadline Supervision) |

## Architecture Documents (Upstream — Complete)

Source: `docs/module/health_monitor/architecture/`

| Document | Taktflow ASPICE Area | Content |
|---|---|---|
| `index.rst` | SWE.2 | Health monitor architecture overview |
| `dm_interface.puml` | SWE.2 | Deadline Monitor interface |
| `dm_static_architecture.puml` | SWE.2 | Deadline Monitor static view |
| `dm_usage.puml` | SWE.2 | Deadline Monitor usage sequence |
| `hbm_interface.puml` | SWE.2 | Heartbeat Monitor interface |
| `hbm_usage.puml` | SWE.2 | Heartbeat Monitor usage sequence |
| `hm_background_thread.puml` | SWE.2 | Background thread lifecycle |
| `hm_creation.puml` | SWE.2 | Health Monitor creation sequence |
| `hm_deadline.puml` | SWE.3 | Deadline supervision detailed design |
| `hm_duration_range.puml` | SWE.3 | Duration range validation |
| `hm_error.puml` | SWE.3 | Error handling sequence |
| `hm_interface.puml` | SWE.2 | Health Monitor public interface |
| `hm_shutdown.puml` | SWE.2 | Shutdown sequence |
| `hm_startup.puml` | SWE.2 | Startup sequence |
| `hm_static_architecture.puml` | SWE.2 | Static architecture diagram |
| `hm_status.puml` | SWE.3 | Status reporting |
| `hm_tag.puml` | SWE.3 | Tag-based supervision |
| `lm_interface.puml` | SWE.2 | Launch Manager interface |
| `lm_state.puml` | SWE.2 | Launch Manager state machine |
| `lm_static_architecture.puml` | SWE.2 | Launch Manager static view |
| `lm_usage.puml` | SWE.2 | Launch Manager usage sequence |

## Component Classification (Upstream)

Source: `docs/module/health_monitor/component_classification.rst`

| Component | ASIL | Role |
|---|---|---|
| Health Monitor Core | B | Alive/Deadline/Logical supervision engine |
| Deadline Monitor | B | Deadline supervision (min/max timing) |
| Heartbeat Monitor | B | Alive supervision (periodic heartbeat) |
| Launch Manager Daemon | QM | Process group management, dependency ordering |
| Lifecycle Client Library | B | Client-side API for registration |

## Taktflow Safety Goal Mapping

| Taktflow SG | Upstream FMEA | Upstream Architecture |
|---|---|---|
| SG-LC-001 (Fault Detection) | HM_FMEA_001, HM_FMEA_002, HM_FMEA_003 | hm_*, hbm_*, dm_* diagrams |
| SG-LC-002 (Orderly Shutdown) | — (not yet in FMEA) | lm_state.puml, hm_shutdown.puml |
| SG-LC-003 (External Watchdog) | — (not yet in FMEA) | hm_background_thread.puml |

## Gaps

1. **Requirements**: All upstream comp_reqs are dummy templates. Our Taktflow SG/FSR fill this gap.
2. **DFA**: Template only. Our `aspice/score-lifecycle/SAF-functional-safety/` provides initial DFA.
3. **Safety Plan**: Not yet created upstream. Our INDEX.md provides initial safety goals.
4. **Detailed Design**: `docs/module/health_monitor/detailed_design/` has static_diagram.puml — needs expansion.
