# Multi-Perspective Gap Analysis: score-logging Module (DLT Middleware)

**Module**: Eclipse S-CORE `score-logging` (mw::log frontend + datarouter daemon)
**Date**: 2026-03-27
**Auditor**: Taktflow Systems HIL bench analysis
**Platform**: Ubuntu x86_64 (bench laptop)

## Bench Test Summary

| Metric | Result |
|--------|--------|
| Build | PASS -- 1,585 actions, 175 targets, 154s |
| Unit Tests | 36/37 PASS, 1 skipped (`slog_recorder_factory_test`) |
| ASan (C++) | 12/12 PASS |
| ASan (Rust bridge) | N/A -- Rust FFI not exercised under ASan |
| Line Coverage | 87.8% (4,381 / 4,989 lines, 209 files) |
| Format Check | Rust diffs present (upstream style divergence) |

## Module Architecture Reference

- `score/mw/log/` -- C++ logging frontend (DLT-compatible, `mw::log` API)
- `score/datarouter/` -- DLT daemon bridge (filtering, UDP routing, shared-memory IPC)
- `score/mw/log/rust/score_log_bridge/` -- Rust FFI bindings to C++ recorder
- Shared memory MWSR ring buffer for zero-copy log transport
- JSON-based configuration (`logging.json`, `log-channels.json`)
- Targets: x86_64-linux, arm64-qnx, x86_64-qnx

---

## 1. ASPICE Auditor Perspective

*Focus: evidence chain, traceability from requirements to tests, process compliance.*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 1.1 | No `.trlc` requirement files exist in the repository. The TRLC tooling infrastructure is present under `third_party/traceability/` with the RSL model, but zero actual requirement specifications are defined for the logging module. No SWR/SRS documents can be traced. | Critical | OPEN | Author TRLC requirement files for mw::log and datarouter components; link to LOBSTER traceability reports. |
| 1.2 | Test cases lack requirement ID annotations. None of the 29+ C++ test files or Rust test modules contain traceability tags (e.g., `@req`, `SWR-LOG-xxx`) linking test cases to requirements. | Critical | OPEN | Add requirement ID comments/annotations to each test case; integrate with `source_code_linker` tool already in `third_party/traceability/tools/`. |
| 1.3 | The skipped test `slog_recorder_factory_test` has no documented rationale. ASPICE SWE.6 requires justification for any excluded test. The test file exists and compiles but is tagged `manual` in BUILD. | High | OPEN | Document skip reason in the BUILD file and in a test deviation report. Evaluate if the dependency issue (`TextRecorder`) is resolvable. |
| 1.4 | No formal design-to-code traceability. The architecture documents in `score/datarouter/doc/design/` are well written but lack bidirectional links to source code components. | Medium | OPEN | Add design element IDs and reference them in source code headers and BUILD files. |
| 1.5 | LOBSTER configuration files exist (`lobster_sw_unit_rep.conf`, etc.) but no generated traceability reports are present in the repository or CI artifacts. | Medium | OPEN | Add a CI workflow step that runs LOBSTER analysis and publishes the traceability matrix as a build artifact. |

---

## 2. Security Engineer Perspective

*Focus: attack surfaces, input validation, shared memory safety, network exposure.*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 2.1 | Shared memory path `/tmp/logging.<app_id>.<uid>` is predictable and world-accessible. An attacker with local access could create a symlink or pre-create the file to hijack or corrupt the logging channel (TOCTOU race). | Critical | OPEN | Use `O_EXCL` / `O_NOFOLLOW` on `open()`, move to a restricted directory (e.g., `/run/score/`), or use `memfd_create()` with fd passing. |
| 2.2 | JSON configuration files (`logging.json`, `log-channels.json`) are parsed with RapidJSON but no schema validation is applied. Malformed or maliciously crafted JSON could cause unexpected behavior or denial of service. | High | OPEN | Add JSON schema validation before consuming configuration. Consider restricting file permissions to root/service-user only. |
| 2.3 | The UDP multicast output (`udp_stream_output.cpp`) binds to `0.0.0.0` on configurable ports (3491-3493). There is no authentication or encryption on the DLT stream, allowing passive eavesdropping and active injection. | High | By design | Document the threat model. For production, consider TLS-wrapped transport or network segmentation requirements. DLT protocol itself lacks encryption by specification. |
| 2.4 | The Rust FFI bridge uses `unsafe` extensively (24+ `unsafe` blocks in `ffi.rs`) including raw pointer dereference, `transmute`, and `from_utf8_unchecked`. While safety comments are present, no `cargo audit` or `miri` pass is documented. | Medium | OPEN | Add `cargo audit` to CI. Run `miri` on unit tests where feasible. Consider reducing `transmute` usage with `to_ne_bytes()` patterns. |
| 2.5 | `set_var()` in `score_log_bridge.rs:113` is called in `unsafe` context to set `MW_LOG_CONFIG_FILE`. The safety comment states "safe only before any other thread started" but this invariant is not enforced by the type system or runtime check. | Medium | OPEN | Consider using `std::sync::OnceLock` or a build-time configuration mechanism instead of environment variable mutation. |
| 2.6 | No rate limiting on log message ingestion at the frontend. A compromised or misconfigured application could flood the shared memory ring buffer, causing log loss for other applications. | Medium | OPEN | Implement per-application quota enforcement in the datarouter. Config keys for quotas exist in test fixtures (`log-channels-quotas*.json`) but are not enabled by default. |

