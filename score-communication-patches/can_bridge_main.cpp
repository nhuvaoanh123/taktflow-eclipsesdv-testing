// Copyright (c) 2026 Taktflow Systems — SPDX-License-Identifier: Apache-2.0
//
// CAN-to-LoLa Bridge: reads CAN frames from socketcan, publishes via LoLa IPC.
// Usage:
//   skeleton: ./can_bridge -m skeleton -c vcan0 -n 0 -s etc/mw_com_config.json
//   proxy:    ./can_bridge -m proxy -n 100 -s etc/mw_com_config.json

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

static void decode(const struct can_frame& f, VehicleSignals& sig) {
    auto id = f.can_id & CAN_SFF_MASK;
    if (id == 0x100 && f.can_dlc >= 6) {
        uint16_t p,v; memcpy(&p, f.data, 2); memcpy(&v, f.data+2, 2);
        sig.pedal_position_pct = p/100.0f; sig.vehicle_speed_kph = v/100.0f; sig.vehicle_state = f.data[4];
    } else if (id == 0x200 && f.can_dlc >= 4) {
        uint16_t r,c; memcpy(&r, f.data, 2); memcpy(&c, f.data+2, 2);
        sig.motor_rpm = float(r); sig.motor_current_a = c/1000.0f;
    } else if (id == 0x201 && f.can_dlc >= 4) {
        int16_t m,b; memcpy(&m, f.data, 2); memcpy(&b, f.data+2, 2);
        sig.motor_temp_c = m/10.0f; sig.battery_temp_c = b/10.0f;
    } else if (id == 0x220 && f.can_dlc >= 4) {
        uint16_t r; memcpy(&r, f.data, 2); sig.motor_rpm = float(r);
    } else if (id == 0x300 && f.can_dlc >= 2) {
        int16_t a; memcpy(&a, f.data, 2); sig.steering_angle_deg = a/10.0f;
    } else if (id == 0x301 && f.can_dlc >= 2) {
        memcpy(&sig.lidar_distance_cm, f.data, 2);
    } else if (id == 0x400 && f.can_dlc >= 4) {
        memcpy(&sig.hsm_heartbeat, f.data, 4);
    }
}

static int run_skeleton(const score::mw::com::InstanceSpecifier& spec, const std::string& iface, size_t n) {
    int sock = open_can(iface);
    if (sock < 0) return EXIT_FAILURE;

    auto skel = VehicleSignalSkeleton::Create(spec);
    if (!skel.has_value()) { std::cerr << "Skeleton: " << skel.error() << "\n"; close(sock); return EXIT_FAILURE; }
    auto offer = skel.value().OfferService();
    if (!offer.has_value()) { std::cerr << "Offer: " << offer.error() << "\n"; close(sock); return EXIT_FAILURE; }

    std::cout << "CAN->LoLa skeleton on " << iface << " (Ctrl+C to stop)\n";
    VehicleSignals sig{}; uint32_t cycle = 0; struct can_frame frame{};

    while (n == 0 || cycle < n) {
        if (read(sock, &frame, sizeof(frame)) <= 0) continue;
        decode(frame, sig);
        sig.sequence = cycle;
        sig.timestamp_ms = uint32_t(std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now().time_since_epoch()).count());

        auto sam = skel.value().vehicle_signals_.Allocate();
        if (!sam.has_value()) continue;
        *sam.value() = sig;
        skel.value().vehicle_signals_.Send(std::move(sam).value());

        if (cycle % 100 == 0)
            std::cout << "[" << cycle << "] rpm=" << sig.motor_rpm << " pedal=" << sig.pedal_position_pct << "%\n";
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
        px.value().vehicle_signals_.GetNewSamples([&rx](score::mw::com::SamplePtr<VehicleSignals> s) noexcept {
            std::cout << "[" << s->sequence << "] pedal=" << s->pedal_position_pct
                      << "% rpm=" << s->motor_rpm << " Tm=" << s->motor_temp_c
                      << "C steer=" << s->steering_angle_deg << "deg\n";
            rx++;
        }, 2);
        std::this_thread::sleep_for(100ms);
    }
    px.value().vehicle_signals_.Unsubscribe();
    return EXIT_SUCCESS;
}

int main(int argc, const char** argv) {
    namespace po = boost::program_options;
    po::options_description opts("CAN-LoLa Bridge");
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
