import json
import uuid
from pathlib import Path


class CertificateEngine:
    def __init__(self, evidence_dir: str = "./evidence"):
        self.evidence_dir = Path(evidence_dir)

    def issue(self, level: str = "BRONZE") -> dict:
        cert = {
            "certificate_id": str(uuid.uuid4()),
            "level": level,
            "status": "ACTIVE"
        }

        out = Path("./reports")
        out.mkdir(exist_ok=True)

        file = out / f"cert-{cert['certificate_id']}.json"
        file.write_text(json.dumps(cert, indent=2))

        return cert
