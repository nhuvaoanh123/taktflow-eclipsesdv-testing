---
document_id: INTEG-PER
title: "Upstream Integration Map — score-persistency (KVS)"
version: "1.0"
status: active
date: 2026-03-20
---

# Upstream S-CORE ↔ Taktflow ASPICE Integration Map — Persistency

## Upstream Requirement Summary

Source: `score-persistency/docs/persistency/kvs/requirements/index.rst`

**27 component requirements** (`comp_req__persistency__*_v2`), all ASIL-B, using Sphinx `needs` directives.

## Upstream comp_req → Taktflow SWR Mapping

| S-CORE comp_req ID | Description | ASIL | Taktflow SWR | Category |
|---|---|---|---|---|
| `comp_req__persistency__key_naming_v2` | Alphanumeric/underscore/dash keys only | B | SWR-PER-KVS-001 | Key mgmt |
| `comp_req__persistency__key_encoding_v2` | UTF-8 key encoding | B | SWR-PER-KVS-001 | Key mgmt |
| `comp_req__persistency__key_uniqueness_v2` | Unique keys guaranteed | B | SWR-PER-KVS-001 | Key mgmt |
| `comp_req__persistency__key_length_v2` | Max key length 32 bytes | B | SWR-PER-KVS-001 | Key mgmt |
| `comp_req__persistency__value_data_types_v2` | Number/String/Null/Array/Dict types | B | SWR-PER-KVS-002 | Value mgmt |
| `comp_req__persistency__value_serialize_v2` | JSON serialization | B | SWR-PER-KVS-002 | Value mgmt |
| `comp_req__persistency__value_length_v2` | Max value length 1024 bytes | B | SWR-PER-KVS-002 | Value mgmt |
| `comp_req__persistency__value_default_v2` | Default value support | B | SWR-PER-KVS-002 | Value mgmt |
| `comp_req__persistency__value_reset_v2` | Reset to default | B | SWR-PER-KVS-002 | Value mgmt |
| `comp_req__persistency__default_value_types_v2` | Default value type constraint | B | SWR-PER-KVS-002 | Value mgmt |
| `comp_req__persistency__default_value_query_v2` | Default value retrieval API | B | SWR-PER-KVS-002 | Value mgmt |
| `comp_req__persistency__default_value_cfg_v2` | Code or config file defaults | B | SWR-PER-KVS-002 | Value mgmt |
| `comp_req__persistency__default_val_chksum_v2` | Checksum for default value config file | B | SWR-PER-KVS-003 | Integrity |
| `comp_req__persistency__constraints_v2` | Compile-time or runtime constraints | B | SWR-PER-KVS-002 | Config |
| `comp_req__persistency__concurrency_v2` | Thread-safe concurrent access | B | SWR-PER-KVS-004 | Safety |
| `comp_req__persistency__multi_instance_v2` | Multiple KVS instances per process | B | SWR-PER-KVS-004 | Safety |
| `comp_req__persistency__persist_data_com_v2` | File API + JSON format for persistence | B | SWR-PER-KVS-001 | Storage |
| `comp_req__persistency__pers_data_csum_v2` | Checksum generation on write | B | **SG-PER-001** → FSR-PER-002 | Integrity |
| `comp_req__persistency__pers_data_csum_vrfy_v2` | Checksum verification on load | B | **SG-PER-001** → FSR-PER-002 | Integrity |
| `comp_req__persistency__pers_data_store_bnd_v2` | File API backend | B | SWR-PER-KVS-001 | Storage |
| `comp_req__persistency__pers_data_store_fmt_v2` | JSON format | B | SWR-PER-KVS-001 | Storage |
| `comp_req__persistency__pers_data_version_v2` | No built-in versioning | B | — | Design decision |
| `comp_req__persistency__pers_data_schema_v2` | App-managed versioning via JSON | B | — | Design decision |
| `comp_req__persistency__snapshot_creation_v2` | Snapshot on every store | B | **SG-PER-002** → FSR-PER-003 | Snapshot |
| `comp_req__persistency__snapshot_max_num_v2` | Configurable max snapshots | B | SWR-PER-KVS-003 | Snapshot |
| `comp_req__persistency__snapshot_id_v2` | ID 1 = newest, increment older | B | SWR-PER-KVS-003 | Snapshot |
| `comp_req__persistency__snapshot_rotate_v2` | Delete oldest when max reached | B | SWR-PER-KVS-003 | Snapshot |
| `comp_req__persistency__snapshot_restore_v2` | Restore by ID | B | **SG-PER-002** → FSR-PER-003 | Snapshot |
| `comp_req__persistency__snapshot_delete_v2` | Delete individual snapshots | B | SWR-PER-KVS-003 | Snapshot |
| `comp_req__persistency__eng_mode_v2` | Debug engineering mode | B | — | QM tooling |
| `comp_req__persistency__field_mode_v2` | Restricted production mode | B | SWR-PER-KVS-005 | Security |
| `comp_req__persistency__async_api_v2` | Async API via kyron | B | SWR-PER-KVS-006 | Interface |
| `comp_req__persistency__permission_control_v2` | Filesystem-based access control | B | SWR-PER-KVS-005 | Security |
| `comp_req__persistency__permission_err_hndl_v2` | Report permission errors | B | SWR-PER-KVS-005 | Security |
| `comp_req__persistency__callback_support_v2` | Data change callbacks | B | SWR-PER-KVS-006 | Interface |

