"""OpenBase Core Verifier — protocol-level evidence validation."""
import json, hashlib, zipfile
from pathlib import Path

def verify_evidence(path: str) -> dict:
"""Verify an OpenBase Evidence package. Returns {valid: bool, errors: [...], warnings: [...]}."""
errors, warnings = [], []

if not Path(path).exists():
return {"valid": False, "errors": ["File not found"], "warnings": []}

try:
with zipfile.ZipFile(path, 'r') as zf:
required = ["manifest.json", "session.json", "events.jsonl", "signature.sig"]
missing = [f for f in required if f not in zf.namelist()]
if missing:
errors.append(f"Missing required files: {missing}")
return {"valid": False, "errors": errors, "warnings": warnings}

events_text = zf.read("events.jsonl").decode("utf-8")
events = [json.loads(line) for line in events_text.strip().split("\n") if line.strip()]
if not events:
errors.append("events.jsonl is empty")

prev_hash = None
for i, event in enumerate(events):
if i == 0:
if event.get("prev_hash") is not None:
errors.append(f"Event[{i}]: genesis event prev_hash must be null")
else:
expected = events[i-1].get("hash", "")
actual = event.get("prev_hash", "")
if actual != expected:
errors.append(f"Event[{i}]: HashChain broken")

except zipfile.BadZipFile:
errors.append("Not a valid ZIP file")
except Exception as e:
errors.append(str(e))

return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}
