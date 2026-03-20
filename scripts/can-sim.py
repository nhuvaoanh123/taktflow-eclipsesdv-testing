#!/usr/bin/env python3
"""
CAN Bus Simulator — sends vehicle signals on vcan0 for LoLa integration testing.

Simulates the ECU CAN traffic that would come from the bench:
- TMS570 (CVC): Pedal position, vehicle state (CAN ID 0x100-0x10F)
- F413ZH (RZC): Motor speed, current, temperature (CAN ID 0x200-0x20F)
- G474RE (FZC): Steering angle, LiDAR distance (CAN ID 0x300-0x30F)
- L552ZE (HSM): Heartbeat (CAN ID 0x400)

Usage:
    # Setup vcan0 (if not already up)
    sudo modprobe vcan
    sudo ip link add dev vcan0 type vcan
    sudo ip link set up vcan0

    # Run simulator
    python3 scripts/can-sim.py --interface vcan0 --rate 100

    # Or with real CAN
    python3 scripts/can-sim.py --interface can0 --rate 100
"""

import argparse
import math
import struct
import time
import sys

try:
    import can
except ImportError:
    print("Install python-can: pip install python-can")
    sys.exit(1)


# CAN IDs matching taktflow-embedded DBC
CAN_IDS = {
    "CVC_VehicleState":  0x100,  # TMS570: vehicle state, pedal pos
    "CVC_PedalCommand":  0x101,  # TMS570: pedal command from ADAS
    "RZC_MotorStatus":   0x200,  # F413ZH: motor speed, current
    "RZC_Temperature":   0x201,  # F413ZH: motor + battery temps
    "FZC_SteeringAngle": 0x300,  # G474RE: steering angle feedback
    "FZC_LidarDistance": 0x301,  # G474RE: obstacle distance
    "HSM_Heartbeat":     0x400,  # L552ZE: alive counter
}


def pack_vehicle_state(pedal_pct: float, speed_kph: float, alive: int) -> bytes:
    """Pack CVC vehicle state: pedal% (u16), speed (u16), alive (u8), state (u8)."""
    pedal_raw = int(pedal_pct * 100)  # 0-10000 = 0-100.00%
    speed_raw = int(speed_kph * 100)  # 0-25500 = 0-255.00 km/h
    state = 0x02  # RUN
    return struct.pack("<HHBBxx", pedal_raw, speed_raw, alive & 0xFF, state)


def pack_motor_status(rpm: float, current_a: float, alive: int) -> bytes:
    """Pack RZC motor status: RPM (u16), current mA (u16), alive (u8)."""
    rpm_raw = int(rpm)
    current_raw = int(current_a * 1000)
    return struct.pack("<HHBxxx", rpm_raw, current_raw, alive & 0xFF)


def pack_temperature(motor_c: float, battery_c: float) -> bytes:
    """Pack RZC temperatures: motor (i16 * 10), battery (i16 * 10)."""
    motor_raw = int(motor_c * 10)
    battery_raw = int(battery_c * 10)
    return struct.pack("<hhxxxx", motor_raw, battery_raw)


def pack_steering(angle_deg: float, alive: int) -> bytes:
    """Pack FZC steering angle: angle (i16 * 10), alive (u8)."""
    angle_raw = int(angle_deg * 10)
    return struct.pack("<hBxxxxx", angle_raw, alive & 0xFF)


def pack_lidar(distance_cm: int) -> bytes:
    """Pack FZC LiDAR distance: distance cm (u16)."""
    return struct.pack("<Hxxxxxx", distance_cm)


def pack_heartbeat(counter: int) -> bytes:
    """Pack HSM heartbeat: counter (u32)."""
    return struct.pack("<Ixxxx", counter & 0xFFFFFFFF)


def main():
    parser = argparse.ArgumentParser(description="CAN Bus Simulator for LoLa bench testing")
    parser.add_argument("--interface", "-i", default="vcan0", help="CAN interface (default: vcan0)")
    parser.add_argument("--rate", "-r", type=int, default=100, help="Send rate in ms (default: 100)")
    parser.add_argument("--duration", "-d", type=int, default=0, help="Duration in seconds (0=infinite)")
    args = parser.parse_args()

    bus = can.interface.Bus(channel=args.interface, interface="socketcan")
    print(f"CAN simulator started on {args.interface} @ {args.rate}ms cycle")
    print(f"Sending: VehicleState(0x100), MotorStatus(0x200), Temperature(0x201), "
          f"Steering(0x300), LiDAR(0x301), Heartbeat(0x400)")

    cycle = 0
    start = time.time()

    try:
        while True:
            t = cycle * args.rate / 1000.0

            # Simulate pedal ramp (0→50% over 10s, then hold)
            pedal = min(50.0, t * 5.0)
            speed = pedal * 0.6  # Simple model: speed proportional to pedal
            rpm = speed * 30  # ~30 RPM per km/h
            current = pedal * 0.1  # ~0.1A per % pedal
            motor_temp = 25.0 + t * 0.5  # Slow warmup
            battery_temp = 22.0 + t * 0.3
            steering = 15.0 * math.sin(t * 0.5)  # Gentle steering oscillation
            lidar = max(30, int(500 - t * 10))  # Approaching object

            msgs = [
                can.Message(arbitration_id=CAN_IDS["CVC_VehicleState"],
                            data=pack_vehicle_state(pedal, speed, cycle), is_extended_id=False),
                can.Message(arbitration_id=CAN_IDS["RZC_MotorStatus"],
                            data=pack_motor_status(rpm, current, cycle), is_extended_id=False),
                can.Message(arbitration_id=CAN_IDS["RZC_Temperature"],
                            data=pack_temperature(motor_temp, battery_temp), is_extended_id=False),
                can.Message(arbitration_id=CAN_IDS["FZC_SteeringAngle"],
                            data=pack_steering(steering, cycle), is_extended_id=False),
                can.Message(arbitration_id=CAN_IDS["FZC_LidarDistance"],
                            data=pack_lidar(lidar), is_extended_id=False),
                can.Message(arbitration_id=CAN_IDS["HSM_Heartbeat"],
                            data=pack_heartbeat(cycle), is_extended_id=False),
            ]

            for msg in msgs:
                bus.send(msg)

            if cycle % 10 == 0:
                print(f"[{t:.1f}s] pedal={pedal:.1f}% speed={speed:.1f}kph rpm={rpm:.0f} "
                      f"temp={motor_temp:.1f}°C steer={steering:.1f}° lidar={lidar}cm")

            cycle += 1
            if args.duration > 0 and (time.time() - start) >= args.duration:
                break

            time.sleep(args.rate / 1000.0)

    except KeyboardInterrupt:
        print(f"\nStopped after {cycle} cycles ({time.time() - start:.1f}s)")
    finally:
        bus.shutdown()


if __name__ == "__main__":
    main()
