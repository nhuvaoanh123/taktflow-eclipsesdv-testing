#!/usr/bin/env python3
# Copyright (c) 2022, 2025 Contributors to the Eclipse Foundation
#
# SPDX-License-Identifier: Apache-2.0
#
# NOTE: Rewritten for KUKSA.val v2 API (kuksa.val.v2.VAL).
# The original sdv.databroker.v1 collector API (RegisterDatapoints / CollectorStub)
# was removed in kuksa-databroker v0.6.x.  All tests now use the v2 VAL service.

import asyncio
import logging
import os
import time

import grpc
import grpc.aio
import pytest

from gen_proto.kuksa.val.v2 import val_pb2, val_pb2_grpc, types_pb2

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", "WARN"))

DATABROKER_ADDRESS = os.environ.get("DATABROKER_ADDRESS", "127.0.0.1:55555")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _insecure_channel():
    return grpc.aio.insecure_channel(DATABROKER_ADDRESS)


def _signal_id(path: str) -> types_pb2.SignalID:
    return types_pb2.SignalID(path=path)


def _float_datapoint(value: float) -> types_pb2.Datapoint:
    return types_pb2.Datapoint(value=types_pb2.Value(float=value))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_databroker_connection():
    """Broker responds to GetServerInfo on the v2 VAL service."""
    async with _insecure_channel() as channel:
        stub = val_pb2_grpc.VALStub(channel)
        response = await stub.GetServerInfo(val_pb2.GetServerInfoRequest())
        logger.info("Server: name=%s version=%s", response.name, response.version)
        assert response.name != "", "Expected non-empty server name"


@pytest.mark.asyncio
async def test_vehicle_speed_metadata():
    """Vehicle.Speed exists in VSS 4.0 metadata loaded by the broker."""
    async with _insecure_channel() as channel:
        stub = val_pb2_grpc.VALStub(channel)
        response = await stub.ListMetadata(
            val_pb2.ListMetadataRequest(root="Vehicle.Speed")
        )
        paths = [m.path for m in response.metadata]
        logger.info("Metadata paths returned: %s", paths)
        assert "Vehicle.Speed" in paths, (
            f"Vehicle.Speed not found in metadata; got: {paths}"
        )


@pytest.mark.asyncio
async def test_publish_and_get_vehicle_speed():
    """PublishValue then GetValue roundtrip for Vehicle.Speed."""
    async with _insecure_channel() as channel:
        stub = val_pb2_grpc.VALStub(channel)
        signal = _signal_id("Vehicle.Speed")

        # Publish a float value
        await stub.PublishValue(
            val_pb2.PublishValueRequest(
                signal_id=signal,
                data_point=_float_datapoint(88.5),
            )
        )

        # Read it back
        response = await stub.GetValue(
            val_pb2.GetValueRequest(signal_id=signal)
        )
        assert response.HasField("data_point"), "No datapoint in GetValue response"
        assert abs(response.data_point.value.float - 88.5) < 0.001, (
            f"Expected 88.5, got {response.data_point.value.float}"
        )


@pytest.mark.asyncio
async def test_subscribe_vehicle_speed():
    """Subscribe to Vehicle.Speed and receive at least one update."""
    async with _insecure_channel() as channel:
        stub = val_pb2_grpc.VALStub(channel)
        signal_path = "Vehicle.Speed"

        # Start subscription first, then publish
        subscribe_req = val_pb2.SubscribeRequest(signal_paths=[signal_path])

        received = []

        async def _publish_after_delay():
            await asyncio.sleep(0.1)
            async with _insecure_channel() as pub_channel:
                pub_stub = val_pb2_grpc.VALStub(pub_channel)
                await pub_stub.PublishValue(
                    val_pb2.PublishValueRequest(
                        signal_id=_signal_id(signal_path),
                        data_point=_float_datapoint(42.0),
                    )
                )

        asyncio.create_task(_publish_after_delay())

        async for update in stub.Subscribe(subscribe_req):
            if signal_path in update.entries:
                received.append(update.entries[signal_path].value.float)
            # Stop once we see the published value or have collected enough updates
            if any(abs(v - 42.0) < 0.001 for v in received):
                break
            if len(received) >= 5:
                break  # avoid infinite wait

        assert len(received) > 0, "No subscription update received"
        assert any(abs(v - 42.0) < 0.001 for v in received), (
            f"Expected 42.0 in any update, got: {received}"
        )


@pytest.mark.asyncio
async def test_get_multiple_signals():
    """GetValues returns datapoints for multiple VSS signals at once."""
    async with _insecure_channel() as channel:
        stub = val_pb2_grpc.VALStub(channel)

        signals = [
            _signal_id("Vehicle.Speed"),
            _signal_id("Vehicle.CurrentLocation.Latitude"),
        ]

        # Publish known values first
        await stub.PublishValue(
            val_pb2.PublishValueRequest(
                signal_id=signals[0],
                data_point=_float_datapoint(60.0),
            )
        )

        response = await stub.GetValues(
            val_pb2.GetValuesRequest(signal_ids=signals)
        )
        assert len(response.data_points) > 0, "GetValues returned no datapoints"
