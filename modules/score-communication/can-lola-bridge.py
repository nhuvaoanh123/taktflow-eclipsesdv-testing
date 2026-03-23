#!/usr/bin/env python3
"""
CAN → LoLa Integration Bridge

Reads live CAN frames from vcan0 (taktflow SIL vECUs), decodes them,
and writes decoded signals to a POSIX shared memory segment that can
be read by any process on the laptop — including LoLa proxies.

This demonstrates the integration pattern:
  vcan0 (taktflow vECUs) → Python decoder → shared memory → any consumer

The shared memory segment uses a simple binary format that's compatible
with mmap-based readers (C++, Python, Rust).

Usage:
    python3 scripts/can-lola-bridge.py --interface vcan0

    # In another terminal, read the signals:
    python3 scripts/can-lola-bridge.py --read
"""

import argparse
import mmap
import os
import struct
import sys
import time

try:
    import can
except ImportError:
    print("Install python-can: pip install python-can")
    sys.exit(1)

# Shared memory file path (POSIX-compatible)
SHM_PATH = "/dev/shm/taktflow_lola_bridge"
SHM_SIZE = 4096

# Signal layout in shared memory (fixed offsets for zero-copy access)
# Offset | Size | Type    | Signal
# 0      | 8    | uint64  | timestamp_ns (monotonic clock)
# 8      | 4    | uint32  | frame_count
# 12     | 4    | float32 | pedal_position_pct
# 16     | 4    | float32 | vehicle_speed_kph
# 20     | 4    | float32 | motor_rpm
# 24     | 4    | float32 | motor_current_a
# 28     | 4    | float32 | motor_temp_c
# 32     | 4    | float32 | battery_temp_c
# 36     | 4    | float32 | steering_angle_deg
# 40     | 4    | uint32  | lidar_distance_cm
# 44     | 4    | uint32  | heartbeat_counter
# 48     | 1    | uint8   | vehicle_state (0=INIT, 1=SAFE, 2=RUN)
# 49     | 1    | uint8   | alive_counter
# 50     | 2    | uint16  | reserved
# 52     | 4    | uint32  | error_count

SHM_FORMAT = "<QI ff ffff fI IB B HI"
SHM_STRUCT_SIZE = struct.calcsize(SHM_FORMAT)

# CAN ID → decoder mapping (matches taktflow-embedded DBC + SIL vECUs)
# The SIL vECUs send on these IDs:
KNOWN_IDS = {
    0x100: "CVC_VehicleState",
    0x101: "CVC_PedalCommand",
    0x200: "RZC_MotorStatus",
    0x201: "RZC_Temperature",
    0x220: "SIL_Combined",       # SIL combined message
    0x300: "FZC_SteeringAngle",
    0x301: "FZC_LidarDistance",
    0x400: "HSM_Heartbeat",
    0x600: "UDS_Request",
    0x601: "UDS_Response",
}


class SignalState:
    """Current state of all decoded vehicle signals."""

    def __init__(self):
        self.timestamp_ns = 0
        self.frame_count = 0
        self.pedal_pct = 0.0
        self.speed_kph = 0.0
        self.motor_rpm = 0.0
        self.motor_current = 0.0
        self.motor_temp = 25.0
        self.battery_temp = 22.0
        self.steering_deg = 0.0
        self.lidar_cm = 0
        self.heartbeat = 0
        self.vehicle_state = 0
        self.alive = 0
        self.error_count = 0

    def pack(self) -> bytes:
        return struct.pack(
            SHM_FORMAT,
            self.timestamp_ns,
            self.frame_count,
            self.pedal_pct,
            self.speed_kph,
            self.motor_rpm,
            self.motor_current,
            self.motor_temp,
            self.battery_temp,
            self.steering_deg,
            self.lidar_cm,
            self.heartbeat,
            self.vehicle_state,
            self.alive,
            0,  # reserved
            self.error_count,
        )

    @classmethod
    def unpack(cls, data: bytes) -> "SignalState":
        s = cls()
        vals = struct.unpack(SHM_FORMAT, data[:SHM_STRUCT_SIZE])
        (s.timestamp_ns, s.frame_count, s.pedal_pct, s.speed_kph,
         s.motor_rpm, s.motor_current, s.motor_temp, s.battery_temp,
         s.steering_deg, s.lidar_cm, s.heartbeat, s.vehicle_state,
         s.alive, _, s.error_count) = vals
        return s

    def decode_frame(self, msg: can.Message):
        """Decode a CAN frame and update signal state."""
        self.frame_count += 1
        self.timestamp_ns = int(time.monotonic_ns())
        data = msg.data

        if msg.arbitration_id == 0x100 and len(data) >= 6:
            # CVC Vehicle State
            pedal_raw, speed_raw, alive, state = struct.unpack_from("<HHBBxx", data)
            self.pedal_pct = pedal_raw / 100.0
            self.speed_kph = speed_raw / 100.0
            self.alive = alive
            self.vehicle_state = state

        elif msg.arbitration_id == 0x200 and len(data) >= 5:
            # RZC Motor Status
            rpm, current_raw, alive = struct.unpack_from("<HHBxxx", data)
            self.motor_rpm = float(rpm)
            self.motor_current = current_raw / 1000.0
            self.alive = alive

        elif msg.arbitration_id == 0x201 and len(data) >= 4:
            # RZC Temperature
            motor_raw, battery_raw = struct.unpack_from("<hhxxxx", data)
            self.motor_temp = motor_raw / 10.0
            self.battery_temp = battery_raw / 10.0

        elif msg.arbitration_id == 0x220 and len(data) >= 8:
            # SIL Combined message (from taktflow SIL vECUs)
            # Decode based on your SIL format
            self.motor_rpm = struct.unpack_from("<H", data, 0)[0]
            self.motor_current = struct.unpack_from("<H", data, 2)[0] / 1000.0

        elif msg.arbitration_id == 0x300 and len(data) >= 3:
            # FZC Steering
            angle_raw, alive = struct.unpack_from("<hBxxxxx", data)
            self.steering_deg = angle_raw / 10.0
            self.alive = alive

        elif msg.arbitration_id == 0x301 and len(data) >= 2:
            # FZC LiDAR
            self.lidar_cm = struct.unpack_from("<Hxxxxxx", data)[0]

        elif msg.arbitration_id == 0x400 and len(data) >= 4:
            # HSM Heartbeat
            self.heartbeat = struct.unpack_from("<Ixxxx", data)[0]