---

## 3. Performance Engineer Perspective

*Focus: benchmarks, latency measurements, throughput characterization.*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 3.1 | No benchmark tests exist anywhere in the repository. Grep for `benchmark`, `latency`, `throughput`, `perf_test` returns zero benchmark harnesses. For a logging framework where "minimal performance overhead" is a stated design constraint, this is a significant gap. | Critical | OPEN | Add Google Benchmark or Bazel benchmark targets measuring: log call latency (p50/p99/p999), throughput (msgs/sec), shared memory write contention, DLT serialization cost. |
| 3.2 | The `ringBufferSize` (768KB) and `slotSizeBytes` (4096) in default `logging.json` are undocumented regarding their sizing rationale. No guidance on how to tune for different workloads. | Medium | OPEN | Document sizing methodology. Provide a benchmark tool that helps users determine optimal parameters for their workload. |
| 3.3 | The shared memory POSIX mutex acquisition strategy (writer never waits for reader) is described in design docs but not validated by stress tests. Race conditions under heavy load are untested. | High | OPEN | Add a multi-threaded stress test with configurable writer count and message rates. Validate that the wait-free producer queue lives up to its name under contention. |
| 3.4 | No profiling data for the datarouter's log parsing and DLT formatting path. The `logparser` component deserializes from shared memory and formats DLT packets -- this is the hot path for production throughput. | Medium | OPEN | Profile the datarouter under realistic load. Publish flame graph or perf analysis as part of release documentation. |
| 3.5 | Build time of 154s for 175 targets is reasonable but no build caching metrics are tracked across CI runs. Incremental build performance is unknown. | Low | OPEN | Add build timing instrumentation to CI. Track and alert on build time regressions. |

---

## 4. Production Deployment Engineer Perspective

*Focus: deployment artifacts, monitoring, operational readiness.*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 4.1 | No container/packaging definition. The module produces Bazel build artifacts but there is no Dockerfile, OCI manifest, or systemd service unit for deploying the datarouter daemon. | High | OPEN | Provide reference deployment artifacts: systemd unit file for datarouter, container image definition, or Yocto recipe. |
| 4.2 | No health check or liveness probe for the datarouter daemon. If the daemon crashes or hangs, there is no mechanism for external monitoring to detect it. | High | OPEN | Implement a health endpoint (e.g., Unix domain socket status query) or watchdog integration (QNX HAM / systemd watchdog). |
| 4.3 | The `statistics_reporter` component exists but its output format and collection mechanism are not documented. Operational metrics (messages processed, buffer utilization, drop count) are not exposed in a monitoring-friendly format. | Medium | OPEN | Expose metrics via a standard interface (e.g., structured JSON on a monitoring socket, or DLT self-logging with well-known context IDs). |
| 4.4 | Log rotation and disk space management for file-based logging (`file_recorder`) is not documented. The `logfilePath` config option points to `/tmp` by default with no size limits. | Medium | OPEN | Document file rotation policy. Implement or document integration with logrotate. Add maximum file size and retention count to configuration. |
| 4.5 | No graceful shutdown sequence documented. The design mentions destructor-based cleanup but does not address signal handling for production daemon lifecycle (SIGTERM, SIGINT). Signal handling code exists in `detail/utils/signal_handling/` but integration is unclear. | Medium | OPEN | Document the shutdown sequence. Add integration test for graceful shutdown under pending messages. |

---

## 5. Upstream Eclipse Maintainer Perspective

