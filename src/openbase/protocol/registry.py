"""
Registry Protocol (RP) - v0.1
Global shared state for agents using CRDT principles
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class RegistryRecord:
    """注册表记录 - 最终一致性"""
    entity_id: str
    entity_type: str  # runtime | agent | execution | certificate
    state: Dict[str, Any] = field(default_factory=dict)
    version: int = 0
    node_id: str = "local"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "state": self.state,
            "version": self.version,
            "node_id": self.node_id,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RegistryRecord":
        return cls(
            entity_id=data["entity_id"],
            entity_type=data["entity_type"],
            state=data.get("state", {}),
            version=data.get("version", 0),
            node_id=data.get("node_id", "local"),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
        )


class CRDTMerge:
    """简单 CRDT 合并器 - 最后写入者胜出 + 版本向量"""

    @staticmethod
    def merge(current: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
        """合并两个状态，返回新状态"""
        merged = current.copy()
        for key, value in incoming.items():
            if key not in merged or _is_newer(value, merged[key]):
                merged[key] = value
        return merged


def _is_newer(a: Any, b: Any) -> bool:
    """判断 a 是否比 b 更新（简单版本比较）"""
    if isinstance(a, dict) and isinstance(b, dict):
        a_ver = a.get("version", 0)
        b_ver = b.get("version", 0)
        return a_ver > b_ver
    return True