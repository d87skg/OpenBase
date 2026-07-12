"""
OpenBase Registry - Runtime Service
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from ..models import Runtime, RuntimeStatus, RuntimeClass
from ..storage import BaseStore


class RuntimeService:
    def __init__(self, store: BaseStore):
        self.store = store
        self._collection = "runtimes"

    def register(self, name: str, version: str, vendor: str,
                 runtime_class: RuntimeClass = RuntimeClass.STANDARD,
                 capabilities: List[str] = None,
                 description: str = None,
                 metadata: Dict[str, Any] = None) -> Runtime:
        runtime_id = f"runtime-{uuid.uuid4().hex[:8]}"
        runtime = Runtime(
            runtime_id=runtime_id,
            name=name,
            version=version,
            vendor=vendor,
            runtime_class=runtime_class,
            capabilities=capabilities or [],
            description=description,
            metadata=metadata or {}
        )
        self.store.create(self._collection, runtime.to_dict())
        return runtime

    def get(self, runtime_id: str) -> Optional[Runtime]:
        data = self.store.get(self._collection, runtime_id)
        if data:
            return Runtime.from_dict(data)
        return None

    def get_by_name(self, name: str) -> Optional[Runtime]:
        items = self.store.list(self._collection, {"name": name})
        if items:
            return Runtime.from_dict(items[0])
        return None

    def list_all(self, status: Optional[RuntimeStatus] = None) -> List[Runtime]:
        filters = {}
        if status:
            filters["status"] = status.value
        items = self.store.list(self._collection, filters)
        return [Runtime.from_dict(item) for item in items]

    def update(self, runtime_id: str, **kwargs) -> bool:
        current = self.get(runtime_id)
        if not current:
            return False
        update_data = {}
        for key, value in kwargs.items():
            if key in ["name", "version", "vendor", "status", "runtime_class", "capabilities", "description", "metadata"]:
                # 如果是枚举，转换为值
                if hasattr(value, 'value'):
                    value = value.value
                update_data[key] = value
        update_data["updated_at"] = datetime.now().isoformat()
        return self.store.update(self._collection, runtime_id, update_data)

    def delete(self, runtime_id: str) -> bool:
        return self.store.delete(self._collection, runtime_id)

    def add_capability(self, runtime_id: str, capability: str) -> bool:
        runtime = self.get(runtime_id)
        if not runtime:
            return False
        if capability not in runtime.capabilities:
            runtime.capabilities.append(capability)
            return self.update(runtime_id, capabilities=runtime.capabilities)
        return True
