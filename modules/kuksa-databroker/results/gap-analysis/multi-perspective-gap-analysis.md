# KUKSA Databroker -- 10-Perspective Gap Analysis

**Module:** eclipse-kuksa-databroker (v0.6.1-dev.0)
**Date:** 2026-03-27
**Bench:** Ubuntu x86_64 laptop (build/test), Raspberry Pi 4 aarch64 (deployment target)
**Source:** 56 Rust source files, ~15K lines across workspace

## Bench Test Summary

| Check          | Result                  | Detail                                           |
|----------------|-------------------------|--------------------------------------------------|
| Cargo Build    | PASS                    | 1m57s, workspace (databroker + proto + CLI + libs)|
| Unit Tests     | 208/208 PASS            | 179 databroker, 6 proto, 23 kuksa-sdv; 1 ignored |
| Clippy         | PASS                    | 0 warnings                                       |
| Format         | PASS                    | All files formatted                               |
| VSS 4.0 JSON   | Present, parseable      | data/vss-core/vss_release_4.0.json                |

---

## 1. ASPICE Auditor

*Perspective: Does the project demonstrate process maturity sufficient for automotive software development (ASPICE SWE.1-SWE.6)?*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 1.1 | No requirements traceability -- unit tests exist but are not mapped to SWE.2/SWE.3 requirements IDs | High | Open | Create requirements.csv or DOORS export; add `#[doc = "REQ-xxx"]` annotations to test functions |
| 1.2 | No documented software architecture description (SWE.2) -- `doc/` has diagrams but no formal SAD linking modules to design decisions | High | Open | Write SAD document covering broker, gRPC layer, authorization, query engine, VSS parser; reference in README |
| 1.3 | 22 TODO/FIXME comments in production source (broker.rs, val.rs, decoder.rs, types.rs, collector.rs) indicate incomplete implementation against design intent | Medium | Open | Triage each TODO, file issues, add requirement IDs; resolve or document accepted deviations |
| 1.4 | No documented verification strategy (SWE.6) -- test harness uses cucumber BDD features but no test plan document exists mapping scenarios to verification criteria | High | Open | Create test-plan.md linking each .feature scenario to a requirement + expected coverage level |
| 1.5 | Integration tests (`integration_test/test_databroker.py`) require a running server but have no documented setup procedure or CI gate | Medium | Open | Add integration test job to CI; document preconditions in test plan |
| 1.6 | No change management or release notes beyond GitHub Actions draft release workflow | Low | Open | Add CHANGELOG.md with semantic versioning entries per release |

---

## 2. Security Engineer

*Perspective: Is the gRPC/JWT authorization stack hardened against automotive threat models (e.g., UNECE R155)?*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 2.1 | JWT algorithm hardcoded to RS256 only (`decoder.rs:72`) -- TODO comment acknowledges this; no support for ES256/EdDSA means no PQC migration path | High | Open | Make algorithm configurable via CLI flag or JWT header `alg` whitelist |
| 2.2 | JWT audience hardcoded to `kuksa.val` (`decoder.rs:74`) -- not configurable; OEM integration requires per-deployment audience validation | Medium | Open | Add `--jwt-audience` CLI flag |
| 2.3 | No cargo-audit / cargo-deny in CI -- no automated dependency vulnerability scanning; 38 direct dependencies with no SBOM generation | Critical | Open | Add `cargo audit` step to CI; generate CycloneDX SBOM via `cargo-cyclonedx` |
| 2.4 | Test JWT tokens in `jwt/` directory have expiry year 2029 -- tokens with long-lived secrets shipped in repo | Medium | Open | Regenerate test-only tokens with short expiry; add .gitignore for production keys; document key rotation procedure |
| 2.5 | TLS certificates in `certificates/` include private keys (CA.key, Server.key, Client.key) committed to source | High | Open | Move to test-only directory with clear naming; add README warning; never use in production |
| 2.6 | No mTLS (mutual TLS) support -- server authenticates to client but client cert verification is not implemented | Medium | Open | Add `--tls-client-ca` flag for client certificate validation |
| 2.7 | `collector.rs:141` has TODO: "Check if sender is allowed to provide datapoint with this id" -- provider authorization bypass in sdv.databroker.v1 collector | Critical | Open | Implement per-signal provider permission check before accepting datapoint updates |
| 2.8 | No rate limiting on gRPC endpoints -- malicious client can flood subscribe/set requests | High | Open | Add tonic middleware for per-client rate limiting; configure via CLI |
| 2.9 | Authorization disabled by default when no JWT key is provided (falls through to `ALLOW_ALL`) with only a warning log | High | Open | Consider fail-closed default or require explicit `--disable-authorization` flag (partially exists but warn path is too permissive) |
| 2.10 | No audit logging of authorization decisions -- successful/failed auth attempts not logged at structured level | Medium | Open | Add structured tracing events for auth success/failure with client identity |

