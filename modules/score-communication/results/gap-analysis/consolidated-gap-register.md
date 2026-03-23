---
document_id: GAP-LOLA-REGISTER
title: "Consolidated Gap Register — All Perspectives"
version: "1.0"
status: final
date: 2026-03-21
---

# Consolidated Gap Register

66 gaps from 10 perspectives. 22 closed, 2 blocked, 42 open with fix paths.

## Summary

| Status | Count |
|---|---|
| CLOSED | 22 |
| BLOCKED | 2 |
| OPEN (fix path defined) | 42 |
| **Total** | **66** |

---

## 1. ASPICE Auditor (6 gaps)

| # | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| A1 | All 65 requirements status "draft", none reviewed | OPEN | Each requirement owner reviews + marks "reviewed". Add HITL-LOCK blocks with reviewer name + date. Batch: 10 reqs per session. | 6 sessions |
| A2 | Traceability matrix is manual markdown, no validation | OPEN | Port `trace-gen.py` from taktflow-embedded. Adapt regex for `SG-COM-*` ID format. Add to CI as PR check. | 1 day |
| A3 | No work product configuration control | OPEN | Add `docs/document-register.yaml` with doc IDs, versions, owners. Add pre-commit hook that validates doc ID uniqueness. | 2 hours |
| A4 | SWE.3 (Detailed Design) empty for bridge code | OPEN | Write `aspice/score-communication/SWE.3-detailed-design/can-bridge-design.md` — describe `decode()` function, data flow, error handling. | 2 hours |
| A5 | No formal verification report | OPEN | Create `aspice/score-communication/SWE.4-unit-verification/verification-report.md` from test results. Template exists in process_description. | 1 hour |
| A6 | Upstream vs own code not separated | OPEN | Add table to integration report: "Our code: 4 files, 250 lines. Upstream: 622 files, 252 tests." Clear ownership boundary. | 30 min |

---

## 2. Security Engineer (7 gaps)

| # | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| S1 | CAN bridge runs with CAP_NET_RAW | OPEN | Create dedicated `can_bridge` user with only CAP_NET_RAW. Drop all other capabilities. Add to deployment guide. | 1 hour |
| S2 | No input validation (fuzz testing) | **CLOSED** | Edge-case frames (DLC 0-8, max values) tested. Skeleton survived all. | Done |
| S3 | Shared memory world-readable (0666) | OPEN | For QM: acceptable. For ASIL-B: already uses 0660 (group-restricted). Document in security analysis which config is deployed. | 30 min |
| S4 | No rate limiting on skeleton | OPEN | Add configurable max-frames-per-second to skeleton. Drop excess frames with counter. Log drops. | 3 hours |
| S5 | Config JSON loaded without signature | OPEN | Add CRC-32 or HMAC verification of config file. Store hash alongside config. Verify at load. | 2 hours |
| S6 | USB CAN is untrusted input boundary | OPEN | Document in security analysis: "CAN bus is untrusted boundary. All CAN data treated as untrusted input. Decoder validates DLC before access." Already true in code, just not documented. | 30 min |
| S7 | SSH control plane not hardened | OPEN | Out of scope for LoLa. Document in bench security notes: SSH key-only auth, firewall rules, no root login. | 30 min |

---

## 3. Performance Engineer (7 gaps)

| # | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| P1 | No percentile distribution | **CLOSED** | 500 samples: p50=28µs, p95=43µs, p99=54µs (debug). | Done |
| P2 | No jitter measurement | **CLOSED** | Jitter=54µs (max-min). Stdev=9.3µs. | Done |
| P3 | Benchmark was debug build | **CLOSED** | Release build measured: p50=9µs, p99=25µs. 3.1x faster. | Done |
| P4 | No CPU/memory profiling | OPEN | Run `perf record` during bridge operation. Generate flame graph. Measure CPU% with `pidstat`. | 2 hours |
| P5 | No sustained load test | **CLOSED** | 2-min test: RSS stable at 8,324 KB, 0 growth. | Done |
| P6 | CAN→LoLa end-to-end latency not measured | **CLOSED** | Skeleton logs `ipc=9688-18275ns` per frame. Proxy `age=10-36µs`. | Done |
| P7 | No comparison baseline | OPEN | Run same CAN decoder without LoLa (direct shared memory write). Compare latency. Quantify LoLa overhead. | 2 hours |

---

## 4. Deployment Engineer (7 gaps)

| # | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| D1 | No deployment guide | OPEN | Write `docs/deployment/can-bridge-deployment.md`: prerequisites, config, user setup, startup. | 2 hours |
| D2 | No startup/shutdown procedure | OPEN | Write systemd service file `can-lola-bridge.service`. Add `ExecStart`, `Restart=on-failure`, `WatchdogSec`. | 1 hour |
| D3 | No monitoring/health check | OPEN | Add `--health-port 8080` option. HTTP endpoint returns JSON: `{alive: true, frames: N, latency_us: M}`. | 3 hours |
| D4 | No log rotation | OPEN | Configure LoLa logging to file with rotation. Or use systemd journal (automatic rotation). | 1 hour |
| D5 | Config path hardcoded in commands | OPEN | Use env var `LOLA_CONFIG_PATH` with fallback to `/etc/taktflow/mw_com_config.json`. | 30 min |
| D6 | No versioning of deployed binary | OPEN | Embed git hash at build time: `bazel build --stamp`. Print on startup. | 1 hour |
| D7 | No rollback procedure | OPEN | Document: "Keep previous binary as `can_bridge.prev`. Rollback: `mv can_bridge.prev can_bridge`." | 30 min |

---

## 5. Upstream Maintainer (6 gaps)

| # | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| U1 | No API compatibility test | OPEN | Pin LoLa version in test. Add `test_api_contract.py` that checks skeleton/proxy creation, offer, subscribe, send, receive against specific API signatures. | 2 hours |
| U2 | Config schema not validated | **CLOSED** | Validated structure matches upstream reference. | Done |
| U3 | StringLiteral lifetime concern | OPEN | Review `score::StringLiteral` documentation. Verify `c_str()` lifetime is valid for InitializeRuntime call. Add comment in code. | 30 min |
| U4 | Findings not reported upstream | **CLOSED** | communication#220, toolchains_qnx#46 filed. | Done |
| U5 | Modified Bazel workspace (local fork) | OPEN | Move can_bridge to separate Bazel module that depends on `score_communication` as external dep. Or maintain as patch set (current `score-communication-patches/`). | 4 hours |
| U6 | VehicleSignals struct not verified with type system | OPEN | Add `static_assert(std::is_trivially_copyable<VehicleSignals>::value)`. Verify LoLa type requirements are met at compile time. | 30 min |

---

## 6. New Team Member (6 gaps)

| # | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| N1 | No single README for the bridge | **CLOSED** | README.md created in can_bridge directory. | Done |
| N2 | Build instructions scattered | OPEN | Add `QUICKSTART.md` at project root: clone → setup → build → test → run, in 10 commands. | 1 hour |
| N3 | Depends on laptop SSH access | OPEN | Add devcontainer config (`.devcontainer/devcontainer.json`) with Bazel + CAN tools pre-installed. Anyone can reproduce. | 2 hours |
| N4 | No development environment setup | OPEN | Same as N3. Devcontainer or `nix-shell` with all deps pinned. | 2 hours |
| N5 | Gap analysis requires reading 5 versions | **CLOSED** | This consolidated register replaces v1-v5 as single source of truth. | Done |
| N6 | No architecture decision records | OPEN | Create `docs/decisions/` with ADR format: "ADR-001: Why LoLa as first pilot", "ADR-002: Why CAN bridge on laptop not Pi". | 1 hour |

---

## 7. OEM Integration (6 gaps)

| # | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| O1 | Hardcoded DBC, not DBC-driven decoder | OPEN | Use `cantools` Python library to auto-generate C++ decode() from DBC file. Or embed DBC parsing at runtime. | 1 day |
| O2 | No AUTOSAR ara::com integration | OPEN | Wrap our bridge in proper ara::com service interface. LoLa IS ara::com — our bridge just doesn't use the standardized type registration. | 2 days |
| O3 | No SOME/IP gateway | OPEN | Depends on `score-inc_someip_gateway` maturity. When available, replace CAN→LoLa with CAN→SOME/IP→LoLa path. | Blocked on upstream |
| O4 | Single ECU vendor tested | OPEN | Test with different CAN controllers (PEAK, Kvaser, Vector) on the laptop. Verify socketcan abstraction holds. | 2 hours |
| O5 | No diagnostic integration | OPEN | Add UDS-over-LoLa service that responds to ReadDID requests for bridge status (frame count, latency, errors). | 1 day |
| O6 | x86_64 only | **BLOCKED** | QNX cross-compile blocked (toolchains_qnx#46). | Blocked |

---

## 8. Regulatory (6 gaps)

| # | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| R1 | No safety case | OPEN | Create GSN-notation safety case: top claim "LoLa IPC is safe for ASIL-B vehicle signal exchange" → sub-claims → evidence links to test results. Use `safetycase` Python tool or draw in draw.io. | 2 days |
| R2 | No independent verification | OPEN | Have a second person (not the developer) re-run all tests and sign off. Minimum: different user account runs `assess-lola.sh`. | 2 hours |
| R3 | ASIL-B claims without ASIL-B process | OPEN | Acknowledge: "Our bridge code is QM. Upstream LoLa is ASIL-B qualified by S-CORE. We inherit their qualification for the LoLa library, our bridge code is QM integration." | 30 min |
| R4 | Tool qualification missing | OPEN | Write tool classification: "Bazel=TI1 (no impact on safety), GCC=TI2 (could inject errors), ASan=TI1 (verification tool)." Per ISO 26262-8 Table 4. | 2 hours |
| R5 | No configuration management plan | OPEN | Write `docs/process/cm-plan.md`: git branching strategy, release tagging, artifact storage, change control. | 2 hours |
| R6 | No problem resolution process | OPEN | Create GitHub project board with columns: New → Investigating → Fix in Progress → Verified → Closed. Link FINDING-001/002/003. | 1 hour |

---

## 9. Test Automation (7 gaps)

| # | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| T1 | No CI pipeline for bridge | OPEN | Create `.github/workflows/can-bridge-ci.yml`: on PR → build bridge → run regression test on vcan0. Use ubuntu-24.04 runner with can-utils. | 3 hours |
| T2 | No regression test suite | **CLOSED** | `scripts/regression-test-lola.sh` created. 6 assertions. | Done |
| T3 | Results not machine-parseable | **CLOSED** | `results-lola.json` created with all metrics. | Done |
| T4 | assess-lola.sh not integrated with pytest | OPEN | Make `assess-lola.sh` output JUnit XML. Or replace with pytest-based assessment using `tests/score-communication/build/test_build.py`. | 2 hours |
| T5 | No test data fixtures | OPEN | Create `tests/common/fixtures/known_can_frames.py` with expected CAN frame bytes + expected decoded values. Use in regression tests. | 1 hour |
| T6 | CAN hardware dependency in CI | OPEN | Create `tests/common/utils/vcan_setup.py` that auto-creates vcan0 if not present. CI runs on vcan0 only. | 30 min |
| T7 | No flaky test handling | OPEN | Mark FINDING-001 tests with `@pytest.mark.flaky(reruns=3)`. Install `pytest-rerunfailures`. | 30 min |

---

## 10. System Architect (8 gaps)

| # | Gap | Status | Fix Path | Effort |
|---|---|---|---|---|
| SA1 | CAN bridge on wrong machine (laptop not Pi) | OPEN | Phase 4 of grand plan: QNX cross-compile → deploy on Pi. Blocked by toolchains_qnx#46. Workaround: native build with cmake on Pi (no Bazel). | 1 day when unblocked |
| SA2 | No Ethernet path tested (SOME/IP) | OPEN | Depends on score-inc_someip_gateway maturity + TMS570 Ethernet wiring. Not closable now. | Blocked on HW + upstream |
| SA3 | Lifecycle integration missing | OPEN | Build score-lifecycle on laptop. Start bridge as managed process. Register with health monitor. | 1 day |
| SA4 | No orchestrator integration | OPEN | Build score-orchestrator. Create workload manifest for bridge. Deploy via orchestrator instead of manual start. | 1 day |
| SA5 | Persistency not connected | OPEN | Build score-persistency. Add signal logging: write vehicle signals to KVS on configurable interval. | 1 day |
| SA6 | FEO not integrated | OPEN | Build score-feo. Wrap bridge publish cycle in FEO task. Deterministic cycle-based publishing. | 1 day |
| SA7 | scorehsm not connected | OPEN | Add HMAC signing to LoLa shared memory data using scorehsm host library. Verify signature in proxy. | 2 days |
| SA8 | Only 1 of 11 S-CORE modules tested | OPEN | Next modules in priority: score-baselibs (foundation), score-lifecycle (health), score-persistency (storage). Same assess→build→test→integrate pattern as LoLa. | 1 day each |

---

## Priority Roadmap

### Sprint 1: Documentation + CI (1 week)
Close: A1-A6, N2, N6, R3, R5, R6, T1, T4-T7, D1, S6, S7, U6
**Impact:** ASPICE audit-ready, CI pipeline, deployment guide

### Sprint 2: Code Quality + Security (1 week)
Close: A2, S1, S3-S5, U1, U3, U5, D2-D7, P4, P7
**Impact:** Production-quality bridge code, secure deployment

### Sprint 3: Multi-Module Integration (2 weeks)
Close: SA3-SA6, SA8
**Impact:** LoLa + lifecycle + persistency + orchestrator stack on laptop

### Sprint 4: OEM + Regulatory (2 weeks)
Close: O1, O2, O4, O5, R1, R2, R4, N3-N4
**Impact:** Integrable, safety-cased, reproducible

### Sprint 5: QNX Target (when unblocked)
Close: SA1, SA2, O6, GAP-004, GAP-007
**Impact:** Full 3-chip SoC integration

---

**Total effort to close all 42 open gaps: ~8-10 weeks (1 person)**
