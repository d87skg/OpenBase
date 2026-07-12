# Gap Analysis

**Asset-Type:** Reference Runtime
**Category:** Gap Registry
**Status:** Draft
**Version:** 1.0.0
**Date:** 2026-07-03

## Purpose

This is the **single source of truth** for all gaps identified during Reference Runtime validation.

All Mapping documents (Execution, Evidence, Replay, Determinism) reference gaps here by ID.

## Gap Registry

| ID | Title | Severity | Resolution | Owner | Status | PCP | Target Version |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| GAP-001 | PLANNING/THINKING granularity | SHOULD | OBSERVE | Architect | OBSERVED | — | — |
| GAP-002 | INTERRUPTED vs SUSPENDED semantics | SHOULD | OBSERVE | Architect | OBSERVED | — | — |
| GAP-003 | MEMORY_READ event missing | SHOULD | PCP | Protocol Steward | TRIAGED | PCP-0001 | 1.1.0 |
| GAP-004 | RETRY event missing | MAY | PCP | Protocol Steward | TRIAGED | PCP-0001 | 1.1.0 |
| GAP-005 | RESUMED event missing | MAY | PCP | Protocol Steward | TRIAGED | PCP-0001 | 1.1.0 |
| GAP-006 | PLAN_CREATED event missing | MAY | PCP | Protocol Steward | TRIAGED | PCP-0001 | 1.1.0 |
| GAP-007 | PLAN_UPDATED event missing | MAY | PCP | Protocol Steward | TRIAGED | PCP-0001 | 1.1.0 |
| GAP-008 | POLICY_DECISION event missing | SHOULD | PCP | Protocol Steward | TRIAGED | PCP-0001 | 1.1.0 |
| GAP-009 | STATE_UPDATE partial coverage | SHOULD | RUNTIME | Maintainer | ASSIGNED | — | 1.0.1 |
| GAP-010 | Determinism profile not declared | MUST | RUNTIME | Maintainer | ASSIGNED | — | 1.0.1 |

## Gap Statistics

| Severity | Open | In Progress | Closed |
| :--- | :--- | :--- | :--- |
| MUST | 0 | 2 | 0 |
| SHOULD | 3 | 1 | 0 |
| MAY | 4 | 0 | 0 |

| Resolution | Count |
| :--- | :--- |
| PCP | 6 |
| RUNTIME | 2 |
| OBSERVE | 2 |
| REJECT | 0 |
| FUTURE | 0 |

## Gap → PCP Mapping

| Gap | PCP | Status |
| :--- | :--- | :--- |
| GAP-003 | PCP-0001 | Open |
| GAP-004 | PCP-0001 | Open |
| GAP-005 | PCP-0001 | Open |
| GAP-006 | PCP-0001 | Open |
| GAP-007 | PCP-0001 | Open |
| GAP-008 | PCP-0001 | Open |

## References

- Gap Lifecycle: framework/governance/gap-lifecycle.md
- Asset Model: framework/meta/asset-model.md
- PCP Process: governance/processes/pcp.md