---

## 3. Performance Engineer

*Perspective: Can the databroker sustain automotive-grade throughput on constrained hardware (RPi4)?*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 3.1 | No benchmark suite -- no criterion or custom benchmarks for signal throughput, subscription fan-out, or query execution | High | Open | Add `benches/` with criterion benchmarks for core paths: set_datapoint, subscribe notify, query execute |
| 3.2 | `Database` uses `HashMap<i32, Entry>` behind `RwLock` -- all reads/writes contend on single lock; will bottleneck on RPi4 with 34 CAN messages at high frequency | Medium | Open | Consider sharded lock or lock-free data structure; profile under load |
| 3.3 | `MAX_SUBSCRIBE_BUFFER_SIZE = 1000` is hardcoded (`broker.rs:40`) -- no runtime tuning for memory-constrained targets | Low | Open | Make configurable via CLI flag |
| 3.4 | Subscription notification clones `EntryUpdate` per subscriber -- with many subscribers, clone overhead may cause GC pressure | Medium | Open | Use `Arc<EntryUpdate>` to share immutable notification across subscribers |
| 3.5 | `FilterManager::get_lowest_filter_interval_per_signal()` calls `.clone()` on entire database HashMap on every invocation (`filter_manager.rs:37`) | Medium | Open | Refactor to avoid full clone; maintain cached lowest-interval map |
| 3.6 | Query executor uses recursive expression evaluation with no depth limit -- deeply nested SQL WHERE clauses could stack overflow | Low | Open | Add recursion depth guard to `execute_internal` |
| 3.7 | No memory usage metrics or OOM protection -- no monitoring of signal tree size or subscription count relative to available RAM on RPi4 (1-4 GB) | Medium | Open | Add prometheus metrics endpoint or log periodic memory stats |
| 3.8 | Release profile uses `opt-level = "s"` (size optimization) -- may sacrifice runtime performance for binary size; needs validation on RPi4 | Low | Open | Benchmark `opt-level = "s"` vs `opt-level = 2` on aarch64 target |

---

## 4. Production Deployment Engineer

*Perspective: Can this be reliably deployed and operated on the Pi4 bench target?*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 4.1 | No aarch64 cross-compilation documented or tested in CI -- `Cross.toml` exists but only passes `RUSTFLAGS`; no `aarch64-unknown-linux-gnu` target in workflows | High | Open | Add cross-compilation job to CI using `cross` tool; validate binary on RPi4 |
| 4.2 | No systemd service file provided -- `sd-notify` integration exists in code but no `.service` unit file for deployment | Medium | Open | Create `kuksa-databroker.service` with appropriate user, working directory, and restart policy |
| 4.3 | No container image for aarch64 -- Dockerfiles exist in `scripts/` but CI only builds x86_64 | Medium | Open | Add multi-arch Docker build (buildx) for linux/arm64 |
| 4.4 | Default bind address is `127.0.0.1` -- bench clients (laptop, other ECUs) cannot connect without explicit `--address 0.0.0.0` | Low | Open | Document deployment command with correct bind address; or change default for production profile |
| 4.5 | No startup validation of VSS JSON file -- if `--vss` file is malformed, errors are logged per-entry but server starts with partial tree | Medium | Open | Add `--strict` mode that fails startup on any VSS parse error |
| 4.6 | Unix socket path `/run/kuksa/databroker.sock` requires root or custom tmpfiles.d -- no documentation for non-root deployment | Low | Open | Document non-root socket path configuration or provide tmpfiles.d config |
| 4.7 | No log rotation configuration -- tracing output goes to stdout; long-running bench deployments will fill journald or log files | Low | Open | Document log rotation setup; consider adding `--log-file` with rotation support |

