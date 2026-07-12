# Mapping Template

## Purpose

Standard template for all OpenBase protocol mapping documents.

## Template Structure

 + "`markdown" + 
---
Asset-Type: Reference Runtime
Category: Mapping
Status: Draft
Version: 1.0.0
Date: YYYY-MM-DD
Related: mapping-rules.md, runtime-inventory.md, [spec].md
---

# [Asset] Mapping

## 1. Purpose

[One paragraph describing the purpose of this mapping.]

## 2. Methodology

This mapping follows:

- Validation Model: framework/validation/validation-model.md
- Traceability Model: framework/traceability/traceability-model.md
- Gap Lifecycle: framework/governance/gap-lifecycle.md
- Coverage Model: framework/validation/coverage-model.md
- Asset Model: framework/meta/asset-model.md
- Terminology: framework/meta/terminology.md

## 3. Mappings

### MAP-XXX-001

| Field | Value |
| :--- | :--- |
| **Source** | [Runtime element] |
| **Target** | [Spec element] |
| **Quality** | DIRECT / SEMANTIC / GRANULAR / MISSING |
| **Validation** | OBSERVED / VERIFIED / AUTOMATED |
| **Normative** | MAPPED / CONFORMANT / CERTIFIED |
| **Traceability** |  + "source/file:line, 	est/file::test_case" +  |
| **Gap** | GAP-XXX (if applicable) |
| **Evidence** | [Evidence event] |

## 4. Coverage Summary

| Dimension | Count |
| :--- | :--- |
| Specification | X / Y |
| Implementation | X / Y |
| Tests | X / Y |
| Evidence | X / Y |
| Certification | Pending |

## 5. Gap Summary

| ID | Title | Severity | Resolution | Status |
| :--- | :--- | :--- | :--- | :--- |
| GAP-XXX | ... | MUST | RUNTIME | OPEN |

## 6. Conformance Impact

| Requirement | Status | Notes |
| :--- | :--- | :--- |
| REQ-XXX-001 | PASS / FAIL / N/A | ... |

## 7. Traceability

[Optional: Traceability graph showing Requirement → Spec → Mapping → Source → Test]

## 8. References

- [Spec]: protocol/specs/[spec].md
- Mapping Rules: reference-runtime/mapping-rules.md
- Runtime Inventory: reference-runtime/runtime-inventory.md
- Gap Analysis: reference-runtime/gap-analysis.md
 + "`" + 

## Template Usage

1. Copy this template to a new mapping document.
2. Replace  + "[Asset]" +  with the mapped asset (Execution, Evidence, Replay, Determinism, etc.).
3. Fill in all sections with actual data.
4. Mark status as  + "Draft" +  until reviewed.
5. Mark status as  + "Frozen" +  after review and consensus.
