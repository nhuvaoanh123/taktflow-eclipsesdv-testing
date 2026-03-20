import pytest
import yaml
from pathlib import Path


@pytest.fixture(scope="session")
def test_config():
    config_path = Path(__file__).parent.parent / "config" / "test_config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def kuksa_config(test_config):
    return test_config["kuksa"]


@pytest.fixture(scope="session")
def target_config(test_config):
    return test_config["target"]


def pytest_addoption(parser):
    parser.addoption(
        "--target",
        action="store",
        default="local",
        help="Target platform: local or qnx",
    )


@pytest.fixture(scope="session")
def target_platform(request):
    return request.config.getoption("--target")