---

## 5. Upstream Eclipse Maintainer

*Perspective: Is this fork/snapshot maintainable and ready for upstream contribution?*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 5.1 | 81 `unwrap()` calls in production source across 11 files -- violates Rust robustness guidelines; panics in production are unacceptable for automotive | High | Open | Audit each unwrap; replace with proper error handling or `expect()` with descriptive message |
| 5.2 | `sqlparser` dependency pinned to 0.16.0 (current: 0.53+) -- over 37 major versions behind; security and feature gap | Medium | Open | Evaluate upgrade path; test query compatibility |
| 5.3 | `opentelemetry` pinned to 0.19.0 (current: 0.27+) -- significant API changes missed; otel feature likely broken with modern collectors | Medium | Open | Upgrade otel stack or document version constraints |
| 5.4 | `lazy_static` used where `std::sync::OnceLock` (stable since Rust 1.70) would suffice -- unnecessary dependency | Low | Open | Replace `lazy_static!` with `OnceLock` or `LazyLock` |
| 5.5 | Workspace excludes `lib/*` from default members -- lib crates build separately, making CI fragile; contributor may miss lib breakage | Low | Open | Consider including libs in workspace or adding explicit lib CI job |
| 5.6 | `viss` module is behind feature flag with no integration tests -- VISS v2 WebSocket server is untested in CI | Medium | Open | Add VISS feature to test matrix; write integration tests for WebSocket API |

---

## 6. New Team Member

*Perspective: Can a new engineer onboard, understand, and contribute to this module within one week?*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 6.1 | `broker.rs` is 5021 lines -- monolithic file covering database, subscriptions, actuation, signal providers, and all tests; extremely hard to navigate | High | Open | Refactor into sub-modules: database.rs, subscriptions.rs, actuation.rs, providers.rs |
| 6.2 | No architecture diagram linking crate structure to runtime data flow -- existing `doc/diagrams/` has sequence diagrams but no component overview | Medium | Open | Create component diagram showing databroker core, gRPC layer, auth interceptor, VSS parser, CAN provider |
| 6.3 | Cucumber BDD test world setup (`tests/world/mod.rs`) is the only integration test pattern but undocumented -- new contributor won't know how to add test scenarios | Low | Open | Add CONTRIBUTING.md section on writing BDD tests |
| 6.4 | Multiple API versions (kuksa_val_v1, kuksa_val_v2, sdv_databroker_v1) with no decision log explaining when to use which | Medium | Open | Document API version strategy: v1 legacy, v2 current, sdv_databroker_v1 deprecated |
| 6.5 | No developer setup guide for Windows -- `main.rs` uses `std::os::unix::fs::FileTypeExt` and Unix signals; won't compile on Windows without guidance | Low | Open | Document that development/build requires Linux or WSL; add to README prerequisites |

---

## 7. OEM Integration Engineer

*Perspective: Can an OEM integrate kuksa-databroker with their CAN stack and vehicle infrastructure on the bench?*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 7.1 | No documented mapping from bench CAN signals (34 messages, 5 ECUs) to VSS paths -- kuksa-can-provider exists but no DBC-to-VSS mapping file for this bench | High | Open | Create CAN signal mapping YAML/JSON for CVC/FZC/RZC/SC/HSM message types |
| 7.2 | No OEM-specific VSS overlay mechanism -- custom signals (e.g., ME-specific BMS paths) require forking vss_release_4.0.json | Medium | Open | Support VSS overlay files via `--vss` flag accepting multiple files (partially supported via comma-separated list) |
| 7.3 | gRPC reflection is always enabled -- exposes full API surface to any client; OEM security policies may require disabling it | Medium | Open | Add `--disable-reflection` CLI flag |
| 7.4 | No SOME/IP or DDS transport -- bench ECUs using automotive middleware cannot connect directly; requires additional bridging | High | Open | Document integration architecture with kuksa-can-provider and any SOME/IP bridge requirements |
| 7.5 | No signal quality metadata (e.g., timestamp accuracy, signal status/validity flags) -- CAN signals may have validity bits that are lost in VSS mapping | Medium | Open | Extend DataValue or Datapoint with quality/status field; align with VSS quality overlay proposal |
| 7.6 | Protobuf v1 and v2 API running simultaneously -- OEM client must know which API version to target; no version negotiation | Low | Open | Document recommended API version; add deprecation notice for v1 in API docs |