*Focus: API correctness, compatibility, contribution quality.*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 5.1 | `project_config.bzl` declares `source_code: ["rust"]` only, but the module is predominantly C++ (~277 .cpp/.h files vs 7 .rs files). This misconfiguration may cause license checking tools to skip C++ source scanning. | High | OPEN | Update to `"source_code": ["cpp", "rust"]` to match actual module content. |
| 5.2 | Rust formatting diffs are present (upstream style divergence). The `rustfmt.toml` exists but CI `format.yml` workflow may not enforce it consistently, or the upstream style differs from local. | Medium | OPEN | Run `rustfmt` with the project's `rustfmt.toml` and submit a formatting PR, or document the accepted divergence. |
| 5.3 | The `MODULE.bazel` version is `0.0.0` with `compatibility_level = 0`. For a module at 87.8% coverage with substantial functionality, a proper semantic version should be established. | Medium | OPEN | Define and publish a versioning strategy. Tag a `0.1.0` release when API stability criteria are met. |
| 5.4 | The `README.md` is a generic template ("C++ & Rust Bazel Template Repository") and does not describe the actual logging module functionality, API, or usage. | Medium | OPEN | Write a module-specific README covering: purpose, API overview, configuration, build instructions, and example usage. |
| 5.5 | Two `git_override` directives in `MODULE.bazel` pin `score_baselibs` and `score_communication` to specific commits rather than tagged releases. This creates fragile dependency chains. | Low | OPEN | Migrate to tagged dependency versions when available in the Bazel registry. |
| 5.6 | The DLT protocol header file (`dlt_protocol.h`) carries a legacy GENIVI MPL-2.0 license header, while the rest of the module uses Apache-2.0. License compatibility should be verified. | Medium | OPEN | Verify MPL-2.0 compatibility with Apache-2.0 for the project. Document the dual-license situation in NOTICE file if acceptable. |

---

## 6. New Team Member Perspective

*Focus: documentation quality, onboarding friction, build reproducibility.*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 6.1 | No developer onboarding guide. The README is template boilerplate. A new contributor would not know: what the module does, how to run tests, how to configure a local dev environment, or how the components relate. | High | OPEN | Write a CONTRIBUTING-specific onboarding section or a `docs/getting-started.md` covering architecture overview, build prerequisites, and test execution. |
| 6.2 | The `.devcontainer/devcontainer.json` exists but its contents and prerequisites are not documented. It is unclear whether it provides a fully reproducible build environment. | Medium | OPEN | Document devcontainer usage. Verify it includes all toolchains (GCC 12.2, Ferrocene Rust, Bazel). |
| 6.3 | Design documents reference UML images (`uml/context-ecu.png`, etc.) that may not render on GitHub. PlantUML sources exist (`.puml` files) but the generated PNG rendering pipeline is not documented. | Low | OPEN | Add PlantUML rendering to the docs build workflow. Alternatively, commit rendered PNGs and keep them in sync. |
| 6.4 | The `docs/` top-level directory contains only Sphinx scaffolding (`conf.py`, `index.rst`) with minimal content. The actual design documentation is scattered across `score/datarouter/doc/` and `score/mw/log/design/`. | Medium | OPEN | Consolidate documentation structure. Either use Sphinx to pull in all design docs, or restructure to a single documentation root. |
| 6.5 | Build requires QNX credentials (`SCORE_QNX_USER`, `SCORE_QNX_PASSWORD`) for cross-compilation configs. It is not clear which builds a contributor can run without QNX access. | Low | OPEN | Document which `--config` flags require QNX access and which work on standard Linux. Make it explicit that `x86_64-linux` is the accessible-to-all config. |

---

## 7. OEM Integration Engineer Perspective