def create_shm():
    """Create or open the shared memory segment."""
    with open(SHM_PATH, "wb") as f:
        f.write(b"\x00" * SHM_SIZE)
    fd = os.open(SHM_PATH, os.O_RDWR)
    mm = mmap.mmap(fd, SHM_SIZE)
    os.close(fd)
    return mm


def open_shm_readonly():
    """Open shared memory for reading."""
    fd = os.open(SHM_PATH, os.O_RDONLY)
    mm = mmap.mmap(fd, SHM_SIZE, access=mmap.ACCESS_READ)
    os.close(fd)
    return mm


def run_bridge(interface: str):
    """Main bridge loop: CAN → shared memory."""
    bus = can.interface.Bus(channel=interface, interface="socketcan")
    mm = create_shm()
    state = SignalState()

    print(f"CAN→LoLa bridge started: {interface} → {SHM_PATH}")
    print(f"Shared memory: {SHM_STRUCT_SIZE} bytes signal struct")
    print(f"Reading CAN frames... (Ctrl+C to stop)")
    print()

    last_print = 0
    try:
        while True:
            msg = bus.recv(timeout=1.0)
            if msg is None:
                continue

            state.decode_frame(msg)

            # Write to shared memory (atomic-ish — single struct write)
            mm.seek(0)
            mm.write(state.pack())

            # Print status every second
            now = time.time()
            if now - last_print >= 1.0:
                last_print = now
                name = KNOWN_IDS.get(msg.arbitration_id, f"0x{msg.arbitration_id:03X}")
                print(
                    f"[{state.frame_count:6d} frames] "
                    f"pedal={state.pedal_pct:5.1f}% "
                    f"speed={state.speed_kph:5.1f}kph "
                    f"rpm={state.motor_rpm:6.0f} "
                    f"I={state.motor_current:5.2f}A "
                    f"Tmotor={state.motor_temp:5.1f}°C "
                    f"Tbatt={state.battery_temp:5.1f}°C "
                    f"steer={state.steering_deg:6.1f}° "
                    f"lidar={state.lidar_cm:4d}cm "
                    f"last={name}"
                )

    except KeyboardInterrupt:
        print(f"\nBridge stopped. {state.frame_count} frames processed.")
    finally:
        mm.close()
        bus.shutdown()


def run_reader():
    """Read and display signals from shared memory (consumer side)."""
    if not os.path.exists(SHM_PATH):
        print(f"Shared memory {SHM_PATH} not found. Start the bridge first.")
        sys.exit(1)

    mm = open_shm_readonly()
    print(f"Reading signals from {SHM_PATH}... (Ctrl+C to stop)")
    print()

    try:
        while True:
            mm.seek(0)
            data = mm.read(SHM_STRUCT_SIZE)
            state = SignalState.unpack(data)

            if state.frame_count == 0:
                print("Waiting for data...", end="\r")
            else:
                age_ms = (time.monotonic_ns() - state.timestamp_ns) / 1e6
                print(
                    f"[frame {state.frame_count:6d} age={age_ms:5.1f}ms] "
                    f"pedal={state.pedal_pct:5.1f}% "
                    f"speed={state.speed_kph:5.1f}kph "
                    f"rpm={state.motor_rpm:6.0f} "
                    f"steer={state.steering_deg:6.1f}° "
                    f"Tmotor={state.motor_temp:5.1f}°C "
                    f"state={'INIT' if state.vehicle_state == 0 else 'SAFE' if state.vehicle_state == 1 else 'RUN'}"
                )

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nReader stopped.")
    finally:
        mm.close()


def main():
    parser = argparse.ArgumentParser(description="CAN → LoLa Shared Memory Bridge")
    parser.add_argument("--interface", "-i", default="vcan0", help="CAN interface")
    parser.add_argument("--read", "-r", action="store_true", help="Read mode (consumer)")
    args = parser.parse_args()

    if args.read:
        run_reader()
    else:
        run_bridge(args.interface)


if __name__ == "__main__":
    main()
