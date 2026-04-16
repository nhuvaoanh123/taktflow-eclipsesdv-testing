# Eclipse SDV Testing - Taktflow Systems

Independent verification workspace for selected Eclipse SDV and Eclipse S-CORE
projects on the Taktflow bench.

## At a Glance

| Item | Current state |
|------|---------------|
| Purpose | Consumer-side validation, comparison, and evidence collection for upstream Eclipse SDV projects |
| Deep evidence set | 8 core modules with detailed build/test/coverage evidence |
| Broader validated set | 24 repos validated across S-CORE, Kuksa, Ankaios, and uProtocol |
| Main local harness | `pytest` rooted at `modules/` |
| Bench intent | Ubuntu bench laptop plus Taktflow bench/HIL integration |
| Important caveat | The workspace contains many more checked-out repos than the currently validated subset |

## What This Repo Is

This repo is not a single product source tree. It is a testing and evidence
workspace that combines:

- upstream project checkouts and submodules,
- Taktflow-owned test harnesses under `modules/`,
- bench configuration and dependency manifests,
- ASPICE-style evidence and analysis artifacts,
- generated "exorcism" analysis exports for offline review.

The workspace contains upstream or mirrored projects from multiple
Eclipse SDV ecosystems, including:

- Eclipse S-CORE
- Eclipse Kuksa
- Eclipse Velocitas
- Eclipse Leda
- Eclipse Ankaios
- Eclipse uProtocol
- Eclipse Chariott
- Eclipse Ibeji
- Eclipse SDV Blueprints

Not every checked-out upstream project is fully bench-validated yet. The
purpose of this workspace is to stage, test, compare, and document that work.

## Module Status

This is the single front-page status section for the repo. It combines:

- the 8-module deep-evidence bench set,
- the additional repos validated in the broader expansion sweep,
- the current backlog where validation is still incomplete.

### Status Summary

| Item | Current state | Source of truth |
|------|---------------|-----------------|
| Deep-evidence bench set | 8 core modules | [docs/BENCH-RESULTS-SUMMARY.md](docs/BENCH-RESULTS-SUMMARY.md) |
| Broader validated set | 24 repos across S-CORE, Kuksa, Ankaios, and uProtocol | [docs/progress-sdv-expansion.md](docs/progress-sdv-expansion.md) |
| Main local harness | `pytest` rooted at `modules/` | [modules/conftest.py](modules/conftest.py) |
| Important caveat | The workspace contains many more checked-out repos than the currently validated subset | Top-level repo inventory |

### Front-Page Status Board

This table is the single front-page status board for the repo.

