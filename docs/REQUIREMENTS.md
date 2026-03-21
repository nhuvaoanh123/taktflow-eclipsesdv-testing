# Eclipse SDV Testing — Dependency Requirements

## System-Level Prerequisites

| Tool | Version | Needed by |
|---|---|---|
| Python | >= 3.10 | Kuksa providers, Velocitas Python SDK, Ankaios SDK, tests |
| Rust (rustup) | stable | Kuksa databroker, Chariott, Ibeji, uProtocol Rust libs, Ankaios |
| Go | >= 1.17 | Leda cloud-connector, vehicle-update-manager |
| Java JDK | >= 11 (17 preferred) | uProtocol up-java, up-core-api |
| Node.js | >= 18 | Velocitas CLI, Leda docs, Kuksa Android SDK tooling |
| CMake | >= 3.10 | Kuksa SOME/IP provider, Leda self-update-agent, uProtocol C++ |
| Conan | >= 2.0 | Velocitas C++ SDK/template, uProtocol C++/Zenoh C++ |
| Docker | latest | All Dockerized components |
| Android SDK + Gradle | latest | Kuksa Android SDK, Velocitas Kotlin template |
| Maven | >= 3.8 | uProtocol up-java, up-core-api |
| protoc (protobuf compiler) | >= 3.21 | gRPC code generation across most projects |
| Boost | >= 1.55 | Kuksa SOME/IP provider (via vsomeip) |
| gpsd | latest | Kuksa GPS provider |

---

## Per-Project Dependencies

### Kuksa — Databroker (Rust)
```
# Cargo.toml workspace — build with:
cargo build --release
# Integration test Python deps:
asyncio, grpcio, protobuf, pytest, pytest-ordering, pytest-asyncio
# Dev: grpcio-tools, mypy, mypy-protobuf
```

### Kuksa — Python SDK
```
cmd2==1.5.0
grpcio==1.68.0
grpcio-tools==1.68.0
jsonpath-ng==1.7.0
protobuf==5.29.6
pygments==2.18.0
websockets==14.1
```

### Kuksa — CAN Provider (Python)
```
cantools==40.5.0
can-j1939==2.0.12
kuksa-client==0.5.0
numpy==2.2.6
python-can==4.6.1
py-expression-eval==0.3.14
pyserial==3.5
pyyaml==6.0.2
# Dev: pytest, pylint
```

### Kuksa — GPS Provider (Python)
```
kuksa-client~=0.4.1
gpsdclient
```

### Kuksa — DDS Provider (Python)
```
cyclonedds
kuksa-client~=0.4.1
pyyaml
py-expression-eval
# Test: pytest, pytest-html, pytest-cov, pytest-asyncio
```

### Kuksa — SOME/IP Provider (C++)
```
# Conan:
grpc/1.38.0
boost/1.72.0
zlib/1.2.13
# CMake fetches: vsomeip 3.1.20.3 from COVESA/vsomeip
```

### Kuksa — Perf Benchmarks (Rust)
```
databroker-proto (from kuksa-databroker git)
tokio, tonic, tower, clap, serde_json, hdrhistogram, indicatif, csv
```

### Kuksa — val.services (Python)
```
# HVAC service:
grpcio>=1.44.0, protobuf>=3.19.4, types-protobuf
# Mock service adds: scipy>=1.10.1, kuksa_client
# Integration tests add: dapr>=1.8.1, grpcio-tools>=1.54.2, pytest, pytest-ordering, pytest-asyncio
```

### Kuksa — Common
```
# JWT tools:
PyJWT==2.12.0
cryptography>=39.0.1
```

### Kuksa — Android SDK (Kotlin/Gradle)
```
# Gradle build — requires Android SDK
# Uses: protobuf, grpc-kotlin, kotlinx-coroutines
# Dev: commitlint, husky
```

---

### Velocitas — Python SDK
```
grpcio==1.64.1
protobuf==5.29.5
cloudevents==1.11.0
aiohttp==3.10.11
paho-mqtt==2.1.0
opentelemetry-distro==0.46b0
opentelemetry-instrumentation-logging==0.46b0
opentelemetry-sdk==1.25.0
opentelemetry-api==1.25.0
# Dev: grpcio-tools, grpc-stubs, mypy-protobuf, apscheduler, pytest, pytest-asyncio, pytest-cov, tox, pre-commit, mypy, pip-tools
```

### Velocitas — C++ SDK
```
# Conan deps: fmt, gRPC, nlohmann_json, PahoMqttCpp, eclipse-paho-mqtt-c, protobuf, absl
# Python: gcovr==5.2, conan~=2.20, pre-commit==3.5.0, cpplint==1.6.1
# CMake >= 3.16, C++17
```

### Velocitas — C++ Template
```
# Conan:
fmt/11.1.1
nlohmann_json/3.11.3
vehicle-model/generated
vehicle-app-sdk/0.7.1
# Python: conan, pre-commit, pip-tools, mypy
```

### Velocitas — Rust SDK
```
# Cargo workspace — build with cargo
```

### Velocitas — Kotlin Template
```
# Gradle build — requires Android SDK + Kotlin plugin
```

### Velocitas — Vehicle Model Python
```
# No external deps (pure Python, setuptools only)
# Package: sdv-model v0.3.0
```

