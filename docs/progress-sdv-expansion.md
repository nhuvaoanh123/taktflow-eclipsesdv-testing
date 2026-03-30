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

## Phase 4: Enable CI — TODO

- [ ] Un-disable simplest workflow (score-baselibs_rust — Cargo only)
- [ ] Add GitHub Actions matrix for all 12 modules
- [ ] Add weekly cron trigger for auto-sync + test
- [ ] Keep `workflow_dispatch` for manual runs

## Phase 5: Ongoing — TODO

- [ ] Weekly sync cadence established
- [ ] Per-release tag pinning process documented

---

## How to resume

Tell Claude: **"Continue SDV testing expansion — check progress doc at `docs/progress-sdv-expansion.md`"**
