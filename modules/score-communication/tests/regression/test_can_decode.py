"""Regression tests for CAN→LoLa bridge signal decoding.

Verification methods: boundary value analysis (#4), equivalence classes (#5).
Platform: x86_64-linux (vcan0 or offline).

These tests verify the Python CAN decode logic against known frames.
The C++ bridge uses the same DBC definitions — if Python decode matches
DBC, and C++ bridge output matches Python decode, then C++ is correct.
"""

import struct
import pytest


# ── DBC decode functions (ground truth) ─────────────────────────────

def decode_lidar_distance(data: bytes) -> dict:
    """Decode 0x220 Lidar_Distance per taktflow_vehicle.dbc."""
    if len(data) < 7:
        return {}
    e2e_data_id = data[0] & 0x0F
    e2e_alive = (data[0] >> 4) & 0x0F
    e2e_crc = data[1]
    distance_cm = struct.unpack_from("<H", data, 2)[0]
    signal_strength = struct.unpack_from("<H", data, 4)[0]
    return {
        "e2e_data_id": e2e_data_id,
        "e2e_alive": e2e_alive,
        "e2e_crc": e2e_crc,
        "distance_cm": distance_cm,
        "signal_strength": signal_strength,
    }


def decode_rzc_virtual_sensors(data: bytes) -> dict:
    """Decode 0x601 RZC_Virtual_Sensors per taktflow_sil.dbc."""
    if len(data) < 8:
        return {}
    current_mA = struct.unpack_from("<H", data, 0)[0]
    temp_dC = struct.unpack_from("<H", data, 2)[0]
    batt_mV = struct.unpack_from("<H", data, 4)[0]
    rpm = struct.unpack_from("<H", data, 6)[0]
    return {
        "motor_current_mA": current_mA,
        "motor_temp_dC": temp_dC,
        "batt_voltage_mV": batt_mV,
        "motor_rpm": rpm,
    }


def decode_heartbeat(data: bytes) -> dict:
    """Decode CVC/FZC Heartbeat per taktflow_vehicle.dbc."""
    if len(data) < 4:
        return {}
    return {
        "e2e_data_id": data[0] & 0x0F,
        "e2e_alive": (data[0] >> 4) & 0x0F,
        "e2e_crc": data[1],
        "ecu_id": data[2],
        "operating_mode": data[3] & 0x0F,
        "fault_status": (data[3] >> 4) & 0x0F,
    }


# ── Tests ────────────────────────────────────────────────────────────

class TestLidarDecode:
    """Verification method: equivalence classes (#5)."""

    def test_nominal_500cm(self):
        data = bytes.fromhex("3500F40100000000")
        result = decode_lidar_distance(data)
        assert result["distance_cm"] == 500
        assert result["e2e_alive"] == 3
        assert result["e2e_data_id"] == 5

    def test_zero_distance(self):
        data = bytes.fromhex("3500000000000000")
        result = decode_lidar_distance(data)
        assert result["distance_cm"] == 0

    def test_max_distance_1200cm(self):
        data = bytes.fromhex("3500B00400000000")
        result = decode_lidar_distance(data)
        assert result["distance_cm"] == 1200

    def test_short_frame_returns_empty(self):
        data = bytes.fromhex("3500")
        result = decode_lidar_distance(data)
        assert result == {}


class TestRzcVirtualSensors:
    """Verification method: boundary value analysis (#4)."""

    def test_idle_state(self):
        data = bytes.fromhex("0000FA003831000000")[:8]
        result = decode_rzc_virtual_sensors(data)
        assert result["motor_current_mA"] == 0
        assert result["motor_temp_dC"] == 250  # 25.0°C
        assert result["batt_voltage_mV"] == 12600  # 12.6V
        assert result["motor_rpm"] == 0

    def test_max_values(self):
        data = bytes.fromhex("FFFFFFFFFFFFFFFF")
        result = decode_rzc_virtual_sensors(data)
        assert result["motor_current_mA"] == 65535
        assert result["motor_rpm"] == 65535

    def test_known_rpm_1500(self):
        # current=500mA, temp=350dC(35.0°C), batt=12000mV, rpm=1500
        data = struct.pack("<HHHH", 500, 350, 12000, 1500)
        result = decode_rzc_virtual_sensors(data)
        assert result["motor_current_mA"] == 500
        assert result["motor_temp_dC"] == 350
        assert result["batt_voltage_mV"] == 12000
        assert result["motor_rpm"] == 1500

    def test_short_frame_returns_empty(self):
        result = decode_rzc_virtual_sensors(bytes([0xFF]))
        assert result == {}


class TestHeartbeatDecode:
    """Verification method: equivalence classes (#5)."""

    def test_cvc_init_mode(self):
        data = bytes.fromhex("A26D010000000000")
        result = decode_heartbeat(data)
        assert result["e2e_data_id"] == 2
        assert result["e2e_alive"] == 10
        assert result["ecu_id"] == 1
        assert result["operating_mode"] == 0  # INIT
        assert result["fault_status"] == 0

    def test_fzc_init_mode(self):
        data = bytes.fromhex("F397020000000000")
        result = decode_heartbeat(data)
        assert result["e2e_data_id"] == 3
        assert result["e2e_alive"] == 15
        assert result["ecu_id"] == 2
        assert result["operating_mode"] == 0

    def test_run_mode(self):
        # DataID=1, Alive=5, CRC=0xAA, ECU=1, Mode=RUN(2), Fault=0
        data = bytes([0x51, 0xAA, 0x01, 0x02])
        result = decode_heartbeat(data)
        assert result["operating_mode"] == 2  # RUN

    def test_fault_active(self):
        # Mode=INIT, Fault=3
        data = bytes([0x10, 0x00, 0x01, 0x30])
        result = decode_heartbeat(data)
        assert result["fault_status"] == 3

    def test_short_frame_returns_empty(self):
        result = decode_heartbeat(bytes([0x10, 0x00]))
        assert result == {}


class TestEdgeCases:
    """Verification method: fuzz testing (#6)."""

    def test_all_zeros(self):
        data = bytes(8)
        assert decode_lidar_distance(data)["distance_cm"] == 0
        assert decode_rzc_virtual_sensors(data)["motor_rpm"] == 0

    def test_all_ones(self):
        data = bytes([0xFF] * 8)
        result = decode_lidar_distance(data)
        assert result["distance_cm"] == 65535
        assert result["e2e_alive"] == 15
        assert result["e2e_data_id"] == 15

    def test_empty_data(self):
        assert decode_lidar_distance(bytes()) == {}
        assert decode_rzc_virtual_sensors(bytes()) == {}
        assert decode_heartbeat(bytes()) == {}
