"""Known CAN frames with expected decoded values for regression testing.

Source: taktflow_sil.dbc + taktflow_vehicle.dbc
Verified: 2026-03-20 via Python manual decode against live SIL traffic.
"""

# SIL frames (vcan0, from can_gateway.main / plant simulator)

SIL_LIDAR_500CM = {
    "can_id": 0x220,
    "data_hex": "3500F401000000000",
    "dbc": "taktflow_vehicle.dbc",
    "message": "Lidar_Distance",
    "expected": {
        "lidar_distance_cm": 500,
        "e2e_alive": 3,
        "e2e_data_id": 5,
    },
}

SIL_RZC_IDLE = {
    "can_id": 0x601,
    "data_hex": "0000FA003831000000",
    "dbc": "taktflow_sil.dbc",
    "message": "RZC_Virtual_Sensors",
    "expected": {
        "motor_current_mA": 0,
        "motor_temp_dC": 250,  # = 25.0°C
        "batt_voltage_mV": 12600,
        "motor_rpm": 0,
    },
}

SIL_FZC_NEUTRAL = {
    "can_id": 0x600,
    "data_hex": "FF1F000000000000",
    "dbc": "taktflow_sil.dbc",
    "message": "FZC_Virtual_Sensors",
    "expected": {
        "steer_angle_raw": 8191,  # = 0 degrees (midpoint)
        "brake_pos_adc": 0,
    },
}

# Real ECU frames (can0, from physical STM32/TMS570)

REAL_CVC_HEARTBEAT_INIT = {
    "can_id": 0x010,
    "data_hex": "A26D010000000000",
    "dbc": "taktflow_vehicle.dbc",
    "message": "CVC_Heartbeat",
    "expected": {
        "e2e_data_id": 2,
        "e2e_alive": 10,
        "ecu_id": 1,
        "operating_mode": 0,  # INIT
        "fault_status": 0,
    },
}

REAL_FZC_HEARTBEAT_INIT = {
    "can_id": 0x011,
    "data_hex": "F397020000000000",
    "dbc": "taktflow_vehicle.dbc",
    "message": "FZC_Heartbeat",
    "expected": {
        "e2e_data_id": 3,
        "e2e_alive": 15,
        "ecu_id": 2,
        "operating_mode": 0,  # INIT
        "fault_status": 0,
    },
}

REAL_BRAKE_RELEASED = {
    "can_id": 0x211,
    "data_hex": "9C96000000000000",
    "dbc": "taktflow_vehicle.dbc",
    "message": "Brake_Status",
    "expected": {
        "brake_position_pct": 0,
        "brake_cmd_echo_pct": 0,
        "servo_current_mA": 0,
    },
}

REAL_STEERING_NEUTRAL = {
    "can_id": 0x210,
    "data_hex": "BBC5000000000000",
    "dbc": "taktflow_vehicle.dbc",
    "message": "Steering_Command",
    "expected": {
        "steering_angle_deg": 0,
    },
}

# Edge cases for security/fuzz testing

EDGE_EMPTY_FRAME = {
    "can_id": 0x220,
    "data_hex": "",
    "dlc": 0,
    "expected": "no crash, signal unchanged",
}

EDGE_SHORT_FRAME = {
    "can_id": 0x601,
    "data_hex": "FF",
    "dlc": 1,
    "expected": "no crash, signal unchanged",
}

EDGE_MAX_VALUES = {
    "can_id": 0x601,
    "data_hex": "FFFFFFFFFFFFFFFF",
    "dlc": 8,
    "expected": {
        "motor_current_mA": 65535,
        "motor_temp_dC": 65535,
        "batt_voltage_mV": 65535,
        "motor_rpm": 65535,
    },
}

# All known frames for iteration
ALL_SIL_FRAMES = [SIL_LIDAR_500CM, SIL_RZC_IDLE, SIL_FZC_NEUTRAL]
ALL_REAL_FRAMES = [REAL_CVC_HEARTBEAT_INIT, REAL_FZC_HEARTBEAT_INIT,
                   REAL_BRAKE_RELEASED, REAL_STEERING_NEUTRAL]
ALL_EDGE_FRAMES = [EDGE_EMPTY_FRAME, EDGE_SHORT_FRAME, EDGE_MAX_VALUES]