## Upstream Safety Documents

| Document | S-CORE ID | Status | Content |
|---|---|---|---|
| Safety Plan | `doc__persistency_safety_plan_v2` | Valid | Roles (Volker Häussler, Lars Bauhofer), scope, tailoring, work product list |
| Safety Manual | `doc__persistency_safety_manual` | Valid | Integration constraints, AoUs |
| KVS FMEA | `doc__persistency_kvs_fmea_v2` | Valid | References feature-level FMEA (`doc__persistency_fmea`) |
| KVS DFA | `doc__persistency_kvs_dfa_v2` | Valid | References feature-level DFA (`doc__persistency_dfa`) |
| Safety Package FDR | `doc__persistency_safety_package_fdr` | Valid | Formal design review record |
| Safety Plan FDR | `doc__persistency_safety_plan_fdr` | Valid | Safety plan review record |
| Security Plan | `doc__persistency_security_plan` | Valid | Security management |
| Security Package FDR | `doc__persistency_security_package_fdr` | Valid | Security review record |

## Feature Requirements (upstream `feat_req__persistency__*`)

Referenced by comp_reqs via `:satisfies:` field:

| Feature Requirement | Comp Reqs Satisfying |
|---|---|
| `feat_req__persistency__support_datatype_keys` | key_naming, key_encoding, key_uniqueness, key_length |
| `feat_req__persistency__support_datatype_value` | value_data_types, value_serialize, value_length, value_default, value_reset |
| `feat_req__persistency__default_values` | default_value_types, default_value_query, default_value_cfg, default_val_chksum |
| `feat_req__persistency__integrity_check` | pers_data_csum, pers_data_csum_vrfy, persist_data_com |
| `feat_req__persistency__store_data` | pers_data_store_bnd, pers_data_store_fmt, persist_data_com |
| `feat_req__persistency__snapshot_create` | snapshot_creation, snapshot_id |
| `feat_req__persistency__snapshot_remove` | snapshot_rotate, snapshot_delete |
| `feat_req__persistency__snapshot_restore` | snapshot_restore, snapshot_rotate |
| `feat_req__persistency__concurrency` | concurrency |
| `feat_req__persistency__multiple_kvs` | multi_instance |
| `feat_req__persistency__async_api` | async_api, callback_support |
| `feat_req__persistency__access_control` | permission_control, permission_err_hndl |
| `feat_req__persistency__cfg` | constraints, snapshot_max_num |
| `feat_req__persistency__dev_mode` | eng_mode |
| `feat_req__persistency__prod_mode` | field_mode |
