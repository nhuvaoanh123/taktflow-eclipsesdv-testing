---
document_id: PLAN-INTEGRATION-001
title: "Testing Integration Plan — Modules 6-8 into Upstream Structure"
version: "1.0"
status: active
date: 2026-03-25
modules: [score-logging, score-orchestrator, eclipse-kuksa-databroker]
---

# Testing Integration Plan

How to integrate taktflow-eclipsesdv-testing test suites into the upstream
structure of each module. Current state: we have standalone pytest tests
under `modules/{module}/tests/`. Target state: tests live in the upstream
repo tree and execute via the same commands upstream CI uses.

---

## Background: What We Have vs. What Upstream Expects

### What We Have (current)

```
modules/score-logging/tests/build/test_build.py         # file-inspection
modules/score-logging/tests/regression/test_api_contract.py
modules/score-logging/tests/integration/test_dependency_chain.py
modules/score-logging/tests/security/test_safety_contracts.py
modules/score-orchestrator/tests/...  (same pattern)
modules/kuksa-databroker/tests/...    (same pattern)
```

These are **file-inspection** tests (check that files exist, contain correct
content). They run standalone: `python3 -m pytest modules/score-logging/tests/`.

### What Upstream Expects

Each module has its own test infrastructure, described below. Integration means
placing or hooking our test logic into that infrastructure.

---

## Module 6: score-logging

### Upstream Test Structure

| Layer | Location | Framework | Command |
|---|---|---|---|
| C++ unit tests | `score/datarouter/test/ut/` | GoogleTest (Bazel `cc_test`) | `bazel test //score/...` |
| Rust unit tests | `score/mw/log/rust/score_log_bridge:tests` | Rust `#[test]` | `bazel test //score/...` |
| Coverage | `.bazelrc` instrumentation_filter | gcov/lcov | `bazel coverage //score/...` |
| Format check | `:format.check` | yapf/rustfmt/buildifier | `bazel test //:format.check` |
| CI build | `.github/workflows/build.yml` | Bazel | PR trigger |
| CI coverage | `.github/workflows/coverage_report.yml` | shared cicd-workflows | PR + main |

**Tags used in BUILD files:** `"unit"`, `"FFI"`, `"manual"` (excluded by default)

**Test aggregation pattern:**
```python
# score/datarouter/test/ut/BUILD
test_suite(
    name = "unit_tests",
    tests = [
        "//score/datarouter/test/ut/ut_logging:...",
    ],
)
```

### What We Need to Add

Our tests check 3 things upstream CI does NOT cover:
1. **Dependency chain integrity** — that MODULE.bazel declares correct versions
2. **Object Seam contract** — that fake_recorder mirrors the real interface
3. **Rust unsafe justification** — `# SAFETY:` annotations on every unsafe block

These belong as **Starlark BUILD analysis tests** (Python wrapped in `py_test`)
not as standalone pytest.

### Integration Plan

#### Step 1 — Create taktflow test package in upstream tree

```
score/mw/log/taktflow_tests/
├── BUILD
├── test_api_contract.py
├── test_seam_contract.py
└── test_unsafe_annotations.py
```

**`score/mw/log/taktflow_tests/BUILD`:**
```python
load("@score_tooling//python_basics:defs.bzl", "score_py_pytest")

score_py_pytest(
    name = "taktflow_contract_tests",
    srcs = [
        "test_api_contract.py",
        "test_seam_contract.py",
        "test_unsafe_annotations.py",
    ],
    data = [
        "//score/mw/log:session_handle_interface",
        "//score/mw/log/test/fake_recorder:fake_recorder",
    ],
    tags = ["unit"],
)
```

**Run command:** `bazel test //score/mw/log/taktflow_tests:taktflow_contract_tests`

#### Step 2 — Port file-inspection tests into Bazel-aware Python

Key change: instead of `os.path.exists(PROJECT_ROOT / "score/mw/log/...")`,
use `bazel query '//score/mw/log/...'` output passed as data, or
`runfiles.rlocation()` for hermetic path resolution.

Example pattern from upstream `tests/cpp/BUILD`:
```python
py_test(
    name = "module_identity_test",
    srcs = ["module_identity_test.py"],
    data = ["//score/mw/log:MODULE.bazel"],  # make it a build dep
    deps = ["@rules_python//python/runfiles"],
)
```

#### Step 3 — Add `.gitattributes` to prevent CRLF issues

In our `taktflow-eclipsesdv-testing/score-logging/` (if we ever push upstream):
```
* text=auto
*.sh text eol=lf
*.py text eol=lf
BUILD text eol=lf
*.bzl text eol=lf
```

#### Step 4 — Add sanitizer config to `.bazelrc` (missing upstream gap)

