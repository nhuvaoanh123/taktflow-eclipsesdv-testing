# Eclipse SDV 56-Module Bench Test Plan

**Project:** taktflow-eclipsesdv-testing
**Date:** 2026-03-20
**Target:** Linux Laptop (SDV host) + Raspberry Pi 4 (QNX 8.0 RTOS) + 4-ECU CAN Bus HIL Bench

---

## 1. Test Infrastructure

### 1.1 Bench Topology

```
┌─────────────────────────────────────────────────────────────────────┐
│  Linux Laptop (192.168.0.158) ◄── SDV HOST (all Eclipse SDV here)  │
│  ├── Ankaios (ank-server + ank-agent)                               │
│  ├── Kuksa Databroker (container or native)                         │
│  ├── CAN Provider (reads CAN via USB adapter)                       │
│  ├── Velocitas apps, Kuksa Python SDK                               │
│  ├── Container runtime (Podman/Docker)                              │
│  ├── pytest test runner                                             │
│  └── USB CAN adapter ─────────────────────┐                        │
└───────┬───────────────────────────────────┼────────────────────────┘
        │ WiFi (192.168.0.x)                │ USB CAN
        ▼                                   ▼
┌───────────────────────┐            ┌─────────────────────┐
│  Raspberry Pi 4       │            │  CAN Bus (500 kbps) │
│  QNX 8.0 (RTOS only) │◄──────────►│  120Ω terminated    │
│  ├── Real-time tasks  │  USB CAN   │                     │
│  ├── CAN gateway      │            │  ┌─────┐ ┌─────┐   │
│  ├── BMS control      │            │  │TMS570│ │G474 │   │
│  └── Safety monitor   │            │  │ CVC  │ │ FZC │   │
│  192.168.0.xxx        │            │  └──┬───┘ └──┬──┘   │
└───────────────────────┘            │  ┌──┴───┐ ┌──┴──┐   │
                                     │  │F413ZH│ │L552ZE│  │
┌───────────────────────┐            │  │ RZC  │ │ HSM  │  │
│  Desktop PC           │            │  └──────┘ └──────┘  │
│  192.168.0.105        │            └─────────────────────┘
│  ├── Build server     │
│  ├── Rigol DHO804 ────┼──── 192.168.1.100:5555 (SCPI)
│  └── Flash tools      │
└───────────────────────┘

IMPORTANT: All Eclipse SDV software runs on the Linux Laptop.
The Pi runs QNX only — no containers, no Linux, no SDV stack.
The laptop reads CAN bus data via its own USB CAN adapter.
The Pi participates as a QNX RTOS node on the CAN bus.
```

### 1.2 Test Categories

| Code | Category | Where it Runs | Description |
|------|----------|---------------|-------------|
| **B** | Build | Laptop | Clone, resolve deps, compile without errors |
| **U** | Unit | Laptop | Run the module's upstream test suite |
| **I** | Integration | Laptop | Cross-module communication (SDV stack on laptop, CAN via USB adapter) |
| **E** | End-to-End | Full Bench | Signal flow: ECUs → CAN bus → Laptop USB CAN → SDV stack → test assertions |
| **P** | Performance | Laptop | Latency, throughput, resource usage of SDV stack |
| **S** | Security | Laptop + HSM ECU | Authentication, TLS, certificate validation |

### 1.3 pytest Markers

```ini
[tool:pytest]
markers =
    build: Build verification tests
    unit: Upstream unit test execution
    integration: Cross-module integration tests
    e2e: End-to-end bench tests (requires full bench)
    perf: Performance benchmarks
    security: Security validation tests
    qnx: Requires QNX target platform
    can: Requires CAN bus hardware
    rigol: Requires oscilloscope
    phase1: Production-Ready modules
    phase2: Growing modules
    phase3: Developing modules
    phase4: Early-Stage modules
    phase5: Incubating modules
```

### 1.4 Test Directory Structure

```
tests/
├── conftest.py              # Extended with new fixtures
├── build/                   # Build verification (B-xx)
├── unit/                    # Upstream test wrappers (U-xx)
├── integration/             # Cross-module tests (I-xx)
├── e2e/                     # Full-bench scenarios (E-xx)
├── platform/                # QNX-specific tests
├── performance/             # Latency/throughput (P-xx)
└── security/                # Auth/TLS/attestation (S-xx)
```

### 1.5 Config Extensions (`config/test_config.yaml`)

