# Multi-Perspective Gap Analysis: score-orchestrator

**Module**: `score-orchestrator` (Eclipse S-CORE)
**Date**: 2026-03-27
**Bench Environment**: Ubuntu x86_64 (laptop)
**Workspace**: 5-crate Cargo workspace (orchestration, orchestration_macros, xtask, test_scenarios/rust, camera_drv_object_det)

## Bench Test Summary

| Check | Result |
|-------|--------|
| Build (Cargo) | PASS -- 48.8s |
| Unit Tests | 108/108 PASS, 0 failed, 3 ignored (doc-tests) |
| Clippy | PASS (0 warnings, -D warnings) |
| Format | Diffs in test_scenarios (upstream style choice) |
| Dependencies | kyron-foundation, kyron, iceoryx2, tracing, libc |

---

## 1. ASPICE Auditor

Assessment of process maturity, traceability, and work product completeness per Automotive SPICE SWE.1-SWE.6.

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 1.1 | No requirements traceability matrix linking SW requirements to unit tests. The 108 unit tests are not mapped to any SWE.1 artifacts. | HIGH | Open | Create RTM linking each test function to a requirement ID. Add `#[doc]` annotations with req IDs on tests. |
| 1.2 | No code coverage report (line, branch, MC/DC). 108 tests pass but coverage percentage is unknown. | HIGH | Open | Integrate `cargo-llvm-cov` or `tarpaulin` into CI. Add coverage gate (target: 80% line, 60% branch). |
| 1.3 | `todo!()` macros in production code (`catch.rs:293`, `api/mod.rs:155`, `program_database.rs:744-752`) will panic at runtime. ASPICE SWE.3 requires complete implementation. | HIGH | Open | Replace all `todo!()` with proper error handling or `unimplemented!()` with documented rationale. File tracking issues for each. |
| 1.4 | No architectural design document (SWE.2 work product). README focuses on build instructions, not component architecture. | MEDIUM | Open | Create architecture document covering Design/Deployment/Orchestration split, action tree model, event subsystem. |
| 1.5 | 3 ignored doc-tests suggest incomplete or broken documentation examples. | LOW | Open | Fix or explicitly mark as `no_run` with justification. |
| 1.6 | No change log or release notes tracked. Version is 0.0.3 with no CHANGELOG file. | MEDIUM | Open | Add CHANGELOG.md following keep-a-changelog format. |

---

## 2. Security Engineer

Assessment of attack surface, unsafe code, dependency supply chain, and data integrity.

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 2.1 | No `cargo-deny` or `cargo-audit` configuration. No SECURITY.md policy. No vulnerability scanning in CI. | HIGH | Open | Add `deny.toml` with license/advisory/sources checks. Add `cargo audit` to CI. Create SECURITY.md with disclosure process. |
| 2.2 | 16 `unsafe` blocks across 5 files (`orch_locks.rs`, `runtime_seq_acc.rs`, `catch.rs`, `event.rs`, `testing/mod.rs`). No `#![forbid(unsafe_code)]` at crate root. No SAFETY justification comments. | HIGH | Open | Add `// SAFETY:` comments per Rust unsafe guidelines on every `unsafe` block. Consider `#![deny(unsafe_code)]` at crate root with `#[allow]` per-block. |
| 2.3 | `unsafe impl Send for HandlerType` in `catch.rs:193` bypasses compiler Send checking. Comment says "underlying type is send" but `Arc<Mutex<dyn FnMut>>` is already Send -- impl may be unnecessary or masking a real issue. | HIGH | Open | Verify if the manual `unsafe impl Send` is actually needed. If so, add formal SAFETY proof. If not, remove it. |
| 2.4 | Raw `libc::poll`, `libc::recv` calls in `event.rs` with manual pointer arithmetic. No bounds checking documented. | MEDIUM | Open | Wrap in safe abstraction layer. Add bounds-check assertions. Consider using `nix` crate for safe POSIX wrappers. |
| 2.5 | Git dependencies pinned to SHA revisions (kyron at `caa9c0b`, iceoryx2 at `d3d1c9a`) but no checksum verification beyond Git SHA. | MEDIUM | Open | Add `Cargo.lock` integrity verification in CI. Consider mirroring dependencies. |
| 2.6 | `InvokeMethod::action_future` calls `.lock().unwrap()` on Mutex -- poison panic on poisoned mutex. | MEDIUM | Open | Handle `PoisonError` gracefully: log and return `ActionExecError::Internal`. |

---

## 3. Performance Engineer

