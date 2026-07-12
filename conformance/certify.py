"""OpenBase Certification — protocol-level conformance tool."""
import sys, json, hashlib, zipfile
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))
from reference.event_validator import validate_event
from reference.evidence_validator import validate_package_structure

def certify(evidence_path: str) -> dict:
    path = Path(evidence_path)
    if not path.exists():
        return {"status": "FAIL", "reason": "File not found"}
    
    struct_result = validate_package_structure(evidence_path)
    if not struct_result["valid"]:
        return {"status": "FAIL", "reason": "Structure validation failed", "details": struct_result["errors"]}
    
    with zipfile.ZipFile(evidence_path, "r") as zf:
        events_text = zf.read("events.jsonl").decode("utf-8")
        events = [json.loads(line) for line in events_text.strip().split("\n") if line.strip()]
        for i, event in enumerate(events):
            ev_result = validate_event(event)
            if not ev_result["valid"]:
                return {"status": "FAIL", "reason": f"Event[{i}] invalid", "details": ev_result["errors"]}
        
        session = json.loads(zf.read("session.json"))
    
    with open(evidence_path, "rb") as f:
        pkg_hash = hashlib.sha256(f.read()).hexdigest()
    
    badge_md = "[![OpenBase Certified](https://img.shields.io/badge/OpenBase-Certified-00AA00)](https://github.com/d87skg/OpenBase)"
    
    return {
        "status": "PASS",
        "package_hash": pkg_hash[:16],
        "session_id": session.get("session_id", ""),
        "objective": session.get("objective", ""),
        "event_count": len(events),
        "certified_at": datetime.now(timezone.utc).isoformat(),
        "badge_markdown": badge_md,
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: openbase-certify <task.evidence>")
        sys.exit(1)
    result = certify(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] == "PASS":
        print(f"\nAdd this badge to your README:\n{result['badge_markdown']}")
