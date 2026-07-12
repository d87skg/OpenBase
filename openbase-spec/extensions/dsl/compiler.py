from .ast import RuleAST, ConditionAST, InvariantAST, ActionAST

def compile_ast(rules):
    ir_rules = []
    for rule in rules:
        ir = {
            "rule_id": rule.name,
            "trigger_event": rule.trigger,
            "conditions": [],
            "invariants": [],
            "decision_tree": {"type": rule.action.type}
        }
        if rule.action.type == "REJECT":
            ir["decision_tree"]["reason"] = rule.action.params.get("reason", "rejected")
        elif rule.action.type == "REWRITE":
            ir["decision_tree"]["suggestion"] = rule.action.params.get("suggestion", "")
        for cond in rule.conditions:
            ir["conditions"].append({"type": cond.type, "params": cond.value})
        for inv in rule.invariants:
            ir["invariants"].append({"type": inv.type, "params": inv.args})
        ir_rules.append(ir)
    return ir_rules
