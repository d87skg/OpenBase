
OpenBase Conformance Specification v1.0
Status
Core — immutable.

Definition
Conformance verifies that an OpenBase Evidence package meets the protocol standard.

Certification Steps
Verify ZIP structure (manifest.json, session.json, events.jsonl, signature.sig)

Validate HashChain integrity

Check required event fields

Output: PASS / FAIL with details

Certification Tool
bash
python conformance/certify.py <task.evidence>
Output:

PASS: [![OpenBase Compatible](badge-url)](repo-url)

FAIL: reason + details