```yaml
# Existing config retained, plus:

ankaios:
  server_host: <pi-ip>
  server_port: 25551

can:
  interface: can0          # Physical CAN on bench
  vcan_interface: vcan0    # Virtual CAN for local testing
  bitrate: 500000
  provider_dbc: config/vehicle.dbc

rigol:
  host: 192.168.1.100
  scpi_port: 5555

bench:
  ecus:
    cvc: { can_id_base: 0x100, uart_port: COM9,  baud: 115200 }
    rzc: { can_id_base: 0x200, uart_port: COM15, baud: 115200 }
    fzc: { can_id_base: 0x300, uart_port: COM3,  baud: 115200 }
    hsm: { can_id_base: 0x400, uart_port: COM7,  baud: 115200 }
```

### 1.6 New Fixtures (conftest.py extensions)

| Fixture | Scope | Description |
|---------|-------|-------------|
| `ankaios_client` | session | gRPC connection to Ankaios API (localhost) |
| `can_interface` | session | python-can interface for `can0` (USB CAN) or `vcan0` |
| `rigol_scope` | session | SCPI TCP connection to Rigol at 192.168.1.100:5555 |
| `ssh_pi` | session | paramiko SSH session to Pi (for QNX RTOS monitoring/CAN gateway control) |
| `databroker_client` | session | gRPC connection to Kuksa databroker (localhost) |

---

## 2. Dependency Graph

Modules must be tested layer-by-layer. Each layer's Build + Unit + Integration must pass before the next layer begins.

```
Layer 0: Infrastructure
  └── Linux laptop ready, USB CAN adapter connected, CAN bus wired, Pi QNX boot, WiFi up

Layer 1: Orchestration
  └── ankaios-ankaios (container orchestrator on Linux laptop)

Layer 2: Data Plane
  └── eclipse-kuksa-databroker (VSS data broker on laptop, deployed via Ankaios)

Layer 3: Signal Ingestion
  ├── kuksa-kuksa-can-provider (reads CAN via laptop USB adapter → feeds databroker)
  ├── kuksa-kuksa.val.feeders (DBC replay → databroker)
  └── kuksa-kuksa-common (JWT, TLS utilities)

Layer 4: Client SDKs
  ├── eclipse-kuksa-python-sdk (Python gRPC client)
  ├── eclipse-velocitas-sdk (Python vehicle app SDK)
  ├── velocitas-vehicle-app-cpp-sdk (C++ vehicle app SDK)
  └── velocitas-cli (scaffolding tool)

Layer 5: Vehicle Applications
  ├── velocitas-vehicle-app-python-template
  ├── velocitas-vehicle-app-cpp-template
  ├── velocitas-vehicle-model-python
  ├── velocitas-vehicle-model-cpp
  └── velocitas-vehicle-model-generator

Layer 6: Middleware & Protocols
  ├── uprotocol-up-spec, up-core-api
  ├── uprotocol-up-rust, up-cpp, up-java
  ├── uprotocol transports (zenoh, mqtt5, vsomeip)
  ├── chariott-chariott (service discovery)
  ├── chariott-Agemo (pub/sub)
  ├── ibeji-ibeji (digital twin)
  └── ibeji-freyja (cloud sync)

Layer 7: Platform & Blueprints
  ├── eclipse-leda-distro, leda-meta-leda
  ├── leda-contrib-* (update agents, OTel, cloud connector)
  ├── ankaios SDKs (Python, Rust)
  └── sdv-blueprints-* (fleet, companion, insurance, etc.)
```

---

## 3. Phase 1 — Production-Ready (Score >= 70)

### 3.1 ankaios-ankaios — Container Orchestrator [70.3]

**Language:** Rust | **Build:** cargo | **Status:** Active | **Stars:** 119

| ID | Cat | Platform | Test Description | Pass Criteria |
|----|-----|----------|------------------|---------------|
| ANK-B-01 | B | Laptop | `cargo build --release` (ank-server + ank-agent) | Exit code 0 |
| ANK-U-01 | U | Laptop | `cargo test --workspace` | All upstream tests pass |
| ANK-I-01 | I | Laptop | Start server + agent, deploy test workload manifest | Workload state = Running |
| ANK-I-02 | I | Laptop | Deploy kuksa-databroker container via Ankaios manifest | Container starts, gRPC port open |
| ANK-I-03 | I | Laptop | `ank get workloads` returns correct state for all workloads | All states reported |
| ANK-E-01 | E | Full Bench | Ankaios deploys databroker + CAN provider, CAN data flows from ECUs via USB CAN | VSS signal value received |
| ANK-P-01 | P | Laptop | Container startup time | < 5 seconds |
| ANK-P-02 | P | Laptop | Memory footprint (ank-server + ank-agent) | < 50 MB combined |
| ANK-S-01 | S | Laptop | mTLS between server and agent | Connection verified with certs |

