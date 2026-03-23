---
document_id: PERF-LOLA-001
title: "LoLa IPC Latency Distribution"
date: 2026-03-21
---

# LoLa IPC Latency Distribution

## Test Setup

| Parameter | Value |
|---|---|
| Interface | vcan0 (SIL traffic from can_gateway.main) |
| Skeleton | CAN→LoLa bridge v3 |
| Proxy | Standard proxy with age measurement |
| Samples | 500 |
| Build | Debug (fastbuild) |
| Host | Linux Laptop (AMD Ryzen 7, 16 cores, 14GB RAM) |

## Results

| Percentile | Latency (µs) |
|---|---|
| Min | 10 |
| p50 (median) | **28** |
| p90 | 39 |
| p95 | **43** |
| p99 | **54** |
| Max | 64 |
| Mean | 29.8 |
| Stdev | 9.3 |
| Jitter (max-min) | 54 |

## NFR-COM-001 Verification

Target: < 100 µs

**PASS** — p99 = 54 µs (46% margin to target)

## Memory Stability

| Metric | Value |
|---|---|
| RSS at start | 8,324 KB |
| RSS after 1 min | 8,324 KB |
| Growth | 0 KB |
| **Verdict** | **No memory leak** |

## Upstream Issues Filed

- [communication#220](https://github.com/eclipse-score/communication/issues/220) — concurrent proxy crash
- [toolchains_qnx#46](https://github.com/eclipse-score/toolchains_qnx/issues/46) — checksum stale
