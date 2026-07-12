# Asset Model

## Purpose

Defines the core objects used across all OpenBase protocol validation assets.

## Core Objects

### Requirement

| Field | Type | Description |
| :--- | :--- | :--- |
|  + "id" +  | string | Unique identifier (REQ-XXX) |
|  + "level" +  | enum | MUST / SHOULD / MAY |
|  + "source" +  | string | Specification section |
|  + "status" +  | enum | Active / Deprecated / Superseded |
|  + "eferences" +  | list | Related requirements |

### Mapping

| Field | Type | Description |
| :--- | :--- | :--- |
|  + "id" +  | string | Unique identifier (MAP-XXX) |
|  + "source" +  | string | Runtime element (hook / state / field) |
|  + "	arget" +  | string | Specification element (state / event / field) |
|  + "quality" +  | enum | DIRECT / SEMANTIC / GRANULAR / MISSING |
|  + "alidation" +  | enum | OBSERVED / VERIFIED / AUTOMATED |
|  + "
ormative" +  | enum | MAPPED / CONFORMANT / CERTIFIED |
|  + "	raceability" +  | list | Source file, line, test case |

### Gap

| Field | Type | Description |
| :--- | :--- | :--- |
|  + "id" +  | string | Unique identifier (GAP-XXX) |
|  + "severity" +  | enum | MUST / SHOULD / MAY |
|  + "esolution" +  | enum | RUNTIME / SPEC / PCP / REJECT / FUTURE / OBSERVE |
|  + "owner" +  | string | Responsible party |
|  + "status" +  | enum | OBSERVED / TRIAGED / ASSIGNED / RESOLVED / VERIFIED / CLOSED |
|  + "pcp" +  | string | Reference to PCP (if applicable) |
|  + "	arget_version" +  | string | Protocol version where resolved |
|  + "eferences" +  | list | Traceability IDs |

### Test Vector

| Field | Type | Description |
| :--- | :--- | :--- |
|  + "id" +  | string | Unique identifier (VEC-XXX) |
|  + "lgorithm" +  | string | Hash / Signature algorithm |
|  + "input" +  | object | Canonical input |
|  + "expected_output" +  | string | Expected result |
|  + "source" +  | string | Reference generator |

### Conformance Report

| Field | Type | Description |
| :--- | :--- | :--- |
|  + "implementation" +  | string | Runtime name |
|  + "protocol_version" +  | string | OBP version |
|  + "class" +  | enum | CORE / STANDARD / ENTERPRISE / REFERENCE |
|  + "equirements" +  | object | Pass / Fail / N/A counts |
|  + "capabilities" +  | object | Declared capability profile |
|  + "	imestamp" +  | string | Report generation time |

### Compatibility Record

| Field | Type | Description |
| :--- | :--- | :--- |
|  + "untime" +  | string | Runtime name |
|  + "protocol_version" +  | string | OBP version |
|  + "execution" +  | enum | PASS / PARTIAL / FAIL / N/A |
|  + "evidence" +  | enum | PASS / PARTIAL / FAIL / N/A |
|  + "eplay" +  | enum | PASS / PARTIAL / FAIL / N/A |
|  + "erification" +  | enum | PASS / PARTIAL / FAIL / N/A |
|  + "determinism" +  | enum | PASS / PARTIAL / FAIL / N/A |
|  + "certification" +  | enum | PASS / PARTIAL / FAIL / N/A |
|  + "coverage" +  | string | Coverage summary |
|  + "ersion" +  | string | Runtime version |