```
# Add to score-logging/.bazelrc:
build:asan --config=x86_64-linux
build:asan --features=address_sanitizer
build:tsan --config=x86_64-linux
build:tsan --features=thread_sanitizer
```
Then: `bazel test --config=asan //score/...`

### Commands (post-integration)

```bash
# Run our contract tests via Bazel:
cd score-logging
bazel test //score/mw/log/taktflow_tests:taktflow_contract_tests

# Run everything (upstream + ours):
bazel test //score/...

# Coverage (includes our test sources excluded via filter):
bazel coverage //score/...
```

---

## Module 7: score-orchestrator

### Upstream Test Structure

| Layer | Location | Framework | Command |
|---|---|---|---|
| Unit tests | `src/orchestration` inline `#[test]` | Rust + Bazel `rust_test` | `bazel test //src/...` |
| CIT (Cargo) | `tests/test_cases/` Python + `tests/test_scenarios/rust/` binary | pytest + CitScenario | `pytest tests/test_cases/tests/` |
| CIT (Bazel) | `tests/test_cases:cit` | score_py_pytest | `bazel test //tests/test_cases:cit` |
| Coverage | `cargo +nightly tarpaulin` | LLVM | nightly CI |
| Miri | `cargo +nightly-2025-05-30 miri test` | Miri | nightly CI |
| LOOM | `cargo xtask build:loom` | loom crate | nightly CI |
| Flake detection | `cit_repeat` (5x) or `--count=20` | pytest-repeat | nightly CI |

**CI files:**
- `tests.yml` — Bazel unit tests
- `component_integration_tests.yml` — Cargo CIT (nightly 20x)
- `component_integration_tests_bazel.yml` — Bazel CIT (nightly `cit_repeat`)
- `cargo_required.yml` — tarpaulin + Miri + LOOM

### What We Need to Add

Our taktflow tests verify:
1. **kyron supply chain** — rev hash is pinned (security requirement)
2. **proc-macro safety** — no `std::fs` or `unsafe` in macros
3. **iceoryx2-ipc feature gate** — optional feature doesn't bleed into default binary size

These should become CIT scenarios because they test behavioral/structural
properties of the orchestration runtime — exactly what `CitScenario` is designed for.

### Integration Plan

#### Step 1 — Add taktflow scenarios to test_scenarios binary

Add a `taktflow/` module under `tests/test_scenarios/rust/src/scenarios/`:

```
tests/test_scenarios/rust/src/scenarios/taktflow/
├── mod.rs
├── supply_chain_verification.rs   # kyron pinned-hash check
├── proc_macro_safety.rs           # no unsafe in compiled macros
└── feature_gate_isolation.rs      # iceoryx2-ipc doesn't affect default build
```

**`tests/test_scenarios/rust/src/scenarios/taktflow/supply_chain_verification.rs`:**
```rust
use test_scenarios_rust::Scenario;

pub struct KyronSupplyChainScenario;

impl Scenario for KyronSupplyChainScenario {
    fn name(&self) -> &str { "taktflow.kyron_supply_chain" }

    fn run(&self, _config: serde_json::Value) -> anyhow::Result<()> {
        // Read Cargo.lock and verify kyron uses `rev =` not `version =`
        let lock = std::fs::read_to_string("Cargo.lock")?;
        assert!(lock.contains("source = \"git+https://github.com/eclipse-score/kyron.git"),
            "kyron must be pinned by git rev");
        assert!(!lock.contains("kyron = \""),
            "kyron must not be resolved from crates.io");
        Ok(())
    }
}
```

**Register in `tests/test_scenarios/rust/src/scenarios/mod.rs`:**
```rust
pub mod taktflow;
```
And add to `root_scenario_group()` in `main.rs`:
```rust
.add_group("taktflow", taktflow::scenarios())
```

#### Step 2 — Add taktflow CIT test cases (Python layer)

```
tests/test_cases/tests/taktflow/
├── __init__.py
└── test_taktflow_contracts.py
```

**`tests/test_cases/tests/taktflow/test_taktflow_contracts.py`:**
```python
import pytest
from tests.cit_scenario import CitScenario

class TestKyronSupplyChain(CitScenario):
    @pytest.fixture
    def scenario_name(self) -> str:
        return "taktflow.kyron_supply_chain"

    @pytest.fixture
    def test_config(self) -> dict:
        return {}

    def test_kyron_is_git_pinned(self, results):
        assert results.return_code == 0
```

**Run command:**
```bash
cd tests/test_cases
pytest tests/taktflow/ -v
```

#### Step 3 — Add taktflow Bazel CIT target

