# Conformance Model

## Purpose

Defines the conformance status taxonomy for all OpenBase Reference Runtime mappings.

## Conformance Status

| Status | Meaning |
| :--- | :--- |
|  + "PASS" +  | Requirement is satisfied |
|  + "FAIL" +  | Requirement is not satisfied |
|  + "N/A" +  | Requirement does not apply |

## Conformance Classes

| Class | Description |
| :--- | :--- |
|  + "CORE" +  | Minimum Implementation |
|  + "STANDARD" +  | Full Protocol Implementation |
|  + "ENTERPRISE" +  | Adds audit / replay / certification |
|  + "REFERENCE" +  | Official Reference Implementation |

## Conformance Report Format

{
  "implementation": "OpenClaw",
  "protocol_version": "1.0.0",
  "class": "STANDARD",
  "requirements": {
    "passed": 0,
    "failed": 0,
    "na": 0
  },
  "capabilities": {
    "replay": "causal",
    "verification": true,
    "determinism": "causal"
  }
}

## Validation vs Conformance

| Dimension | Scope | Example |
| :--- | :--- | :--- |
| **Validation** | Implementation → Evidence | Observed, Verified, Automated |
| **Conformance** | Implementation → Specification | PASS, FAIL, N/A |
| **Certification** | Implementation → Ecosystem | Candidate, Certified, Expired |

## References

- Validation Model: validation/validation-model.md
- Coverage Model: validation/coverage-model.md
