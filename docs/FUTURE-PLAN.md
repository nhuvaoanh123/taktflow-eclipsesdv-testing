---
document_id: PLAN-001
title: "Eclipse SDV Testing - Future Plan"
date: 2026-04-16
status: active
---

# Future Plan

This file is the current forward-looking plan for the `taktflow-eclipsesdv-testing`
workspace.

The older March 2026 version of this file mixed historical status, completed
items, and future tasks in a way that had gone stale. The current source of
truth is:

- `README.md` for workspace orientation
- `docs/BENCH-RESULTS-SUMMARY.md` for the core 8-module bench snapshot
- `docs/progress-sdv-expansion.md` for the broader cross-ecosystem expansion log

## Current Position

We now have two evidence layers in the workspace:

1. Core bench snapshot

   The 8-module core set has the deepest documented evidence:

   - `score-communication`
   - `score-baselibs`
   - `score-lifecycle`
   - `score-persistency`
   - `score-feo`
   - `score-logging`
   - `score-orchestrator`
   - `eclipse-kuksa-databroker`

2. Broader expansion layer

   The wider workspace has grown beyond the original core set into additional
   S-CORE, Ankaios, uProtocol, and staged Kuksa coverage. See
   `docs/progress-sdv-expansion.md` for that roll-up.

## Completed Since The Original Plan

These items are no longer future work:

- `score-logging` moved beyond structural review into build/test evidence.
- `score-orchestrator` moved beyond structural review into `cargo build` and
  `cargo test` evidence.
- `eclipse-kuksa-databroker` moved beyond structural review into build, unit,
  integration, and BDD evidence.
- `ankaios` is recorded as complete in the expansion log.
- The root README has been refreshed so it no longer overstates or understates
  module status.

## Remaining Technical Work

The remaining technical work is still real, but it should be framed against the
current evidence base instead of the older structural snapshot.

### High priority

- Backfill commit-accurate tested states into `config/tested-commits.yaml` for
  expansion-era modules.
- Finish the detailed Kuksa per-repo notes so the phase log matches the
  ecosystem roll-up.
- Decide whether Velocitas becomes the next deep-evidence target or remains a
  staged ecosystem.
- Decide whether `kuksa-can-provider` is the next bench-critical module to move
  from staged to deeply verified.

### Medium priority

- aarch64 deployment and Pi-native confirmation runs where still missing
- Rust coverage improvements where the current summaries still say coverage is
  limited or unavailable
- Miri / Clippy follow-up on Rust-heavy modules where useful
- continued upstream drift checks across the checked-out SDV repos

### Lower priority

- CI automation for the validation laptop
- cleaner generated dashboards and reading-list regeneration
- additional cross-ecosystem integration scenarios beyond the current core set

## Working Assumptions

- The active local pytest entry point is `modules/`, not the older `tests/`
  root.
- The current active status should be read from the Markdown docs, not from
  generated HTML snapshots.
- QNX remains relevant as historical context and upstream comparison, but the
  current local bench story is not centered on the older QNX-only Pi plan.

## Next Suggested Focus

1. Make the status ledger honest everywhere:
   - finish commit-register backfill
   - finish Kuksa phase-note backfill
   - keep generated artifacts clearly labeled when they lag

2. Pick one next deep-evidence target:
   - `kuksa-can-provider`, or
   - one Velocitas SDK path

3. Keep the distinction sharp between:
   - deeply bench-verified modules
   - broader ecosystem modules with lighter validation

## Revision Note

This file was rewritten on 2026-04-16 to replace a stale mixed historical plan
with a current forward-looking summary.