In `tests/test_cases/BUILD`, add:
```python
score_py_pytest(
    name = "cit_taktflow",
    srcs = glob(["tests/taktflow/*.py"]),
    deps = [":cit_deps"],
    data = ["//tests/test_scenarios/rust:test_scenarios"],
    args = ["--target-path=$(location //tests/test_scenarios/rust:test_scenarios)"],
    tags = ["unit"],
)
```

**Run command:** `bazel test //tests/test_cases:cit_taktflow`

#### Step 4 — Add Miri + Clippy to our regression script

Update `modules/score-orchestrator/regression.sh` to support `--miri` flag:
```bash
if [[ "${1:-}" == "--miri" ]]; then
    cargo +nightly-2025-05-30 miri test --workspace 2>&1 | tee /tmp/orch-miri.log
fi
```

### Commands (post-integration)

```bash
# Bazel unit tests (includes taktflow):
bazel test //src/...

# CIT via pytest:
cd tests/test_cases && pytest tests/taktflow/ -v

# CIT via Bazel:
bazel test //tests/test_cases:cit_taktflow

# Full upstream nightly (20x):
bazel test //tests/test_cases:cit_repeat
```

---

## Module 8: eclipse-kuksa-databroker

### Upstream Test Structure

| Layer | Location | Framework | Command |
|---|---|---|---|
| Cucumber integration | `databroker/tests/read_write_values.rs` | cucumber 0.20 | `cargo test` |
| Python integration | `integration_test/test_databroker.py` | pytest + grpcio | `./integration_test/run.sh` |
| Coverage | `cargo llvm-cov --all-features` | llvm-cov → Codecov | CI |
| Lint/Format | `cargo fmt --check && cargo clippy` | clippy | CI (blocking) |
| Multi-arch | Docker + QEMU | cross | nightly CI |
| Lib tests | `lib/` crate (with live Docker broker) | cargo test | `cargo test` in lib/ |

**Critical finding:** The Python integration tests (`test_databroker.py`) use the
**deprecated sdv.databroker.v1 collector API** (`RegisterDatapoints`). The current
broker (v0.6.1-dev) returns `UNIMPLEMENTED`. Upstream `provider.py` already
uses the v2 API — the test file is the stale part.

### What We Need to Add / Fix

1. **Rewrite `integration_test/test_databroker.py`** for KUKSA.val v2 API — highest priority
2. **Add taktflow security tests** as Cucumber scenarios in `databroker/tests/`
3. **Add JWT live test** — verify token authorization round-trip against running broker

### Integration Plan

#### Step 1 — Rewrite integration_test/test_databroker.py for v2 API

The v2 API is already in `gen_proto/kuksa/val/v2/` (generated from `kuksa.val.v2.proto`).
`provider.py` in the same directory already uses it correctly.

**New `test_databroker.py` structure:**
```python
from gen_proto.kuksa.val.v2.val_pb2_grpc import VALStub
from gen_proto.kuksa.val.v2.val_pb2 import (
    GetValueRequest, SetValueRequest, SubscribeRequest, SignalID
)

DATABROKER_ADDRESS = os.environ.get("DATABROKER_ADDRESS", "127.0.0.1:55555")

@pytest.mark.asyncio
async def test_databroker_connection():
    async with grpc.aio.insecure_channel(DATABROKER_ADDRESS) as channel:
        stub = VALStub(channel)
        # v2: GetServerInfo is in VAL service
        response = await stub.GetServerInfo(GetServerInfoRequest())
        assert response.name == "databroker"

@pytest.mark.asyncio
async def test_vehicle_speed_get_set():
    """Verify Vehicle.Speed can be read and set via KUKSA.val v2."""
    async with grpc.aio.insecure_channel(DATABROKER_ADDRESS) as channel:
        stub = VALStub(channel)
        # Set via v2 API
        signal_id = SignalID(path="Vehicle.Speed")
        value = Value(float=42.5)
        await stub.PublishValue(PublishValueRequest(
            signal_id=signal_id,
            data_point=Datapoint(value=value)
        ))
        # Get via v2 API
        response = await stub.GetValue(GetValueRequest(signal_id=signal_id))
        assert response.data_point.value.float == pytest.approx(42.5)

@pytest.mark.asyncio
async def test_subscribe_vehicle_speed():
    """Verify subscription stream receives updates."""
    # ... subscribe, publish, read first streamed response
```

**Checklist before rewriting:**
- [ ] Read `gen_proto/kuksa/val/v2/val_pb2.py` to get exact message names
- [ ] Read `provider.py` — already uses v2, copy the pattern
- [ ] Check what `GetServerInfoRequest` returns in v2 (name/version fields)
- [ ] Verify `PublishValue` vs `SetValue` — the v2 API has changed endpoint names