Assessment of latency, allocation patterns, scalability, and real-time suitability.

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 3.1 | `Program::run_n_cycle` uses `std::thread::sleep` (blocking) for cycle timing. Comment explicitly says "ATTENTION: Currently this is `dev` feature that does BLOCKING sleep". Blocks the async runtime. | HIGH | Open | Replace with async timer (e.g., `kyron::time::sleep` or platform timer). Current impl will starve other tasks on the same worker. |
| 3.2 | `Meter` uses `println!` for metrics output. No structured metrics export (Prometheus, Perfetto, or tracing spans). | MEDIUM | Open | Replace `println!` with `tracing::info!` or structured metrics sink. Module already has Perfetto script but `Meter` bypasses it. |
| 3.3 | `max_concurrent_action_executions` defaults to 2 in `DesignConfig`. No documentation on how to tune this for production workloads or what happens when pool is exhausted. | MEDIUM | Open | Document pool sizing guidance. Add tracing when pool acquisition fails. Consider dynamic sizing or backpressure. |
| 3.4 | No benchmarks (`cargo bench`, `criterion`). 48.8s build but zero performance regression data. | MEDIUM | Open | Add `benches/` with criterion benchmarks for action dispatch, concurrency join, and program iteration latency. |
| 3.5 | `ReusableBoxFuturePool` pool exhaustion returns `CommonErrors::GenericError` with no diagnostic context. Silent failure in hot path. | MEDIUM | Open | Add pool exhaustion counter/tracing. Return a more specific error variant. |
| 3.6 | `Meter` running average uses `i64` division which truncates. Over many iterations this introduces cumulative error. | LOW | Open | Use exponential moving average or floating-point accumulator for production metering. |

---

## 4. Production Deployment Engineer

