# taktflow-eclipsesdv-testing

Eclipse SDV testing framework for Taktflow Systems — targeting QNX-based Raspberry Pi platform.

## Overview

This project provides integration and validation testing using the [Eclipse SDV](https://sdv.eclipse.org/) ecosystem, including:

- **Eclipse Velocitas** — Vehicle app development and testing
- **Eclipse Kuksa** — Vehicle data broker (KUKSA.val) integration tests
- **Eclipse Leda** — Deployment and container runtime validation on QNX
- **Eclipse SommR** — Service-oriented middleware testing

## Project Structure

```
taktflow-eclipsesdv-testing/
├── config/              # Test and environment configuration
├── tests/
│   ├── integration/     # Cross-component integration tests
│   ├── e2e/             # End-to-end vehicle signal flow tests
│   └── platform/        # QNX platform-specific tests
├── fixtures/            # Test data and mock vehicle signals
├── scripts/             # CI/CD and test runner scripts
└── docs/                # Test plans and architecture
```

## Target Platform

- **OS:** QNX on Raspberry Pi
- **Runtime:** Container-based (Eclipse Leda / Kanto)
- **Data Broker:** KUKSA.val databroker
- **Vehicle Model:** VSS (Vehicle Signal Specification)

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run platform-specific tests (requires QNX target)
pytest tests/platform/ -v --target=qnx
```

## License

MIT
