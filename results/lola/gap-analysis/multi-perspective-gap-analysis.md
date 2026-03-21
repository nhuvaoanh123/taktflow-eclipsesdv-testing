---
document_id: GAP-LOLA-MULTI
title: "Multi-Perspective Gap Analysis — 10 Stakeholder Views"
version: "1.0"
status: final
date: 2026-03-21
---

# Multi-Perspective Gap Analysis

Same work, 10 different eyes. Each stakeholder asks different questions.

---

## 1. ASPICE Auditor

*"Show me the evidence chain."*

| Gap | Severity | Issue |
|---|---|---|
| No formal review records | High | Every requirement (65 total) has status "draft". None reviewed. No HITL-LOCK blocks filled. Zero signatures. An auditor sees 65 unreviewed requirements — that's a Level 0, not Level 2. |
| Traceability is manual | High | The traceability matrix is hand-written markdown. No `trace-gen.py` validates it. Links could be wrong and nobody would know. |
| No work product configuration control | Medium | Reports are loose markdown files. No document IDs in a controlled registry. No revision history tracked. No change log. |
| SWE.3 (Detailed Design) is empty | High | We have SWE.1 (requirements) and SWE.2 (architecture) but SWE.3 (detailed design) was never created for our bridge code. ASPICE requires it. |
| No verification report | Medium | SWE.4 references test results but there's no formal verification report document — just console logs in gap analysis. |
| Upstream vs ours not separated | Medium | We mix upstream LoLa evidence (their 252 tests) with our bridge evidence (15 samples on can0). An auditor needs to know which code WE own and which we inherited. |

**Verdict:** Would fail ASPICE Level 2 assessment. Documentation framework exists but content is draft quality.

---

## 2. Security Engineer

*"What attack surfaces did you introduce?"*

| Gap | Severity | Issue |
|---|---|---|
| CAN bridge runs as root-equivalent | Critical | Our skeleton reads raw CAN sockets — requires `CAP_NET_RAW`. If compromised, attacker has raw network access. |
| No input validation on CAN frames | High | `decode()` trusts CAN frame content. A malicious ECU could send crafted frames to exploit the decoder (integer overflow in signal scaling, buffer overread on short DLC partially guarded but not fuzzed). |
| Shared memory world-readable | High | QM config uses mode `0666` — any process can read vehicle signals. No authentication, no encryption. |
| No rate limiting on skeleton | Medium | Skeleton publishes every CAN frame. An attacker flooding the CAN bus with 100k frames/sec would consume all LoLa slots and CPU. |
| No integrity check on config JSON | Medium | Service config loaded from filesystem without signature verification. Attacker modifying config could redirect shared memory to controlled region. |
| USB CAN adapter is untrusted input | Medium | Physical CAN bus is an untrusted boundary. We treat it like trusted internal data. |
| SSH to laptop is the control plane | Low | All test execution via SSH. If laptop SSH is compromised, attacker controls the entire bench. |

**Verdict:** Zero security hardening. Fine for testing, not for any connected deployment.

---

## 3. Performance Engineer

*"Where are the real numbers?"*

| Gap | Severity | Issue |
|---|---|---|
| No percentile distribution | High | We report "8-36 µs" but never computed p50/p95/p99/p99.9 over thousands of samples. Min/max without distribution is meaningless for real-time guarantees. |
| No jitter measurement | High | IPC latency varies 8-36 µs (4.5x range). For ASIL-B real-time, jitter matters more than average. Never measured. |
| Benchmark was debug build | Medium | All measurements on `-c fastbuild` (debug). Release build (`-c opt`) latency could be 2-5x different. We never measured release performance. |
| No CPU/memory profiling | Medium | Never measured CPU utilization, memory allocation patterns, or cache behavior during CAN→LoLa operation. |
| No sustained load test | Medium | Longest test was ~10 seconds. No 1-hour, 24-hour, or multi-day stability run. Memory leaks only visible over time. |
| CAN→LoLa end-to-end latency not measured | High | We measured IPC latency (skeleton→proxy) but not CAN-frame-on-wire → proxy-callback total latency. The socketcan read() adds unknown delay. |
| No comparison baseline | Low | No comparison between LoLa IPC and alternatives (Unix sockets, shared memory without LoLa, pipe). Can't justify LoLa overhead. |

**Verdict:** Latency "measured" but not characterized. No real-time performance profile.

---

## 4. Production Deployment Engineer

*"How do I deploy this?"*

