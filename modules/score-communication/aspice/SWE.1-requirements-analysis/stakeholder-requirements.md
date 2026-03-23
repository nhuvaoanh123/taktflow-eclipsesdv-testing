---
document_id: STK-COM
title: "Stakeholder Requirements — score-communication (LoLa)"
version: "1.0"
status: draft
aspice_process: SWE.1
date: 2026-03-20
---

# Stakeholder Requirements

## STK-COM-001: Low-Latency Intra-ECU Communication

- **Stakeholder**: Vehicle Application Developer
- **Need**: A communication middleware that provides sub-millisecond data exchange between processes on the same ECU for real-time vehicle applications.
- **Traces down**: SYS-COM-001, SYS-COM-002
- **Priority**: Critical

## STK-COM-002: AUTOSAR ara::com API Compatibility

- **Stakeholder**: AUTOSAR Adaptive Platform Integrator
- **Need**: The middleware API must follow the Adaptive AUTOSAR Communication Management (ara::com) specification so that existing application code is portable.
- **Traces down**: SYS-COM-003
- **Priority**: High

## STK-COM-003: Safety-Critical Data Exchange (ASIL-B)

- **Stakeholder**: Safety Engineer
- **Need**: The middleware must be qualifiable for ASIL-B safety-critical signal exchange (e.g., battery SOC, motor torque commands) with guaranteed data integrity and bounded latency.
- **Traces down**: SYS-COM-004, SG-COM-001, SG-COM-002, SG-COM-003
- **Priority**: Critical

## STK-COM-004: Multi-Platform Deployment

- **Stakeholder**: Platform Architect
- **Need**: The middleware must run on both Linux (development, SIL) and QNX (production HPC target) without code changes in the application layer.
- **Traces down**: SYS-COM-005
- **Priority**: High

## STK-COM-005: Zero-Copy Data Transfer

- **Stakeholder**: Performance Engineer
- **Need**: Large data payloads (camera frames, point clouds) must be transferable between processes without memory copy overhead to meet real-time frame rates.
- **Traces down**: SYS-COM-001
- **Priority**: High

## STK-COM-006: Service-Oriented Architecture

- **Stakeholder**: Vehicle Application Developer
- **Need**: Applications must be able to discover, connect to, and communicate with services dynamically without hardcoded addresses or configuration.
- **Traces down**: SYS-COM-006
- **Priority**: Medium

## STK-COM-007: Fault Isolation

- **Stakeholder**: System Architect
- **Need**: A failing application process must not bring down other communicating processes. The middleware must support partial restart and error containment.
- **Traces down**: SYS-COM-007
- **Priority**: High

## STK-COM-008: Observable Communication

- **Stakeholder**: Integration Test Engineer
- **Need**: Communication events (publish, subscribe, discover) must be traceable for debugging and performance analysis without impacting runtime behavior.
- **Traces down**: SYS-COM-008
- **Priority**: Medium

## STK-COM-009: Deterministic Scheduling Integration

- **Stakeholder**: Safety Engineer
- **Need**: Communication must integrate with the Fixed Execution Order (FEO) framework so that data is published and consumed at deterministic cycle boundaries.
- **Traces down**: SYS-COM-009
- **Priority**: High

## STK-COM-010: Scalable Multi-Subscriber

- **Stakeholder**: Platform Architect
- **Need**: A single data producer must be able to serve multiple consumers simultaneously without performance degradation proportional to subscriber count.
- **Traces down**: SYS-COM-010
- **Priority**: Medium
