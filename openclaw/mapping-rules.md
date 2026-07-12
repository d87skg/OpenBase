# Mapping Rules

**Asset-Type:** Reference Runtime
**Category:** Rules
**Status:** Frozen
**Version:** 1.0.0
**Date:** 2026-07-03

## 1. Purpose

Mapping Rules define the operational procedures used to map Runtime artifacts to Protocol specifications.

They do **not** define models (see Framework). They do **not** define validation (see Framework). They only define **how to map**.

## 2. Dependencies

This document depends on the Framework:

Framework
├── meta/
│   ├── asset-model.md
│   ├── terminology.md
│   └── mapping-template.md
├── validation/
│   ├── validation-model.md
│   ├── coverage-model.md
│   └── conformance-model.md
├── traceability/
│   └── traceability-model.md
└── governance/
    └── gap-lifecycle.md

All terms, statuses, and lifecycle definitions are referenced from Framework.

## 3. Operational Rules

| ID | Rule | Description |
| :--- | :--- | :--- |
| MR-001 | Inventory | List all Runtime artifacts (states, hooks, events, fields) |
| MR-002 | Map | Map each Runtime artifact to a Specification artifact |
| MR-003 | Classify Quality | Assign one of: DIRECT / SEMANTIC / GRANULAR / MISSING |
| MR-004 | Assign Validation | Assign Observation and Verification statuses |
| MR-005 | Create Traceability | Link to source file, line, test case, requirement |
| MR-006 | Record Gap | If no mapping exists, record a Gap in gap-analysis.md |
| MR-007 | Evaluate Conformance | Assess PASS / FAIL / N/A against requirements |
| MR-008 | Update Coverage | Update coverage counts in coverage model |

## 4. Mapping Workflow

Inventory
    │
    ▼
Map
    │
    ▼
Validate
    │
    ▼
Trace
    │
    ▼
Gap?
    ├── No
    │       │
    │       ▼
    │   Coverage
    │       │
    │       ▼
    │   Conformance
    │
    └── Yes
            │
            ▼
        Gap Lifecycle
            │
            ▼
        Conformance

## 5. Mapping Immutability

> Mappings are observational artifacts.

- Mappings describe Runtime behavior as observed.
- Mappings MUST NOT modify Runtime behavior.
- Mappings MUST NOT redefine Specification semantics.
- Specification changes MUST be handled through the PCP process.

**MR-009** Mappings are observational. They do not define, design, or modify. Specification changes require PCP.
