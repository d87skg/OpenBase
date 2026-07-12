from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class RuleIR:
    rule_id: str
    trigger_event: str
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    invariants: List[Dict[str, Any]] = field(default_factory=list)
    decision_tree: Dict[str, Any] = field(default_factory=dict)
