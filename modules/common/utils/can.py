"""CAN bus utilities for bench testing."""

import struct
import subprocess


def can_send(interface, can_id, data_hex):
    """Send a CAN frame via cansend."""
    cmd = f"cansend {interface} {can_id:03X}#{data_hex}"
    return subprocess.run(cmd, shell=True, capture_output=True, timeout=5)


def can_interface_up(interface):
    """Check if a CAN interface is UP."""
    result = subprocess.run(
        f"ip link show {interface}", shell=True,
        capture_output=True, text=True, timeout=5,
    )
    return result.returncode == 0 and "UP" in result.stdout


def encode_lidar_frame(distance_cm, alive=0, data_id=5):
    """Encode a Lidar_Distance frame per taktflow_vehicle.dbc (0x220)."""
    byte0 = (data_id & 0x0F) | ((alive & 0x0F) << 4)
    crc = 0  # simplified — real E2E CRC would go here
    return struct.pack("<BBHxxxx", byte0, crc, distance_cm)


def encode_rzc_virtual_sensors(current_mA, temp_dC, batt_mV, rpm):
    """Encode RZC_Virtual_Sensors per taktflow_sil.dbc (0x601)."""
    return struct.pack("<HHHH", current_mA, temp_dC, batt_mV, rpm)


def decode_heartbeat(data):
    """Decode CVC/FZC Heartbeat per taktflow_vehicle.dbc."""
    data_id = data[0] & 0x0F
    alive = (data[0] >> 4) & 0x0F
    crc = data[1]
    ecu_id = data[2] if len(data) > 2 else 0
    op_mode = data[3] & 0x0F if len(data) > 3 else 0
    fault = (data[3] >> 4) & 0x0F if len(data) > 3 else 0
    modes = {0: "INIT", 1: "SAFE_STOP", 2: "RUN", 3: "DEGRADED", 4: "SAFE_STATE"}
    return {
        "data_id": data_id, "alive": alive, "crc": crc,
        "ecu_id": ecu_id, "mode": modes.get(op_mode, str(op_mode)),
        "fault": fault,
    }
