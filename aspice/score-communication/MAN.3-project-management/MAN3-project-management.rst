.. # *******************************************************************************
   # Copyright (c) 2026 Taktflow Systems
   # SPDX-License-Identifier: Apache-2.0
   # *******************************************************************************

MAN.3 — Project Management
############################

Module: score-communication (LoLa)
**********************************

:ASPICE Level: 2
:Status: Active

Project Overview
================

.. list-table::
   :header-rows: 0
   :widths: 30 70

   * - Repository
     - `eclipse-score/communication <https://github.com/eclipse-score/communication>`_
   * - Commits
     - 1,295
   * - Contributors
     - 65
   * - Releases
     - 6 tagged versions
   * - License
     - Apache-2.0
   * - Build System
     - Bazel 6.0+
   * - Languages
     - C++17, Python (tooling)
   * - CI/CD
     - GitHub Actions
   * - Last Activity
     - 2026-03-20 (Active)

Roles and Responsibilities
==========================

Per S-CORE process description (``score-process_description/process/roles/``):

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Role
     - S-CORE Role ID
     - Responsibilities for this module
   * - Project Lead
     - ``rl__project_lead``
     - Define communication feature scope, release planning, progress tracking
   * - SW Architect / Committer
     - ``rl__committer``
     - Architecture design, code review (2 reviewers for ASIL-B), feature breakdown
   * - Contributor
     - ``rl__contributor``
     - Implementation, unit tests, documentation
   * - Safety Engineer
     - ``rl__safety_engineer``
     - DFA, FMEA, safety plan review, ASIL classification decisions
   * - Security Engineer
     - ``rl__security_manager``
     - Security analysis of shared memory access, process isolation verification
   * - Tester
     - ``rl__committer``
     - Integration test design, qualification test execution, coverage analysis

Development Workflow
====================

Per S-CORE contribution guide (``CONTRIBUTING.md``):

1. **Fork** the repository
2. **Create feature branch** from ``main``
3. **Implement** following coding guidelines (``.clang-format``, ``.clang-tidy``)
4. **Write tests** — unit tests required, integration tests for cross-component changes
5. **Run locally**: ``bazel test //...``
6. **Submit PR** using template (``.github/RELEASE_TEMPLATE.md``)
7. **Review** — 1 reviewer for QM, 2 reviewers for ASIL-B changes
8. **CI gate** — all tests pass, clang-tidy clean, coverage gate met
9. **Merge** by committer

Release Process
===============

Per S-CORE release management (``score-process_description/process/process_areas/release_management/``):

1. Version tagging follows semantic versioning (current: v0.1.4)
2. Release notes generated from PR descriptions
3. Release template: ``.github/RELEASE_TEMPLATE.md``
4. Release artifacts: Bazel module published to S-CORE registry

Quality Gates
=============

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Gate
     - Threshold
     - Enforcement
   * - Unit test pass rate
     - 100%
     - CI blocks merge on failure
   * - Integration test pass rate
     - 100%
     - CI blocks merge on failure
   * - Static analysis (clang-tidy)
     - 0 warnings
     - CI blocks merge on warning
   * - Code coverage (ASIL-B)
     - Branch ≥ 80%
     - CI reports, manual review
   * - Code coverage (QM)
     - Statement ≥ 70%
     - CI reports
   * - Code review
     - 2 approvals (ASIL-B) / 1 (QM)
     - GitHub branch protection
   * - License compliance
     - Apache-2.0 headers on all files
     - CI check via ``//:copyright.check``

Risk Register
=============

.. list-table::
   :header-rows: 1
   :widths: 10 30 15 45

   * - ID
     - Risk
     - Impact
     - Mitigation
   * - R1
     - QNX message passing backend has fewer tests than Linux
     - High
     - Prioritize QNX integration tests on Pi target
   * - R2
     - Lock-free algorithms difficult to verify for all edge cases
     - High
     - Stress tests + future model checking (TLA+)
   * - R3
     - SOME/IP inter-ECU path not yet implemented
     - Medium
     - Track upstream issue eclipse-score/score#914
   * - R4
     - Bazel build complexity limits contributor onboarding
     - Low
     - DevContainer provides pre-configured environment
