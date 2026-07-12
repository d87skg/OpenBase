#!/usr/bin/env python3
"""
OpenBase Reference Runtime
"""

import json
import uuid
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from .state import RuntimeState, StateTransition


class Runtime:
    """
    OpenBase Reference Runtime

    最小生命周期:
        Start → Execute → Emit Evidence → Finish → Persist
    """

    def __init__(self, agent_id: str, output_dir: str = "./evidence"):
        self.agent_id = agent_id
        self.run_id = str(uuid.uuid4())
        self.output_dir = Path(output_dir)
        self.state = RuntimeState.CREATED
        self.evidence: List[Dict[str, Any]] = []
        self._previous_hash: Optional[str] = None

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def initialize(self) -> "Runtime":
        """初始化 Runtime"""
        StateTransition.validate(self.state, RuntimeState.INITIALIZING)
        self.state = RuntimeState.INITIALIZING
        print(f"✅ Runtime 已初始化: {self.run_id}")
        return self

    def execute(self, input_data: Dict[str, Any]) -> "Runtime":
        """执行 Agent"""
        StateTransition.validate(self.state, RuntimeState.RUNNING)
        self.state = RuntimeState.RUNNING

        # 生成开始证据
        self._emit_evidence("AGENT_STARTED", {"input": input_data})

        # 模拟执行
        result = self._run_agent(input_data)

        # 生成结束证据
        self._emit_evidence("AGENT_FINISHED", {"output": result})

        return self

    def _run_agent(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """实际执行逻辑"""
        # 模拟 LLM 调用
        self._emit_evidence("LLM_CALL", {
            "model": "gpt-4",
            "prompt": input_data.get("prompt", "Hello, OpenBase!")
        })

        # 模拟工具调用
        self._emit_evidence("TOOL_CALL", {
            "tool": "echo",
            "args": input_data
        })

        return {
            "status": "success",
            "output": f"Echo: {input_data.get('prompt', 'Hello')}"
        }

    def _emit_evidence(self, event_type: str, payload: Dict[str, Any]) -> str:
        """生成证据"""
        # 保存当前状态
        previous_state = self.state

        # 切换到 EMITTING
        StateTransition.validate(previous_state, RuntimeState.EMITTING)
        self.state = RuntimeState.EMITTING

        evidence_id = f"evid-{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()

        # 构建证据对象（符合 Evidence Schema v1.0）
        evidence = {
            "evidence_id": evidence_id,
            "spec_version": "1.0",
            "agent_id": self.agent_id,
            "run_id": self.run_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "payload": payload,
            "proof": {
                "hash": self._compute_hash(payload),
                "signature": "ed25519:reference_runtime_signature"
            }
        }

        # 存储证据
        self.evidence.append(evidence)
        self._persist_evidence(evidence)

        print(f"   📝 {event_type}: {evidence_id}")

        # 恢复状态
        self.state = previous_state

        return evidence_id

    def _compute_hash(self, payload: Dict[str, Any]) -> str:
        """计算哈希"""
        content = json.dumps(payload, sort_keys=True)
        return f"sha256:{hashlib.sha256(content.encode()).hexdigest()}"

    def _persist_evidence(self, evidence: Dict[str, Any]) -> None:
        """持久化证据"""
        filepath = self.output_dir / f"{evidence['evidence_id']}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)

    def finish(self) -> "Runtime":
        """完成执行"""
        StateTransition.validate(self.state, RuntimeState.FINISHED)
        self.state = RuntimeState.FINISHED
        print(f"✅ Runtime 执行完成: {self.run_id}")
        print(f"   📁 证据目录: {self.output_dir.absolute()}")
        print(f"   📄 共生成 {len(self.evidence)} 条证据")
        return self

    def get_evidence(self) -> List[Dict[str, Any]]:
        """获取所有证据"""
        return self.evidence

    def get_state(self) -> RuntimeState:
        """获取当前状态"""
        return self.state