**Entry:** Layer 0 (laptop ready, USB CAN connected, CAN bus wired) confirmed.
**Exit:** ANK-B-01, ANK-U-01, ANK-I-02 all PASS.

---

## 4. Phase 2 — Growing (Score 40-54)

### 4.1 eclipse-kuksa-databroker — Vehicle Data Broker [54.5]

**Language:** Rust | **Build:** cargo | **Status:** Active | **Contributors:** 33

| ID | Cat | Platform | Test Description | Pass Criteria |
|----|-----|----------|------------------|---------------|
| KDB-B-01 | B | Laptop | `cargo build --release` (databroker + CLI) | Exit code 0 |
| KDB-U-01 | U | Laptop | `cargo test --workspace` | Upstream tests pass |
| KDB-I-01 | I | Laptop | Run upstream `integration_test/test_databroker.py` against local instance | All tests pass |
| KDB-I-02 | I | Laptop | Deploy via Ankaios, query via gRPC | gRPC response received |
| KDB-I-03 | I | Laptop | Load VSS 4.0, verify 4 configured signals queryable | All 4 signals found |
| KDB-E-01 | E | Full Bench | CAN provider reads ECU frames via USB CAN → feeds databroker → Python client reads | Values match |
| KDB-P-01 | P | Laptop | Subscribe to 100 VSS signals simultaneously | > 1000 updates/sec |
| KDB-P-02 | P | Laptop | Signal publish-to-subscribe latency | < 10ms |
| KDB-S-01 | S | Laptop | JWT token authentication | Unauthorized request rejected |

**Entry:** ANK-I-02 PASS (Ankaios can deploy containers).
**Exit:** KDB-I-03 PASS (databroker serves VSS signals).

### 4.2 eclipse-velocitas-sdk — Vehicle App Python SDK [43.9]

**Language:** Python | **Build:** pip | **Status:** Maintained

| ID | Cat | Platform | Test Description | Pass Criteria |
|----|-----|----------|------------------|---------------|
| VPY-B-01 | B | Laptop | `pip install -e .` in venv | Exit code 0 |
| VPY-U-01 | U | Laptop | `pytest` (upstream, 10 test files) | All pass |
| VPY-I-01 | I | Laptop | Minimal VehicleApp connects to local databroker, reads Vehicle.Speed | Value returned |
| VPY-I-02 | I | Laptop | VehicleApp connects to Ankaios-deployed databroker | Value returned |
| VPY-E-01 | E | Full Bench | VehicleApp receives battery temp from ECUs via USB CAN → databroker, triggers alert | Alert fires |

**Exit:** VPY-I-01 PASS.

### 4.3 velocitas-cli — CLI Tool [42.8]

**Language:** TypeScript/Node.js | **Build:** npm | **Status:** Maintained

| ID | Cat | Platform | Test Description | Pass Criteria |
|----|-----|----------|------------------|---------------|
| VCL-B-01 | B | Laptop | `npm install && npm run build` | Exit code 0 |
| VCL-U-01 | U | Laptop | `npm test` (mocha/chai, 20 test files) | All pass |
| VCL-I-01 | I | Laptop | `velocitas init` + `velocitas create` — scaffold Python app | Project created |
| VCL-I-02 | I | Laptop | `velocitas exec` — run scaffolded app against local databroker | App connects |

**Exit:** VCL-B-01, VCL-U-01 PASS.

### 4.4 uprotocol-up-spec — Universal Protocol Specification [42.4]

**Language:** Protobuf/Spec | **Status:** Active

| ID | Cat | Platform | Test Description | Pass Criteria |
|----|-----|----------|------------------|---------------|
| UPS-B-01 | B | Laptop | `protoc` compiles all .proto files | No errors |
| UPS-U-01 | U | Laptop | Proto schema lint + validation | Clean |
| UPS-I-01 | I | Laptop | Generate Python/C++/Rust stubs, verify compilation | All compile |

**Exit:** UPS-B-01 PASS.

### 4.5 eclipse-kuksa-python-sdk — Python Client [42.2]

**Language:** Python | **Build:** pip | **Status:** Active | **Contributors:** 31

