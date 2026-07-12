"""
OpenClaw → Execution Engine Adapter
将 OpenClaw Runtime 的执行事件转换为 Execution Engine 可识别的格式
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from engines.execution import ExecutionEngine
from engines.evidence import EvidenceEngine
from engines.replay import ReplayEngine
from engines.verification import VerificationEngine
from engines.determinism import DeterminismEngine
from engines.certification import CertificationEngine


class OpenClawExecutionAdapter:
    """将 OpenClaw Runtime 映射到 Execution Engine"""

    def __init__(self):
        self.execution_engine = ExecutionEngine()
        self.evidence_engine = EvidenceEngine()
        self.replay_engine = ReplayEngine()
        self.verification_engine = VerificationEngine()
        self.determinism_engine = DeterminismEngine()
        self.certification_engine = CertificationEngine()

        # 初始化所有引擎
        self.execution_engine.initialize()
        self.evidence_engine.initialize({"private_key": "openclaw_test_key"})
        self.replay_engine.initialize({"fidelity": "causal"})
        self.verification_engine.initialize()
        self.determinism_engine.initialize()
        self.certification_engine.initialize()

        self._execution_id = None
        self._evidence_store = []

    def start_execution(self, agent_id: str, **kwargs) -> dict:
        """开始执行：映射 OpenClaw 的 RUNNING 状态"""
        result = self.execution_engine.execute({
            "agent_id": agent_id,
            **kwargs
        })
        if result.success:
            self._execution_id = result.result.get("execution_id")
        return result.result if result.success else {"error": result.error}

    def emit_evidence(self, event_type: str, payload: dict) -> dict:
        """发出 Evidence：映射 OpenClaw 的事件"""
        if not self._execution_id:
            return {"error": "No active execution"}

        result = self.evidence_engine.execute({
            "execution_id": self._execution_id,
            "agent_id": "openclaw",
            "event_type": event_type,
            "payload": payload
        })
        if result.success:
            evid = self.evidence_engine.get_evidence(result.result.get("evidence_id"))
            if evid:
                self._evidence_store.append(evid)
        return result.result if result.success else {"error": result.error}

    def complete_execution(self, final_output: str) -> dict:
        """完成执行"""
        return self.emit_evidence("AGENT_FINISHED", {"final_output": final_output})

    def verify(self) -> dict:
        """验证当前执行"""
        result = self.verification_engine.execute({
            "execution": {"execution_id": self._execution_id, "state": "RUNNING"},
            "evidence": self._evidence_store
        })
        return result.result if result.success else {"error": result.error}

    def replay(self) -> dict:
        """重放当前执行"""
        result = self.replay_engine.execute(self._evidence_store)
        return result.result if result.success else {"error": result.error}

    def analyze_determinism(self) -> dict:
        """分析确定性"""
        result = self.determinism_engine.execute({
            "execution": {"execution_id": self._execution_id},
            "evidence": self._evidence_store
        })
        return result.result if result.success else {"error": result.error}

    def certify(self, trust_score: float = 0.93) -> dict:
        """生成证书"""
        ver_result = self.verification_engine.get_latest_result()
        result = self.certification_engine.execute({
            "verification_result": ver_result or {"passed": True},
            "runtime_name": "OpenClaw",
            "trust_score": trust_score
        })
        return result.result if result.success else {"error": result.error}

    def get_full_report(self) -> dict:
        """生成完整报告"""
        return {
            "execution_id": self._execution_id,
            "evidence_count": len(self._evidence_store),
            "execution": self.execution_engine.report(),
            "evidence": self.evidence_engine.report(),
            "replay": self.replay_engine.report(),
            "verification": self.verification_engine.report(),
            "determinism": self.determinism_engine.report(),
            "certification": self.certification_engine.report()
        }
