// Copyright (c) 2026 Taktflow Systems — SPDX-License-Identifier: Apache-2.0
//
// CAN-to-LoLa Bridge v2: Correct DBC decoding from taktflow_vehicle.dbc + taktflow_sil.dbc
//
// Real CAN IDs on vcan0 from SIL:
//   0x220 (544)  = Lidar_Distance (FZC) — E2E + distance_cm + signal_strength
//   0x600 (1536) = FZC_Virtual_Sensors (SIL plant) — steer_raw, brake_adc, brake_mA
//   0x601 (1537) = RZC_Virtual_Sensors (SIL plant) — motor_mA, motor_temp, batt_mV, motor_RPM

#include "vehicle_signals.h"
#include "score/mw/com/runtime.h"

#include <boost/program_options.hpp>
#include <chrono>
#include <cstring>
#include <iostream>
#include <thread>

#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <unistd.h>

using namespace std::chrono_literals;
using taktflow::can_bridge::VehicleSignals;
using taktflow::can_bridge::VehicleSignalProxy;
using taktflow::can_bridge::VehicleSignalSkeleton;

static int open_can(const std::string& iface) {
    int s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if (s < 0) { std::cerr << "socket: " << strerror(errno) << "\n"; return -1; }
    struct ifreq ifr{}; std::strncpy(ifr.ifr_name, iface.c_str(), IFNAMSIZ-1);
    if (ioctl(s, SIOCGIFINDEX, &ifr) < 0) { std::cerr << iface << ": " << strerror(errno) << "\n"; close(s); return -1; }
    struct sockaddr_can addr{}; addr.can_family = AF_CAN; addr.can_ifindex = ifr.ifr_ifindex;
    if (bind(s, reinterpret_cast<struct sockaddr*>(&addr), sizeof(addr)) < 0) { close(s); return -1; }
    struct timeval tv{1,0}; setsockopt(s, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
    return s;
}

/// Extract unsigned integer from CAN data at bit position, little-endian.
static uint64_t extract_le(const uint8_t* data, int start_bit, int length) {
    uint64_t val = 0;
    for (int i = 0; i < length; i++) {
        int bit = start_bit + i;
        int byte_pos = bit / 8;
        int bit_pos = bit % 8;
        if (data[byte_pos] & (1 << bit_pos)) {
            val |= (1ULL << i);
        }
    }
    return val;
}

/// Decode CAN frame using actual taktflow DBC definitions.
static void decode(const struct can_frame& f, VehicleSignals& sig) {
    auto id = f.can_id & CAN_SFF_MASK;
    const uint8_t* d = f.data;

    switch (id) {

    // 0x220 (544) Lidar_Distance from FZC — taktflow_vehicle.dbc
    // E2E_DataID:4 | E2E_AliveCounter:4 | E2E_CRC8:8 | Distance_cm:16 | SignalStrength:16 | ObstacleZone:4 | SensorStatus:4
    case 0x220:
        if (f.can_dlc >= 7) {
            sig.lidar_distance_cm = static_cast<uint16_t>(extract_le(d, 16, 16));
            // alive counter from E2E
            sig.sequence = static_cast<uint32_t>(extract_le(d, 4, 4));
        }
        break;

    // 0x600 (1536) FZC_Virtual_Sensors from SIL plant sim — taktflow_sil.dbc
    // FzcVS_SteerAngle_Raw:16 | FzcVS_BrakePos_ADC:16 | FzcVS_BrakeCurrent_mA:16
    case 0x600:
        if (f.can_dlc >= 6) {
            uint16_t steer_raw = static_cast<uint16_t>(extract_le(d, 0, 16));
            // 0=−45deg, 8191=0deg, 16383=+45deg
            sig.steering_angle_deg = (static_cast<float>(steer_raw) - 8191.0f) * 45.0f / 8192.0f;
            uint16_t brake_adc = static_cast<uint16_t>(extract_le(d, 16, 16));
            sig.pedal_position_pct = static_cast<float>(brake_adc) / 10.0f; // 0-1000 = 0-100%
        }
        break;

    // 0x601 (1537) RZC_Virtual_Sensors from SIL plant sim — taktflow_sil.dbc
    // RzcVS_MotorCurrent_mA:16 | RzcVS_MotorTemp_dC:16 | RzcVS_BattVoltage_mV:16 | RzcVS_MotorRPM:16
    case 0x601:
        if (f.can_dlc >= 8) {
            sig.motor_current_a = static_cast<float>(extract_le(d, 0, 16)) / 1000.0f;
            sig.motor_temp_c = static_cast<float>(extract_le(d, 16, 16)) / 10.0f;
            float batt_mv = static_cast<float>(extract_le(d, 32, 16));
            sig.vehicle_speed_kph = batt_mv / 1000.0f; // Store battery voltage in speed field for now
            sig.motor_rpm = static_cast<float>(extract_le(d, 48, 16));
        }
        break;

    // Real ECU messages (when physical bench is on)
    case 0x300: // Motor_Status from RZC (768 dec)
        if (f.can_dlc >= 6) {
            // Skip E2E header (16 bits), TorqueEcho (8 bits), then MotorSpeed_RPM (16 bits)
            sig.motor_rpm = static_cast<float>(extract_le(d, 24, 16));
        }
        break;

    case 0x010: // CVC_Heartbeat (16 dec)
        if (f.can_dlc >= 4) {
            sig.vehicle_state = static_cast<uint8_t>(extract_le(d, 24, 4)); // OperatingMode
            sig.hsm_heartbeat = static_cast<uint32_t>(extract_le(d, 4, 4)); // AliveCounter
        }
        break;

    default:
        break;
    }
}

static int run_skeleton(const score::mw::com::InstanceSpecifier& spec, const std::string& iface, size_t n) {
    int sock = open_can(iface);
    if (sock < 0) return EXIT_FAILURE;

    auto skel = VehicleSignalSkeleton::Create(spec);
    if (!skel.has_value()) { std::cerr << "Skeleton: " << skel.error() << "\n"; close(sock); return EXIT_FAILURE; }
    auto offer = skel.value().OfferService();
    if (!offer.has_value()) { std::cerr << "Offer: " << offer.error() << "\n"; close(sock); return EXIT_FAILURE; }

    std::cout << "CAN->LoLa skeleton v2 on " << iface << " (DBC-correct decoding)\n";
    VehicleSignals sig{}; uint32_t cycle = 0; struct can_frame frame{};

    while (n == 0 || cycle < n) {
        if (read(sock, &frame, sizeof(frame)) <= 0) continue;

        auto t_before = std::chrono::steady_clock::now();

        decode(frame, sig);
        sig.timestamp_ms = uint32_t(std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now().time_since_epoch()).count());

        auto sam = skel.value().vehicle_signals_.Allocate();
        if (!sam.has_value()) { std::cerr << "Alloc fail\n"; continue; }
        *sam.value() = sig;
        auto send = skel.value().vehicle_signals_.Send(std::move(sam).value());

        auto t_after = std::chrono::steady_clock::now();
        auto ipc_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t_after - t_before).count();

        if (cycle % 100 == 0) {
            auto id_hex = frame.can_id & CAN_SFF_MASK;
            std::cout << "[" << cycle << "] 0x" << std::hex << id_hex << std::dec
                      << " rpm=" << sig.motor_rpm
                      << " steer=" << sig.steering_angle_deg << "deg"
                      << " lidar=" << sig.lidar_distance_cm << "cm"
                      << " Tm=" << sig.motor_temp_c << "C"
                      << " Ia=" << sig.motor_current_a << "A"
                      << " ipc=" << ipc_ns << "ns"
                      << "\n";
        }
        cycle++;
    }
    skel.value().StopOfferService(); close(sock);
    std::cout << "Done (" << cycle << " frames)\n";
    return EXIT_SUCCESS;
}

