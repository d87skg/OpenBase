"""
DSL 规则定义（Python 函数形式）
"""

def rule_EvidenceFirst(proposal, state):
    """证据必须在信任更新之前存在"""
    if proposal.get("state_type") != "TrustUpdate":
        return None  # 不匹配此规则
    if "evidence" not in state or not state["evidence"]:
        return {"decision": "REJECT", "reason": "No evidence found before trust update"}
    trust = state.get("trust", {})
    if trust.get("score", 0) < 0.7:
        return {"decision": "REJECT", "reason": "Trust score too low"}
    return {"decision": "ACCEPT", "reason": "Evidence exists and trust stable"}

def rule_TrustStability(proposal, state):
    """信任更新需要稳定性窗口"""
    if proposal.get("state_type") not in ["TrustUpdate", "GraphUpdate", "CertificateIssue"]:
        return None
    trust = state.get("trust", {})
    if trust.get("score", 0) < 0.7:
        return {"decision": "REJECT", "reason": "Trust not stable enough"}
    return {"decision": "ACCEPT", "reason": "Trust stable"}

def rule_NoConflict(proposal, state):
    """不能有冲突"""
    if proposal.get("state_type") not in ["GraphUpdate", "CertificateIssue"]:
        return None
    graph = state.get("graph", {})
    if graph.get("conflicts", False):
        return {"decision": "REJECT", "reason": "Conflict detected"}
    return {"decision": "ACCEPT", "reason": "No conflict"}

def rule_CertificateIssuance(proposal, state):
    """证书颁发需要信任稳定且无冲突"""
    if proposal.get("state_type") != "CertificateIssue":
        return None
    trust = state.get("trust", {})
    if trust.get("score", 0) < 0.8:
        return {"decision": "REJECT", "reason": "Trust score below 0.8"}
    graph = state.get("graph", {})
    if graph.get("conflicts", False):
        return {"decision": "REJECT", "reason": "Conflict exists"}
    return {"decision": "ACCEPT", "reason": "Certificate can be issued"}

# 规则列表
RULES = [
    rule_EvidenceFirst,
    rule_TrustStability,
    rule_NoConflict,
    rule_CertificateIssuance,
]
