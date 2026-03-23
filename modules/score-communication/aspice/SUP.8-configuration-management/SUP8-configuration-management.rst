.. # *******************************************************************************
   # Copyright (c) 2026 Taktflow Systems
   # SPDX-License-Identifier: Apache-2.0
   # *******************************************************************************

SUP.8 — Configuration Management
##################################

Module: score-communication (LoLa)
**********************************

:ASPICE Level: 2
:Status: Active

Version Control
===============

:VCS: Git (GitHub)
:Repository: ``eclipse-score/communication``
:Default Branch: ``main``
:Branch Protection: Required reviews, CI pass, no force push

Build Configuration
===================

:Build System: Bazel 6.0+
:Bazel Version: Pinned in ``.bazelversion``
:Module Definition: ``MODULE.bazel``
:Workspace: ``WORKSPACE`` (legacy, being migrated to bzlmod)

Dependencies
------------

External dependencies managed via Bazel module registry (``score-bazel_registry``):

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Dependency
     - Source
     - Purpose
   * - score-baselibs
     - S-CORE registry
     - OS abstraction, memory utilities, result types
   * - GoogleTest
     - Bazel central registry
     - Unit testing framework
   * - Google Benchmark
     - Bazel central registry
     - Performance benchmarking
   * - score-docs-as-code
     - S-CORE registry
     - Documentation build tooling

Cross-Compilation Targets
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Target
     - Toolchain
     - Notes
   * - x86_64-linux
     - ``score-toolchains_gcc``
     - Primary development and CI target
   * - aarch64-linux
     - ``score-toolchains_gcc``
     - Raspberry Pi Linux (testing)
   * - aarch64-qnx
     - ``score-toolchains_qnx``
     - Raspberry Pi QNX 8.0 (production target)

Build Commands
--------------

.. code-block:: bash

   # Build all
   bazel build //...

   # Build for QNX
   bazel build //... --config=qnx

   # Test all
   bazel test //...

   # Coverage
   bazel coverage //score/mw/com/...

   # Format check
   bazel test //:format.check

   # License check
   bazel run //:copyright.check

Development Environment
=======================

:DevContainer: ``.devcontainer/`` configuration
:IDE: VS Code with Esbonio extension (for RST docs)
:Formatter: clang-format (C++), black (Python)
:Linter: clang-tidy (C++), pylint (Python)

Setup: See ``SETUP.md`` for prerequisites and workarounds.

CI/CD Pipeline
==============

:Platform: GitHub Actions
:Triggers: Pull request, push to main
:Matrix: Linux x86_64 (primary), QNX cross-compile (where applicable)

Pipeline stages:

1. **Format check** — clang-format, license headers
2. **Build** — ``bazel build //...``
3. **Unit tests** — ``bazel test //...``
4. **Integration tests** — Docker-based multi-process tests
5. **Static analysis** — clang-tidy
6. **Coverage** — lcov report
7. **Documentation** — Sphinx build verification

Artifact Management
===================

- Build artifacts: Bazel cache (remote cache in CI)
- Test results: JUnit XML in CI artifacts
- Coverage reports: lcov format, uploaded to CI artifacts
- Release packages: Published to S-CORE Bazel registry via tagged releases
