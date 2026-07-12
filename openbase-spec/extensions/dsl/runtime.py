from typing import Dict, Any, List
from .ir import RuleIR

class DSLRuntime:
    def __init__(self, rules: List[RuleIR]):
        self.rules = rules

    def evaluate(self, proposal: Dict[str, Any], global_state: Dict[str, Any]) -> Dict[str, Any]:
        results = []
        for rule in self.rules:
            if not self._match_trigger(rule, proposal):
                continue
            cond_pass = self._check_conditions(rule, global_state)
            if not cond_pass:
                results.append({
                    "rule": rule.rule_id,
                    "decision": "REJECT",
                    "reason": f"Condition failed in rule {rule.rule_id}"
                })
                continue
            inv_pass = self._check_invariants(rule, global_state)
            if not inv_pass:
                results.append({
                    "rule": rule.rule_id,
                    "decision": "REJECT",
                    "reason": f"Invariant failed in rule {rule.rule_id}"
                })
                continue
            results.append({
                "rule": rule.rule_id,
                "decision": rule.decision_tree.get("type", "ACCEPT"),
                "details": rule.decision_tree
            })
        return self._reduce_results(results)

    def _match_trigger(self, rule, proposal):
        return rule.trigger_event == proposal.get("state_type")

    def _check_conditions(self, rule, state):
        for cond in rule.conditions:
            if cond["type"] == "EXISTS_EVIDENCE":
                if "evidence" not in state or not state["evidence"]:
                    return False
            # 可扩展更多条件类型
        return True

    def _check_invariants(self, rule, state):
        for inv in rule.invariants:
            if inv["type"] == "STABILITY_WINDOW":
                # 模拟稳定性检查
                window = inv["params"].get("window", 5)
                # 简单示例：信任分数 > 0.7 视为稳定
                trust = state.get("trust", {})
                score = trust.get("score", 0)
                if score < 0.7:
                    return False
            if inv["type"] == "NO_CONFLICT":
                graph = state.get("graph", {})
                if graph.get("conflicts", False):
                    return False
        return True

    def _reduce_results(self, results):
        if not results:
            return {"decision": "ACCEPT", "reason": "No rules matched"}
        # 如果有任何 REJECT，则总体拒绝
        for r in results:
            if r["decision"] == "REJECT":
                return {"decision": "REJECT", "reason": r.get("reason", "Unknown")}
        # 取第一个 ACCEPT
        for r in results:
            if r["decision"] == "ACCEPT":
                return {"decision": "ACCEPT", "reason": "Accepted"}
        return {"decision": "ACCEPT", "reason": "Default accept"}
