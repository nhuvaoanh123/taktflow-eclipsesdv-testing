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

### GAP-001: Build Not Executed (High)

**Claim:** "Cargo build succeeds"

**Reality:** `cargo build --workspace` not run. Proto compilation requires
`protoc` which may not be in PATH. tonic-build requires gRPC toolchain.

**Status:** NOT VERIFIED.

---

### GAP-002: Unit Tests Not Run (High)

**Claim:** "Unit tests pass"

**Reality:** Test files exist in databroker/tests/ but no test run has occurred.

**Status:** NOT VERIFIED.

---

### GAP-003: Integration Tests Not Run (High)

**Claim:** "Integration tests verify signal flow"

**Reality:** integration_test/test_databroker.py exists and tests gRPC
Get/Set/Subscribe — but requires a live broker on port 55555. Never executed.

**What's needed:**
1. `cargo run -- --metadata data/vss-core/vss_release_4.0.json`
2. `python3 integration_test/test_databroker.py`

**Status:** NOT VERIFIED. High priority — this is the core functional test.

---

### GAP-004: aarch64 Cross-Compile Not Verified (Medium)

**Claim:** "Deployable to Raspberry Pi 4"

**Reality:** Cross.toml exists but `cross build --target aarch64-unknown-linux-gnu`
not executed. Pi is the taktflow bench target.

**Status:** NOT VERIFIED.

---

### GAP-005: Authorization Not Live-Tested (High)

**Claim:** "JWT authorization works"

**Reality:** authorization/ module present. But no test has verified:
- Valid token → access granted
- Invalid token → access denied
- Missing permission → specific signal denied

**Status:** STRUCTURAL. Live test needed.

---

### GAP-006: Sanitizers Not Run (Medium)

**Claim:** "Memory safe"

**Reality:** Broker processes untrusted network input (gRPC messages). No
ASan/UBSan run. Deserialization of malformed protobuf could panic.

**Status:** NOT RUN.

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