---

## 8. ISO 26262 Compliance Officer

*Perspective: What evidence gaps exist if this module were part of an ASIL-rated system?*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 8.1 | No ASIL classification or safety analysis -- databroker handles actuator targets (e.g., Vehicle.ADAS.ABS.IsEnabled) that are safety-relevant | Critical | Open | Perform HARA; classify signals by ASIL level; document safety requirements for actuator path |
| 8.2 | No defensive programming against data corruption -- `HashMap`-based database has no checksums, no redundant storage, no plausibility checks on values | High | Open | Add range/plausibility validation at ingestion; implement watchdog for stale signals |
| 8.3 | 172 `panic!` calls (mostly in tests but pattern leaks to production via `unwrap`) -- any panic in production = uncontrolled system shutdown | High | Open | Eliminate all panics from non-test code; use `#[cfg(not(test))]` deny-panic lint |
| 8.4 | No defined failure mode for subscription channel overflow -- broadcast channel will drop oldest when full; safety-relevant signals may be silently lost | High | Open | Implement overflow detection with logging; consider back-pressure or fail-safe notification |
| 8.5 | No monotonic timestamp validation -- `SystemTime::now()` can jump backward (NTP correction); signal ordering may be violated | Medium | Open | Use `Instant` for internal ordering; validate source_ts monotonicity |
| 8.6 | No diversity or redundancy in authorization path -- single JWT decoder with single key; compromised key = full system access | Medium | Open | Support multiple trusted keys; add key rotation mechanism |
| 8.7 | Floating point comparison uses direct `==` with TODO comments (types.rs:440,444,466,470) -- IEEE 754 equality is unreliable for safety comparisons | Medium | Open | Implement epsilon-based comparison or use fixed-point for safety-relevant signals |

---

## 9. Test Automation Engineer

*Perspective: Is the test infrastructure sufficient for continuous verification and regression prevention?*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 9.1 | 1 test ignored with no documented reason -- ignored tests indicate either flaky behavior or dead code; neither is acceptable | Low | Open | Investigate ignored test; fix or remove with documented justification |
| 9.2 | No code coverage measurement -- 208 tests exist but coverage percentage unknown; `broker.rs` (5021 lines) likely has significant untested paths | High | Open | Add `cargo-llvm-cov` to CI; set minimum coverage threshold (target: 80%) |
| 9.3 | No fuzz testing -- gRPC protobuf deserialization + SQL query parser + JWT decoder are prime fuzz targets | High | Open | Add `cargo-fuzz` targets for: protobuf input, SQL WHERE clause, JWT token, VSS JSON |
| 9.4 | Integration tests (`integration_test/test_databroker.py`) use Python with sdv.databroker.v1 API only -- kuksa.val.v1 and v2 APIs have no integration tests | High | Open | Add Python integration tests for kuksa.val.v2 API; update proto bindings |
| 9.5 | BDD cucumber tests cover read/write permissions but not: subscribe, actuation, query, glob matching, TLS, multi-client scenarios | Medium | Open | Expand .feature files to cover subscription lifecycle, concurrent access, error paths |
| 9.6 | No load/stress test for subscription fan-out -- unknown behavior when 100+ clients subscribe to same signal | Medium | Open | Create k6 or custom load test targeting subscribe endpoint; measure latency and memory |
| 9.7 | No negative/adversarial test cases -- e.g., malformed JWT, oversized protobuf, SQL injection via query API, path traversal in signal names | High | Open | Add adversarial test suite covering input validation boundaries |
| 9.8 | No test for aarch64 target -- all tests run on x86_64; endianness and alignment issues could surface on ARM | Medium | Open | Add cross-test job using QEMU or native RPi4 in CI |

