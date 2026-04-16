"""Root conftest.py for the active `modules/` test harness.

Active hierarchy:
    modules/
    ├── {module}/             Per-module wrapper directories
    │   ├── build/            Build verification
    │   ├── unit/             Upstream test wrappers
    │   ├── integration/      Cross-module tests
    │   ├── e2e/              End-to-end bench tests
    │   ├── performance/      Latency/throughput benchmarks
    │   ├── security/         Security validation
    │   └── regression/       Known-input regression tests
    ├── common/               Shared utilities
    │   ├── fixtures/         Reusable test data
    │   └── utils/            Helper functions
    └── bench/                Physical bench tests
        ├── can/              CAN bus tests
        ├── qnx/              Historical target tests
        └── hil/              Hardware-in-the-loop

Legacy note:
    A separate `tests/` tree still exists in the workspace for older or
    auxiliary scenarios, but the root `pytest.ini` currently points at
    `modules/`.

Usage:
    pytest modules/score-communication -v
    pytest modules -m build
    pytest modules -m "can and not slow"
    pytest modules --module score-communication
"""

from pathlib import Path
import subprocess

import pytest
import yaml


PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "test_config.yaml"


@pytest.fixture(scope="session")
def project_root():
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def test_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def kuksa_config(test_config):
    return test_config.get("kuksa", {})


@pytest.fixture(scope="session")
def target_config(test_config):
    return test_config.get("target", {})


@pytest.fixture(scope="session")
def score_config(test_config):
    return test_config.get("score", {})


@pytest.fixture(scope="session")
def target_platform(request):
    return request.config.getoption("--target")


@pytest.fixture(scope="session")
def can_interface(request):
    return request.config.getoption("--can")


@pytest.fixture(scope="session")
def pi_host():
    return "<pi-ip>"


def run_cmd(cmd, cwd=None, timeout=120):
    """Run a shell command and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd or PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def module_dir(module_name):
    """Get the submodule directory for a given module."""
    return PROJECT_ROOT / module_name


def pytest_addoption(parser):
    parser.addoption(
        "--target",
        action="store",
        default="local",
        help="Target platform: local, qnx, or bench",
    )
    parser.addoption(
        "--can",
        action="store",
        default="vcan0",
        help="CAN interface: vcan0 or can0",
    )
    parser.addoption(
        "--module",
        action="store",
        default=None,
        help="Filter to specific module",
    )


def pytest_configure(config):
    # Test level markers
    for marker, desc in [
        ("build", "Build verification tests"),
        ("unit", "Upstream unit test execution"),
        ("integration", "Cross-module integration tests"),
        ("e2e", "End-to-end bench tests"),
        ("performance", "Latency/throughput benchmarks"),
        ("security", "Security validation tests"),
        ("regression", "Regression tests with known inputs"),
        # Platform markers
        ("qnx", "Requires QNX target"),
        ("can", "Requires CAN bus hardware"),
        ("bench", "Requires full bench (ECUs powered)"),
        ("slow", "Takes >60s to run"),
        # Module markers
        ("score_communication", "LoLa IPC module"),
        ("score_baselibs", "S-CORE base libraries"),
        ("score_persistency", "S-CORE key-value storage"),
        ("score_lifecycle", "S-CORE lifecycle/health monitor"),
        ("score_feo", "S-CORE fixed execution order"),
        ("kuksa", "Eclipse Kuksa modules"),
        ("velocitas", "Eclipse Velocitas modules"),
        ("ankaios", "Eclipse Ankaios orchestrator"),
        ("score_logging", "S-CORE DLT logging middleware"),
        ("score_orchestrator", "S-CORE fixed execution orchestrator"),
        ("score_baselibs_rust", "S-CORE Rust foundation libraries"),
        ("score_kyron", "S-CORE Rust runtime scheduler"),
        ("score_config_management", "S-CORE configuration middleware"),
        ("score_scrample", "S-CORE middleware component"),
        ("uprotocol", "Eclipse uProtocol transport modules"),
        # ASIL markers
        ("asil_b", "ASIL B safety-critical test - ISO 26262 Part 6"),
        ("asil_d", "ASIL D safety-critical test - ISO 26262 Part 6"),
    ]:
        config.addinivalue_line("markers", f"{marker}: {desc}")