| Group | Module / repo | ASIL / class | Build | Tests | Coverage | Sanitizers | Status |
|-------|----------------|--------------|-------|-------|----------|------------|--------|
| Core bench | `score-communication` | B | PASS | `252/252` PASS | `93.7%` | ASan/UBSan/LSan/TSan clean | Bench-verified |
| Core bench | `score-baselibs` | QM-B | PASS | `278/279` PASS | `97.9%` | ASan/UBSan/LSan clean | Bench-verified |
| Core bench | `score-lifecycle` | QM | PASS | `6/6` PASS | `82.1%` | ASan clean | Bench-verified |
| Core bench | `score-persistency` | D | PASS | C++ and Rust unit + CIT PASS | `95.3%` C++ | Not summarized in v4 snapshot | Bench-verified |
| Core bench | `score-feo` | QM | PASS | `8/8` PASS + `4/4` format | Rust side not summarized | Not summarized in v4 snapshot | Bench-verified |
| Core bench | `score-logging` | QM | PASS | `36/37` PASS | `87.8%` C++ | Configured, not run in v4 snapshot | Bench-verified |
| Core bench | `score-orchestrator` | QM | Cargo PASS; Bazel blocked | `108/108` PASS | Rust / no lcov | Rust / N/A | Bench-verified on cargo path |
| Core bench | `eclipse-kuksa-databroker` | QM | PASS | `208/209` unit + `5/5` v2 + `3/3` BDD | Rust / no lcov | Rust / N/A | Bench-verified |
| Expansion | `score-baselibs_rust` | B | PASS | `12` pass / `1` skip | N/A | Not summarized | Expansion-validated |
| Expansion | `score-kyron` | B | PASS | `14` pass / `0` skip | N/A | Not summarized | Expansion-validated |
| Expansion | `score-config_management` | B | PASS | `9` pass / `1` skip | N/A | Not summarized | Expansion-validated |
| Expansion | `score-scrample` | B | PASS | `11` pass / `1` skip | N/A | Not summarized | Expansion-validated |
| Expansion | `ankaios-ankaios` | N/A | GREEN | `1,033` pass / `2` TLS skip | N/A | Not summarized | Expansion-validated |
| Expansion | `ankaios-ank-sdk-python` | N/A | GREEN | `4/4` PASS | N/A | Not summarized | Expansion-validated |
| Expansion | `ankaios-ank-sdk-rust` | N/A | GREEN | `2` pass / `2` skip | N/A | Not summarized | Expansion-validated |
| Expansion | `uprotocol-up-rust` | N/A | GREEN | `3` pass / `2` skip | N/A | Not summarized | Expansion-validated |
| Expansion | `uprotocol-up-transport-zenoh-rust` | N/A | GREEN | `4/4` PASS | N/A | Not summarized | Expansion-validated |
| Expansion | `uprotocol-up-cpp` | N/A | GREEN | `3` pass / `2` skip | N/A | Not summarized | Expansion-validated |
| Expansion | `uprotocol-up-transport-zenoh-cpp` | N/A | GREEN | `2` pass / `2` skip | N/A | Not summarized | Expansion-validated |
| Roll-up | S-CORE ecosystem | Mixed | Mixed | `12/12` testable repos validated | Mixed | Mixed | DONE |
| Roll-up | Kuksa ecosystem | Mixed | Mixed | `5/7` testable repos validated | Mixed | Mixed | PARTIAL |
| Roll-up | Ankaios ecosystem | N/A | GREEN | `3/3` repos validated | N/A | N/A | DONE |
| Roll-up | uProtocol ecosystem | N/A | GREEN | `4/4` testable repos validated | N/A | N/A | DONE |
| Backlog | `eclipse-kuksa-python-sdk` | N/A | TODO | TODO | N/A | N/A | Planned |
| Backlog | `kuksa-kuksa-can-provider` | N/A | TODO | TODO | N/A | N/A | Bench-critical backlog |
| Backlog | `kuksa-kuksa.val.feeders` | N/A | TODO | TODO | N/A | N/A | Planned |
| Backlog | `kuksa-kuksa.val.services` | N/A | TODO | TODO | N/A | N/A | Planned |
| Backlog | `kuksa-kuksa-someip-provider` | N/A | TODO | TODO | N/A | N/A | Planned |
| Backlog | `kuksa-kuksa-perf` | N/A | TODO | TODO | N/A | N/A | Planned |
| Backlog | Velocitas ecosystem | N/A | TODO | `0/8` repos validated | N/A | N/A | Not started |
| Backlog | Leda ecosystem | N/A | TODO | `0/8` repos validated | N/A | N/A | Not started |
| Backlog | SDV Blueprints ecosystem | N/A | TODO | `0/6` repos validated | N/A | N/A | Not started |
| Backlog | Chariott/Ibeji ecosystem | N/A | TODO | `0/5` repos validated | N/A | N/A | Not started |

Overall:

- `8` core modules are bench-verified with the deepest evidence.
- `24` repos are validated in the broader expansion sweep.
- `S-CORE`, `Ankaios`, and `uProtocol` are the most complete validated areas today.
- `Kuksa` is partially validated, but its detailed per-repo backfill lags the roll-up totals in `docs/progress-sdv-expansion.md`.

## How To Read This Repo

If you are visiting this repo for the first time:

1. Start with `Module Status` above for the current front-page picture.
2. Read [docs/BENCH-RESULTS-SUMMARY.md](docs/BENCH-RESULTS-SUMMARY.md) for the strongest evidence set.
3. Read [docs/progress-sdv-expansion.md](docs/progress-sdv-expansion.md) for the broader repo sweep and remaining backfill work.
4. Treat top-level directories as workspace inventory, not as proof that every repo is already validated.
5. Treat [docs/BENCH-RESULTS-SUMMARY.md](docs/BENCH-RESULTS-SUMMARY.md) and [docs/progress-sdv-expansion.md](docs/progress-sdv-expansion.md) as the live status sources.

## Repository Layout

The top level intentionally mixes several kinds of content:

- `modules/`
  Taktflow-owned test harnesses and wrappers around selected upstream modules.
  This is the main pytest entry point today.

- top-level upstream project directories
  Examples: `eclipse-kuksa-databroker/`, `score-orchestrator/`,
  `uprotocol-up-rust/`, `velocitas-*`, `leda-*`, `ankaios-*`.
  These are the actual upstream codebases we build and inspect.