---

## 10. System Architect

*Perspective: Does the databroker fit cleanly into the SDV bench architecture with 5 ECUs and CAN bus?*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 10.1 | No defined interface contract between kuksa-can-provider and databroker -- provider uses sdv.databroker.v1 collector API which has authorization gaps (see 2.7) | High | Open | Define and document ICD (Interface Control Document) for CAN provider to databroker communication |
| 10.2 | Single-instance architecture with no replication or failover -- RPi4 crash loses all signal state (in-memory only, no persistence) | High | Open | Add optional signal state persistence (SQLite or file-based snapshot); document recovery procedure |
| 10.3 | No signal timestamping alignment across ECUs -- each ECU (CVC/FZC/RZC/SC/HSM) has independent clock; databroker applies server-side timestamp with no correlation | Medium | Open | Support `source_ts` from CAN timestamps; document clock synchronization requirements (PTP/gPTP) |
| 10.4 | No defined signal update frequency contract -- CAN messages arrive at various rates (1ms-1000ms); databroker has no mechanism to validate or enforce expected rates | Medium | Open | Add configurable signal timeout/staleness detection per VSS path |
| 10.5 | gRPC server has no connection limit -- RPi4 with limited file descriptors could be exhausted by misbehaving clients | Medium | Open | Add `--max-connections` flag; configure fd limits in systemd unit |
| 10.6 | No observability stack integration documented -- OpenTelemetry feature exists but uses obsolete API (0.19); no Grafana/Prometheus integration guide for bench monitoring | Medium | Open | Upgrade otel dependency; provide docker-compose with Grafana+Tempo+Prometheus for bench |
| 10.7 | VISS v2 WebSocket server runs on separate port (8090) with no shared auth -- creates split management plane | Low | Open | Unify auth configuration between gRPC and VISS endpoints |
| 10.8 | No message size limits on gRPC -- large array-typed signals (e.g., BMS cell voltages, 96+ values) could create oversized protobuf messages | Low | Open | Configure tonic max message size; validate array signal size at registration |

---

## Summary

| Perspective                    | Gaps | Critical | High | Medium | Low |
|--------------------------------|------|----------|------|--------|-----|
| 1. ASPICE Auditor              |    6 |        0 |    3 |      2 |   1 |
| 2. Security Engineer           |   10 |        2 |    3 |      4 |   1 |
| 3. Performance Engineer        |    8 |        0 |    2 |      4 |   2 |
| 4. Production Deployment       |    7 |        0 |    1 |      3 |   3 |
| 5. Upstream Maintainer         |    6 |        0 |    1 |      3 |   2 |
| 6. New Team Member             |    5 |        0 |    1 |      2 |   2 |
| 7. OEM Integration Engineer    |    6 |        0 |    2 |      3 |   1 |
| 8. ISO 26262 Compliance        |    7 |        1 |    3 |      3 |   0 |
| 9. Test Automation Engineer    |    8 |        0 |    4 |      3 |   1 |
| 10. System Architect           |    8 |        0 |    2 |      5 |   1 |
| **TOTAL**                      | **71** | **3** | **22** | **32** | **14** |

### Top-5 Immediate Actions

1. **[2.3] Add cargo-audit to CI** -- No dependency vulnerability scanning in a security-critical automotive component
2. **[2.7] Fix provider authorization bypass** -- sdv.databroker.v1 collector accepts datapoints without per-signal permission checks
3. **[8.1] Perform safety classification** -- Actuator target signals flow through this component with no ASIL analysis
4. **[9.2] Enable code coverage** -- 208 tests exist but coverage is unmeasured; 5K-line broker.rs likely has significant gaps
5. **[9.3] Add fuzz testing** -- gRPC protobuf, SQL parser, JWT decoder, and VSS JSON parser are high-value fuzz targets

---

*Generated by Taktflow SDV bench testing pipeline, 2026-03-27*
*Audited codebase: eclipse-kuksa-databroker v0.6.1-dev.0*