Assessment of packaging, configuration, observability, and operational readiness.

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 4.1 | `use_config(&mut self, _path: &Path)` is `todo!()`. Config-by-file deployment path is completely unimplemented. | HIGH | Open | Implement config file parser (TOML/JSON) or remove from public API and document config-by-code as the only supported mode. |
| 4.2 | No health check or readiness probe API. `OrchProgramManager` provides no way to query orchestration state. | MEDIUM | Open | Add `is_running()`, `program_count()`, `last_error()` status methods to `OrchProgramManager`. |
| 4.3 | No graceful shutdown timeout enforcement. `stop_timeout` field exists in `Program` but is marked `#[allow(dead_code)]` and the TODO(#151) confirms it is unused. | HIGH | Open | Implement stop timeout with abort-on-expiry. This is critical for production shutdown sequencing. |
| 4.4 | No container/packaging artifacts (Dockerfile, systemd unit, OCI manifest). Only raw Cargo/Bazel build. | LOW | Open | Add deployment packaging for target platforms. At minimum, document the deployment artifact and its runtime requirements. |
| 4.5 | Iceoryx2 IPC polling thread is started as a side-effect in `design_done()` with no shutdown path visible. Thread leak risk on re-initialization. | MEDIUM | Open | Add explicit lifecycle management for the IPC polling thread. Ensure cleanup on drop or explicit shutdown. |

---

## 5. Upstream Eclipse Maintainer

Assessment of project hygiene, CI completeness, and contribution readiness.

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 5.1 | `rustfmt` diffs present in `test_scenarios`. CI has a format workflow but either it does not cover test_scenarios or upstream intentionally diverges. | MEDIUM | Open | Either add `test_scenarios` to `rustfmt` CI check scope or add `.rustfmt.toml` override with documented rationale. |
| 5.2 | `InvokeMethod` returns name `"InvokeAsync"` (line 363 of invoke.rs). This is a copy-paste bug -- synchronous method invoke reports as async. | MEDIUM | Open | Fix `fn name()` to return `"InvokeMethod"`. Same issue for `InvokeMethodAsync` which also returns `"InvokeAsync"`. |
| 5.3 | `#[allow(clippy::from_over_into)]` used in `catch.rs:217` and `action.rs:50`. These should be `From` impls per Rust API guidelines. | LOW | Open | Refactor `Into` impls to `From` impls. Remove the clippy allows. |
| 5.4 | `#![allow(dead_code)]` at module level in `catch.rs:14`. Suppresses warnings across the entire file rather than on specific items. | LOW | Open | Move `#[allow(dead_code)]` to specific unused items with documented reason. |
| 5.5 | LICENSE file referenced as `LICENSE.md` in workspace Cargo.toml but actual file is `LICENSE` (no .md extension). | LOW | Open | Align `license-file` in Cargo.toml with actual filename. |

---

## 6. New Team Member

Assessment of onboarding friction, documentation completeness, and API discoverability.

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 6.1 | No inline documentation on `ActionTrait` explaining the reusable-box-future pattern. The `try_execute` contract is non-obvious (returns a pool-managed future, not a new allocation). | HIGH | Open | Add extensive `///` docs on `ActionTrait` explaining the reusable future pool lifecycle, ownership, and re-entrancy rules. |
| 6.2 | `Design` vs `Deployment` vs `Orchestration` split is documented in module-level doc comment (`api/mod.rs`) but not linked from README or any onboarding guide. | MEDIUM | Open | Add "Architecture Overview" section to README or link to the module docs. |
| 6.3 | Test helpers (`MockActionBuilder`, `OrchTestingPoller`) in `testing/mod.rs` are `#[cfg(test)]` only. No explanation of how to write a new test scenario. | MEDIUM | Open | Add a `TESTING.md` or doc comments explaining how to add a new test scenario, use mock runtime, and interpret results. |
| 6.4 | `Tag` type is a copy type wrapping a string but uses `from_str_static` and `.into()` inconsistently across the codebase. No style guide on which to use. | LOW | Open | Document preferred `Tag` construction pattern. Consider deprecating one path. |

---

## 7. OEM Integration Engineer

Assessment of integration readiness for automotive OEM platforms (AUTOSAR Adaptive, QNX, custom RTOS).

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 7.1 | QNX8 build is scripted but no cross-compilation CI evidence for aarch64-linux targets. Bench tests run on x86_64 only. | HIGH | Open | Add aarch64 cross-compilation to CI. Run unit tests under QEMU or on target hardware. |
| 7.2 | No SOME/IP, DDS, or AUTOSAR Adaptive binding for the event system. Only iceoryx2 IPC is implemented. | MEDIUM | Open | Define event provider abstraction (already partially done via `IpcProvider` trait). Document how OEMs can implement custom IPC backends. |
| 7.3 | No integration test demonstrating multi-process orchestration. All 12 test scenarios are single-process. | MEDIUM | Open | Add multi-process integration test using iceoryx2 IPC between two orchestrator instances. |
| 7.4 | Hard dependency on `libc` for raw poll/recv in iceoryx event handling. Not portable to non-POSIX RTOS. | MEDIUM | Open | Abstract platform-specific polling behind a trait. Provide QNX-specific implementation. |
| 7.5 | No API versioning or stability guarantees. Version 0.0.3 with no deprecation policy. OEMs need stable API surface. | MEDIUM | Open | Mark stable public API items. Document semver policy. Consider 0.1.0 release with API freeze on core traits. |

---

## 8. ISO 26262 Compliance Officer

Assessment against ISO 26262 Part 6 (Software Development) for ASIL-B or higher.

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 8.1 | No ASIL classification or safety concept document for the orchestration module. | HIGH | Open | Create safety concept defining ASIL level, freedom from interference arguments, and safety mechanisms. |
| 8.2 | `unsafe` code in `orch_locks.rs` and `runtime_seq_acc.rs` implements custom synchronization primitives. No formal proof of correctness beyond loom tests. | HIGH | Open | Complete loom model-checking coverage. Document formal safety argument for each unsafe block per ISO 26262-6 Table 9. |
| 8.3 | `not_recoverable_error!` macro calls are scattered without documented recovery strategy. ISO 26262 requires defined behavior for all error paths. | HIGH | Open | Map each `not_recoverable_error!` call to a safety-relevant failure mode. Document whether system enters safe state. |
| 8.4 | No FMEA or FTA for orchestrator failure modes (action timeout, pool exhaustion, IPC failure, shutdown race). | MEDIUM | Open | Conduct FMEA for orchestration subsystem. Cross-reference with `ActionExecError` variants. |
| 8.5 | `ConcurrencyJoin` does not abort sibling branches on failure. A failed branch continues to run while error is reported. Potential freedom-from-interference violation. | MEDIUM | Open | Document design decision (no cancellation). Add safety argument that running branches cannot cause hazardous output after error detection. |

---

## 9. Test Automation Engineer

Assessment of test infrastructure, coverage, flake resilience, and CI/CD integration.

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 9.1 | Component integration tests (Python/pytest) are nightly-only with 20x repeat for flake detection. No evidence these were run on the bench. | MEDIUM | Open | Run CIT suite on bench. Document results. Add to bench test matrix. |
| 9.2 | `#[ensure_clear_mock_runtime]` macro is used on ~10 tests but its cleanup semantics are not documented. Potential test isolation issue if a test panics before cleanup. | MEDIUM | Open | Document `ensure_clear_mock_runtime` behavior on panic. Verify it uses Drop-based cleanup. |
| 9.3 | No property-based or fuzz testing. `ActionExecError` has limited variants but `UserErrValue(u64)` has full u64 range -- no boundary tests. | MEDIUM | Open | Add `proptest` or `quickcheck` tests for error propagation paths. Add fuzz target for `ProgramDatabase` registration. |
| 9.4 | No Miri CI step. Tests are `#[cfg(not(miri))]` excluded in `deployment.rs` but no evidence Miri runs on any subset. | MEDIUM | Open | Add Miri to CI for at least the core action/lock modules that use unsafe. |
| 9.5 | Mock runtime `step()` uses fixed step counts (e.g., `for _ in 0..10`). Brittle if internal scheduling changes. | LOW | Open | Replace fixed-count stepping with `step_until_idle()` or `step_until(predicate)` pattern. |
| 9.6 | No test for `OrchProgramManager::get_shutdown_notifier` error path or `get_shutdown_all_notifier` with empty events. | LOW | Open | Add negative test cases for shutdown notifier retrieval. |

---

## 10. System Architect

Assessment of modularity, extensibility, design patterns, and cross-cutting concerns.

| # | Gap | Severity | Status | Fix Path |
|---|-----|----------|--------|----------|
| 10.1 | `Rc<RefCell<>>` used for `EventCreator` (`events_provider.rs`) in what is otherwise a `Send + Sync` architecture. This prevents moving the Deployment phase across threads. | HIGH | Open | Replace `Rc<RefCell<>>` with `Arc<Mutex<>>` or redesign event creator lifecycle to avoid shared mutability. |
| 10.2 | Type-state pattern (`_EmptyTag` -> `_DesignTag`) for API phases is good but does not compile-enforce the Deployment -> ProgramManager transition. `use_config` and `add_program` can be called in wrong order. | MEDIUM | Open | Add `_DeploymentTag` type state. Enforce Deployment -> build transition at compile time. |
| 10.3 | `Program` struct mixes execution state (running action) with definition (name, action tree). No separation of program definition from program instance. | MEDIUM | Open | Split into `ProgramDef` (immutable definition) and `ProgramRunner` (mutable execution state). Enables program re-instantiation. |
| 10.4 | No plugin/extension point for custom action types. All actions (Sequence, Concurrency, Invoke, Catch, Graph, IfElse) are hardcoded. Third parties must fork to add new action types. | MEDIUM | Open | `ActionTrait` is public but `ActionBaseMeta` construction requires internal knowledge. Document how to implement custom actions. |
| 10.5 | `DesignConfig::max_concurrent_action_executions` is a global constant but different programs may need different concurrency limits. No per-program configuration. | LOW | Open | Allow per-program or per-action concurrency configuration. |
| 10.6 | `GrowableVec` used pervasively as the collection type. Its growth/lock semantics are opaque from the orchestrator's perspective. Tight coupling to kyron-foundation internals. | LOW | Open | Abstract collection usage behind a trait or type alias to enable alternative implementations. |

---

## Summary

| Perspective | Gaps | Critical/High | Medium | Low |
|-------------|------|---------------|--------|-----|
| 1. ASPICE Auditor | 6 | 3 | 2 | 1 |
| 2. Security Engineer | 6 | 3 | 3 | 0 |
| 3. Performance Engineer | 6 | 1 | 4 | 1 |
| 4. Production Deployment | 5 | 2 | 2 | 1 |
| 5. Upstream Maintainer | 5 | 0 | 2 | 3 |
| 6. New Team Member | 4 | 1 | 2 | 1 |
| 7. OEM Integration | 5 | 1 | 4 | 0 |
| 8. ISO 26262 Compliance | 5 | 3 | 2 | 0 |
| 9. Test Automation | 6 | 0 | 4 | 2 |
| 10. System Architect | 6 | 1 | 3 | 2 |
| **Total** | **54** | **15** | **28** | **11** |

## Top-Priority Actions (High/Critical)

1. **Replace `todo!()` in production paths** -- 5 instances across `catch.rs`, `api/mod.rs`, `program_database.rs` will panic on execution
2. **Implement stop_timeout** -- `TODO(#151)` leaves no graceful shutdown enforcement
3. **Add `cargo-audit`/`cargo-deny`** -- zero supply-chain security tooling
4. **Document all `unsafe` blocks** -- 16 unsafe blocks with no SAFETY justification
5. **Verify `unsafe impl Send for HandlerType`** -- potentially unsound manual Send impl
6. **Replace `std::thread::sleep` in cycle timing** -- blocks async runtime
7. **Add code coverage to CI** -- 108 tests pass but coverage unknown
8. **Add requirements traceability** -- no SWE.1 mapping for any test
9. **Create safety concept** -- no ASIL classification for automotive deployment
10. **Fix Rc/RefCell usage in EventCreator** -- prevents thread-safe Deployment phase

---

*Analysis generated from source inspection of score-orchestrator at workspace version 0.0.3.*
*Rust toolchain: 1.85.0 stable.*
*Dependencies: kyron (caa9c0b), iceoryx2 (d3d1c9a), libc 0.2.*
