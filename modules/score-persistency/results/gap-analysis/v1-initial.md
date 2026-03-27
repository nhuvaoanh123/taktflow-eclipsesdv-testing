# Gap Analysis: score-persistency v0.0.0

**Date:** 2026-03-23
**Safety Classification:** ASIL-D
**Status:** Initial Assessment

## Summary

12 gaps identified across build infrastructure, testing, safety verification,
and documentation. ASIL-D classification imposes a higher bar than QM/ASIL-B
components (e.g., score-baselibs). 4 gaps are classified as critical for
ASIL-D compliance.

---

## GAP-PER-001: No Sanitizer Configurations [CRITICAL]

**Category:** Build Infrastructure
**Severity:** Critical (ASIL-D)

The `.bazelrc` does not define `--config=asan`, `--config=tsan`, or
`--config=ubsan` sanitizer configurations. ASIL-D requires memory safety
and undefined behavior detection via AddressSanitizer, ThreadSanitizer,
and UndefinedBehaviorSanitizer.

**Recommendation:** Add sanitizer configs to `.bazelrc` following the pattern
used by other S-CORE components. Run sanitized tests in CI.

---

## GAP-PER-002: No MISRA/AUTOSAR C++ Compliance Check [CRITICAL]

**Category:** Code Quality
**Severity:** Critical (ASIL-D)

No static analysis tooling for MISRA C++ or AUTOSAR C++ coding guidelines is
configured. ASIL-D C++ code must comply with an approved coding standard.

**Recommendation:** Integrate a MISRA/AUTOSAR C++ checker (e.g., Polyspace,
Parasoft, or cppcheck with MISRA rules) into the CI pipeline.

---

## GAP-PER-003: No Formal Safety Analysis Artifacts [CRITICAL]

**Category:** Safety Documentation
**Severity:** Critical (ASIL-D)

No FMEA, FTA, or safety case documentation found in the repository.
ASIL-D requires formal safety analysis artifacts per ISO 26262.

**Recommendation:** Create safety analysis directory with FMEA for KVS
failure modes (data corruption, CRC mismatch, snapshot inconsistency,
flush failure).

---

## GAP-PER-004: Unsafe Rust Code Review Not Documented [CRITICAL]

**Category:** Safety Verification
**Severity:** Critical (ASIL-D)

Unsafe Rust blocks (if any) lack documented safety justifications via
`// SAFETY:` comments as required by the Rust unsafe code guidelines.
ASIL-D demands traceable justification for all unsafe operations.

**Recommendation:** Audit all `unsafe` blocks, add `// SAFETY:` comments,
and configure clippy `undocumented_unsafe_blocks` lint as `deny`.

---

## GAP-PER-005: No Mutation Testing

**Category:** Test Quality
**Severity:** High

No mutation testing framework (e.g., cargo-mutants for Rust, mull for C++)
is configured. ASIL-D test suites should demonstrate fault detection
capability through mutation score metrics.

**Recommendation:** Integrate cargo-mutants for Rust crates and evaluate
mull or similar for C++ test targets.

---

## GAP-PER-006: No Fault Injection Tests

**Category:** Testing
**Severity:** High

No fault injection tests for the KVS library. ASIL-D requires testing
under fault conditions: corrupted JSON files, disk full, permission errors,
CRC mismatches, and partial writes.

**Recommendation:** Create fault injection test scenarios using the existing
`kvs_mock.rs` mock infrastructure and `@score_baselibs` filesystem mocks.

---

## GAP-PER-007: No Coverage Threshold Enforcement

**Category:** Testing
**Severity:** High

Code coverage is collectible (LCOV for C++, ferrocene for Rust) but no
minimum threshold is enforced. ASIL-D typically requires >95% MC/DC
coverage for safety-critical code paths.

**Recommendation:** Configure coverage thresholds in CI. Define MC/DC
coverage targets for critical paths (flush, snapshot, CRC validation).

---

## GAP-PER-008: No Concurrency/Thread Safety Tests

**Category:** Testing
**Severity:** High

No dedicated concurrency or thread safety tests for the KVS API.
If the KVS is accessed from multiple threads (common in automotive ECUs),
data races must be prevented and tested.

**Recommendation:** Add multi-threaded test scenarios. Run with TSan
(once GAP-PER-001 is resolved). Document thread-safety guarantees in API.

---

## GAP-PER-009: No Performance Regression Tracking

**Category:** Benchmarks
**Severity:** Medium

Google Benchmark (`bm_kvs.cpp`) exists but no baseline comparison or
regression detection is configured. Performance regressions in KVS
operations could violate timing requirements.

**Recommendation:** Store benchmark baselines and configure CI to detect
regressions >10% in key operations (read, write, flush, snapshot).

---

## GAP-PER-010: No API Stability Guarantee Documentation

**Category:** Documentation
**Severity:** Medium

No API stability policy or changelog documenting breaking changes.
Version 0.0.0 suggests pre-release, but consumers need to understand
the API contract.

**Recommendation:** Add CHANGELOG.md and define API stability policy.
Consider semver graduation plan (0.0.0 -> 0.1.0 -> 1.0.0).

---

## GAP-PER-011: No Cargo Miri in CI

**Category:** Rust Quality
**Severity:** Medium

`cargo miri` (undefined behavior detector for Rust) is not integrated
into CI workflows. While Rust's type system prevents many UB classes,
miri catches issues in unsafe code and FFI boundaries.

**Recommendation:** Add cargo miri test step to at least one CI workflow.
Requires nightly Rust toolchain.

---

## GAP-PER-012: No Cross-Platform Build Verification

**Category:** Build Infrastructure
**Severity:** Low

Only `--config=per-x86_64-linux` is tested. No evidence of cross-compilation
testing for automotive target architectures (ARM, AArch64). While this may
be handled at integration level, the library itself should verify portability.

**Recommendation:** Add build verification for target architectures used in
production (e.g., `per-aarch64-linux` if applicable).

---

## Priority Matrix

| Priority | Gaps | Action |
|----------|------|--------|
| P0 (Critical) | PER-001, PER-002, PER-003, PER-004 | Must resolve before ASIL-D qualification |
| P1 (High) | PER-005, PER-006, PER-007, PER-008 | Required for production readiness |
| P2 (Medium) | PER-009, PER-010, PER-011 | Recommended for maturity |
| P3 (Low) | PER-012 | Nice to have |

## ASIL-D vs QM/ASIL-B Delta

The following requirements apply to score-persistency (ASIL-D) that do
**not** apply to QM or ASIL-B components like score-baselibs:

1. **MC/DC coverage** required (not just statement/branch coverage)
2. **MISRA/AUTOSAR C++ compliance** mandatory (not optional)
3. **Formal safety analysis** (FMEA/FTA) required
4. **Fault injection testing** required
5. **All unsafe code** must have documented safety justification
6. **Mutation testing** recommended for test quality assurance
7. **Independent review** of safety-critical code paths
