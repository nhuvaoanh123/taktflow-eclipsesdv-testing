# ASPICE Folder Hierarchy — Eclipse SDV Testing

This directory organizes documentation from all 56 Eclipse SDV submodules into
an Automotive SPICE (ASPICE) process-area hierarchy for traceability and
compliance analysis.

## ASPICE Process Areas

| Code | Process Area | Description |
|---|---|---|
| **SWE.1** | Requirements Analysis | Project READMEs, feature descriptions, requirements |
| **SWE.2** | Architectural Design | System architecture, protocol design, interface docs |
| **SWE.3** | Detailed Design | API docs, user guides, CLI references, configuration |
| **SWE.4** | Unit Verification | Unit test documentation and test plans |
| **SWE.5** | Integration Test | Integration test docs and procedures |
| **SWE.6** | Qualification Test | Examples, demos, sample applications |
| **MAN.3** | Project Management | Contributing guides, dev setup, PR templates |
| **SUP.1** | Quality Assurance | Notices, 3rd-party content, license compliance |
| **SUP.8** | Configuration Mgmt | Build docs, Docker, deployment, setup guides |
| **SUP.9** | Problem Resolution | Troubleshooting, debugging, migration guides |
| **SUP.10** | Change Request Mgmt | (placeholder — tracked in GitHub Issues) |
| **ACQ.4** | Supplier Monitoring | (placeholder — upstream Eclipse project tracking) |
| **SYS.1** | Requirements Elicitation | (placeholder — stakeholder requirements) |
| **SYS.2** | System Req. Analysis | (placeholder — system-level requirements) |
| **SYS.3** | System Arch. Design | Specifications, mappings, principles |
| **SYS.4** | System Integration Test | (placeholder — system integration tests) |
| **SYS.5** | System Qualification | (placeholder — system qualification tests) |
| **SEC** | Security | Security policies, TLS, auth, certificates, privacy |
| **REL** | Release Management | Release docs, versioning, changelogs |

## Structure

```
aspice/
├── {module-name}/
│   ├── SWE.1-requirements-analysis/
│   ├── SWE.2-architectural-design/
│   ├── SWE.3-detailed-design/
│   ├── SWE.4-unit-verification/
│   ├── SWE.5-integration-test/
│   ├── SWE.6-qualification-test/
│   ├── MAN.3-project-management/
│   ├── SUP.1-quality-assurance/
│   ├── SUP.8-configuration-management/
│   ├── SUP.9-problem-resolution/
│   ├── SUP.10-change-request-management/
│   ├── ACQ.4-supplier-monitoring/
│   ├── SYS.1-requirements-elicitation/
│   ├── SYS.2-system-requirements-analysis/
│   ├── SYS.3-system-architectural-design/
│   ├── SYS.4-system-integration-test/
│   ├── SYS.5-system-qualification-test/
│   ├── SEC-security/
│   └── REL-release-management/
└── ...  (56 modules)
```

## Statistics

- **56 modules** × **19 ASPICE folders** = **1,064 categorized slots**
- **270 documents** placed from upstream Eclipse SDV repos
- Empty folders (`.gitkeep`) indicate gaps to be filled during testing

## Doc Mapping Rules

| Source doc pattern | ASPICE target |
|---|---|
| `README.md` | SWE.1 (requirements/features overview) |
| `*architecture*`, `*protocol*`, `*system-design*` | SWE.2 |
| `*api*`, `*quickstart*`, `*user_guide*`, `*cli*`, `*config*` | SWE.3 |
| `test/`, `utest/` READMEs | SWE.4 |
| `integration_test/` docs | SWE.5 |
| `examples/`, `samples/`, `demo/` docs | SWE.6 |
| `CONTRIBUTING*`, `DEVELOPMENT*`, `PULL_REQUEST_TEMPLATE*` | MAN.3 |
| `NOTICE*`, `*3RD-PARTY*`, `*license*` | SUP.1 |
| `*build*`, `*docker*`, `*deploy*`, `*setup*` | SUP.8 |
| `*troubleshoot*`, `*debug*`, `*migration*` | SUP.9 |
| `*spec*`, `*principle*`, `*mapping*` | SYS.3 |
| `SECURITY*`, `*tls*`, `*auth*`, `*cert*`, `*privacy*` | SEC |
| `RELEASE*`, `*version*` | REL |
