import json
import hashlib
import uuid
from datetime import datetime
from typing import List, Dict, Any
from .merkle import MerkleTree

class ProofGenerator:
    def __init__(self, events: List[Dict], execution_id: str):
        self.events = events
        self.execution_id = execution_id
        self._event_hashes = [self._event_hash(e) for e in events]
        self.merkle = MerkleTree(self._event_hashes)

    def _event_hash(self, event: Dict) -> str:
        """为单个事件生成唯一哈希"""
        # 规范化事件（排序键）
        event_str = json.dumps(event, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(event_str.encode()).hexdigest()

    def _state_hash(self) -> str:
        """计算最终状态的哈希"""
        # 提取关键状态字段
        state = {
            "execution_id": self.execution_id,
            "event_count": len(self.events),
            "last_timestamp": self.events[-1].get("timestamp") if self.events else None,
            "last_event": self.events[-1].get("event_type") if self.events else None
        }
        state_str = json.dumps(state, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(state_str.encode()).hexdigest()

    def generate_proof(self, event_index: int = -1) -> Dict:
        """生成执行证明"""
        if not self.events:
            return {"error": "No events to prove"}
        
        if event_index == -1:
            event_index = len(self.events) - 1  # 默认最后一个事件
        
        if event_index < 0 or event_index >= len(self.events):
            raise ValueError("Invalid event index")
        
        # 获取该事件的 Merkle 证明路径
        proof_path = self.merkle.get_proof(event_index)
        
        return {
            "execution_id": self.execution_id,
            "root_hash": self.merkle.get_root(),
            "state_commitment": self._state_hash(),
            "event_count": len(self.events),
            "target_event": self.events[event_index],
            "target_index": event_index,
            "merkle_proof": proof_path,
            "timestamp": datetime.now().isoformat(),
            "signature_placeholder": "pending"  # 后续集成签名
        }

    def generate_full_proof(self) -> Dict:
        """生成完整的执行证明（包含所有事件的验证路径）"""
        return {
            "execution_id": self.execution_id,
            "root_hash": self.merkle.get_root(),
            "state_commitment": self._state_hash(),
            "event_count": len(self.events),
            "event_proofs": [
                {
                    "index": i,
                    "event": self.events[i],
                    "proof": self.merkle.get_proof(i)
                }
                for i in range(len(self.events))
            ],
            "timestamp": datetime.now().isoformat()
        }