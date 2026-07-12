import json
import fnmatch
from typing import Dict, Any, Optional

class PolicyRule:
    def __init__(self, tool_pattern: str, action: str, reason: str = ""):
        self.tool_pattern = tool_pattern
        self.action = action  # "allow" | "deny"
        self.reason = reason

    def matches(self, tool_name: str) -> bool:
        return fnmatch.fnmatch(tool_name, self.tool_pattern)

class PolicyEngine:
    def __init__(self, config_path: Optional[str] = None):
        self.rules: list[PolicyRule] = []
        self.default_action = "allow"
        if config_path:
            self.load(config_path)

    def load(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.rules = []
        for rule_data in data.get("rules", []):
            self.rules.append(PolicyRule(
                tool_pattern=rule_data["tool_pattern"],
                action=rule_data["action"],
                reason=rule_data.get("reason", "")
            ))
        self.default_action = data.get("default_action", "allow")

    def evaluate(self, tool_name: str) -> tuple[str, str]:
        """返回 (action, reason)"""
        for rule in self.rules:
            if rule.matches(tool_name):
                return rule.action, rule.reason
        return self.default_action, "No specific rule matched, using default"