#### Step 2 — Add taktflow Cucumber scenarios

Add a new Cucumber feature file for taktflow-specific security checks:

**`databroker/tests/features/taktflow_security.feature`:**
```gherkin
Feature: taktflow Security Contracts

  Scenario: Broker rejects missing JWT on actuator path
    Given a running databroker with JWT auth enabled
    When a client without a token calls Actuate on Vehicle.Body.Lights.IsHighBeamOn
    Then the response status code should be PERMISSION_DENIED

  Scenario: Broker rejects wildcard subscription without explicit scope
    Given a running databroker with JWT auth enabled
    When a client with read-only token subscribes to Vehicle.*
    Then the subscription should be accepted but filter to permitted paths

  Scenario: Broker returns valid VSS 4.0 metadata for Vehicle.Speed
    Given a running databroker with VSS 4.0 loaded
    When a client calls GetServerInfo
    Then the response includes VSS version 4.0
```

**`databroker/tests/taktflow_security.rs`:**
```rust
use cucumber::World;

#[tokio::main]
async fn main() {
    TaktflowWorld::run("tests/features/taktflow_security.feature").await;
}

#[derive(cucumber::World, Debug, Default)]
struct TaktflowWorld {
    // reuse DataBrokerWorld fields
}
```

**`databroker/Cargo.toml` addition:**
```toml
[[test]]
name = "taktflow_security"
harness = false
```

#### Step 3 — Run live broker for integration tests (without Docker)

The `run.sh` script uses Docker to start the broker. On our bench (no Docker on
Ubuntu laptop) we run it directly:

```bash
# Start broker:
./target/debug/databroker \
  --metadata data/vss-core/vss_release_4.0.json \
  --port 55555 \
  --insecure &
BROKER_PID=$!

# Run v2 integration tests:
cd integration_test
source /tmp/kuksa-venv/bin/activate
python3 -m pytest test_databroker.py -v

kill $BROKER_PID
```

Add this as `--integration` flag to our `modules/kuksa-databroker/regression.sh`.

#### Step 4 — Add llvm-cov to regression.sh

```bash
if [[ "${1:-}" == "--coverage" ]]; then
    source ~/.cargo/env
    cargo +nightly install cargo-llvm-cov 2>/dev/null || true
    cd "$BROKER_DIR"
    cargo llvm-cov --all-features --workspace \
        --lcov --output-path /tmp/kuksa-lcov.info
    echo "Coverage report: /tmp/kuksa-lcov.info"
fi
```

### Commands (post-integration)

```bash
# Unit + Cucumber tests:
cargo test --workspace

# New taktflow security Cucumber tests:
cargo test --test taktflow_security

# Coverage:
cargo llvm-cov --all-features --workspace --lcov --output-path lcov.info

# v2 Integration tests (after broker is running):
cd integration_test && python3 -m pytest test_databroker.py -v

# Full pipeline (our regression script):
bash modules/kuksa-databroker/regression.sh --build --integration
```

---

## Cross-Module Actions

### 1. Fix `.gitattributes` in parent repo (prevents CRLF regression)

```
# taktflow-eclipsesdv-testing/.gitattributes
* text=auto
*.sh text eol=lf
*.py text eol=lf
BUILD text eol=lf
*.bzl text eol=lf
*.rs text eol=lf
*.toml text eol=lf
```

### 2. Update our regression.sh scripts to match upstream CI

| Module | CI command (upstream) | Our regression.sh should use |
|---|---|---|
| score-logging | `bazel test --config=x86_64-linux //score/...` | Already does this |
| score-orchestrator | `bazel test --config=x86_64-linux //src/...` | Add Bazel path alongside Cargo |
| kuksa-databroker | `cargo llvm-cov --all-features --workspace` | Add `--coverage` flag |

### 3. Prioritization

| Task | Module | Effort | Priority |
|---|---|---|---|
| Rewrite integration test for KUKSA.val v2 | kuksa-databroker | 2h | **HIGH** |
| Add taktflow Rust scenarios to CIT binary | score-orchestrator | 3h | **MEDIUM** |
| Add taktflow BUILD targets to upstream tree | score-logging | 1h | **MEDIUM** |
| Add sanitizer config to score-logging .bazelrc | score-logging | 30min | **MEDIUM** |
| Add Cucumber taktflow_security.feature | kuksa-databroker | 2h | **MEDIUM** |
| Add .gitattributes to prevent CRLF | all | 15min | **LOW** |
| llvm-cov integration in regression.sh | kuksa-databroker | 30min | **LOW** |

---

**Plan created:** 2026-03-25
**Status:** Ready for implementation — start with kuksa-databroker v2 API rewrite.