- `exorcism-*`
  Generated static analysis and review exports for individual upstream projects.
  These are not the primary source trees; they are derived artifacts used for
  offline comparison and dashboarding.

- `aspice/`
  Process, traceability, and quality artifacts organized in an ASPICE-style
  structure.

- `docs/`
  Project-level plans, testing strategy, bench results, requirements, security
  analysis, and deployment notes.

- `config/`
  Shared test configuration, target settings, and tested-commit tracking.

- `results/`
  Test reports and machine-readable outputs.

- `scripts/`
  Workspace maintenance and reporting helpers such as submodule update scripts
  and dashboard generation.

## Canonical Docs

Start here before assuming the repo status from directory names alone:

- [docs/BENCH-RESULTS-SUMMARY.md](docs/BENCH-RESULTS-SUMMARY.md)
  Latest bench-oriented results summary.

- [docs/TESTING-STRATEGY.md](docs/TESTING-STRATEGY.md)
  Test philosophy, levels, and lessons learned.

- [docs/TESTING-STRATEGY-upstream-comparison.md](docs/TESTING-STRATEGY-upstream-comparison.md)
  Comparison between our practice and upstream testing maturity.

- [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md)
  Dependency and tool requirements across the ecosystems in this workspace.

- [docs/DEPLOYMENT-GUIDE.md](docs/DEPLOYMENT-GUIDE.md)
  Bench and deployment setup notes.

- [docs/progress-sdv-expansion.md](docs/progress-sdv-expansion.md)
  Ongoing expansion and upstream-sync progress.

## Test Harness

The root pytest configuration currently points at `modules/`:

```ini
[pytest]
addopts = --import-mode=importlib --ignore-glob=**/upstream/**
testpaths = modules
```

That means the repo's canonical local test harness is the wrapper layer under
`modules/`, not the raw upstream repos.

Useful examples:

```bash
# Run the full local harness
pytest

# Run one module's tests
pytest modules/score-communication -v

# Run only build-tagged checks
pytest -m build

# Filter by target and CAN interface when a test supports it
pytest --target local --can vcan0
```

The shared pytest fixtures and markers live in
[`modules/conftest.py`](modules/conftest.py).

## Environment and Dependencies

The lightweight root Python requirements for the local harness are in
[`requirements.txt`](requirements.txt).

Core shared runtime/test configuration is in:

- [`config/test_config.yaml`](config/test_config.yaml)
- [`config/tested-commits.yaml`](config/tested-commits.yaml)

The wider cross-ecosystem dependency matrix is documented in
[docs/REQUIREMENTS.md](docs/REQUIREMENTS.md).

## Upstream Sync Model

This workspace uses git submodules and checked-out upstream repos to keep a
local validation surface for many SDV projects at once.

Useful maintenance commands:

```bash
# Initialize or refresh submodules
git submodule update --init --recursive

# Update tracked submodules and emit drift information
bash scripts/update-submodules.sh
```

Not every project updates cleanly on every host. For example, the expansion log
documents Windows-specific issues such as case-sensitive path conflicts in
`score-reference_integration`.

## Bench Scope

This workspace is intended to support both:

- laptop-based validation on Ubuntu,
- Taktflow bench and HIL validation against the zonal ECU setup.

Bench details, evidence depth, and exact module status should be taken from the
current docs, not inferred from this README alone. The old README embedded a
point-in-time bench architecture snapshot that aged badly; that detail now
belongs in the project docs instead of the root landing page.

## What This README Does Not Claim

This README does not claim:

- that every checked-out upstream repo is fully tested,
- that all ecosystems here have equal evidence depth,
- that laptop validation is the same as bench validation,
- that all generated analysis exports are authoritative over source repos.

It is a current map of the workspace, not a blanket completion claim.

## Recommended Reading Order

1. [docs/BENCH-RESULTS-SUMMARY.md](docs/BENCH-RESULTS-SUMMARY.md)
2. [docs/TESTING-STRATEGY.md](docs/TESTING-STRATEGY.md)
3. [docs/progress-sdv-expansion.md](docs/progress-sdv-expansion.md)
4. [config/test_config.yaml](config/test_config.yaml)
5. [modules/conftest.py](modules/conftest.py)

## License and Upstream Ownership

Each upstream project in this workspace keeps its own license, contribution,
and project-governance files. This repo does not replace those upstream rules;
it layers testing, comparison, and evidence collection on top of them.
