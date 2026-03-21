---
document_id: TS-002
title: "Testing Strategy — Upstream Comparison & Adoption Plan"
version: "1.0"
status: active
date: 2026-03-21
---

# Testing Strategy — What Upstream Does vs What We Do

## Gap Summary

| Practice | S-CORE Upstream | We Do It? | Priority |
|---|---|---|---|
| Bazel-based CI (build + test per PR) | 6 workflows per module | **No** — manual SSH | Critical |
| 3-config matrix (default, LLVM, GCC 12) | Yes | **No** — single config | Medium |
| Docker integration tests | OCI image + custom pytest runner | **No** — run directly | Medium |
| QNX QEMU integration | QEMU runner with multi-serial harness | **No** — can't cross-compile | Blocked |
| TRLC + Lobster traceability | Automated req→test linkage | **No** — manual markdown | High |
| CodeQL / MISRA static analysis | SARIF output, coding standards pack | **No** — only clang-tidy | Medium |
| Sanitizer suppression files | .supp files for known false positives | **No** — run raw | Low |
| Coverage HTML reports | genhtml dashboards | **No** — raw lcov numbers | Medium |
| `safety_software_unit` Bazel rule | Links reqs+design+impl+tests | **No** — separate documents | High |
| Ferrocene Rust coverage | Safety-qualified Rust toolchain | **No** — standard Rust | Low |
| Scenario-based testing tools | `score-testing_tools` framework | **No** — ad-hoc scripts | Medium |
| Reference integration repo | Cross-module Bazel build validation | **No** — module-by-module only | High |
| Verification methods catalog | 8 methods defined (boundary, fuzz, etc.) | **Partial** — fuzz + boundary done | Medium |
| Test metadata (method, derivation) | Per-test annotation | **No** — no metadata | Medium |
| Requirement hash tracking | Change in req triggers re-test | **No** — no change detection | High |

---

## What They Do That We Should Adopt

### 1. CI Pipeline (Critical)

**Their approach:** 6 GitHub Actions workflows per module:
- `build_and_test_host.yml` — 3 compiler configs (default, LLVM, GCC 12)
- `build_and_test_qnx.yml` — QNX cross-compile (gated by secrets)
- `address_undefined_behavior_leak_sanitizer.yml` — ASan+UBSan+LSan
- `thread_sanitizer.yml` — TSan
- `coverage_report.yml` — lcov + genhtml HTML report
- `automated_release.yml` — Tagged releases

**Our gap:** Everything manual via SSH.

**Adoption plan:**
```yaml
# .github/workflows/test.yml
on: [push, pull_request]
jobs:
  build-and-test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
        with: {submodules: recursive}
      - name: Setup vcan0
        run: sudo modprobe vcan && sudo ip link add vcan0 type vcan && sudo ip link set up vcan0
      - name: Install deps
        run: bash scripts/setup-lola-env.sh
      - name: Build LoLa
        run: cd score-communication && bazel build //...
      - name: Test LoLa
        run: cd score-communication && bazel test //... --build_tests_only
      - name: Regression test
        run: bash scripts/regression-test-lola.sh
```

**Effort:** 3 hours. **Impact:** Every PR automatically tested.

### 2. TRLC + Lobster Traceability (High)

**Their approach:**
- Requirements in `.trlc` files with typed fields (safety, version, derived_from)
- Lobster config maps requirement types to "needs" (stakeholder, feature, component)
- `safety_software_unit` Bazel rule links: requirements + design + implementation + tests
- Source code linker extracts `@verifies` tags from test files
- Traceability report auto-generated — shows gaps, orphans, coverage

**Our gap:** Manual markdown traceability matrix. No validation. No change detection.

**Adoption plan:**
1. Install TRLC + Lobster on laptop
2. Convert our 65 requirements from markdown to TRLC format
3. Add `@verifies SWR-COM-SHM-001` tags to our bridge test code
4. Run Lobster to generate traceability report
5. Add to CI as quality gate

**Effort:** 1 day. **Impact:** Automated traceability validation.

### 3. Docker/QEMU Integration Testing (Medium)

**Their approach:**
- OCI images built by Bazel (`rules_oci` + `rules_distroless`)
- Ubuntu 24.04 base with pinned APT packages (locked JSON)
- Docker runner: shared memory 1GB, init process, auto-cleanup
- QNX QEMU: multi-serial-port harness, per-process stdout isolation
- Exit codes via sentinel strings in serial output

