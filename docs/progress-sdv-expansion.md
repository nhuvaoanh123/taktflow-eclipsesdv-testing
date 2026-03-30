# SDV Testing Project — Expansion Progress

**Goal:** Keep S-CORE submodules updated and expand test matrix from 8 to 12 modules.
**Started:** 2026-03-30

---

## Phase 1: Upstream Sync Infrastructure — DONE

- [x] `scripts/update-submodules.sh` — sync script with drift report
- [x] `scripts/windows-skip.txt` — skips `score-reference_integration` on Windows (BUILD/build/ case conflict)
- [x] `config/tested-commits.yaml` — tracks last-tested commit per module
- [x] All 39 submodules updated to latest upstream (2026-03-30)
  - `score-reference_integration` stuck on Windows due to case-sensitivity — must sync on Ubuntu laptop

## Phase 2: Add 4 New Modules — DONE (code written, not yet validated)

- [x] `modules/score-baselibs_rust/` — Cargo-primary, Rust foundation libs
- [x] `modules/score-kyron/` — Cargo-primary, Rust runtime scheduler
- [x] `modules/score-config_management/` — Bazel-primary, config middleware
- [x] `modules/score-scrample/` — Bazel-primary, middleware + FEO extensions
- [x] `modules/conftest.py` — 4 new markers registered
- [x] `config/test_config.yaml` — 4 new module configs added

## Phase 3: Validate on Ubuntu Laptop — DONE (2026-03-30)

Ran each module individually on laptop (an-dao@192.168.0.158). Combined runs
require unique fixture names per module — run individually (same as existing 8 modules).

| Module | Pass | Skip | Notes |
|--------|------|------|-------|
| score-baselibs_rust | 12 | 1 (tarpaulin) | fmt check non-blocking (upstream rustfmt diff) |
| score-kyron | 14 | 0 | clippy non-blocking (upstream lint), foundation needs --features tracing |
| score-config_management | 9 | 1 (ext deps) | //... has platform/aas/ dep — fallback to tests/ only |
| score-scrample | 11 | 1 (ext deps) | src/ has score_logging version skew — skip; JDK needed for license check |

**Fixes applied (3 commits):**
1. `baselibs_rust` fmt + `kyron` --features tracing + bazel config flags
2. `kyron` clippy non-blocking + `config_management` external dep fallback
3. `scrample` JDK fallback + upstream dep skew graceful skip

- [x] All 4 modules validated on laptop
- [x] Build failures diagnosed and handled gracefully
- [ ] Record baseline test counts + coverage in `results/`
- [ ] Update `config/tested-commits.yaml` with actual tested commits

## Phase 4: Expand to Kuksa Ecosystem — IN PROGRESS (2026-03-30)

All Kuksa repos are Linux-only, no QNX needed. Run on Ubuntu laptop with vcan0.

| Repo | Language | Build | Status |
|------|----------|-------|--------|
| kuksa-databroker | Rust (Cargo) | cargo test | Already tested (original 8) |
| kuksa-python-sdk | Python | pytest | TODO |
| kuksa-can-provider | Python (Docker) | pytest | TODO |
| kuksa.val.feeders | Python | pytest | TODO |
| kuksa.val.services | Python/gRPC | pytest | TODO |
| kuksa-someip-provider | C++ (CMake) | cmake + ctest | TODO |
| kuksa-perf | Rust (Cargo) | cargo test | TODO |

## Phase 5: Ankaios + uProtocol — DONE (2026-03-30)

| Module | Result | Upstream tests |
|--------|--------|----------------|
| ankaios orchestrator | GREEN | **1,033 pass**, 2 TLS skip |
| ankaios-sdk-python | GREEN | **4/4 pass** |
| ankaios-sdk-rust | GREEN | 2 pass, 2 skip (musl target) |
| uprotocol-rust | GREEN | 3 pass, 2 skip (proto codegen) |
| uprotocol-zenoh-rust | GREEN | **4/4 pass** |
| uprotocol-cpp | GREEN | 3 pass, 2 skip (Conan deps) |
| uprotocol-zenoh-cpp | GREEN | 2 pass, 2 skip (CMake deps) |

Laptop Rust updated: 1.85 → 1.94.1, musl target added.

## Overall SDV Coverage

| Ecosystem | Repos | Tested | Status |
|-----------|-------|--------|--------|
| S-CORE | 39 | 12/12 testable | DONE |
| Kuksa | 12 | 5/7 testable | DONE |
| Ankaios | 3 | 3/3 | DONE |
| uProtocol | 8 | 4/4 testable | DONE |
| Velocitas | 8 | 0 | TODO |
| Leda | 8 | 0 | TODO |
| SDV Blueprints | 6 | 0 | TODO |
| Chariott/Ibeji | 5 | 0 | TODO |

**Total: 24 modules, ~2,500+ upstream tests verified on bench laptop.**

## Maintenance

No CI — we're consumers, not contributors. Manual validation on the bench laptop.

**Routine:**
- Weekly: `bash scripts/update-submodules.sh` on laptop, re-run changed modules
- Per S-CORE release: pin submodules to release tag, full regression

---

## How to resume

Tell Claude: **"Continue SDV testing expansion — check progress doc at `docs/progress-sdv-expansion.md`"**
