/********************************************************************************
 * Copyright (c) 2025 Contributors to the Eclipse Foundation
 *
 * See the NOTICE file(s) distributed with this work for additional
 * information regarding copyright ownership.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Apache License 2.0 which is available at
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * SPDX-License-Identifier: Apache-2.0
 ********************************************************************************/

//! taktflow Security and Contract Tests for eclipse-kuksa-databroker
//!
//! Verifies:
//! - Broker reports a valid server identity (KUKSA.val v2 GetServerInfo)
//! - VSS 4.0 Vehicle.Speed signal is present and typed correctly
//! - Broker correctly stores and retrieves a float signal (publish/get round-trip)

use std::{
    future::poll_fn,
    net::SocketAddr,
    sync::{Arc, Mutex},
    task::{Poll, Waker},
};

use cucumber::{given, then, when, World as _};
use databroker::{
    authorization::Authorization,
    broker,
    grpc::{self, server::ServerTLS},
    permissions,
};
use databroker_proto::kuksa::val::v2 as proto;
use kuksa_common::ClientTraitV2;
use kuksa_val_v2::KuksaClientV2;
use tokio::net::TcpListener;
use tokio_stream::wrappers::TcpListenerStream;

// ---------------------------------------------------------------------------
// World
// ---------------------------------------------------------------------------

#[derive(Debug)]
struct BrokerState {
    running: bool,
    address: Option<SocketAddr>,
    waker: Option<Waker>,
}

#[derive(cucumber::World, Debug)]
#[world(init = Self::new)]
pub struct TaktflowWorld {
    broker_state: Arc<Mutex<BrokerState>>,
    pub client: Option<KuksaClientV2>,
    pub server_name: Option<String>,
    pub metadata: Vec<proto::Metadata>,
    pub stored_value: Option<f32>,
}

impl TaktflowWorld {
    pub fn new() -> Self {
        TaktflowWorld {
            broker_state: Arc::new(Mutex::new(BrokerState {
                running: false,
                address: None,
                waker: None,
            })),
            client: None,
            server_name: None,
            metadata: vec![],
            stored_value: None,
        }
    }

    async fn start_broker(
        &mut self,
        entries: Vec<(
            String,
            broker::DataType,
            broker::ChangeType,
            broker::EntryType,
        )>,
    ) {
        {
            let state = self.broker_state.lock().expect("lock broker state");
            if state.running {
                return;
            }
        }

        let owned_state = self.broker_state.clone();
        let listener = TcpListener::bind("127.0.0.1:0")
            .await
            .expect("bind TcpListener");
        let addr = listener.local_addr().expect("local_addr");
        let incoming = TcpListenerStream::new(listener);

        tokio::spawn(async move {
            let data_broker = broker::DataBroker::new("taktflow-test", "unknown");
            let database = data_broker.authorized_access(&permissions::ALLOW_ALL);
            for (name, data_type, change_type, entry_type) in entries {
                database
                    .add_entry(
                        name,
                        data_type,
                        change_type,
                        entry_type,
                        "taktflow contract test".to_string(),
                        None, // min
                        None, // max
                        None,
                        None,
                    )
                    .await
                    .expect("add_entry");
            }
            {
                let mut state = owned_state.lock().expect("lock state");
                state.running = true;
                state.address = Some(addr);
            }
            grpc::server::serve_with_incoming_shutdown(
                incoming,
                data_broker,
                #[cfg(feature = "tls")]
                ServerTLS::Disabled,
                &[grpc::server::Api::KuksaValV2],
                Authorization::Disabled,
                poll_fn(|cx| {
                    let mut state = owned_state.lock().expect("lock state in poll_fn");
                    if state.running {
                        state.waker = Some(cx.waker().clone());
                        Poll::Pending
                    } else {
                        Poll::Ready(())
                    }
                }),
            )
            .await
            .ok();
        });

        // Give the gRPC server a moment to start processing requests
        tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;

        let url = format!("http://{}:{}", addr.ip(), addr.port());
        let uri = kuksa_common::to_uri(url).expect("URI parse");
        self.client = Some(KuksaClientV2::new(uri));
    }
}

