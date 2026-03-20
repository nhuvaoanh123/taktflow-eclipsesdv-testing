---
document_id: TRACE-BL
title: "Bidirectional Traceability Matrix — score-baselibs"
version: "1.0"
status: draft
date: 2026-03-20
---

# Bidirectional Traceability Matrix

## Safety Chains

```
SG-BL-001: Memory Safety (ASIL-B)
├── FSR-BL-001: Bounds-Checked Shared Memory Access
│   ├── TSR-BL-001 → SSR-BL-SHM-001 → SWR-BL-SHM-001
│   └── TSR-BL-002 → SSR-BL-SHM-002 → SWR-BL-SHM-002
└── FSR-BL-002: No Dynamic Allocation on ASIL-B Path
    └── TSR-BL-003 → SSR-BL-CON-001 → SWR-BL-CON-001

SG-BL-002: Deterministic Execution (ASIL-B)
├── FSR-BL-003: Lock-Free Concurrency Primitives
│   └── TSR-BL-004 → SSR-BL-CON-002 → SWR-BL-CON-002
└── FSR-BL-004: Abort-on-Exception Policy
    └── TSR-BL-005 → SSR-BL-SAFE-001 → SWR-BL-SAFE-001

SG-BL-003: Platform Behavioral Equivalence (ASIL-B)
└── FSR-BL-005: OS Abstraction Behavioral Parity
    ├── TSR-BL-006 → SSR-BL-OS-001 → SWR-BL-OS-001 (Linux)
    └── TSR-BL-007 → SSR-BL-OS-002 → SWR-BL-OS-002 (QNX)
```

## Statistics

- **Total requirements**: 30 (3 SG + 5 FSR + 7 TSR + 7 SSR + 8 SWR)
- **Bidirectional links**: 56
- **Safety chains**: 7 complete SG→SWR
- **ASIL-B**: 100% of documented requirements
