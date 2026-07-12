# Framework Overview

## Purpose

This directory defines the **validation and conformance infrastructure** for the OpenBase Protocol.

It provides the shared models, rules, and processes used by all Reference Runtime validation assets.

## Directory Structure

| Directory | Responsibility |
| :--- | :--- |
|  + "meta/" +  | Defines **what** things are (Asset Model, Terminology, Template) |
|  + "alidation/" +  | Defines **how** things are validated (Validation Model, Coverage Model, Conformance Model) |
|  + "	raceability/" +  | Defines **how** things are traced (Traceability Model) |
|  + "governance/" +  | Defines **how** things evolve (Gap Lifecycle) |

## Layer Responsibilities

| Layer | Responsibility |
| :--- | :--- |
| **Meta** | Object definitions, terminology, document templates |
| **Framework** | Shared models for validation, coverage, conformance, traceability, governance |
| **Rules** | Mapping rules that reference the Framework |
| **Mappings** | Runtime → Specification traceability documents |
| **Reports** | Conformance reports and compatibility matrix |

## Document Relationships

meta/
    ├── asset-model.md
    ├── terminology.md
    └── mapping-template.md
        ↓
validation/
    ├── validation-model.md
    ├── coverage-model.md
    └── conformance-model.md
        ↓
traceability/
    └── traceability-model.md
        ↓
governance/
    └── gap-lifecycle.md
        ↓
mapping-rules.md
        ↓
execution-mapping.md
evidence-mapping.md
replay-mapping.md
determinism-mapping.md
        ↓
gap-analysis.md
        ↓
conformance-report.md
compatibility-matrix.md

## Lifecycle

Meta → Framework → Rules → Mappings → Reports → Certification

All assets in this directory are stable and should not change without a PCP.
