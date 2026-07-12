"""
OpenBase Registry - In-Memory Storage
"""

from typing import Optional, List, Dict, Any
from .base_store import BaseStore


class MemoryStore(BaseStore):
    """内存存储实现（用于开发/测试）"""

    def __init__(self):
        self._data: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def _ensure_collection(self, collection: str) -> None:
        if collection not in self._data:
            self._data[collection] = {}

    def create(self, collection: str, data: Dict[str, Any]) -> str:
        self._ensure_collection(collection)
        doc_id = data.get("id") or data.get("runtime_id") or data.get("cert_id") or data.get("evidence_id")
        if not doc_id:
            import uuid
            doc_id = str(uuid.uuid4())
            data["id"] = doc_id
        self._data[collection][doc_id] = data
        return doc_id

    def get(self, collection: str, id: str) -> Optional[Dict[str, Any]]:
        self._ensure_collection(collection)
        return self._data[collection].get(id)

    def list(self, collection: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        self._ensure_collection(collection)
        items = list(self._data[collection].values())
        if filters:
            result = []
            for item in items:
                match = True
                for key, value in filters.items():
                    if item.get(key) != value:
                        match = False
                        break
                if match:
                    result.append(item)
            return result
        return items

    def update(self, collection: str, id: str, data: Dict[str, Any]) -> bool:
        self._ensure_collection(collection)
        if id not in self._data[collection]:
            return False
        if "id" in data:
            del data["id"]
        self._data[collection][id].update(data)
        return True

    def delete(self, collection: str, id: str) -> bool:
        self._ensure_collection(collection)
        if id not in self._data[collection]:
            return False
        del self._data[collection][id]
        return True

    def query(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return self.list(collection, query)
