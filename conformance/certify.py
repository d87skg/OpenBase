"""OpenBase Conformance Certifier — generates certification badge."""
import sys, json, hashlib
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(file).parent.parent))
from core.verify import verify_evidence

def certify(evidence_path: str) -> dict:
path = Path(evidence_path)
if not path.exists():
return {"status": "FAIL", "reason": "File not found"}

result = verify_evidence(evidence_path)
if not result["valid"]:
return {"status": "FAIL", "reason": "Verification failed", "details": result["errors"]}

with open(evidence_path, "rb") as f:
pkg_hash = hashlib.sha256(f.read()).hexdigest()

with zipfile.ZipFile(evidence_path, "r") as zf:
session = json.loads(zf.read("session.json"))
events_text = zf.read("events.jsonl").decode("utf-8")
event_count = len([l for l in events_text.strip().split("\n") if l.strip()])

badge_md = "https://img.shields.io/badge/OpenBase-Compatible-00AA00"

return {
"status": "PASS",
"package_hash": pkg_hash[:16],
"session_id": session.get("session_id", ""),
"objective": session.get("objective", ""),
"event_count": event_count,
"certified_at": datetime.now(timezone.utc).isoformat(),
"badge_markdown": badge_md,
}

if name == "main":
if len(sys.argv) < 2:
print("Usage: python certify.py <task.evidence>")
sys.exit(1)
result = certify(sys.argv[1])
print(json.dumps(result, indent=2, ensure_ascii=False))
if result["status"] == "PASS":
print(f"\nAdd this badge to your README:\n{result['badge_markdown']}")
