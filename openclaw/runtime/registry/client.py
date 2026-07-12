#!/usr/bin/env python3
"""
Local Registry Client
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List


class RegistryClient:
    """本地 Registry 客户端"""

    def __init__(self, registry_dir: str = "./.openbase/registry"):
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self._runtimes_file = self.registry_dir / "runtimes.json"
        self._evidence_file = self.registry_dir / "evidence_index.json"

    def _load_json(self, filepath: Path) -> Dict:
        if filepath.exists():
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_json(self, filepath: Path, data: Dict) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def register_runtime(self, name: str, version: str, vendor: str,
                         capabilities: List[str] = None) -> Dict[str, Any]:
        runtimes = self._load_json(self._runtimes_file)

        runtime_id = f"rt-{uuid.uuid4().hex[:8]}"
        runtime = {
            "runtime_id": runtime_id,
            "name": name,
            "version": version,
            "vendor": vendor,
            "capabilities": capabilities or [],
            "registered_at": datetime.now().isoformat(),
            "status": "ACTIVE"
        }

        runtimes[runtime_id] = runtime
        if "by_name" not in runtimes:
            runtimes["by_name"] = {}
        runtimes["by_name"][name] = runtime_id

        self._save_json(self._runtimes_file, runtimes)
        print(f"✅ Runtime 已注册: {name} ({runtime_id})")
        return runtime

    def get_runtime(self, runtime_id: str) -> Optional[Dict[str, Any]]:
        runtimes = self._load_json(self._runtimes_file)
        return runtimes.get(runtime_id)

    def get_runtime_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        runtimes = self._load_json(self._runtimes_file)
        runtime_id = runtimes.get("by_name", {}).get(name)
        if runtime_id:
            return runtimes.get(runtime_id)
        return None

    def list_runtimes(self) -> List[Dict[str, Any]]:
        runtimes = self._load_json(self._runtimes_file)
        result = []
        for key, value in runtimes.items():
            if key not in ["by_name"]:
                result.append(value)
        return result

    def index_evidence(self, evidence_id: str, runtime_id: str,
                       event_type: str, timestamp: str) -> None:
        index = self._load_json(self._evidence_file)

        if "evidence" not in index:
            index["evidence"] = {}

        index["evidence"][evidence_id] = {
            "evidence_id": evidence_id,
            "runtime_id": runtime_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "indexed_at": datetime.now().isoformat()
        }

        self._save_json(self._evidence_file, index)

    def list_evidence(self, runtime_id: Optional[str] = None) -> List[Dict]:
        index = self._load_json(self._evidence_file)
        evidence_list = list(index.get("evidence", {}).values())

        if runtime_id:
            evidence_list = [e for e in evidence_list if e.get("runtime_id") == runtime_id]

        return evidence_list

    def get_runtime_evidence_count(self, runtime_id: str) -> int:
        return len(self.list_evidence(runtime_id))

    def get_summary(self) -> Dict[str, Any]:
        runtimes = self.list_runtimes()
        evidence = self.list_evidence()
        return {
            "total_runtimes": len(runtimes),
            "total_evidence": len(evidence),
            "runtimes": runtimes
        }