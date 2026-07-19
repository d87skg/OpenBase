import os

code = '''"""
OpenBase Registry Engine
Manages identities, runtimes, and certificates.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


@dataclass
class RegistryEntry:
    """An entry in the OpenBase Registry."""
    entry_id: str
    entry_type: str  # runtime, agent, adapter, certificate
    name: str
    version: str = "0.0.0"
    status: str = "active"  # active, deprecated, retired
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "entry_type": self.entry_type,
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "metadata": self.metadata,
            "registered_at": self.registered_at,
            "updated_at": self.updated_at,
        }


class Registry:
    """Central registry for all OpenBase entities."""

    def __init__(self):
        self._entries: Dict[str, RegistryEntry] = {}
        self._runtimes: Dict[str, RegistryEntry] = {}
        self._agents: Dict[str, RegistryEntry] = {}
        self._adapters: Dict[str, RegistryEntry] = {}

    def register(self, entry_type: str, name: str, version: str = "0.0.0",
                 metadata: Optional[Dict] = None) -> RegistryEntry:
        """Register a new entity."""
        entry_id = f"{entry_type}_{uuid.uuid4().hex[:8]}"
        entry = RegistryEntry(
            entry_id=entry_id,
            entry_type=entry_type,
            name=name,
            version=version,
            metadata=metadata or {},
        )
        self._entries[entry_id] = entry

        if entry_type == "runtime":
            self._runtimes[entry_id] = entry
        elif entry_type == "agent":
            self._agents[entry_id] = entry
        elif entry_type == "adapter":
            self._adapters[entry_id] = entry

        return entry

    def get(self, entry_id: str) -> Optional[RegistryEntry]:
        """Get an entry by ID."""
        return self._entries.get(entry_id)

    def list_by_type(self, entry_type: str) -> List[RegistryEntry]:
        """List all entries of a given type."""
        return [e for e in self._entries.values() if e.entry_type == entry_type]

    def list_all(self) -> List[RegistryEntry]:
        """List all registered entries."""
        return list(self._entries.values())

    def update_status(self, entry_id: str, status: str) -> Optional[RegistryEntry]:
        """Update the status of an entry."""
        entry = self._entries.get(entry_id)
        if entry:
            entry.status = status
            entry.updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return entry

    def get_runtime_count(self) -> int:
        return len(self._runtimes)

    def get_agent_count(self) -> int:
        return len(self._agents)

    def get_adapter_count(self) -> int:
        return len(self._adapters)

    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        return {
            "total_entries": len(self._entries),
            "runtimes": self.get_runtime_count(),
            "agents": self.get_agent_count(),
            "adapters": self.get_adapter_count(),
            "certificates": len([e for e in self._entries.values() if e.entry_type == "certificate"]),
        }
'''

path = r'D:\OpenBase\openbase_core\registry\engine.py'
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print('registry/engine.py written')
