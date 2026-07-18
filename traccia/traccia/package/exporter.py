"""
Package Exporter
Exports session + evidence as .evidence ZIP package.
"""

import json
import zipfile
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional


def export_package(
    session,
    evidence_chain: list,
    output_path: str,
    attribution: Optional[Dict] = None,
) -> str:
    """Export session and evidence as a .evidence ZIP package.

    Package structure:
        task.evidence
        ├── manifest.json
        ├── session.json
        ├── events.jsonl
        ├── evidence.json
        ├── attribution.json (optional)
        └── signature.sig

    Returns:
        Path to the created .evidence file.
    """
    if not output_path.endswith('.evidence'):
        output_path += '.evidence'

    manifest = {
        "version": "2.0.0",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "session_id": session.session_id if hasattr(session, 'session_id') else "unknown",
        "event_count": len(session.get_events()) if hasattr(session, 'get_events') else 0,
        "evidence_count": len(evidence_chain),
    }

    import hashlib
    events_jsonl = "\n".join(json.dumps(e, ensure_ascii=False) for e in session.get_events()) if hasattr(session, 'get_events') else ""

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False))
        zf.writestr('session.json', json.dumps(session.to_dict() if hasattr(session, 'to_dict') else {}, indent=2, ensure_ascii=False))
        zf.writestr('events.jsonl', events_jsonl)
        zf.writestr('evidence.json', json.dumps(evidence_chain, indent=2, ensure_ascii=False))
        if attribution:
            zf.writestr('attribution.json', json.dumps(attribution, indent=2, ensure_ascii=False))
        zf.writestr('signature.sig', hashlib.sha256(events_jsonl.encode()).hexdigest())

    return os.path.abspath(output_path)