| ID | Cat | Platform | Test Description | Pass Criteria |
|----|-----|----------|------------------|---------------|
| KPY-B-01 | B | Laptop | `pip install -e .` | Exit code 0 |
| KPY-U-01 | U | Laptop | `pytest` (3 test files) | All pass |
| KPY-I-01 | I | Laptop | Connect to local databroker, subscribe + publish + readback | Values match |
| KPY-I-02 | I | Laptop | Connect to Ankaios-deployed databroker, full CRUD on VSS signals | All ops succeed |
| KPY-E-01 | E | Full Bench | Read CAN-sourced signals from ECUs via USB CAN, validate vs Rigol measurement | Within tolerance |
| KPY-P-01 | P | Laptop | Round-trip latency for 1000 sequential get/set ops | < 5ms avg |

**Exit:** KPY-I-01 PASS.

### 4.6 velocitas-vehicle-app-cpp-sdk — C++ Vehicle App SDK [40.7]

**Language:** C++ | **Build:** Conan + CMake | **Status:** Maintained

| ID | Cat | Platform | Test Description | Pass Criteria |
|----|-----|----------|------------------|---------------|
| VCS-B-01 | B | Laptop | `conan install . && cmake --build .` | Exit code 0 |
| VCS-U-01 | U | Laptop | `ctest` (16 test files, gtest) | All pass |
| VCS-I-01 | I | Laptop | Build sample C++ VehicleApp, connect to local databroker | Connection OK |
| VCS-I-02 | I | Laptop | Cross-compile for aarch64, deploy to Pi, verify connection | Connects |

**Exit:** VCS-B-01, VCS-U-01 PASS.

---

## 5. Phase 3 — Developing (Score 25-39)

### 5.1 ankaios-ank-sdk-python [39.3]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| ASP-B-01 | B | Laptop | `pip install -e .` + proto gen | Exit 0 |
| ASP-U-01 | U | Laptop | `pytest` (25 test files) | All pass |
| ASP-I-01 | I | Laptop | Python script creates/deletes workload via gRPC | State changes |
| ASP-I-02 | I | Laptop | Same targeting Ankaios-deployed workloads | Workload created |

### 5.2 velocitas-vehicle-app-python-template [38.7]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| VPT-B-01 | B | Laptop | Clone template, install deps | Exit 0 |
| VPT-U-01 | U | Laptop | `pytest` (4 test files) | All pass |
| VPT-I-01 | I | Laptop | Run template app against local databroker | Connects |
| VPT-E-01 | E | Full Bench | Deploy via Ankaios on laptop, process CAN signals from ECUs via USB CAN | Signals received |

### 5.3 uprotocol-up-cpp [38.1]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| UPC-B-01 | B | Laptop | Conan + CMake (C++17) | Exit 0 |
| UPC-U-01 | U | Laptop | gtest suite | All pass |
| UPC-I-01 | I | Laptop | uEntity message serialization round-trip | Data matches |

### 5.4 chariott-chariott — Service Discovery [35.8]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| CHR-B-01 | B | Laptop | `cargo build --release` | Exit 0 |
| CHR-U-01 | U | Laptop | `cargo test` | All pass |
| CHR-I-01 | I | Laptop | Register + discover service via gRPC | Service found |
| CHR-I-02 | I | Laptop | Deploy locally, register databroker as a service, discover via gRPC | Found |

### 5.5 kuksa-kuksa-incubation [34.9]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| KIN-B-01 | B | Laptop | Build all incubation components | Exit 0 |
| KIN-U-01 | U | Laptop | Run available tests (3 files) | Pass |
| KIN-I-01 | I | Laptop | Validate against databroker | Connected |

### 5.6 kuksa-kuksa.val.services [33.9]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| KVS-B-01 | B | Laptop | Python build + proto gen | Exit 0 |
| KVS-U-01 | U | Laptop | `pytest` (6 test files) | All pass |
| KVS-I-01 | I | Laptop | HVAC service connects to databroker, set/get temp | Values match |
| KVS-I-02 | I | Laptop | Deploy HVAC service alongside databroker via Ankaios | Both running |

### 5.7 eclipse-leda-distro [32.9]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| LDD-B-01 | B | Laptop | Verify Yocto config (or pull pre-built image) | Config valid |
| LDD-I-01 | I | Laptop | Validate Leda components can run on Linux laptop | Services start |
| LDD-I-02 | I | Laptop | Verify Kanto container runtime on laptop | Containers manageable |

### 5.8 uprotocol-up-rust [32.3]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| UPR-B-01 | B | Laptop | `cargo build --release` | Exit 0 |
| UPR-U-01 | U | Laptop | `cargo test` (cucumber + mockall) | All pass |
| UPR-I-01 | I | Laptop | Send/receive UMessage between two uEntities | Delivered |

