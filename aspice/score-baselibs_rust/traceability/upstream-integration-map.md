---
document_id: INTEG-BLR
title: "Upstream Integration Map — score-baselibs_rust"
version: "1.0"
status: active
date: 2026-03-20
---

# Upstream S-CORE ↔ Taktflow ASPICE Integration Map — Base Libraries (Rust)

## Upstream Safety Documents (Complete)

Source: `score-baselibs_rust/docs/`

| Document | S-CORE ID | ASIL | Content |
|---|---|---|---|
| `module_docs/safety_mgt/module_safety_plan.rst` | `doc__baselibs_rust_safety_plan` | B | Safety plan with work product list |
| `module_docs/safety_mgt/module_safety_plan_fdr.rst` | FDR record | B | Formal design review of safety plan |
| `module_docs/safety_mgt/module_safety_package_fdr.rst` | FDR record | B | Safety package review |
| `module_docs/manual/safety_manual.rst` | Safety manual | B | Integration constraints and AoUs |
| `module_docs/verification/module_verification_report.rst` | Verification report | B | Test results and coverage |
| `module_docs/release/release_note.rst` | Release note | B | Version history |

## Log Component Safety Analysis

Source: `docs/baselibs_rust/log/safety_analysis/`

| Document | Content | Taktflow Mapping |
|---|---|---|
| `fmea.rst` | Failure modes for Rust log library | — (QM component) |
| `dfa.rst` | Dependent failure analysis for log | — (QM component) |

## Log Component Architecture

Source: `docs/baselibs_rust/log/architecture/`

5 PlantUML diagrams:
- `interface.puml` — Log interface definition
- `static_view.puml` — Static architecture
- `log_with_global_logger.puml` — Global logger usage
- `log_with_local_logger.puml` — Local logger usage
- `register_global_logger.puml` — Registration sequence

## Containers Component (ASIL-B)

Source: `docs/baselibs_rust/containers_rust/`

| Document | Content | Taktflow Mapping |
|---|---|---|
| `architecture/index.rst` | Fixed-size container architecture | SG-BLR-001 (Container Memory Safety) |
| `requirements/index.rst` | Container requirements | SWR-BLR-CON-001 |

## Gaps

1. **Containers comp_req**: Template only — not yet populated with real requirements.
2. **FMEA for containers**: Not yet created (only log has FMEA). Our SG-BLR-001 fills this gap.
