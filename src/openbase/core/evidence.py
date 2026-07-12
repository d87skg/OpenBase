import json
import uuid
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List


class EvidenceEngine:
    """证据引擎 - 生成、验证、存储 Evidence"""

    def __init__(self, agent_id: str, output_dir: str = "./evidence"):
        self.agent_id = agent_id
        self.run_id = str(uuid.uuid4())
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._evidence: List[Dict[str, Any]] = []
        self._previous_hash: Optional[str] = None

    def emit(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """生成一条 Evidence"""
        evidence_id = f"evid-{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()

        # 构建证据
        evidence = {
            "evidence_id": evidence_id,
            "spec_version": "1.0",
            "agent_id": self.agent_id,
            "run_id": self.run_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "payload": payload,
            "proof": {
                "hash": self._compute_hash(payload),
                "signature": "ed25519:reference_runtime_signature"
            }
        }

        # 存储到内存和文件
        self._evidence.append(evidence)
        self._save(evidence)

        return evidence

    def _compute_hash(self, payload: Dict[str, Any]) -> str:
        content = json.dumps(payload, sort_keys=True)
        return f"sha256:{hashlib.sha256(content.encode()).hexdigest()}"

    def _save(self, evidence: Dict[str, Any]) -> None:
        filepath = self.output_dir / f"{evidence['evidence_id']}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)

    def get_all(self) -> List[Dict[str, Any]]:
        return self._evidence

    def count(self) -> int:
        return len(self._evidence)
