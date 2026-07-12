"""
OpenBase Registry - Runtime Model
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class RuntimeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DEPRECATED = "DEPRECATED"
    SUSPENDED = "SUSPENDED"


class RuntimeClass(str, Enum):
    CORE = "CORE"
    STANDARD = "STANDARD"
    ENTERPRISE = "ENTERPRISE"
    REFERENCE = "REFERENCE"


@dataclass
class Runtime:
    runtime_id: str
    name: str
    version: str
    vendor: str
    status: RuntimeStatus = RuntimeStatus.ACTIVE
    runtime_class: RuntimeClass = RuntimeClass.STANDARD
    capabilities: List[str] = field(default_factory=list)
    description: Optional[str] = None
    registered_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        # 确保 runtime_class 是字符串
        runtime_class_value = self.runtime_class.value if hasattr(self.runtime_class, 'value') else self.runtime_class
        status_value = self.status.value if hasattr(self.status, 'value') else self.status
        return {
            "runtime_id": self.runtime_id,
            "name": self.name,
            "version": self.version,
            "vendor": self.vendor,
            "status": status_value,
            "runtime_class": runtime_class_value,
            "capabilities": self.capabilities,
            "description": self.description,
            "registered_at": self.registered_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        }

    @staticmethod
    def from_dict(data: dict) -> "Runtime":
        # 处理枚举值
        status_str = data.get("status", "ACTIVE")
        class_str = data.get("runtime_class", "STANDARD")
        return Runtime(
            runtime_id=data["runtime_id"],
            name=data["name"],
            version=data["version"],
            vendor=data["vendor"],
            status=RuntimeStatus(status_str) if status_str in ["ACTIVE", "INACTIVE", "DEPRECATED", "SUSPENDED"] else RuntimeStatus.ACTIVE,
            runtime_class=RuntimeClass(class_str) if class_str in ["CORE", "STANDARD", "ENTERPRISE", "REFERENCE"] else RuntimeClass.STANDARD,
            capabilities=data.get("capabilities", []),
            description=data.get("description"),
            registered_at=datetime.fromisoformat(data["registered_at"]) if "registered_at" in data else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.now(),
            metadata=data.get("metadata", {})
        )