### 5.9 kuksa-kuksa-can-provider [31.8] — CRITICAL FOR BENCH

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| KCP-B-01 | B | Laptop | `pip install -e .` | Exit 0 |
| KCP-U-01 | U | Laptop | `pytest` (6 test files) | All pass |
| KCP-I-01 | I | Laptop | CAN provider reads from `vcan0`, feeds local databroker | Signals appear |
| KCP-I-02 | I | Laptop | CAN provider reads laptop USB CAN adapter, feeds real ECU frames to databroker | Signals appear |
| KCP-E-01 | E | Full Bench | TMS570 sends pedal angle on CAN → laptop USB CAN → CAN provider → databroker → test asserts | Value matches |
| KCP-E-02 | E | Full Bench | Verify CAN timing with Rigol SCPI measurement | Within spec |
| KCP-P-01 | P | Laptop | CAN frame processing rate at 500 kbps bus load | > 1000 frames/sec |

### 5.10 kuksa-kuksa.val.feeders [30.8]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| KVF-B-01 | B | Laptop | `pip install -e .` | Exit 0 |
| KVF-I-01 | I | Laptop | DBC feeder maps CAN frames to VSS, feeds databroker | Signals mapped |
| KVF-E-01 | E | Full Bench | DBC feeder on laptop maps physical ECU CAN traffic via USB CAN | VSS values correct |

### 5.11 kuksa-kuksa-common [30.0]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| KCM-B-01 | B | Laptop | `pip install -e .` | Exit 0 |
| KCM-U-01 | U | Laptop | Verify JWT token generation/validation | Valid token |

### 5.12 uprotocol-up-java [30.0]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| UPJ-B-01 | B | Laptop | `mvn package` (Java 17) | Exit 0 |
| UPJ-U-01 | U | Laptop | `mvn test` (JUnit + Mockito) | All pass |

### 5.13 velocitas-vehicle-app-cpp-template [29.3]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| VCT-B-01 | B | Laptop | Conan + CMake build | Exit 0 |
| VCT-U-01 | U | Laptop | `ctest` (2 test files) | All pass |
| VCT-I-01 | I | Laptop | Template app connects to local databroker | Connects |
| VCT-I-02 | I | Laptop | Build and run against Ankaios-deployed databroker | Runs |

### 5.14 leda-meta-leda [29.1]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| MLM-B-01 | B | Laptop | Validate Yocto layer config (bitbake parse) | No errors |
| MLM-I-01 | I | Laptop | Layer dependencies resolve | All resolved |

### 5.15 velocitas-vehicle-model-generator [27.9]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| VMG-B-01 | B | Laptop | `pip install -e .` | Exit 0 |
| VMG-U-01 | U | Laptop | `pytest` (1 test file) | Pass |
| VMG-I-01 | I | Laptop | Generate Python vehicle model from VSS 4.0 | Model importable |

### 5.16 uprotocol-up-core-api [26.7]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| UCA-B-01 | B | Laptop | `mvn package` (Java 11+) | Exit 0 |
| UCA-U-01 | U | Laptop | `mvn test` | All pass |
| UCA-I-01 | I | Laptop | Proto stubs compile for Python/C++/Rust/Java | All compile |

### 5.17 leda-leda-contrib-self-update-agent [26.5]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| LSU-B-01 | B | Laptop | CMake build (C++14) | Exit 0 |
| LSU-I-01 | I | Laptop | Deploy agent on laptop, trigger OTA update simulation via MQTT | Update reported |

### 5.18 ibeji-ibeji — Digital Twin [26.0]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| IBJ-B-01 | B | Laptop | `cargo build --release` | Exit 0 |
| IBJ-U-01 | U | Laptop | `cargo test` | All pass |
| IBJ-I-01 | I | Laptop | Create twin entity mapped to VSS signal | Twin readable |
| IBJ-I-02 | I | Laptop | Deploy Ibeji locally, connect to databroker | Twin mirrors VSS |

### 5.19 uprotocol-up-transport-zenoh-cpp [26.0]

| ID | Cat | Platform | Test | Pass Criteria |
|----|-----|----------|------|---------------|
| UTZ-B-01 | B | Laptop | Conan + CMake (zenohcpp 1.2.1) | Exit 0 |
| UTZ-U-01 | U | Laptop | gtest suite | All pass |
| UTZ-I-01 | I | Laptop | Send uProtocol message over Zenoh transport | Delivered |

---