*Focus: AUTOSAR/DLT mapping, vehicle integration, ECU compatibility.*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 7.1 | No `ara::log` adapter implementation is present in this repository. The design documents reference `ara::log` extensively as the AUTOSAR-standard interface, but the actual adapter code appears to live elsewhere (possibly in `score_baselibs`). Cross-module dependency is not documented. | High | OPEN | Document where `ara::log` implementation lives and how it depends on `mw::log`. Provide a clear integration guide for OEM AUTOSAR stacks. |
| 7.2 | DLT non-verbose mode is disabled by default (`enable_nonverbose_dlt=False` in `.bazelrc`). For production vehicle deployment, non-verbose DLT is essential for bandwidth efficiency. The enablement path and testing status are unclear. | High | OPEN | Test and document the non-verbose DLT path. Add CI coverage for the `enable_nonverbose_dlt=True` build configuration. |
| 7.3 | The ECU ID in `log-channels.json` uses test values (`TST1`, `TST2`, `TST3`). No guidance exists for how OEMs should map their ECU topology to the channel configuration. | Medium | OPEN | Provide an OEM integration guide with ECU ID mapping strategy, channel configuration examples for multi-ECU setups. |
| 7.4 | FIBEX/ODX metadata generation for non-verbose messages is referenced in the design doc (`fibex_helper_visitor`) but no FIBEX output files or generation tooling is present in the repository. | Medium | OPEN | Include or reference the FIBEX generator tooling. Provide sample FIBEX output for DLT viewer integration. |
| 7.5 | Persistent logging feature is disabled by default (`persistent_logging=False`). For OEM crash analysis use cases (post-mortem log retrieval), this is a key feature. No test coverage is visible for the enabled path. | Medium | OPEN | Enable and test persistent logging in CI. Document storage requirements and flash wear considerations for automotive deployment. |
| 7.6 | The file transfer feature (`file_transfer=False`) is disabled by default. The DLT file transfer capability is important for uploading core dumps and diagnostic files. | Low | OPEN | Document enablement path. Add integration test for DLT file transfer end-to-end. |

---

## 8. ISO 26262 Compliance Officer Perspective

*Focus: safety case, ASIL classification, tool qualification, freedom from interference.*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 8.1 | The `project_config.bzl` declares `asil_level: "QM"`, but the design document states "Application-side library requires safety-critical qualification" and discusses ASIL D writers sharing memory with QM reader. The safety classification is inconsistent. | Critical | OPEN | Clarify the ASIL decomposition. If `mw::log` frontend runs in ASIL D processes, it needs appropriate qualification or FFI analysis. Document the ASIL boundary explicitly. |
| 8.2 | No freedom-from-interference (FFI) analysis document exists. The design doc mentions "freedom-from-interference analysis only for mw::log interactions" is needed, but no such analysis is present. | Critical | OPEN | Produce an FFI analysis for the shared memory interface between ASIL D applications and the QM datarouter. Address memory corruption propagation, timing interference, and resource exhaustion. |
| 8.3 | Tool qualification evidence is absent. Bazel, GCC 12.2, Ferrocene Rust, GoogleTest, and RapidJSON are used as development tools but no Tool Confidence Level (TCL) assessment or tool qualification report exists. | High | OPEN | Perform TCL assessment per ISO 26262-8 Clause 11. Ferrocene Rust has ISO 26262 qualification -- reference its qualification report. Assess remaining tools. |
| 8.4 | No MISRA C++ or AUTOSAR C++ coding guideline compliance check is configured. For safety-related C++ code, static analysis against automotive coding standards is expected. | High | OPEN | Configure `clang-tidy` with AUTOSAR C++ checks or integrate a MISRA checker. Add results to CI. |
| 8.5 | The shared memory design allows the QM reader (datarouter) to modify shared memory used by ASIL D writers. The design doc acknowledges this: "the reader can (and does) modify the shared memory." This is an FFI violation for mixed-ASIL deployments. | Critical | OPEN | Implement the read-only fd handle approach described in the design doc (`/proc/self/fd/<fd>` reopening). Until then, document the restriction that mixed-ASIL deployment is not supported. |
| 8.6 | No software safety manual or safety plan references the logging module. | Medium | OPEN | Create a safety manual entry for the logging module defining its role in the safety architecture, usage constraints, and diagnostic capabilities. |

---

## 9. Test Automation Engineer Perspective

*Focus: CI pipeline completeness, regression detection, result format, flakiness.*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 9.1 | CI does not run tests -- only builds. The `build.yml` workflow runs `bazel build` but not `bazel test`. Tests are only indirectly run via the `coverage_report.yml` workflow. A build-only CI misses runtime failures. | Critical | OPEN | Add explicit `bazel test //... --config x86_64-linux` step to the main build workflow. |
| 9.2 | No ASan/TSan/UBSan CI workflow exists. The bench ASan results (12/12 pass) were run manually. Sanitizer runs should be automated. | High | OPEN | Add CI workflows for Address Sanitizer, Thread Sanitizer (critical for shared memory concurrency), and Undefined Behavior Sanitizer. |
| 9.3 | No QNX cross-compilation test execution in CI. The `build_qnx8.yml` workflow likely only builds (not tests) for QNX targets. Runtime testing on QNX requires target hardware or QEMU. | Medium | OPEN | Document the QNX test execution strategy. If QEMU-based testing is feasible, add it to CI. Otherwise, define the manual test matrix. |
| 9.4 | Test results are not published in machine-parseable format (JUnit XML, TAP). The `test_output=errors` in `.bazelrc` only shows errors in stdout. No CI artifact collection for test results. | Medium | OPEN | Add `--test_output=xml` or use `bazel-testlogs` artifact collection. Publish JUnit XML results for CI dashboard integration. |
| 9.5 | Coverage is measured at 87.8% but no coverage gate (minimum threshold) is configured in CI. Coverage could regress without detection. | Medium | OPEN | Add a coverage threshold check (e.g., fail CI if coverage drops below 85%). Use `genhtml` or a coverage comparison tool. |
| 9.6 | The Rust bridge tests are not run under ASan. The bench results show "Rust bridge N/A" for ASan. FFI boundary bugs are a known class of memory safety issues. | High | OPEN | Configure Rust tests with `-Zsanitizer=address` (requires nightly or Ferrocene support). At minimum, test the C++ adapter layer that backs the Rust FFI calls. |
| 9.7 | No integration test exists for the full pipeline: application -> mw::log -> shared memory -> datarouter -> DLT output. All tests are unit-level with mocks. | High | OPEN | Add end-to-end integration tests. The `examples/` directory has sample code but no automated verification of its output. |

