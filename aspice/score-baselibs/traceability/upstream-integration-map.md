---
document_id: INTEG-BL
title: "Upstream Integration Map — score-baselibs"
version: "1.0"
status: active
date: 2026-03-20
---

# Upstream S-CORE ↔ Taktflow ASPICE Integration Map — Base Libraries

## Upstream Documentation Structure

Source: `score-baselibs/score/` — each subdirectory contains design docs (README.md + PlantUML).

| Component | Design Docs | PlantUML Diagrams | Taktflow ASPICE Area |
|---|---|---|---|
| `score/os` | README.md, libod.md | osal_arch.puml | SWE.2 (OS Abstraction) |
| `score/os/interface/linux` | README.md | — | SWE.3 (Linux backend) |
| `score/os/interface/qnx` | README.md | — | SWE.3 (QNX backend) |
| `score/os/utils/qnx/resource_manager` | detailed_design/README.md | 6 PlantUML diagrams | SWE.3 (QNX resource mgr) |
| `score/memory` | README.md, design/README.md | — | SWE.2 (Memory abstraction) |
| `score/memory/design/shared_memory` | README.md, OffsetPtrDesign.md, offset_ptr_problems.md | 6 PlantUML diagrams | SWE.3 (Shared memory detail) |
| `score/concurrency` | README.md, design/README.md | structural_view.puml | SWE.2 (Concurrency) |
| `score/concurrency/future` | README.md, design/Readme.md | class.puml | SWE.3 (Future impl) |
| `score/result` | README.md | static_design.puml | SWE.2 (Result/Error types) |
| `score/mw/log` | README.md, design/*.md | 20+ PlantUML diagrams | SWE.3 (Logging frontend) |
| `score/json` | README.md, detailed_design/README.md | class_diagram.puml | SWE.3 (JSON lib) |
| `score/filesystem` | README.md, design/README.md | structure.puml | SWE.3 (File API) |
| `score/language/safecpp` | Readme.md + 5 sub-READMEs | — | SWE.3 (Safe C++ patterns) |
| `score/static_reflection_with_serialization` | requirements.md, ser_dser_lib.md | — | SWE.1 + SWE.3 (Serialization) |
| `score/bitmanipulation` | design/README.md | — | SWE.3 (Bit utils) |
| `score/utils` | design/README.md | — | SWE.3 (General utils) |
| `score/analysis/tracing` | flexible_circular_allocator/design/Readme.md | sequence_diagram.puml | SWE.3 (Tracing allocator) |

## ASIL Classification per Component

| Component | ASIL | Justification |
|---|---|---|
| `score/os` | **B** | All ASIL-B modules depend on OS abstraction |
| `score/os/utils/qnx/resource_manager` | **B** | QNX IPC mechanism used by safety services |
| `score/memory/shared_memory` | **B** | Used by LoLa for zero-copy IPC |
| `score/concurrency` | **B** | Lock-free primitives for safety-critical paths |
| `score/result` | **B** | Error handling without exceptions (ASIL-B mandate) |
| `score/language/safecpp` | **B** | Safe math, abort-on-exception |
| `score/mw/log` | QM | Logging is not safety-critical |
| `score/json` | QM | Data format, not safety path |
| `score/filesystem` | QM | File I/O abstraction |
| `score/static_reflection_with_serialization` | QM | Compile-time utilities |
| `score/bitmanipulation` | QM | Bit manipulation utilities |

## Key Design Docs with Safety Relevance

| Document | Content | Taktflow Safety Mapping |
|---|---|---|
| `score/memory/design/shared_memory/OffsetPtrDesign.md` | Offset pointer design for shared memory across processes | SG-BL-001 (Memory Safety) |
| `score/memory/design/shared_memory/offset_ptr_problems.md` | Known issues with offset pointers | SG-BL-001 — known limitations |
| `score/memory/design/shared_memory/bounds_checking.puml` | Bounds checking sequence diagram | FSR-BL-001 (Bounds-Checked Access) |
| `score/memory/design/shared_memory/memory_allocation.puml` | Memory allocation flow | FSR-BL-002 (No Dynamic Alloc) |
| `score/os/diagrams/osal_arch.puml` | OS abstraction layer architecture | SG-BL-003 (Platform Equivalence) |
| `score/concurrency/design/structural_view.puml` | Concurrency primitives structure | FSR-BL-003 (Lock-Free Primitives) |
| `score/language/safecpp/aborts_upon_exception/README.md` | Exception abort policy | FSR-BL-004 (Abort-on-Exception) |
| `score/language/safecpp/safe_math/Readme.md` | Overflow-safe arithmetic | SG-BL-001 (Memory Safety) |

## QNX Resource Manager (Critical for Bench)

Source: `score/os/utils/qnx/resource_manager/detailed_design/`

6 PlantUML diagrams documenting the QNX resource manager framework:
- `ResourceManager_ClassDiagram.puml` — Class structure
- `ResourceManager_ComponentDiagram.puml` — Component view
- `ResourceManager_ActivityDiagram_Initialize.puml` — Init sequence
- `ResourceManager_ActivityDiagram_Run.puml` — Run loop
- `ResourceManager_RuntimeSequenceDiagram.puml` — Runtime interactions
- `ResourceManager_StartupSequenceDiagram.puml` — Startup sequence

This is directly relevant to our Pi QNX deployment — the resource manager is how QNX services expose themselves via the `/dev/` namespace.

## Gaps

1. **Formal requirements (comp_req)**: Not present in baselibs — design docs serve as implicit requirements.
2. **FMEA/DFA**: Not created for baselibs upstream. Our SG-BL-001..003 + FSR-BL-001..005 fill this gap.
3. **Verification report**: Not present. Our SWE.4 docs reference Bazel test targets.