## 6. Phase 4 — Early-Stage (Score 15-24)

Build + Unit only. All on Linux laptop.

| # | Module | Score | ID | Build Command | Unit Command | Notes |
|---|--------|-------|----|---------------|--------------|-------|
| 27 | leda-contrib-vehicle-update-manager | 24.9 | VUM | `go build` | `go test ./...` (25 files) | Go 1.17+ |
| 28 | sdv-blueprints-fleet-management | 23.7 | SFM | `docker-compose build` | `docker-compose up` (smoke) | Docker based |
| 29 | leda-leda | 22.7 | LDA | Docs/spec build | N/A | Documentation project |
| 30 | kuksa-kuksa-android-sdk | 22.3 | KAS | `./gradlew build` | `./gradlew test` | Requires Android SDK |
| 31 | uprotocol-up-transport-zenoh-rust | 22.2 | UTZR | `cargo build` | `cargo test` | |
| 32 | ankaios-ank-sdk-rust | 22.1 | ASR | `cargo build` | `cargo test` (1 file) | Also: I-01 Rust client → local Ankaios |
| 33 | chariott-Agemo | 22.1 | CAG | `cargo build` | `cargo test` | Pub/sub |
| 34 | ibeji-freyja | 22.1 | IFR | `cargo build` | `cargo test` | Cloud sync |
| 35 | leda-leda-utils | 22.1 | LLU | Build utils | N/A | Run sdv-health locally |
| 36 | leda-leda-example-applications | 21.9 | LEA | Docker build | N/A | Deploy 1 example via Ankaios |
| 37 | ibeji-ibeji-example-applications | 21.5 | IEA | `cargo build` | N/A | Run example provider |
| 38 | kuksa-kuksa-perf | 21.2 | KPF | `cargo build` | N/A | **Bench:** run vs local databroker |
| 39 | uprotocol-up-transport-mqtt5-rust | 20.2 | UTM | `cargo build` | `cargo test` | Needs MQTT broker |
| 40 | kuksa-kuksa-dds-provider | 18.2 | KDD | `pip install -e .` | `pytest` (4 files) | Needs CycloneDDS |
| 41 | kuksa-kuksa-someip-provider | 17.7 | KSP | CMake (vsomeip + Boost) | N/A | SOME/IP integration |
| 42 | kuksa-kuksa-gps-provider | 17.2 | KGP | `pip install -e .` | N/A | Mock GPS (no hw) |
| 43 | uprotocol-up-transport-vsomeip-rust | 17.0 | UTV | `cargo build` | N/A | |
| 44 | leda-contrib-cloud-connector | 15.5 | LCC | `go build` | N/A | Mock MQTT cloud |

---

## 7. Phase 5 — Incubating (Score < 15)

Build verification only. Document result as PASS/FAIL/SKIP.

| # | Module | Score | Status | Build Command | Expected |
|---|--------|-------|--------|---------------|----------|
| 45 | velocitas-vehicle-app-kotlin-template | 13.2 | Maintained | `./gradlew build` | Should build |
| 46 | sdv-blueprints-software-orchestration | 12.0 | Maintained | `docker-compose build` | Should build |
| 47 | kuksa-kuksa-hardware | 11.8 | Slowing | N/A (HW docs only) | SKIP |
| 48 | sdv-blueprints-ros-racer | 10.6 | Active | ROS2 workspace build | May fail (no ROS2) |
| 49 | velocitas-vehicle-model-python | 10.5 | Slowing | `pip install -e .` | Should build |
| 50 | sdv-blueprints-insurance | 8.0 | Slowing | `pip install -r requirements.txt` | Should build |
| 51 | sdv-blueprints-service-to-signal | 7.5 | Maintained | Docker build | Should build |
| 52 | velocitas-vehicle-model-cpp | 7.1 | Slowing | Conan + CMake | May fail |
| 53 | sdv-blueprints-companion-application | 6.5 | Maintained | Docker build | Should build |
| 54 | leda-contrib-container-update-agent | 1.5 | Stale | Verify source exists | SKIP (1 commit) |
| 55 | leda-contrib-otel | 1.5 | Stale | Verify source exists | SKIP (1 commit) |
| 56 | velocitas-vehicle-app-rust-sdk | 1.4 | Maintained | `cargo build` | May fail (1 commit) |

---

## 8. Cross-Cutting E2E Bench Scenarios

These scenarios exercise multiple modules simultaneously on the physical bench. All require Phase 1+2+3 modules passing.

### E2E-BENCH-01: CAN-to-Cloud Signal Pipeline

