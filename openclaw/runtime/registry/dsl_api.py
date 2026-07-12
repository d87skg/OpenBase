from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from dsl.rules import RULES

router = APIRouter(prefix="/dsl", tags=["dsl"])

class RuleCheckRequest(BaseModel):
    proposal: Dict[str, Any]
    global_state: Dict[str, Any]

class RuleCheckResponse(BaseModel):
    decision: str
    reason: str
    rule: Optional[str] = None

@router.post("/evaluate", response_model=RuleCheckResponse)
async def evaluate_rules(request: RuleCheckRequest):
    """使用 DSL 规则评估提案"""
    proposal = request.proposal
    state = request.global_state
    
    # 遍历所有规则
    for rule in RULES:
        result = rule(proposal, state)
        if result is not None:
            # 如果规则匹配并且返回拒绝，则立即返回拒绝
            if result["decision"] == "REJECT":
                return RuleCheckResponse(
                    decision="REJECT",
                    reason=result.get("reason", "Rejected by rule"),
                    rule=rule.__name__
                )
            # 否则继续检查，但记住最后一个接受
            accepted_rule = rule.__name__
            accepted_reason = result.get("reason", "Accepted")
    
    # 默认接受（如果没有拒绝）
    return RuleCheckResponse(
        decision="ACCEPT",
        reason="All rules passed",
        rule="default"
    )

@router.get("/rules")
async def list_rules():
    """列出所有已注册的规则"""
    return {"rules": [r.__name__ for r in RULES]}

@router.post("/compile")
async def compile_rules():
    """兼容旧 API，返回规则名称列表"""
    return {"rules": [r.__name__ for r in RULES]}
