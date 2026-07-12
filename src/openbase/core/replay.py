import json
from pathlib import Path
from typing import List, Dict, Any


class ReplayEngine:
    """重放引擎 - 从证据重建执行过程"""

    def __init__(self, evidence_dir: str = "./evidence"):
        self.evidence_dir = Path(evidence_dir)
        self.evidence: List[Dict[str, Any]] = []

    def load(self) -> "ReplayEngine":
        if not self.evidence_dir.exists():
            return self

        for f in self.evidence_dir.glob("*.json"):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    self.evidence.append(json.load(fp))
            except Exception:
                pass

        self.evidence.sort(key=lambda x: x.get("timestamp", ""))
        return self

    def replay(self) -> Dict[str, Any]:
        if not self.evidence:
            return {"status": "FAILED", "reason": "No evidence loaded", "events": []}

        state = {}
        events = []

        for ev in self.evidence:
            event_type = ev.get("event_type", "UNKNOWN")
            event = {"event_type": event_type, "payload": ev.get("payload", {})}
            events.append(event)

            if event_type == "AGENT_STARTED":
                state["status"] = "running"
                state["agent"] = ev.get("agent_id", "unknown")
            elif event_type == "AGENT_FINISHED":
                state["status"] = "completed"

        return {"status": "SUCCESS", "events": events, "state": state}

    def get_state(self) -> Dict[str, Any]:
        return self.replay().get("state", {})
