# Gap Lifecycle

## Purpose

Defines the lifecycle and resolution process for all gaps identified during Reference Runtime validation.

## Gap → PCP Integration

OBSERVED
    ↓
TRIAGED
    ↓
ASSIGNED
    ↓
PCP Required?
    ├── YES
    │       ↓
    │   PCP Submitted
    │       ↓
    │   PCP Accepted?
    │       ├── YES → Spec Updated
    │       └── NO  → Gap Rejected
    │
    └── NO
            ↓
        Runtime Fix
            ↓
        Verified
            ↓
        Closed

## Gap Resolution Types

| Resolution | Meaning |
| :--- | :--- |
|  + "RUNTIME" +  | Gap should be resolved in Reference Runtime |
|  + "SPEC" +  | Gap should be resolved in Protocol Specification |
|  + "PCP" +  | Gap requires Protocol Change Proposal |
|  + "REJECT" +  | Gap is intentionally not addressed |
|  + "FUTURE" +  | Gap will be addressed in a future version |
|  + "OBSERVE" +  | Gap is acceptable as-is, no action needed |

## Gap Severity Levels

| Severity | Meaning |
| :--- | :--- |
|  + "MUST" +  | Must be resolved before Certification |
|  + "SHOULD" +  | Should be resolved, but not blocking Certification |
|  + "MAY" +  | Optional resolution |

## Gap Record Format

| Field | Type | Description |
| :--- | :--- | :--- |
|  + "id" +  | string | GAP-XXX |
|  + "	itle" +  | string | Brief description |
|  + "severity" +  | enum | MUST / SHOULD / MAY |
|  + "esolution" +  | enum | RUNTIME / SPEC / PCP / REJECT / FUTURE / OBSERVE |
|  + "owner" +  | string | Responsible party |
|  + "status" +  | enum | OBSERVED / TRIAGED / ASSIGNED / RESOLVED / VERIFIED / CLOSED |
|  + "pcp" +  | string | Reference to PCP (if applicable) |
|  + "	arget_version" +  | string | Protocol version where resolved |
|  + "eferences" +  | list | Traceability IDs |

## Gap → PCP Relationship

GAP-012 → PCP-0001 → Spec Updated → GAP-012 Resolved
