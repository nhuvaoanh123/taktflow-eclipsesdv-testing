# Taktflow Bench Deployment Guide

## Architecture

| Machine | Role | OS | IP |
|---|---|---|---|
| Windows PC | Development, Claude Code | Windows 10 | localhost |
| Laptop | Build machine (x86_64) | Ubuntu 24.04 | 192.168.0.158 |
| Raspberry Pi | Test target (aarch64) | Ubuntu 24.04 Server | 192.168.0.197 |

## Prerequisites

### Laptop (Build Machine)
- Ubuntu 24.04 LTS, x86_64
- Bazelisk installed as `/usr/local/bin/bazel`
- GCC (system — Bazel downloads hermetic 12.2.0)
- Git, Python 3.12, cargo/rustc
- QEMU user-static + binfmt-support (for aarch64 test emulation)
- fakechroot (for lifecycle smoke tests)
- SSH key access from Windows PC

### Raspberry Pi (Test Target)
- Ubuntu 24.04 Server, arm64
- SSH enabled
- Bazelisk installed (for local experiments — not primary build)
- Note: Native aarch64 builds fail due to LLVM toolchain incompatibility. Use laptop for builds, Pi for execution.

## Build Commands

### score-baselibs
```bash
cd ~/taktflow-eclipsesdv-testing/score-baselibs
bazel build --config=bl-x86_64-linux //score/...          # x86_64
bazel build --config=bl-aarch64-linux //score/...         # aarch64 cross
bazel test --config=bl-x86_64-linux //score/...           # run tests
bazel test --config=bl-x86_64-linux --config=asan_ubsan_lsan //score/...  # sanitizers
bazel coverage --config=bl-x86_64-linux //score/...       # coverage
```

### score-lifecycle
```bash
cd ~/taktflow-eclipsesdv-testing/score-lifecycle
bazel build --config=x86_64-linux //src/... //examples/...
bazel test --config=x86_64-linux //src/... //tests/...
bazel test --config=x86_64-linux --define sanitize=address //src/...
```

### score-persistency
```bash
cd ~/taktflow-eclipsesdv-testing/score-persistency
bazel build --config=per-x86_64-linux //src/...
bazel test --config=per-x86_64-linux //:unit_tests
bazel test --config=per-x86_64-linux //:cit_tests
```

### score-feo
```bash
cd ~/taktflow-eclipsesdv-testing/score-feo
bazel build --config=x86_64-linux //...
bazel test --config=x86_64-linux //...
```

## Transferring Code
GitHub account is flagged — use SCP:
```bash
scp -r /h/VS-Taktflow-Systems/Taktflow-Systems/taktflow-eclipsesdv-testing an-dao@192.168.0.158:~/
```
Fix Windows line endings after SCP:
```bash
find . -type f \( -name 'BUILD' -o -name '*.bzl' -o -name '*.sh' -o -name '*.toml' -o -name '*.rs' \) | xargs sed -i 's/\r$//'
```

## Running Local Tests (Windows PC)
```bash
cd h:/VS-Taktflow-Systems/Taktflow-Systems/taktflow-eclipsesdv-testing
python -m pytest tests/score-baselibs/ tests/score-lifecycle/ tests/score-persistency/ tests/score-feo/
```

## Known Issues
1. Native aarch64 Pi build fails (LLVM ARM64 binary not available, GCC 13 -Werror compat)
2. QEMU aarch64 test runner needs explicit setup (qemu-user-static + binfmt-support)
3. Windows→Linux SCP introduces \r line endings in text files
4. score-feo BUILD genrule particularly sensitive to line endings
