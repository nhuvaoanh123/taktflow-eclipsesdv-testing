---
document_id: SCORE-COM-INDEX
title: "Eclipse S-CORE Communication Module (LoLa) — ASPICE + ASIL-B Document Registry"
version: "1.0"
status: active
date: 2026-03-20
---

# LoLa (score-communication) — Document Registry

Pilot ASPICE Level 2 + ASIL-B documentation for the Eclipse S-CORE Communication Module.

## Requirement Hierarchy

```
STK-COM-xxx  Stakeholder Requirements (what users need)
  └── SYS-COM-xxx  System Requirements (what the system must do)
       ├── SG-COM-xxx  Safety Goals (ISO 26262-3, ASIL-B)
       │    └── FSR-COM-xxx  Functional Safety Requirements (ISO 26262-3)
       │         └── TSR-COM-xxx  Technical Safety Requirements (ISO 26262-4)
       │              ├── SSR-COM-xxx  Software Safety Requirements (ISO 26262-6, per component)
       │              └── HSR-COM-xxx  Hardware Safety Requirements (ISO 26262-5, N/A — pure SW)
       └── SWR-COM-xxx  Software Requirements (ASPICE SWE.1, per component)
            └── @verifies in test code (bidirectional)
```

## ID Format

| Level | Pattern | Example | Scope |
|---|---|---|---|
| STK | `STK-COM-NNN` | STK-COM-001 | Stakeholder need |
| SYS | `SYS-COM-NNN` | SYS-COM-001 | System requirement |
| SG | `SG-COM-NNN` | SG-COM-001 | Safety goal |
| FSR | `FSR-COM-NNN` | FSR-COM-001 | Functional safety |
| TSR | `TSR-COM-NNN` | TSR-COM-001 | Technical safety |
| SSR | `SSR-COM-[COMP]-NNN` | SSR-COM-SHM-001 | SW safety per component |
| SWR | `SWR-COM-[COMP]-NNN` | SWR-COM-SHM-001 | SW requirement per component |

Component prefixes: SHM (shared_mem), MP (message_passing), SK (skeleton), PX (proxy), SD (service_discovery), EF (events_fields), MT (methods), RT (runtime), PR (partial_restart), TR (tracing), CF (configuration)

## Document Map

| ASPICE Area | Document | Status |
|---|---|---|
| — | `INDEX.md` (this file) | Active |
| STK | `SWE.1-requirements-analysis/stakeholder-requirements.md` | Active |
| SYS | `SWE.1-requirements-analysis/system-requirements.md` | Active |
| SWE.1 | `SWE.1-requirements-analysis/sw-requirements/SWR-COM-*.md` | Active |
| SWE.2 | `SWE.2-architectural-design/architecture.md` | Active |
| SWE.3 | `SWE.3-detailed-design/detailed-design-*.md` | Active |
| SWE.4 | `SWE.4-unit-verification/unit-test-plan.md` | Active |
| SWE.5 | `SWE.5-integration-test/integration-test-plan.md` | Active |
| SWE.6 | `SWE.6-qualification-test/qualification-test-plan.md` | Active |
| SAF/SG | `SAF-functional-safety/safety-goals.md` | Active |
| SAF/FSR | `SAF-functional-safety/functional-safety-reqs.md` | Active |
| SAF/TSR | `SAF-functional-safety/technical-safety-reqs.md` | Active |
| SAF/SSR | `SAF-functional-safety/sw-safety-reqs.md` | Active |
| SAF/FMEA | `SAF-functional-safety/fmea.md` | Active |
| SAF/DFA | `SAF-functional-safety/dfa.md` | Active |
| SAF/Plan | `SAF-functional-safety/safety-plan.md` | Active |
| MAN.3 | `MAN.3-project-management/MAN3-project-management.rst` | Created |
| SUP.8 | `SUP.8-configuration-management/SUP8-configuration-management.rst` | Created |
| SUP.9 | `SUP.9-problem-resolution/problem-resolution.md` | Planned |
| SEC | `SEC-security/security-analysis.md` | Planned |
| REL | `REL-release-management/release-plan.md` | Planned |
| TRACE | `traceability/traceability-matrix.md` | Auto-generated |

## Traceability Tags

In source code:
```cpp
/**
 * @safety_req SSR-COM-SHM-001, SSR-COM-SHM-002
 */
void SharedMemoryManager::allocateSlot() { ... }
```

In test code:
```cpp
/** @verifies SWR-COM-SHM-001 */
TEST(SharedMemTest, AllocateSlot_Success) { ... }
```

In test YAML:
```yaml
verifies:
  - SWR-COM-SHM-001
  - SSR-COM-SHM-001
  - SG-COM-001
```

## HITL-LOCK Convention

```markdown
<!-- HITL-LOCK START:COMMENT-BLOCK-FSR-COM-001 -->
**HITL Review (<reviewer>) — Reviewed: YYYY-MM-DD:** [Review comment]
<!-- HITL-LOCK END:COMMENT-BLOCK-FSR-COM-001 -->
```

Rules:
- AI must NEVER edit, reformat, move, or delete text inside HITL-LOCK blocks
- Append-only outside locks
