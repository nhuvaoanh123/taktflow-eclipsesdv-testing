---
document_id: GAP-ORCH-001
title: "Gap Analysis -- score-orchestrator Initial Assessment"
version: "1.0"
status: active
date: 2026-03-25
severity_scale: "Critical > High > Medium > Low"
---

# score-orchestrator Gap Analysis

Honest assessment of what was verified, what was claimed but not verified,
and what was never attempted.

---

## 1. Verified (Genuine PASS)

| Claim | Evidence | Confidence |
|---|---|---|
| MODULE.bazel declares score_orchestrator v0.0.0 | File exists, name parsed | High |
| Rust workspace version 0.0.3 | Cargo.toml [workspace.package] version | High |
| 5 workspace members present | src/orchestration, orchestration_macros, xtask, test_scenarios + example | High |
| kyron dependency hash-pinned | rev = "caa9c0b..." in root Cargo.toml | High |
| iceoryx2-ipc is a feature flag | [features] iceoryx2-ipc in orchestration/Cargo.toml | High |
| Cargo.lock present | File exists at root | High |
| Rust toolchain 1.85.0 | rust-toolchain.toml channel = "1.85.0" | High |
| proc-macro crate declared | proc-macro = true in orchestration_macros/Cargo.toml | High |
| syn + quote dependencies | Both present in orchestration_macros/Cargo.toml | High |
| Test scenarios present | tests/test_scenarios/rust/ directory exists | High |
| Core source files exist | lib.rs, program.rs, program_database.rs, prelude.rs | High |
| Architecture components | actions/, api/, common/, core/, events/, testing/ subdirs | High |
| Bazel 8.3.0 | .bazelversion = "8.3.0" | High |

---

## 2. Not Yet Verified (Requires Build Execution)

### GAP-001: Build Not Executed (High)

**Claim:** "Cargo build and Bazel build succeed"

**Reality:** Neither `cargo build` nor `bazel build --config=x86_64-linux //...`
has been run. kyron sourced from GitHub — network access required for first build.

**What's needed:** SSH to Ubuntu laptop, run both build systems, record output.

**Status:** NOT VERIFIED.

---

### GAP-002: Unit Test Count Unknown (High)

**Claim:** "Unit tests pass"

**Reality:** Test count not measured. Upstream nightly runs 20× for flake detection —
our bench ran 0×.

**Status:** NOT VERIFIED.

---

### GAP-003: Clippy / Static Analysis Not Run (Medium)

**Claim:** "Clippy clean with score_rust_policies"

**Reality:** `cargo clippy -- -D warnings` not executed.

**Status:** NOT VERIFIED.

---

### GAP-004: Component Integration Tests Not Run (Medium)

**Claim:** "CIT scenarios pass"

**Reality:** test_scenarios/rust/ exists but CIT has never been executed.
CIT tests the full program lifecycle end-to-end.

**Status:** NOT VERIFIED.

---

## 3. Security Gaps

### GAP-005: kyron Supply Chain (Medium)

kyron is pinned by rev hash — this is good practice. But the hash is
not verified against a signed release. An attacker with write access to
the kyron GitHub repo could push a new commit to the same branch that
bypasses the pinned hash if the hash is not validated at build time.

**Mitigation:** Build via Cargo uses the pinned hash from Cargo.lock. Risk is LOW.

---

### GAP-006: No Sanitizer Results (Medium)

TSan/ASan not run for orchestration crate. Concurrent program lifecycle
transitions could have data races.

**Status:** NOT VERIFIED.

---

## 4. Architecture Properties

| Property | Status |
|---|---|
| Dual Bazel + Cargo build | STRUCTURAL (file verified) |
| kyron IPC dependency | STRUCTURAL (hash pinned, not built) |
| iceoryx2 feature-gated | VERIFIED (feature flag present) |
| proc-macro safe (no unsafe, no fs) | VERIFIED (source inspected) |
| Nightly flake detection (20×) | NOT RUN |

---

**Next step:** Execute `cargo build && cargo test` on Ubuntu laptop.
Update this document with test count and pass/fail results.
