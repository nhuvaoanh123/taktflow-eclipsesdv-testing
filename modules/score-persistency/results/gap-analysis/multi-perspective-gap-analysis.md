---
document_id: GAP-PER-MULTI
title: "Multi-Perspective Gap Analysis — score-persistency"
version: "1.0"
status: verified
date: 2026-03-23
---

# Multi-Perspective Gap Analysis — score-persistency

Same work, 10 different eyes. Each stakeholder asks different questions.

**Module:** score_persistency v0.0.0 | **Safety Level:** ASIL-D | **Languages:** C++ + Rust (dual KVS)

---

## 1. ASPICE Auditor

*"Show me the ASIL-D evidence chain."*

| # | Gap | Severity | Status | Issue |
|---|-----|----------|--------|-------|
| 1 | ASPICE docs exist but completeness unknown | High | OPEN | FMEA, DFA, safety manual, and security plan exist in `aspice/score-persistency/SAF/`. However, we have not verified whether these documents satisfy ASPICE SWE.1-SWE.6 work products completely. Existence is not compliance. |
| 2 | Traceability from requirements to tests unverified | High | OPEN | 61/61 local tests pass, but there is no published traceability matrix linking safety requirements to specific test cases. ASIL-D demands bidirectional traceability. |
| 3 | Unit test evidence pending | High | OPEN | Unit tests are RUNNING on laptop — results not yet available. Without unit test evidence, SWE.4 (Software Unit Verification) cannot be assessed. |
| 4 | CIT evidence pending | High | OPEN | CIT pipeline RUNNING — results not yet available. SWE.5 (Software Integration Testing) has no evidence artifact. |
| 5 | Version 0.0.0 signals pre-release maturity | Medium | OPEN | A v0.0.0 tag means upstream considers this pre-release. ASPICE assessors will question whether process rigor was applied to code the maintainers themselves label as immature. |
| 6 | Review records not inspected | Medium | OPEN | We have not checked whether upstream PRs have formal review sign-off. ASIL-D requires documented review evidence per ASPICE SWE.4/SWE.5. |
| 7 | No independent verification of our local test run | Medium | OPEN | 61/61 tests run by us (the developer). No independent verification or witness. ISO 26262 Part 8 requires independence for ASIL-D. |

**Verdict:** ASPICE documentation artifacts exist (FMEA, DFA, safety manual) — far ahead of LoLa. But completeness and review evidence remain unverified. Pending unit/CIT results block SWE.4/SWE.5 closure.

---

## 2. Security Engineer

*"How safe is the persisted data?"*