---

## 10. System Architect Perspective

*Focus: integration with other S-CORE modules, interface contracts, scalability.*

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 10.1 | Hard dependency on `score_baselibs` and `score_communication` via `git_override` commit pins. Interface contracts between modules are implicit (header compatibility) rather than explicit (versioned API). | High | OPEN | Define explicit API versioning and compatibility guarantees. Publish interface headers as a stable, versioned artifact. |
| 10.2 | The message passing interface between mw::log and datarouter uses `score/message_passing/` from `score_communication`. The protocol is not versioned -- a mismatch between frontend and daemon versions could cause silent data corruption. | High | OPEN | Add protocol version negotiation to the connect handshake. Include version in `DatarouterMessageIdentifier::kConnect` message. |
| 10.3 | No documentation of the module's resource requirements (CPU, memory, file descriptors, shared memory segments). System integrators cannot size their platform without this data. | Medium | OPEN | Document resource consumption: shared memory per application (configurable), file descriptors per connection, CPU budget for datarouter. |
| 10.4 | The logging module does not integrate with S-CORE's execution management or state management modules. Startup ordering and dependency declaration rely on OS-level mechanisms. | Medium | OPEN | Define the integration contract with S-CORE execution management. Document startup dependencies and ordering requirements. |
| 10.5 | Shared memory naming convention (`/tmp/logging.<app_id>.<uid>`) may conflict with other S-CORE modules using `/tmp` for IPC. No namespace isolation mechanism is documented. | Low | OPEN | Coordinate shared memory naming with other S-CORE modules. Consider a centralized IPC namespace registry or use abstract Unix domain socket names. |
| 10.6 | The datarouter's dependency on `score/os/utils/path.h` and other OS abstraction layers is not documented. It is unclear which S-CORE OS abstraction features are required vs. optional. | Low | OPEN | Document the OS abstraction layer dependency graph. This helps platform porters understand what must be implemented for new targets. |

---

## Summary Statistics

| Severity | Count |
|----------|-------|
| Critical | 7 |
| High | 15 |
| Medium | 21 |
| Low | 7 |
| Info | 0 |
| **Total** | **50** |

| Status | Count |
|--------|-------|
| OPEN | 49 |
| By design | 1 |
| CLOSED | 0 |

## Top 5 Priority Actions

1. **FFI/Safety analysis** (8.1, 8.2, 8.5): The mixed-ASIL shared memory interface is the highest-risk gap. The design doc already identifies the mitigation (read-only fd) but it is not implemented. This blocks any safety-related deployment.

2. **Requirement traceability** (1.1, 1.2): Zero TRLC requirement files means zero traceability evidence. The tooling infrastructure is ready -- it just needs content. This is an ASPICE SWE.1-SWE.6 blocker.

3. **CI test execution** (9.1, 9.2, 9.7): Tests are not run in the main CI workflow, sanitizers are not automated, and no integration tests exist. The module has good unit test coverage but the CI pipeline does not exploit it.

4. **Performance validation** (3.1, 3.3): A logging framework with "minimal overhead" as a design goal but zero benchmarks cannot substantiate its claims. The wait-free producer queue needs stress testing.

5. **Shared memory security** (2.1, 2.6): The predictable `/tmp` path and lack of rate limiting are exploitable in multi-tenant deployments. The mitigations are straightforward (`memfd_create`, quotas).

---

*Generated by Taktflow Systems bench analysis pipeline, 2026-03-27.*
