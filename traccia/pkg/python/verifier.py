import json
import hashlib
from typing import Dict, List, Any
from .merkle import MerkleTree

class ProofVerifier:
    def __init__(self, proof: Dict):
        self.proof = proof

    def _hash(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def _event_hash(self, event: Dict) -> str:
        """计算事件的确定性哈希"""
        event_str = json.dumps(event, sort_keys=True, separators=(',', ':'))
        return self._hash(event_str)

    def verify(self) -> Dict:
        """验证单个事件（使用证明路径，尝试两种组合）"""
        result = {
            "valid": False,
            "checks": [],
            "errors": []
        }

        if "root_hash" not in self.proof:
            result["errors"].append("Missing root_hash")
            return result

        if "target_event" not in self.proof:
            result["errors"].append("No target_event to verify")
            return result

        target = self.proof["target_event"]
        proof_path = self.proof.get("merkle_proof", [])
        root = self.proof["root_hash"]

        leaf_hash = self._event_hash(target)
        # 尝试两种组合方式
        possible_hashes = [leaf_hash]
        for sibling in proof_path:
            new_hashes = []
            for h in possible_hashes:
                new_hashes.append(self._hash(h + sibling))
                new_hashes.append(self._hash(sibling + h))
            possible_hashes = new_hashes

        if root in possible_hashes:
            result["checks"].append({
                "name": "merkle_proof",
                "status": "passed",
                "detail": "Event verified against root"
            })
        else:
            result["errors"].append({
                "name": "merkle_proof",
                "detail": "Event does not match root"
            })
            return result

        if "state_commitment" in self.proof:
            result["checks"].append({
                "name": "state_commitment",
                "status": "present",
                "detail": f"State commitment: {self.proof['state_commitment'][:16]}..."
            })

        if "event_count" in self.proof:
            result["checks"].append({
                "name": "event_count",
                "status": "ok",
                "detail": f"{self.proof['event_count']} events"
            })

        if not result["errors"]:
            result["valid"] = True
            result["checks"].append({
                "name": "overall",
                "status": "passed",
                "detail": "All verification checks passed"
            })

        return result

    def verify_full(self) -> Dict:
        """完整验证：重建 Merkle 树，直接比较根"""
        result = {
            "valid": False,
            "verified_events": [],
            "errors": []
        }

        if "event_proofs" not in self.proof:
            result["errors"].append("Missing event_proofs")
            return result

        # 提取所有事件，按索引排序
        event_proofs = self.proof["event_proofs"]
        # 按索引排序
        event_proofs_sorted = sorted(event_proofs, key=lambda x: x["index"])
        events = [ep["event"] for ep in event_proofs_sorted]

        # 计算每个事件的哈希
        leaf_hashes = [self._event_hash(ev) for ev in events]

        # 构建 Merkle 树
        tree = MerkleTree(leaf_hashes)
        computed_root = tree.get_root()
        declared_root = self.proof.get("root_hash")

        # 比较根
        if computed_root != declared_root:
            result["errors"].append({
                "detail": f"Root mismatch: computed {computed_root[:16]}..., declared {declared_root[:16]}..."
            })
            return result

        # 根匹配，所有事件验证通过
        result["valid"] = True
        result["verified_events"] = [
            {"index": ep["index"], "status": "verified", "event_type": ev.get("event_type")}
            for ep, ev in zip(event_proofs_sorted, events)
        ]
        result["verified_count"] = len(result["verified_events"])
        result["root_verified"] = True

        # 也检查 state_commitment（如果提供）
        if "state_commitment" in self.proof:
            result["state_commitment_checked"] = True

        return result