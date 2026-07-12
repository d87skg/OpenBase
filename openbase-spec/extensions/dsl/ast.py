from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class RuleAST:
    name: str
    trigger: str
    conditions: List[Dict[str, Any]]
    invariants: List[Dict[str, Any]]
    action: Dict[str, Any]

@dataclass
class ConditionAST:
    type: str
    params: Dict[str, Any]

@dataclass
class InvariantAST:
    type: str
    params: Dict[str, Any]

@dataclass
class ActionAST:
    type: str
    params: Dict[str, Any]