| Gap | Severity | Issue |
|---|---|---|
| No deployment guide | Critical | Zero documentation on how to deploy CAN→LoLa bridge. What config files go where? What systemd service? What user/group? |
| No startup/shutdown procedure | High | Bridge is run manually via SSH. No init script, no service file, no container, no orchestration. |
| No monitoring/health check | High | If the bridge crashes, nobody knows. No watchdog, no health endpoint, no log aggregation. |
| No log rotation | Medium | LoLa logs to console (fallback). In production, logs would fill disk. |
| Config file path hardcoded in commands | Medium | `-s path/to/config.json` passed manually. No standard config location. |
| No versioning of deployed binary | Medium | Binary is `can_bridge` without version number. Can't tell which version is running. |
| No rollback procedure | Low | If new version breaks, no documented way to rollback. |

**Verdict:** Lab prototype, not deployable. Would require significant productization.

---

## 5. Upstream Eclipse S-CORE Maintainer

*"Are you using our API correctly?"*

| Gap | Severity | Issue |
|---|---|---|
| No API compatibility test | High | Our bridge uses LoLa v0.1.4 API. When upstream updates, our code may break. No test verifies API contract. |
| Config schema not validated | Medium | We wrote `mw_com_config.json` by hand copying from the example. Never ran LoLa's config schema validator on it. |
| StringLiteral usage may be wrong | Medium | `score::StringLiteral args[2] = {"--service_instance_manifest", p.c_str()};` — unclear if temporary `c_str()` lifetime is safe here. |
| No contribution back | Low | We found FINDING-001 (concurrent proxy crash) and FINDING-002 (toolchain checksum) but never filed upstream issues. |
| Modified Bazel workspace | Medium | We added `can_bridge/` inside their `score/mw/com/example/` directory. This is a local fork, not a proper external dependency. On upstream update, our code disappears. |
| VehicleSignals struct not registered with LoLa type system | Medium | We defined `VehicleSignals` as a plain struct. LoLa may require types to be registered or meet specific trait requirements. Not verified. |

**Verdict:** Works by coincidence, not by contract. Upstream change could silently break everything.

---

## 6. New Team Member (Onboarding)

*"How do I reproduce this?"*

| Gap | Severity | Issue |
|---|---|---|
| No single README for the bridge | High | To understand what we built, you'd have to read 8 result files + 3 scripts + the patches directory. No single "start here" document. |
| Build instructions scattered | Medium | Some steps in `assess-lola.sh`, some in test reports, some in gap analysis. No single build-and-run guide. |
| Depends on laptop SSH access | Medium | Can't reproduce without SSH to `192.168.0.158`. If laptop is off or IP changes, everything breaks. |
| No development environment setup | Medium | We used the laptop's existing environment. No Dockerfile, no devcontainer, no `nix-shell` for reproducible setup. |
| Gap analysis requires reading 5 versions | Low | v1→v2→v3→v4→v5 — new person has to read all 5 to understand current state. Should be one document. |
| No architecture decision records | Low | Why LoLa? Why not Kuksa? Why C++ bridge not Python? Decisions are in chat history, not documented. |

**Verdict:** Tribal knowledge. Bus factor of 1.

---

## 7. OEM Integration Engineer

*"Can I plug this into my vehicle platform?"*

| Gap | Severity | Issue |
|---|---|---|
| Only tested with taktflow DBC | High | Would it work with a different DBC? Different CAN IDs? Different signal layouts? Decoder is hardcoded, not DBC-driven. |
| No AUTOSAR integration | High | LoLa implements ara::com but our bridge bypasses it entirely. Uses raw LoLa C++ API, not the standardized AUTOSAR interface. |
| No SOME/IP gateway | High | The bridge reads CAN directly. In a real OEM architecture, CAN→SOME/IP→LoLa is the path. We skip the middle layer. |
| Single ECU vendor support | Medium | Only tested with STM32/TMS570. Different ECU hardware (Infineon, Renesas, NXP) may have different CAN frame timing. |
| No diagnostic integration | Medium | Bridge doesn't expose any diagnostic interface (UDS, SOME/IP-SD). Can't query its state remotely. |
| x86_64 only | Medium | Built for laptop x86_64. OEM HPC is typically aarch64 (like our Pi). Cross-compilation failed. |

**Verdict:** Proof of concept, not integrable into any OEM platform without significant adaptation.

---

## 8. Regulatory / Compliance Officer

*"What can I show to the authority?"*

| Gap | Severity | Issue |
|---|---|---|
| No safety case | Critical | No structured safety case (GSN/CAE notation) linking hazards → safety goals → requirements → evidence. Just loose documents. |
| No independent verification | Critical | All tests run by the developer (us). No independent verification or third-party assessment. ISO 26262 Part 8 requires independence. |
| ASIL-B claims without ASIL-B process | High | We wrote "ASIL-B" on documents but didn't follow ASIL-B development process (no FMEDA, no hardware metrics, no tool qualification). |
| Tool qualification missing | High | Bazel, GCC, clang-tidy, ASan — none tool-qualified per ISO 26262-8 Clause 11. Test results from unqualified tools have reduced confidence. |
| No configuration management plan | Medium | Documents version-controlled in git but no formal CM plan per ASPICE SUP.8 / ISO 26262-8 Clause 7. |
| No problem resolution process | Medium | FINDING-001/002/003 documented but no formal tracking (no JIRA, no issue board, no resolution timeline). |