### Velocitas — Vehicle Model Generator (Python)
```
vss-tools==4.0
# Dev: pre-commit, mypy
# Test: pytest, pytest-cov, conan==2.*, velocitas-lib==0.0.13
```

### Velocitas — CLI (Node.js)
```
@oclif/core: 3.27.0
fs-extra: 11.2.0
inquirer: 8.2.7
node-pty: 1.0.0
semver: 7.6.3
simple-git: 3.26.0
# Dev: typescript, mocha, chai, eslint, sinon, nyc
```

---

### Leda — Distro
```
# Yocto/BitBake build system
# See meta-leda for layer dependencies
```

### Leda — Cloud Connector (Go)
```
github.com/ThreeDotsLabs/watermill v1.1.1
github.com/eclipse-kanto/azure-connector
github.com/eclipse-kanto/suite-connector v0.1.0-M2
github.com/eclipse/ditto-clients-golang
github.com/eclipse/paho.mqtt.golang v1.4.1
```

### Leda — Vehicle Update Manager (Go)
```
github.com/docker/docker v20.10.12
github.com/eclipse-kanto/container-management v0.1.0-M1
github.com/eclipse/paho.mqtt.golang v1.3.5
github.com/spf13/cobra v1.2.1
k8s.io/api, k8s.io/client-go, k8s.io/kubectl v0.23.5
```

### Leda — Self-Update Agent (C++)
```
# CMake build, C++14
# See cmake/dependencies.cmake for fetched deps
```

### Leda — OTel Exporter
```
# OpenTelemetry — check repo for specific deps
```

---

### uProtocol — Core API (Java/Maven)
```
protobuf 3.21.10
junit-jupiter 5.7.0
assertj-core 3.16.1
# Java 11+, Maven
```

### uProtocol — up-java (Maven)
```
protobuf 4.33.0
# Java 17, Maven
# Test: JUnit, Mockito
```

### uProtocol — up-rust
```
async-trait, bytes, protobuf 3.7.2, rand, regex, tokio, tracing, uriparse, uuid-simd
# Build: protobuf-codegen, protoc-bin-vendored
# Test: cucumber, mockall, test-case, clap
```

### uProtocol — up-cpp (CMake/Conan)
```
# Conan:
protobuf/3.21.12
spdlog/1.13.0
up-core-api/~1.6
# Test: gtest/1.14.0
# C++17
```

### uProtocol — Zenoh Transport Rust
```
up-rust 0.9, zenoh 1.6.2, async-trait, bytes, protobuf, tokio, tracing
# Test: serial_test, test-case, chrono
```

### uProtocol — Zenoh Transport C++ (CMake/Conan)
```
up-cpp/^1.0.1
zenohcpp/1.2.1, zenohc/1.2.1
spdlog/~1.13
up-core-api/1.6.0-alpha4
protobuf/~3.21
# Test: gtest/1.14.0
```

### uProtocol — MQTT5 Transport Rust
```
up-rust 0.9, paho-mqtt 0.13.3, async-channel, backon, futures, protobuf, tokio, slab
# Test: testcontainers, mockall, serial_test, env_logger
```

### uProtocol — VSOMEIP Transport Rust
```
# See Cargo.toml workspace members for deps
```

---

### Chariott — Service Discovery (Rust)
```
# Cargo workspace — build with cargo
```

### Chariott — Agemo Pub/Sub (Rust)
```
# Cargo workspace — build with cargo
```

### Ibeji — Digital Twin (Rust)
```
# Cargo workspace — build with cargo
```

### Ibeji — Freyja Cloud Sync (Rust)
```
# Cargo workspace — build with cargo
```

---

### Ankaios — Orchestrator (Rust)
```
# Cargo workspace — build with cargo
```

### Ankaios — Python SDK
```
# setup.py with grpc_tools for proto generation
# Requires: grpcio, protobuf, requests (for proto download)
# Test: pytest, coverage
```

### Ankaios — Rust SDK
```
prost 0.14, tonic 0.14, tokio 1.41, serde, serde_yaml, thiserror, uuid, async-trait, log, env_logger, home
# Build: tonic-prost-build
# Test: tempfile, nix, mockall
```

---

### SDV Blueprints — Insurance (Python)
```
grpcio==1.62.0
grpcio-tools==1.62.0
numpy==1.26.4
paho-mqtt==2.0.0
protobuf==4.25.3
GitPython==3.1.41
coverage==7.4.4
```

### SDV Blueprints — Fleet Management, Companion App, Service-to-Signal, Software Orchestration, ROS Racer
```
# Docker Compose based — check docker-compose.yml in each repo
```

---

## Quick Install (Linux Laptop)

```bash
# System packages (Ubuntu/Debian)
sudo apt update && sudo apt install -y \
  python3 python3-pip python3-venv \
  build-essential cmake g++ \
  protobuf-compiler libprotobuf-dev \
  golang-go \
  default-jdk maven \
  nodejs npm \
  docker.io docker-compose \
  gpsd libboost-all-dev \
  git curl

# Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Conan (for C++ projects)
pip install conan

# Python test deps
pip install pytest pytest-asyncio grpcio grpcio-tools kuksa-client paho-mqtt pyyaml

# Clone with all submodules
git clone --recursive https://github.com/<your-org>/taktflow-eclipsesdv-testing.git
```
