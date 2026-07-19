import os, json

base = r'D:\OpenBase'
spec_dir = os.path.join(base, 'openbase-spec', 'trust')
examples_dir = os.path.join(spec_dir, 'examples')
os.makedirs(examples_dir, exist_ok=True)

# --- Trust Specification ---
spec = '# OpenBase Trust Specification v1.0\n\n## Version\n**1.0**\n\n## Status\n**Draft**\n\n---\n\n## 1. Abstract\n\nThe Trust Layer defines how trust scores are computed for Runtimes, Agents, and other actors in the OpenBase ecosystem. Trust is derived from verifiable evidence, not subjective reputation.\n\n## 2. Trust Model\n\n### 2.1 Core Principle\n\nTrust = f(Evidence, Time, Consistency, Peer Verification)\n\nTrust is:\n- Evidence-based: only verified evidence counts\n- Time-weighted: recent evidence matters more\n- Decay-enabled: trust decays without fresh evidence\n- Multi-dimensional: not a single number\n\n### 2.2 Trust Dimensions\n\n| Dimension | Weight | Description |\n|:---|:---|:---|\n| evidence_volume | 0.30 | Quantity of valid evidence |\n| evidence_quality | 0.25 | Signature validity, hash integrity |\n| consistency | 0.20 | No contradictory events |\n| recency | 0.15 | Freshness of evidence |\n| peer_attestation | 0.10 | Certificates from trusted peers |\n\n### 2.3 Score Range\n\n- 0.00 - 0.20: Untrusted\n- 0.21 - 0.40: Low Trust\n- 0.41 - 0.60: Moderate Trust\n- 0.61 - 0.80: High Trust\n- 0.81 - 1.00: Fully Trusted\n\n### 2.4 Decay Function\n\nscore(t) = score(t0) * e^(-lambda * (t - t0))\n\nWhere lambda = 0.01 per day (configurable).\n\n## 3. Trust Update Events\n\nTrust scores update on:\n- New evidence accepted (+0.02 to +0.05)\n- Evidence rejected (-0.05 to -0.10)\n- Certificate issued (+0.05 to +0.15)\n- Certificate revoked (-0.10 to -0.20)\n- Time decay (continuous)\n\n## 4. Trust Graph\n\nTrust is not isolated. A Trust Graph models relationships:\n\n`\nRuntime A --vouches_for--> Agent A1\nRuntime B --vouches_for--> Agent B1\nAgent A1 --delegates_to--> Tool T1\n`\n\nTrust propagates through the graph via PageRank-like algorithm.\n\n## 5. References\n\n- Evidence v2.0 (evidence validation)\n- Certificate v1.0 (attestation)\n- Identity v1.0 (actor identification)\n'
with open(os.path.join(spec_dir, 'TRUST_SPEC_v1.0.md'), 'w', encoding='utf-8') as f:
    f.write(spec)
print('[1/4] Spec done')

# --- JSON Schema ---
schema = {
    "": "http://json-schema.org/draft-07/schema#",
    "": "https://openbase.dev/schemas/trust/v1.0/trust.schema.json",
    "title": "OpenBase Trust v1.0",
    "description": "Trust score for a Runtime or Agent",
    "type": "object",
    "required": ["subject_id", "subject_type", "score", "dimensions", "evidence_count", "last_updated"],
    "properties": {
        "subject_id": {"type": "string"},
        "subject_type": {"type": "string", "enum": ["runtime", "agent", "model", "tool"]},
        "score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "dimensions": {
            "type": "object",
            "properties": {
                "evidence_volume": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "evidence_quality": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "consistency": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "recency": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "peer_attestation": {"type": "number", "minimum": 0.0, "maximum": 1.0}
            }
        },
        "evidence_count": {"type": "integer", "minimum": 0},
        "last_evidence_id": {"type": "string"},
        "certificates": {
            "type": "array",
            "items": {"type": "string"}
        },
        "last_updated": {"type": "string", "format": "date-time"},
        "previous_score": {"type": "number"},
        "trend": {"type": "string", "enum": ["rising", "stable", "falling"]}
    },
    "additionalProperties": False
}
with open(os.path.join(spec_dir, 'trust.schema.json'), 'w', encoding='utf-8') as f:
    json.dump(schema, f, indent=2)
print('[2/4] Schema done')

# --- README ---
readme = '# OpenBase Trust v1.0\n\nDefines the trust scoring model for Runtimes and Agents in the OpenBase ecosystem.\n\n## Contents\n\n| File | Description |\n|:---|:---|\n| TRUST_SPEC_v1.0.md | Full specification |\n| trust.schema.json | JSON Schema |\n| examples/ | Example trust scores |\n'
with open(os.path.join(spec_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme)
print('[3/4] README done')

# --- Examples ---
examples = {
    "trust_high.json": {
        "subject_id": "runtime.openclaw.0.1.0",
        "subject_type": "runtime",
        "score": 0.85,
        "confidence": 0.90,
        "dimensions": {
            "evidence_volume": 0.90,
            "evidence_quality": 0.95,
            "consistency": 0.88,
            "recency": 0.80,
            "peer_attestation": 0.75
        },
        "evidence_count": 150,
        "last_evidence_id": "evid_f7e8d9c0b1a2",
        "certificates": ["cert_gold_001"],
        "last_updated": "2026-07-07T12:00:00Z",
        "previous_score": 0.83,
        "trend": "rising"
    },
    "trust_moderate.json": {
        "subject_id": "agent.newcomer.bot",
        "subject_type": "agent",
        "score": 0.45,
        "confidence": 0.50,
        "dimensions": {
            "evidence_volume": 0.30,
            "evidence_quality": 0.60,
            "consistency": 0.50,
            "recency": 0.70,
            "peer_attestation": 0.10
        },
        "evidence_count": 15,
        "last_updated": "2026-07-07T11:00:00Z",
        "previous_score": 0.40,
        "trend": "rising"
    },
    "trust_low.json": {
        "subject_id": "agent.untrusted.bot",
        "subject_type": "agent",
        "score": 0.15,
        "confidence": 0.80,
        "dimensions": {
            "evidence_volume": 0.05,
            "evidence_quality": 0.10,
            "consistency": 0.20,
            "recency": 0.30,
            "peer_attestation": 0.00
        },
        "evidence_count": 3,
        "last_updated": "2026-07-06T00:00:00Z",
        "previous_score": 0.22,
        "trend": "falling"
    }
}
for filename, data in examples.items():
    with open(os.path.join(examples_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
print('[4/4] Examples done')