| # | Gap | Severity | Status | Issue |
|---|-----|----------|--------|-------|
| 1 | CRC is Adler-32, not cryptographic | High | OPEN | Adler-32 detects accidental corruption but provides zero protection against intentional tampering. An attacker can craft data with matching Adler-32 checksums trivially. For ASIL-D safety-critical persisted data, a cryptographic MAC (HMAC-SHA256) is expected. |
| 2 | No encryption of persisted KVS data | High | OPEN | Key-value store writes to filesystem in plaintext. Sensitive calibration data, secrets, or safety parameters stored via KVS are readable by any process with file access. |
| 3 | File permission model unknown | Medium | OPEN | We have not verified what permissions KVS files are created with. If world-readable/writable (like LoLa's 0666 shm), any process can corrupt persisted safety data. |
| 4 | No scorehsm integration | Medium | OPEN | score-persistency does not integrate with scorehsm for key management or authenticated storage. Data integrity relies solely on Adler-32. |
| 5 | Snapshot file injection risk | Medium | OPEN | Snapshots written to filesystem could be replaced by an attacker between write and read. No file integrity verification beyond CRC on content. No filesystem-level protection (dm-verity, signed files). |
| 6 | Default values bypass CRC validation | Medium | OPEN | When defaults are loaded (no snapshot exists), CRC validation is skipped. An attacker deleting the snapshot file forces fallback to defaults — potential denial-of-service for learned values. |
| 7 | Mock filesystem in tests masks real attack surface | Low | OPEN | `kvs_mock.rs` and `@score_baselibs` mocks replace filesystem I/O in tests. Real filesystem attack vectors (symlink attacks, race conditions, disk-full) are never exercised. |

**Verdict:** Adler-32 is an integrity check, not a security mechanism. For ASIL-D persisted data, the lack of cryptographic protection and file-level access control is a significant gap.

---

## 3. Performance Engineer

*"What are the KVS throughput numbers?"*

| # | Gap | Severity | Status | Issue |
|---|-----|----------|--------|-------|
| 1 | Google Benchmark exists but results not collected | High | OPEN | `bm_kvs.cpp` is configured for C++ KVS benchmarking. We have not run it or collected results. No throughput, latency, or operation-count data available. |
| 2 | No Rust benchmark equivalent | Medium | OPEN | C++ has `bm_kvs.cpp` via Google Benchmark. Rust side has 5 examples but no dedicated `criterion` or `bench` harness for KVS operations. Cannot compare C++/Rust performance. |
| 3 | Snapshot flush latency unknown | High | OPEN | Flush writes KVS state to persistent storage. Latency depends on data size, storage medium, and filesystem. Never measured. For ASIL-D, worst-case flush time during shutdown must be bounded. |
| 4 | CRC computation overhead not profiled | Medium | OPEN | Adler-32 CRC is computed on every write/read. For large KVS stores, CRC overhead could be significant. Never profiled. |
| 5 | No sustained write stress test | Medium | OPEN | No test hammering KVS with thousands of writes to measure degradation, memory growth, or storage fragmentation over time. |
| 6 | Build performance is strong | Info | CLOSED | 9 targets, 755 actions, 67s build time. Dual C++/Rust compilation completes in reasonable time. No build performance gap. |

**Verdict:** Benchmark infrastructure exists (`bm_kvs.cpp`) but zero results collected. Flush latency — critical for safe shutdown — is completely unknown.

---

## 4. Deployment Engineer

*"How does KVS map to real storage?"*

| # | Gap | Severity | Status | Issue |
|---|-----|----------|--------|-------|
| 1 | Storage backend configuration unknown | High | OPEN | KVS writes to "persistent storage" but the mapping to actual storage (eMMC, NOR flash, tmpfs, NFS) is not documented or tested. Different backends have vastly different durability and performance. |
| 2 | No migration strategy for KVS schema changes | High | OPEN | v0.0.0 implies schema will change. When KVS key names, types, or structure change between versions, how are existing persisted files migrated? No tooling or documentation exists. |
| 3 | No backup/restore procedure | Medium | OPEN | If KVS snapshot files are corrupted, how does an ECU recover? No documented backup strategy, no redundant storage, no recovery procedure. |
| 4 | Snapshot file format not documented for operations | Medium | OPEN | Operations teams need to know: where files live, what format they use, how to inspect them, how to manually reset them. Only the `kvs_tool` CLI exists — its capabilities are unknown. |
| 5 | `kvs_tool` CLI capabilities not tested | Medium | OPEN | A CLI tool exists but we have not tested it. Does it support dump, restore, validate, migrate operations? Unknown. |
| 6 | No storage quota or size limit | Medium | OPEN | KVS could grow unbounded if application keeps adding keys. No documented limit on store size, key count, or value size. On embedded storage, this is critical. |
| 7 | No wear-leveling consideration for flash storage | Medium | OPEN | Frequent KVS flush to NOR/NAND flash without wear-leveling awareness could degrade storage lifetime. No documentation on recommended storage backends. |

**Verdict:** KVS is a logical abstraction. The mapping to physical storage, migration, and operational procedures are entirely undocumented.

---

## 5. Upstream Eclipse S-CORE Maintainer

*"Is the dual C++/Rust API coherent?"*

| # | Gap | Severity | Status | Issue |
|---|-----|----------|--------|-------|
| 1 | Version 0.0.0 — API is explicitly unstable | High | OPEN | Semver 0.0.0 means "no public API guaranteed." Any consumer building on this API accepts that everything may change without notice. |
| 2 | C++/Rust API parity not verified | High | OPEN | C++ exposes `kvs.hpp`, `kvsbuilder.hpp`, `kvsvalue.hpp`. Rust has 9 modules including `kvs_mock.rs`. Whether these APIs offer identical functionality, semantics, and error handling is unverified. |
| 3 | Dependency chain is narrow | Medium | CLOSED | Dependencies are score_baselibs 0.2.4, score_logging 0.1.0, score_baselibs_rust 0.1.0 — all S-CORE modules. No external dependency sprawl. Clean. |
| 4 | No sanitizer configuration in .bazelrc | High | OPEN | score_baselibs has ASan/TSan/UBSan configured in `.bazelrc`. score-persistency does not. For ASIL-D C++ code, running without sanitizers is a significant gap vs the project's own baseline. |
| 5 | 14 CI workflows suggest strong upstream process | Info | CLOSED | Build, check, CIT, clippy, copyright, format, license, docs, coverage, release, bzlmod, gitlint, docs-cleanup, qnx_integration — comprehensive CI. |
| 6 | Miri testing configured but results unknown | Medium | OPEN | Miri (Rust undefined behavior detector) configured with nightly-2025-12-15. Whether it passes or what it catches is unknown to us. |
| 7 | Mock strategy couples to score_baselibs internals | Medium | OPEN | `kvs_mock.rs` uses `@score_baselibs` mocks for filesystem/JSON. If baselibs changes mock API, persistency tests break. No interface contract between the two. |

**Verdict:** Upstream CI is impressively comprehensive (14 workflows). But v0.0.0 + missing sanitizers + unverified C++/Rust parity are real gaps for ASIL-D code.

---

## 6. New Team Member (Onboarding)

*"How do I work with dual-language KVS?"*

| # | Gap | Severity | Status | Issue |
|---|-----|----------|--------|-------|
| 1 | Dual C++/Rust codebase doubles learning curve | High | OPEN | A new contributor must understand both C++ and Rust KVS implementations, their build systems (Bazel for both), and how they interact. Steep onboarding. |
| 2 | 5 Rust examples exist — quality not assessed | Medium | OPEN | Five Rust examples are provided. We have not reviewed whether they demonstrate realistic usage patterns or are minimal stubs. |
| 3 | C++ API headers are clear entry points | Info | CLOSED | `kvs.hpp`, `kvsbuilder.hpp`, `kvsvalue.hpp` — well-named headers that signal the API surface. A new developer knows where to start for C++. |
| 4 | No "getting started" walkthrough for KVS usage | Medium | OPEN | Examples exist but no narrative documentation explaining: when to use C++ vs Rust API, how to configure a KVS, how snapshots work, when flush is called. |
| 5 | 61 local tests serve as living documentation | Low | CLOSED | 61/61 passing tests covering API contract, dependency chain, and safety contracts provide executable specification. A new developer can read tests to understand behavior. |
| 6 | ASPICE documentation provides architectural context | Low | CLOSED | FMEA, DFA, safety manual in `aspice/score-persistency/SAF/` give a new team member safety context that most open-source projects lack. |
| 7 | `kvs_tool` CLI could aid exploration | Medium | OPEN | A CLI tool exists for KVS interaction. If well-documented, it could be the fastest way for a new person to understand KVS behavior. Currently untested by us. |

**Verdict:** Better than most S-CORE modules for onboarding — examples, tests, and ASPICE docs exist. But dual-language complexity and missing narrative documentation remain barriers.

---

## 7. OEM Integration Engineer

*"How does this map to AUTOSAR Persistency?"*

| # | Gap | Severity | Status | Issue |
|---|-----|----------|--------|-------|
| 1 | AUTOSAR Persistency (ara::per) mapping not documented | High | OPEN | AUTOSAR defines `ara::per` with Key-Value Storage and File Storage APIs. How score-persistency maps to `ara::per::KeyValueStorage` is not documented. OEMs need this mapping. |
| 2 | No ECU integration test | High | OPEN | KVS tested only on host (laptop). No test on target ECU hardware (QNX, aarch64). Storage behavior on embedded filesystems (UBIFS, JFFS2) may differ significantly. |
| 3 | Storage quota management missing | Medium | OPEN | AUTOSAR Persistency defines per-application storage quotas via the Persistency deployment manifest. No equivalent quota mechanism visible in score-persistency. |
| 4 | No redundant storage / safe state | High | OPEN | ASIL-D requires that persistence failures have a defined safe state. If KVS flush fails mid-write (power loss), is the store corrupted? Is there a backup copy? Atomic write semantics unclear. |
| 5 | QNX integration workflow exists in CI | Info | CLOSED | `qnx_integration` CI workflow is one of the 14 pipelines. Upstream is at least testing on QNX — the primary automotive RTOS. |
| 6 | No SOME/IP-SD or diagnostic access to KVS | Medium | OPEN | OEM diagnostic tools expect to read/write persisted data via UDS (ReadDataByIdentifier/WriteDataByIdentifier). No diagnostic interface to KVS exists. |
| 7 | Multi-process concurrent access not tested | Medium | OPEN | In an ECU, multiple SWCs may access KVS. Whether score-persistency supports concurrent access from multiple processes, and with what locking semantics, is unknown. |

**Verdict:** KVS functionality exists but AUTOSAR mapping, ECU integration, and production safety semantics (atomic writes, quotas, concurrent access) are all gaps.

---

## 8. Regulatory / ISO 26262 Compliance Officer

*"This claims ASIL-D — prove it."*

| # | Gap | Severity | Status | Issue |
|---|-----|----------|--------|-------|
| 1 | FMEA and DFA artifacts exist | Info | CLOSED | `aspice/score-persistency/SAF/` contains FMEA and DFA documents. This is more safety evidence than any other S-CORE module we have tested. Existence verified; completeness not yet assessed. |
| 2 | ASIL-D requires the most rigorous methods | Critical | OPEN | ISO 26262 Table 2-9 requires for ASIL-D: modified condition/decision coverage (MC/DC), formal verification methods, and back-to-back testing. Whether upstream applies these is unverified. |
| 3 | No tool qualification evidence | High | OPEN | Bazel, GCC, Rust compiler, clippy, Miri — none tool-qualified per ISO 26262-8 Clause 11. ASIL-D has the strictest tool confidence requirements (TCL1 requires validation suite or proven-in-use argument). |
| 4 | Safety manual exists but content not reviewed | High | OPEN | A safety manual in `aspice/score-persistency/SAF/` exists. We have not read it to verify it covers: assumptions of use, safety-relevant configuration, integration constraints. |
| 5 | Coverage data not collected | High | OPEN | CI includes a `coverage` workflow. Results not collected by us. ASIL-D requires MC/DC coverage — statement/branch coverage alone is insufficient. |
| 6 | No dependent failure analysis between C++ and Rust KVS | Medium | OPEN | If both C++ and Rust KVS share the same storage backend, a storage failure causes both to fail. DFA document exists but we have not verified it addresses this specific common-cause failure. |
| 7 | Security plan exists — rare and valuable | Info | CLOSED | A security plan in the SAF directory addresses ISO 21434 (cybersecurity). Combined ISO 26262 + ISO 21434 evidence is ahead of most S-CORE modules. |
| 8 | Pending test results block safety case closure | High | OPEN | Unit tests and CIT RUNNING but not complete. A safety case requires all verification activities to be complete with documented results. Cannot close. |

**Verdict:** score-persistency has more safety documentation than any S-CORE module tested so far (FMEA, DFA, safety manual, security plan). But ASIL-D is the highest bar — MC/DC coverage, tool qualification, and complete test evidence are all needed and all missing.

---

## 9. Test Automation Engineer

*"What does the CI pipeline actually catch?"*

| # | Gap | Severity | Status | Issue |
|---|-----|----------|--------|-------|
| 1 | 14 CI workflows — strongest pipeline of any S-CORE module | Info | CLOSED | Build, check, CIT, clippy, copyright, format, license, docs, coverage, release, bzlmod, gitlint, docs-cleanup, qnx_integration. Comprehensive. |
| 2 | Miri testing for Rust UB detection | Info | CLOSED | Miri configured with nightly-2025-12-15. Tests Rust code for undefined behavior, uninitialized memory, and aliasing violations. Rare in automotive Rust projects. |
| 3 | No sanitizer config for C++ | High | OPEN | ASan, TSan, UBSan not configured in `.bazelrc`. score_baselibs has them. C++ KVS code runs without memory safety checks in CI. |
| 4 | Benchmark regression not automated | Medium | OPEN | `bm_kvs.cpp` exists but no CI job compares benchmark results across commits. Performance regressions would go unnoticed. |
| 5 | CIT uses pytest — results pending | High | OPEN | Python integration tests (pytest CIT) are RUNNING. Results not available. Cannot assess test quality or coverage. |
| 6 | Unit test results pending | High | OPEN | Unit tests RUNNING on laptop. Cannot assess pass rate, coverage, or failure modes. |
| 7 | No fuzz testing | Medium | OPEN | For ASIL-D code handling external data (file I/O, CRC validation, deserialization), fuzz testing is expected. None configured. |
| 8 | clippy configured — Rust lint quality enforced | Info | CLOSED | clippy CI workflow enforces Rust idioms and catches common bugs. Combined with Miri, Rust code quality enforcement is strong. |

**Verdict:** Strongest CI pipeline of any S-CORE module tested (14 workflows, Miri, clippy). Key gap is missing C++ sanitizers — inconsistent with the project's own baselibs standard. Pending test results block full assessment.

---

## 10. System Architect

*"How does KVS fit into the S-CORE platform?"*

| # | Gap | Severity | Status | Issue |
|---|-----|----------|--------|-------|
| 1 | No integration with score-lifecycle | High | OPEN | KVS flush should be triggered by lifecycle shutdown events. If the system crashes without flush, persisted data may be stale or corrupted. No lifecycle hook documented. |
| 2 | No integration with LoLa for signal persistence | High | OPEN | LoLa publishes real-time signals. Persisting selected signals (e.g., learned values, calibration) via KVS is a natural integration point. Not implemented or designed. |
| 3 | Dependencies are well-structured | Info | CLOSED | score_baselibs 0.2.4, score_logging 0.1.0, score_baselibs_rust 0.1.0 — clean dependency graph within S-CORE ecosystem. No circular dependencies. |
| 4 | Data flow between KVS and other S-CORE modules undefined | High | OPEN | Which modules write to KVS? Which read? What is the data ownership model? No architectural data flow diagram for persistency within the S-CORE platform. |
| 5 | Snapshot strategy vs event-driven persistence | Medium | OPEN | KVS uses snapshots (periodic? on-demand? on-shutdown?). For safety-critical data, event-driven persistence (write-on-change with fsync) may be required. Strategy not documented. |
| 6 | No FEO integration for deterministic persistence timing | Medium | OPEN | FEO (Fixed Execution Order) defines deterministic task cycles. KVS operations are not integrated with FEO — persistence timing is non-deterministic. |
| 7 | Dual C++/Rust KVS — which is the primary? | Medium | OPEN | Both languages have full KVS implementations. Which is canonical? Does an application choose one, or do they interoperate (shared storage)? Architectural intent unclear. |
| 8 | ASIL-D is the highest safety level in S-CORE | Info | CLOSED | score-persistency at ASIL-D sets the safety ceiling for the platform. This means it should have the strictest processes — and it does have the most safety documentation. Consistent. |

**Verdict:** score-persistency is an infrastructure module that every other S-CORE component may depend on. The lack of defined integration points with lifecycle, LoLa, and FEO means it exists as an island — capable but unconnected.

---

## Cross-Perspective Summary

| # | Perspective | Gaps | Closed | Open | Key Theme |
|---|------------|------|--------|------|-----------|
| 1 | ASPICE Auditor | 7 | 0 | 7 | Artifacts exist, completeness unverified, pending results |
| 2 | Security Engineer | 7 | 0 | 7 | Adler-32 is not security, no encryption, no file protection |
| 3 | Performance Engineer | 6 | 1 | 5 | Benchmark infra exists, zero results collected |
| 4 | Deployment Engineer | 7 | 0 | 7 | Storage mapping, migration, operations all undefined |
| 5 | Upstream Maintainer | 7 | 2 | 5 | v0.0.0 unstable, strong CI, missing sanitizers |
| 6 | New Team Member | 7 | 3 | 4 | Dual-language complexity, but examples + tests help |
| 7 | OEM Integration | 7 | 1 | 6 | No AUTOSAR mapping, no ECU test, no atomic writes |
| 8 | Regulatory (ISO 26262) | 8 | 2 | 6 | FMEA/DFA exist (rare!), but ASIL-D bar is highest |
| 9 | Test Automation | 8 | 3 | 5 | 14 CI workflows (best in S-CORE), missing C++ sanitizers |
| 10 | System Architect | 8 | 2 | 6 | Capable but unconnected — no lifecycle/LoLa/FEO integration |

**Total gaps identified: 72** (14 CLOSED, 58 OPEN)

**Pending items (will update when results arrive):**
- Unit tests: RUNNING on laptop
- CIT: RUNNING in pipeline

---

## Top Recurring Themes

1. **Most mature safety documentation in S-CORE** — FMEA, DFA, safety manual, security plan all exist. No other tested module has this.
2. **ASIL-D is the highest bar** — and the gap between "documentation exists" and "ASIL-D compliance proven" is enormous (MC/DC, tool qualification, independent verification).
3. **Pending results block closure** — unit tests and CIT running but incomplete. Multiple perspectives cannot close until results arrive.
4. **Strongest CI of any S-CORE module** — 14 workflows including Miri, clippy, coverage, QNX integration. But missing C++ sanitizers.
5. **Island architecture** — KVS works in isolation but has no defined integration with lifecycle, LoLa, FEO, or scorehsm.
6. **Adler-32 is not security** — fine for accidental corruption detection, insufficient for ASIL-D tamper resistance.
7. **v0.0.0 means "trust nothing"** — semver explicitly says no stability guarantee. Every API consumer accepts breakage risk.

---

**The honest conclusion:** score-persistency is the most process-mature S-CORE module we have tested — it has ASPICE safety artifacts, 14 CI workflows, Miri testing, and dual-language implementations. The 9/9 build targets and 61/61 local tests demonstrate real engineering quality. But ASIL-D is the highest safety integrity level in automotive, and the gap between "good open-source project" and "ASIL-D certified component" is vast. The 58 open gaps across 10 perspectives map the distance still to travel. The most critical next steps are: (1) collect pending unit/CIT results, (2) run the existing benchmarks, (3) add C++ sanitizers, and (4) define lifecycle integration points.