**Our gap:** Run tests directly on laptop. No isolation.

**Adoption plan:**
1. Use their Docker test infrastructure as-is (it's in the repo)
2. `bazel test //quality/integration_testing/...` already works
3. For our bridge: add integration test that starts skeleton+proxy in Docker
4. QNX QEMU: blocked by toolchain, but infrastructure exists when unblocked

**Effort:** 2 hours (Docker already works). **Impact:** Isolated, reproducible tests.

### 4. CodeQL / MISRA Static Analysis (Medium)

**Their approach:**
- CodeQL with MISRA-C++ coding standards pack
- `codeql_lint.py` creates database during Bazel build
- SARIF + CSV output for results
- Integrated as Bazel test target (`--config=codeql`)

**Our gap:** Only clang-tidy (which passed). No MISRA compliance check on our bridge code.

**Adoption plan:**
1. Run CodeQL on our bridge: `bazel test --config=codeql //score/mw/com/example/can_bridge:...`
2. Review MISRA violations in our `decode()` function
3. Fix or document deviations

**Effort:** 2 hours. **Impact:** MISRA compliance evidence for our code.

### 5. Reference Integration Build (High)

**Their approach:**
- `score-reference_integration` repo builds ALL S-CORE modules together
- `known_good.json` pins compatible versions of all modules
- Platform-specific showcases (Linux, QNX, AutoSD)
- Feature integration tests run across module boundaries

**Our gap:** We test modules individually. Never tested if they build together.

**Adoption plan:**
1. Clone `score-reference_integration`
2. Build with our module versions
3. Run feature integration tests
4. This validates: LoLa + baselibs + lifecycle + persistency + feo work together

**Effort:** Half day. **Impact:** Proves multi-module compatibility.

### 6. Verification Methods Catalog (Medium)

**Their approach (from process_description):**
1. Structural coverage (statement + branch)
2. Interface testing (parameters, protocols, errors, stress)
3. Fault injection (macros, function wrapping, error codes)
4. Boundary value analysis (min, max, just-above, just-below)
5. Equivalence classes (valid, invalid, special)
6. Fuzzy testing (semi-random malformed input)
7. Inspection (manual walkthrough)
8. Analysis (control/data flow)

**Our gap:** We did fuzz (#6), boundary (#4), and some interface testing (#2). Missing: fault injection (#3), equivalence classes (#5), inspection (#7), formal analysis (#8).

**Adoption plan:**
- Add fault injection: wrap `decode()` to return errors, verify caller handles them
- Add equivalence classes: valid frame, invalid DLC, unknown CAN ID, all-zeros, all-0xFF
- Inspection: code review checklist for bridge code
- Mark each test with which method it uses

**Effort:** 1 day. **Impact:** Complete verification method coverage.

---

## What They Do That We Can Skip

| Practice | Why Skip |
|---|---|
| Ferrocene Rust coverage | We don't have safety-qualified Rust toolchain |
| `automated_release.yml` | We're not releasing a library |
| Multi-serial QEMU harness | Overkill for our bridge testing |
| Lobster `safety_software_unit` rule | Can adopt simpler traceability first |
| `known_good.json` version pinning | We use git submodule pinning already |

---

## What We Do That They Don't

| Practice | Why It's Valuable |
|---|---|
| Multi-perspective gap analysis (10 views) | Finds 5x more gaps than single-lens review |
| Real CAN bus testing (can0 + ECUs) | They test on vcan0/QEMU only |
| DBC ground truth verification | They don't decode vehicle signals |
| Release vs debug build performance | They only benchmark one config |
| Testing strategy with lessons learned | Their process docs are prescriptive, ours are experiential |
| Upstream issue filing from testing | They test their own code; we test and report externally |

---

## Adoption Roadmap

| Week | Adopt | Effort | Impact |
|---|---|---|---|
| 1 | CI pipeline (GitHub Actions) | 3 hours | Automatic testing on every PR |
| 1 | Docker integration tests | 2 hours | Isolated, reproducible |
| 2 | TRLC requirements conversion | 1 day | Machine-readable requirements |
| 2 | CodeQL/MISRA on bridge code | 2 hours | Compliance evidence |
| 3 | Reference integration build | Half day | Multi-module validation |
| 3 | Verification methods catalog | 1 day | Complete method coverage |
| 4 | Lobster traceability automation | 1 day | Automated req→test linking |

**Total: ~4 weeks to reach upstream testing maturity.**
