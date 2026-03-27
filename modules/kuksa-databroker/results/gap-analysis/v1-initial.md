---
document_id: GAP-KUKSA-001
title: "Gap Analysis -- eclipse-kuksa-databroker Initial Assessment"
version: "1.0"
status: active
date: 2026-03-25
severity_scale: "Critical > High > Medium > Low"
---

# KUKSA.val Databroker Gap Analysis

Honest assessment of what was verified, what was claimed but not verified,
and what was never attempted.

---

## 1. Verified (Genuine PASS)

| Claim | Evidence | Confidence |
|---|---|---|
| Rust workspace with 3 members | Cargo.toml [workspace] with databroker, databroker-proto, databroker-cli | High |
| Cargo.lock present | File exists at root | High |
| KUKSA.val v1 + v2 proto files exist | proto/kuksa/val/v1/val.proto + v2/val.proto | High |
| VSS 4.0 JSON data present | data/vss-core/vss_release_4.0.json | High |
| JWT authorization module | src/authorization/ directory present | High |
| TLS certificate directory | certificates/ directory present | High |
| OpenTelemetry observability | src/open_telemetry.rs present | High |
| VISS API module | src/viss/ directory present | High |
| Filter + query modules | src/filter/ + src/query/ present | High |
| gRPC via tonic | tonic in root Cargo.toml workspace deps | High |
| Python integration tests | integration_test/test_databroker.py present | High |
| Cross-compile config | Cross.toml present for aarch64 | High |
| wildcard_matching.md | Documentation present | High |
| lib/common shared library | lib/common/Cargo.toml present | High |
| build.rs for proto codegen | databroker/build.rs + databroker-proto/build.rs | High |

---

## 2. Not Yet Verified (Requires Build Execution)

### GAP-001: Build — CLOSED

**Claim:** "Cargo build succeeds"

**Result (2026-03-25):** `cargo build --workspace` — PASS. 57s, 4 workspace
crates (databroker, databroker-proto, databroker-cli, lib/common).
Required: `sudo apt install protobuf-compiler clang libclang-dev`.

**Status:** VERIFIED.

---

### GAP-002: Unit Tests — CLOSED

**Claim:** "Unit tests pass"

**Result (2026-03-25):** `cargo test --workspace` — 208/209 PASS, 1 ignored.
179 databroker + 6 databroker-proto + 23 lib/sdv tests.

**Status:** VERIFIED.

---

### GAP-003: Integration Tests — PARTIAL (Upstream API Gap)

**Claim:** "Integration tests verify signal flow"

**Result (2026-03-25):** Live broker started on 127.0.0.1:55555. PASS.
Python integration tests: 0/3 PASS.

**Root cause:** `integration_test/test_databroker.py` uses `sdv.databroker.v1`
collector API (`CollectorStub.RegisterDatapoints`). This returns
`StatusCode.UNIMPLEMENTED` in databroker v0.6.1-dev which has migrated to
KUKSA.val v2 API. The integration test has NOT been updated upstream.

**What's needed:** Rewrite `test_databroker.py` using KUKSA.val v2 gRPC API
(`kuksa.val.v2.VAL`), or wait for upstream to provide updated integration tests.

**Status:** UPSTREAM GAP — broker runs, v1 integration test is obsolete.

---

### GAP-004: aarch64 Cross-Compile Not Verified (Medium)

**Claim:** "Deployable to Raspberry Pi 4"

**Reality:** Cross.toml exists but `cross build --target aarch64-unknown-linux-gnu`
not executed. Pi is the taktflow bench target.

**Status:** NOT VERIFIED.

---

### GAP-005: Authorization Not Live-Tested (High)

**Claim:** "JWT authorization works"

**Reality:** authorization/ module present. Unit tests include JWT test scenarios
(verified via `cargo test`). But no live test has verified:
- Valid token → access granted
- Invalid token → access denied

**Status:** UNIT TESTED. Live round-trip not verified.

---

### GAP-006: Sanitizers Not Run (Medium)

**Claim:** "Memory safe"

**Reality:** Rust provides memory safety by default (no unsafe blocks in hot path).
No Miri or cargo-sanitize run. Deserialization of malformed protobuf via prost
could cause panics in error paths.

**Status:** DEFERRED — Rust safety guarantees cover most of ASan/UBSan scope.

---

## 3. Architecture Properties

| Property | Status |
|---|---|
| KUKSA.val v2 API (current) | VERIFIED (proto file present) |
| KUKSA.val v1 API (legacy) | VERIFIED (proto file present) |
| JWT authorization | STRUCTURAL |
| TLS support | STRUCTURAL |
| OpenTelemetry traces | STRUCTURAL |
| VISS2 browser API | STRUCTURAL |
| VSS 4.0 signal data | VERIFIED |
| Python integration test | STRUCTURAL (not run) |

---

**Next step:** Build and run unit tests on Ubuntu laptop. Then start broker
and run integration_test/test_databroker.py. Record test count + results.
Update this document with actual measurements.

**Integration target:** Connect taktflow SIL → CAN provider → kuksa-databroker.
This is the full SDV data path: ECU → CAN → VSS → broker → vehicle app.