**Modules:** kuksa-can-provider + kuksa-databroker + kuksa-python-sdk + ankaios

```
TMS570 (CVC) ──CAN bus──► Laptop USB CAN ──► CAN Provider ──► Databroker ──► Python Client
                                     (all on Linux laptop)
```

| Step | Action | Verify |
|------|--------|--------|
| 1 | Ankaios deploys databroker + CAN provider on laptop | `ank get workloads` = Running |
| 2 | TMS570 sends pedal angle (CAN ID 0x100) | CAN frame on bus |
| 3 | CAN provider maps frame to `Vehicle.Chassis.Accelerator.PedalPosition` | Signal in databroker |
| 4 | Python client on laptop reads signal | Value matches physical pedal |
| 5 | Rigol captures CAN_H/CAN_L timing | Bit timing within 500kbps spec |

**Pass:** Signal value matches within 5%, latency < 100ms.

### E2E-BENCH-02: Vehicle App Round-Trip

**Modules:** velocitas-sdk + kuksa-databroker + kuksa-can-provider

```
F413ZH (RZC) encoder ──CAN bus──► Laptop USB CAN ──► CAN Provider ──► Databroker ──► Velocitas App
                                          (all on Linux laptop)
```

| Step | Action | Verify |
|------|--------|--------|
| 1 | RZC sends motor encoder quadrature data on CAN | Frames on bus |
| 2 | CAN provider converts to Vehicle.Speed | Signal in databroker |
| 3 | Velocitas Python app subscribes to Vehicle.Speed | Updates received |
| 4 | App computes speed from encoder rate | Physically correct |

**Pass:** Speed values within 2% of manual encoder calculation.

### E2E-BENCH-03: Orchestrated Multi-Container Deployment

**Modules:** ankaios + kuksa-databroker + kuksa-can-provider + velocitas app

| Step | Action | Verify |
|------|--------|--------|
| 1 | Single Ankaios manifest deploys entire SDV stack on laptop | All containers start |
| 2 | `ank get workloads` | All states = Running |
| 3 | Databroker gRPC health check from laptop | Healthy |
| 4 | CAN provider processing frames | Signals flowing |
| 5 | Velocitas app receiving data | Subscribes OK |

**Pass:** All 3+ containers running, signal pipeline functional within 30s of manifest apply.

### E2E-BENCH-04: Digital Twin Synchronization

**Modules:** ibeji-ibeji + kuksa-databroker + kuksa-can-provider

```
RZC NTC thermistor ──CAN──► Databroker ──► Ibeji Digital Twin ──► Twin Query API
```

| Step | Action | Verify |
|------|--------|--------|
| 1 | RZC sends battery temperature via CAN | Frame on bus |
| 2 | CAN provider maps to `Vehicle.Powertrain.Battery.Temperature` | Signal in databroker |
| 3 | Ibeji maintains digital twin of battery | Twin state updated |
| 4 | Query twin API | Temperature within 1°C of physical |

**Pass:** Digital twin reflects physical temperature within 1°C.

### E2E-BENCH-05: UDS + SDV Coexistence

**Modules:** kuksa-can-provider + hop_test.py (existing HIL tool)

| Step | Action | Verify |
|------|--------|--------|
| 1 | CAN provider running on laptop, processing signals via USB CAN | VSS signals flowing |
| 2 | `hop_test.py` sends TesterPresent (0x3E) on same CAN bus | Positive response |
| 3 | `hop_test.py` sends ReadDID (0x22) | DID value returned |
| 4 | Check VSS signal flow still active | No interruption |

**Pass:** Both VSS signal flow and UDS diagnostics work simultaneously without interference.

---

## 9. Execution Timeline

| Week | Phase | Modules | Focus | Gate Criteria |
|------|-------|---------|-------|---------------|
| **1** | Infra | — | Laptop Linux setup, USB CAN adapter, CAN bus wiring, Pi QNX boot, vcan0 | CAN echo on `can0` works |
| **2** | Phase 1 | #1 Ankaios | Build + unit + deploy container on laptop | ANK-I-02 PASS |
| **3** | Phase 2a | #2-3 Databroker, Velocitas SDK | Build + unit + databroker serving on laptop | KDB-I-03 PASS |
| **4** | Phase 2b | #4-7 CLI, uProto spec, Kuksa PY SDK, C++ SDK | Build + unit all | All B+U PASS |
| **5** | Phase 3a | #8-16 SDKs, providers, CAN provider | Integration with CAN bus | KCP-E-01 PASS |
| **6** | Phase 3b | #17-26 Feeders, Ibeji, transports | Build + unit + integration | All B PASS |
| **7** | Phase 4 | #27-44 Early-stage | Build verification only | All B attempted |
| **8** | Phase 5 | #45-56 Incubating | Build verification only | Best-effort |
| **9** | E2E | All passing | Cross-cutting bench scenarios (5 E2E tests) | E2E-BENCH-01..05 |
| **10** | Report | — | Results aggregation, gap analysis, ASPICE evidence update | Final report published |