// ---------------------------------------------------------------------------
// Steps --- Given
// ---------------------------------------------------------------------------

#[given("a databroker is started")]
async fn start_empty_databroker(w: &mut TaktflowWorld) {
    w.start_broker(vec![]).await;
    assert!(w.client.is_some(), "KuksaClientV2 should be created");
}

#[given("a databroker is started with VSS metadata")]
async fn start_databroker_with_vss(w: &mut TaktflowWorld) {
    w.start_broker(vec![(
        "Vehicle.Speed".to_string(),
        broker::DataType::Float,
        broker::ChangeType::Continuous,
        broker::EntryType::Sensor,
    )])
    .await;
    assert!(w.client.is_some(), "KuksaClientV2 should be created");
}

// ---------------------------------------------------------------------------
// Steps --- When
// ---------------------------------------------------------------------------

#[when("I request server info")]
async fn request_server_info(w: &mut TaktflowWorld) {
    let client = w.client.as_mut().expect("client not set up");
    let info = client
        .get_server_info()
        .await
        .expect("get_server_info failed");
    w.server_name = Some(info.name);
}

#[when("I query metadata for Vehicle.Speed")]
async fn query_vehicle_speed_metadata(w: &mut TaktflowWorld) {
    let client = w.client.as_mut().expect("client not set up");
    let result = client
        .list_metadata(("Vehicle.Speed".to_string(), "*".to_string()))
        .await
        .expect("list_metadata failed");
    w.metadata = result;
}

#[when("I provide the value 120.5 for Vehicle.Speed")]
async fn provide_vehicle_speed(w: &mut TaktflowWorld) {
    let client = w.client.as_mut().expect("client not set up");
    let value = proto::Value {
        typed_value: Some(proto::value::TypedValue::Float(120.5_f32)),
    };
    client
        .publish_value("Vehicle.Speed".to_string(), value)
        .await
        .expect("publish_value failed");
}

#[when("I request the current value of Vehicle.Speed")]
async fn get_vehicle_speed(w: &mut TaktflowWorld) {
    let client = w.client.as_mut().expect("client not set up");
    let maybe_dp = client
        .get_value("Vehicle.Speed".to_string())
        .await
        .expect("get_value failed");
    if let Some(dp) = maybe_dp {
        if let Some(val) = dp.value {
            if let Some(proto::value::TypedValue::Float(f)) = val.typed_value {
                w.stored_value = Some(f);
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Steps --- Then
// ---------------------------------------------------------------------------

#[then("the server name should not be empty")]
fn check_server_name(w: &mut TaktflowWorld) {
    let name = w.server_name.as_ref().expect("server name not captured");
    assert!(
        !name.is_empty(),
        "server name should not be empty, got: {name:?}"
    );
}

#[then("the signal should be present")]
fn check_signal_present(w: &mut TaktflowWorld) {
    assert!(
        !w.metadata.is_empty(),
        "Vehicle.Speed should be present in metadata"
    );
}

#[then("the data type should be float")]
fn check_data_type_float(w: &mut TaktflowWorld) {
    let md = w.metadata.first().expect("no metadata entry");
    // DATA_TYPE_FLOAT = 11 in kuksa.val.v2 DataType enum
    assert_eq!(
        md.data_type,
        proto::DataType::Float as i32,
        "Vehicle.Speed data_type should be DATA_TYPE_FLOAT (11)"
    );
}

#[then("the value should be 120.5")]
fn check_value_120_5(w: &mut TaktflowWorld) {
    let v = w.stored_value.expect("no value retrieved");
    assert!(
        (v - 120.5_f32).abs() < 1e-4,
        "expected 120.5 but got {v}"
    );
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() {
    TaktflowWorld::cucumber()
        .run("tests/features/taktflow_security.feature")
        .await;
}
