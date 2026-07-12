# Coverage Model

## Purpose

Defines how coverage is measured across all OpenBase Protocol assets.

## Coverage Dimensions

| Dimension | Measures |
| :--- | :--- |
| **Specification** | Protocol requirements defined in specs |
| **Schema** | Protocol schema defined |
| **Implementation** | Runtime features implemented |
| **Tests** | Automated test coverage |
| **Evidence** | Evidence emitted during execution |
| **Conformance** | Formal conformance status |

## Coverage Metrics Format

Use concrete counts:

Specification:   18 requirements defined
Implementation:  18 requirements implemented
Tests:           16 requirements have tests
Evidence:        15 requirements emit evidence
Conformance:     Pending

## Coverage Asset Matrix

| Asset | Specification | Schema | Implementation | Tests | Evidence | Conformance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Execution | 18/18 | 1/1 | 18/18 | 16/18 | 15/18 | Pending |
| Evidence | 10/10 | 1/1 | 10/10 | 10/10 | 10/10 | Pending |
| Replay | TBD | TBD | TBD | TBD | TBD | TBD |

## Coverage Principle

> Coverage is measured against requirements, not against code.

- Missing tests do not lower coverage if the requirement is met by existing evidence.
- Missing evidence lowers coverage.
- Missing implementation lowers coverage.