---

## 10. Test Execution Commands

```bash
# ── Quick smoke (Phase 1 build only) ──
pytest tests/build/ -k "ank" -v --tb=short

# ── Phase 1+2 core stack ──
pytest tests/ -m "phase1 or phase2" -m "build or unit or integration" --target=qnx -v

# ── Phase 3 with CAN bus ──
pytest tests/ -m "phase3 and (build or unit or integration)" --target=qnx -v

# ── E2E bench scenarios (requires full bench powered on) ──
pytest tests/e2e/ -m "e2e and can" --target=qnx -v

# ── Performance suite ──
pytest tests/performance/ -m "perf" --target=qnx -v

# ── Security suite ──
pytest tests/security/ -m "security" --target=qnx -v

# ── Nightly full run (all phases, all categories) ──
pytest tests/ --target=qnx -v \
  --junitxml=test-results/sdv-full-$(date +%Y%m%d).xml \
  --html=test-results/sdv-full-$(date +%Y%m%d).html

# ── Single module (example: kuksa-can-provider) ──
pytest tests/ -k "KCP" --target=qnx -v
```

---

## 11. Risk Register

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|------------|------------|
| R1 | QNX on Pi not ready (SD card, BSP pending) | Pi cannot participate in CAN bus | Medium | ECUs still generate CAN traffic; laptop reads via USB CAN regardless |
| R2 | CAN bus not wired yet (pending) | Blocks KCP, KVF, E2E tests | Medium | Use `vcan0` virtual CAN for integration; defer physical CAN to week 5 |
| R3 | USB CAN adapter not recognized on Linux | Blocks CAN-based tests | Low | Install `can-utils`, verify with `candump can0`; try alternative adapter |
| R4 | Stale modules won't build (5 stale, 16 slowing) | Blocks Phase 4-5 | High | Document build failure as result; do not block other phases |
| R5 | Module interdependency failures cascade | Multiple test failures | Low | Strict layer-by-layer execution; mock missing layers |
| R6 | Laptop resource constraints (RAM/CPU) | Cannot run all containers simultaneously | Low | Limit concurrent containers; prioritize databroker + CAN provider |
| R7 | Rigol not connected (Ethernet 192.168.1.100) | Cannot verify CAN timing | Low | Skip Rigol-dependent tests; defer to manual verification |
| R8 | Android SDK not available on laptop | Cannot build Kuksa Android SDK | Medium | Mark KAS-B-01 as SKIP; no Android device on bench anyway |

---

## 12. Results Tracking

### Per-Module Results Template

| Module | B | U | I | E | P | S | Score | Notes |
|--------|---|---|---|---|---|---|-------|-------|
| ankaios-ankaios | ? | ? | ? | ? | ? | ? | 70.3 | |
| eclipse-kuksa-databroker | ? | ? | ? | ? | ? | ? | 54.5 | |
| ... | | | | | | | | |

Legend: PASS / FAIL / SKIP / N/A

### Aggregate Metrics

| Metric | Target |
|--------|--------|
| Phase 1 modules all B+U+I passing | 100% |
| Phase 2 modules all B+U passing | 100% |
| Phase 3 modules all B passing | > 90% |
| Phase 4 modules B attempted | 100% |
| Phase 5 modules B attempted | Best-effort |
| E2E bench scenarios passing | >= 3/5 |
| Total test cases executed | ~180 |
| Total test cases passing | > 70% |

---

## 13. ASPICE Evidence Mapping

Test results from this plan map to ASPICE work products:

| ASPICE Area | Evidence From This Plan |
|---|---|
| SWE.4 (Unit Verification) | All U-xx test results |
| SWE.5 (Integration Test) | All I-xx test results |
| SWE.6 (Qualification Test) | All E-xx test results |
| SYS.4 (System Integration Test) | E2E-BENCH-01..05 results |
| SYS.5 (System Qualification Test) | Final aggregate report |
| SUP.1 (Quality Assurance) | Build verification (B-xx) for all modules |

Results will be placed in each module's respective `aspice/` folder upon completion.