**Verdict:** Zero regulatory standing. Would not pass any ISO 26262 assessment.

---

## 9. Test Automation Engineer

*"Can I run this in CI?"*

| Gap | Severity | Issue |
|---|---|---|
| No CI pipeline for the bridge | High | Our bridge code has no GitHub Actions workflow. Tests run manually via SSH. |
| No regression test suite | High | When we change the decoder, how do we know we didn't break something? No automated regression. |
| Results not machine-parseable | Medium | All results in markdown. No JUnit XML, no JSON test output, no coverage artifact for CI consumption. |
| `assess-lola.sh` not integrated with pytest | Medium | Two separate test systems — shell script and pytest. Neither talks to the other. |
| No test data fixtures | Medium | Ground truth values hardcoded in gap analysis text, not in a test fixture file. Can't re-verify automatically. |
| CAN hardware dependency | Medium | Tests requiring `can0` can't run in CI (no USB CAN adapter in cloud). No mock/stub for CAN interface. |
| No flaky test handling | Low | FINDING-001 (concurrent proxy crash) is inherently flaky. No retry logic, no flaky test annotation. |

**Verdict:** Manual testing only. Zero CI integration for our custom code.

---

## 10. System Architect

*"Does this fit the big picture?"*

| Gap | Severity | Issue |
|---|---|---|
| CAN bridge is on wrong machine | High | In the target architecture, CAN→LoLa should run on the Pi (QNX HPC). We run it on the laptop (Linux). Proves the concept on the wrong platform. |
| No Ethernet path tested | High | The 3-chip SoC uses Ethernet (TMS570↔Pi), not CAN. We tested CAN→LoLa but the production path is Ethernet→SOME/IP→LoLa. |
| Lifecycle integration missing | High | LoLa processes not managed by score-lifecycle. No health monitoring, no supervised restart. Standalone processes. |
| No orchestrator integration | Medium | Processes started manually, not by score-orchestrator. No workload manifest. |
| Persistency not connected | Medium | Vehicle signals published via LoLa but not persisted. No score-persistency integration. |
| FEO not integrated | Medium | Events published asynchronously, not on FEO cycle boundaries. Non-deterministic timing. |
| scorehsm not connected | Medium | No cryptographic protection of LoLa IPC. Shared memory is plaintext. |
| Only 1 of 11 S-CORE modules tested | High | Tested LoLa only. 10 other S-CORE modules (lifecycle, persistency, orchestrator, feo, kyron, baselibs, etc.) not built or tested at all. |

**Verdict:** Proved one module in isolation on the wrong platform. Integration architecture not validated.

---

## Cross-Perspective Summary

| Perspective | Critical Gaps | Key Theme |
|---|---|---|
| ASPICE Auditor | 6 | All docs are draft, no reviews, no trace validation |
| Security Engineer | 7 | Zero hardening, untrusted input, world-readable shm |
| Performance Engineer | 7 | No percentiles, no jitter, no sustained load, debug build |
| Deployment Engineer | 7 | No deploy guide, no service file, no monitoring |
| Upstream Maintainer | 6 | Local fork, no API contract test, findings not reported |
| New Team Member | 6 | No README, no repro guide, tribal knowledge |
| OEM Integration | 6 | Hardcoded DBC, no AUTOSAR, no SOME/IP, x86 only |
| Regulatory | 6 | No safety case, no independence, no tool qualification |
| Test Automation | 7 | No CI, no regression, no machine-parseable results |
| System Architect | 8 | Wrong platform, wrong path, 1/11 modules, no integration |

**Total unique gaps identified: 66**

**Top recurring themes:**
1. **Lab prototype, not production** — every perspective says this
2. **No process rigor** — no reviews, no CI, no formal anything
3. **Wrong platform** — proved on Linux laptop, need QNX Pi
4. **Isolation testing** — LoLa alone, no integration with other S-CORE modules
5. **No sustained/stress testing** — everything tested for seconds, not hours

---

**The honest conclusion:** We proved that LoLa's IPC works and can connect to CAN data. That's valuable as a first step. But from every other angle, the work is a prototype-quality proof of concept with 66 identified gaps across 10 perspectives. The gap analysis iterations (v1→v5) only looked through one lens — the test engineer's. These 9 other lenses reveal how much further the work needs to go.
