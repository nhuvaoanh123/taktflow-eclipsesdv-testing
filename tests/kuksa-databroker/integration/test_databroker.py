"""Integration tests for KUKSA.val databroker connectivity and VSS signal access."""

import pytest


class TestKuksaDatabrokerConnection:
    """Verify databroker is reachable and serving VSS signals."""

    def test_databroker_reachable(self, kuksa_config):
        """Databroker gRPC endpoint should be reachable."""
        host = kuksa_config["databroker_host"]
        port = kuksa_config["databroker_port"]
        # TODO: Implement gRPC health check
        assert host is not None
        assert port == 55555

    def test_vss_metadata_available(self, test_config):
        """VSS metadata for configured signals should be queryable."""
        signals = test_config["vss"]["signals"]
        assert len(signals) > 0
        # TODO: Query databroker for metadata of each signal

    @pytest.mark.parametrize("signal", [
        "Vehicle.Speed",
        "Vehicle.Powertrain.Battery.StateOfCharge.Current",
        "Vehicle.Powertrain.Battery.Temperature",
    ])
    def test_signal_subscription(self, signal, kuksa_config):
        """Should be able to subscribe to VSS signals."""
        # TODO: Subscribe to signal via gRPC and verify response
        assert signal.startswith("Vehicle.")
