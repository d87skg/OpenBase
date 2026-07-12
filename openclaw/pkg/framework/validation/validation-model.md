# Validation Model

## Purpose

Defines the validation status taxonomy for all OpenBase Reference Runtime mappings.

## Two Dimensions

Validation is evaluated along two independent dimensions:

### 1. Observation (事实层)

| Status | Meaning |
| :--- | :--- |
|  + "OBSERVED" +  | Behavior observed in Runtime source code |
|  + "REPRODUCED" +  | Observed behavior confirmed by manual reproduction |
|  + "AUTOMATED" +  | Reproduced behavior has CI coverage |

### 2. Verification (验证层)

| Status | Meaning |
| :--- | :--- |
|  + "UNCHECKED" +  | Not yet verified |
|  + "VERIFIED" +  | Verified by automated test |
|  + "REJECTED" +  | Verified but found invalid |

## Combined Status Matrix

| Observation \ Verification | UNCHECKED | VERIFIED | REJECTED |
| :--- | :--- | :--- | :--- |
| OBSERVED | Observed, not verified | Verified manually | Invalid |
| REPRODUCED | Reproduced, not verified | Verified, test exists | Invalid, documented |
| AUTOMATED | In CI, not verified | Verified by CI | Invalid, CI failing |

## Validation Graph

Requirement → Specification → Schema → Mapping → Implementation → Source → Test → Evidence → Conformance Report → Certification

Each node is independently verifiable.

## References

- Conformance Model: validation/conformance-model.md
- Coverage Model: validation/coverage-model.md
- Traceability Model: traceability/traceability-model.md