static int run_proxy(const score::mw::com::InstanceSpecifier& spec, size_t n) {
    std::cout << "Finding vehicle signal service...\n";
    score::mw::com::ServiceHandleContainer<score::mw::com::impl::HandleType> h{};
    do { auto r = VehicleSignalProxy::FindService(spec); if (r.has_value()) h = std::move(r).value();
         if (h.empty()) std::this_thread::sleep_for(500ms);
    } while (h.empty());

    auto px = VehicleSignalProxy::Create(std::move(h.front()));
    if (!px.has_value()) { std::cerr << "Proxy: " << px.error() << "\n"; return EXIT_FAILURE; }
    px.value().vehicle_signals_.Subscribe(2);

    std::cout << "Subscribed! Receiving...\n";
    size_t rx = 0;
    while (n == 0 || rx < n) {
        auto t_before = std::chrono::steady_clock::now();
        px.value().vehicle_signals_.GetNewSamples([&rx, &t_before](score::mw::com::SamplePtr<VehicleSignals> s) noexcept {
            auto t_now = std::chrono::steady_clock::now();
            auto age_us = std::chrono::duration_cast<std::chrono::microseconds>(t_now - t_before).count();
            std::cout << "[seq=" << s->sequence
                      << "] rpm=" << s->motor_rpm
                      << " steer=" << s->steering_angle_deg << "deg"
                      << " lidar=" << s->lidar_distance_cm << "cm"
                      << " Tm=" << s->motor_temp_c << "C"
                      << " Ia=" << s->motor_current_a << "A"
                      << " age=" << age_us << "us"
                      << "\n";
            rx++;
        }, 2);
        std::this_thread::sleep_for(100ms);
    }
    px.value().vehicle_signals_.Unsubscribe();
    return EXIT_SUCCESS;
}

int main(int argc, const char** argv) {
    namespace po = boost::program_options;
    po::options_description opts("CAN-LoLa Bridge v2 (DBC-correct)");
    opts.add_options()("help,h","")("mode,m",po::value<std::string>(),"skeleton|proxy")
        ("can,c",po::value<std::string>()->default_value("vcan0"),"CAN iface")
        ("num-cycles,n",po::value<size_t>()->default_value(0),"0=inf")
        ("service_instance_manifest,s",po::value<std::string>(),"config json");
    po::variables_map vm; po::store(po::parse_command_line(argc, argv, opts), vm);
    if (vm.count("help") || !vm.count("mode")) { std::cerr << opts << "\n"; return 1; }

    if (vm.count("service_instance_manifest")) {
        auto p = vm["service_instance_manifest"].as<std::string>();
        score::StringLiteral a[2] = {"--service_instance_manifest", p.c_str()};
        score::mw::com::runtime::InitializeRuntime(2, a);
    }
    auto spec = score::mw::com::InstanceSpecifier::Create("taktflow/vehicle_signals");
    if (!spec.has_value()) { std::cerr << "Bad specifier\n"; return 1; }

    auto mode = vm["mode"].as<std::string>();
    auto n = vm["num-cycles"].as<size_t>();
    if (mode == "skeleton") return run_skeleton(spec.value(), vm["can"].as<std::string>(), n);
    if (mode == "proxy") return run_proxy(spec.value(), n);
    std::cerr << "Unknown mode: " << mode << "\n"; return 1;
}
