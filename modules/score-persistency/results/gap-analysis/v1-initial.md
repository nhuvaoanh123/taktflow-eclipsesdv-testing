---
document_id: GAP-PER-001
title: "Gap Analysis v1 — Initial Assessment"
version: "1.0"
status: initial
date: 2026-03-23
---

# score-persistency Gap Analysis v1

## Summary

| Status | Count |
|---|---|
| Open | 12 |
| Blocked | 0 |
| Closed | 0 |

ASIL-D rated module — highest safety bar of all S-CORE modules assessed so far.

## Gaps

| Gap | Description | Status | Command |
|---|---|---|---|
| GAP-001 | Build verification | OPEN | `bazel build --config=per-x86_64-linux //src/... //tests/...` |
| GAP-002 | C++ unit tests | OPEN | `bazel test --config=per-x86_64-linux //:test_kvs_cpp` |
| GAP-003 | Rust unit tests | OPEN | `bazel test --config=per-x86_64-linux //src/rust/rust_kvs:tests` |
| GAP-004 | Component integration tests | OPEN | `bazel test --config=per-x86_64-linux //:cit_tests` |
| GAP-005 | Sanitizers | OPEN | No asan/tsan config in .bazelrc — gap vs baselibs |
| GAP-006 | C++ coverage | OPEN | `bazel coverage --config=per-x86_64-linux` |
| GAP-007 | Rust coverage | OPEN | ferrocene-coverage config |
| GAP-008 | Rust Clippy | OPEN | `cargo clippy` or `bazel build --config=lint` |
| GAP-009 | Rust Miri | OPEN | `cargo +nightly miri test` |
| GAP-010 | Benchmarks | OPEN | `bazel test //:bm_kvs_cpp` |
| GAP-011 | ASIL-D safety evidence | OPEN | FMEA, DFA, safety manual exist in aspice/ but unverified |
| GAP-012 | Snapshot/CRC integrity test | OPEN | Verify snapshot create/restore + CRC validation |
