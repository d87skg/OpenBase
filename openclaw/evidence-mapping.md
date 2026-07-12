# Evidence Mapping

**Asset-Type:** Reference Runtime
**Category:** Mapping
**Status:** Draft
**Version:** 1.0.0
**Date:** 2026-07-03
**Related:** mapping-rules.md, runtime-inventory.md, evidence.md

## 1. Purpose

This document maps OpenClaw Runtime observable behaviors to OpenBase Evidence Specification v1.0.

All mappings follow the rules defined in  + "mapping-rules.md" + .

## 2. Observable Action → Evidence Event

| ID | Observable Action | Evidence Event | Status |
| :--- | :--- | :--- | :--- |
| EM-001 | Execution Created | AGENT_STARTED | Verified |
| EM-002 | LLM Request | LLM_CALL | Verified |
| EM-003 | LLM Response | LLM_RESPONSE | Verified |
| EM-004 | Tool Invocation | TOOL_CALL | Verified |
| EM-005 | Tool Result | TOOL_RESULT | Verified |
| EM-006 | Memory Read | MEMORY_READ | Gap |
| EM-007 | Memory Write | MEMORY_UPDATE | Verified |
| EM-008 | Error Raised | ERROR | Verified |
| EM-009 | Execution Finished | AGENT_FINISHED | Verified |

## 3. Evidence Field Mapping

| Runtime Field | Evidence Field | Required | Mapping |
| :--- | :--- | :--- | :--- |
| execution_id | execution_id | MUST | DIRECT |
| agent_id | agent_id | MUST | DIRECT |
| event_type | event_type | MUST | DIRECT |
| payload | payload | MUST | DIRECT |
| timestamp | timestamp | MUST | DIRECT |
| parent_id | parent_id | SHOULD | DIRECT |
| vector_clock | vector_clock | MUST | DIRECT |
| hash | hash | MUST | DIRECT |
| signature | signature | MUST | DIRECT |
| public_key | public_key | MUST | DIRECT |

## 4. Gap Summary

Refer to  + "eference-runtime/gap-analysis.md" +  for all gaps.

## 5. References

- Evidence Specification: protocol/specs/evidence.md
- Mapping Rules: reference-runtime/mapping-rules.md
- Runtime Inventory: reference-runtime/runtime-inventory.md
- Gap Analysis: reference-runtime/gap-analysis.md
