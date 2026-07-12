#!/usr/bin/env python3
"""
LangGraph Adapter - 位于 openclaw/runtime/adapters/langgraph.py
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class LangGraphCallback:
    """
    LangGraph 回调适配器

    记录 Graph 节点执行和状态转换
    """

    def __init__(self, runtime_id: str, evidence_dir: str = "./evidence"):
        self.runtime_id = runtime_id
        self.evidence_dir = Path(evidence_dir)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self._evidence: List[Dict[str, Any]] = []

    def _generate_evidence(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        evidence_id = f"evid-{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()

        evidence = {
            "evidence_id": evidence_id,
            "spec_version": "1.0",
            "runtime_id": self.runtime_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "payload": payload,
            "proof": {
                "hash": "sha256:langgraph_adapter_hash",
                "signature": "ed25519:langgraph_adapter_signature"
            }
        }

        filepath = self.evidence_dir / f"{evidence_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)

        self._evidence.append(evidence)
        return evidence

    # ============================================================
    # Graph 生命周期
    # ============================================================

    def on_graph_start(self, graph_name: str, inputs: Dict) -> None:
        """Graph 开始执行"""
        self._generate_evidence("LANGGRAPH_START", {
            "graph_name": graph_name,
            "inputs": inputs
        })

    def on_graph_end(self, outputs: Dict) -> None:
        """Graph 执行完成"""
        self._generate_evidence("LANGGRAPH_END", {
            "outputs": outputs
        })

    def on_graph_error(self, error: Exception) -> None:
        """Graph 执行出错"""
        self._generate_evidence("ERROR", {
            "error_type": type(error).__name__,
            "error_message": str(error)
        })

    # ============================================================
    # 节点执行
    # ============================================================

    def on_node_start(self, node_name: str, inputs: Dict) -> None:
        """节点开始执行"""
        self._generate_evidence("LANGGRAPH_NODE_START", {
            "node_name": node_name,
            "inputs": inputs
        })

    def on_node_end(self, node_name: str, outputs: Dict) -> None:
        """节点执行完成"""
        self._generate_evidence("LANGGRAPH_NODE_END", {
            "node_name": node_name,
            "outputs": outputs
        })

    def on_node_error(self, node_name: str, error: Exception) -> None:
        """节点执行出错"""
        self._generate_evidence("ERROR", {
            "node_name": node_name,
            "error_type": type(error).__name__,
            "error_message": str(error)
        })

    # ============================================================
    # 状态转换
    # ============================================================

    def on_state_transition(self, from_state: str, to_state: str, payload: Dict) -> None:
        """状态转换"""
        self._generate_evidence("LANGGRAPH_STATE_TRANSITION", {
            "from": from_state,
            "to": to_state,
            "payload": payload
        })

    # ============================================================
    # 分支决策
    # ============================================================

    def on_condition_eval(self, condition: str, result: bool) -> None:
        """条件评估结果"""
        self._generate_evidence("LANGGRAPH_CONDITION", {
            "condition": condition,
            "result": result
        })

    # ============================================================
    # 获取证据
    # ============================================================

    def get_evidence(self) -> List[Dict[str, Any]]:
        return self._evidence


class LangGraphAdapter:
    """
    LangGraph 适配器包装类
    """

    def __init__(self, runtime_id: str, evidence_dir: str = "./evidence"):
        self.runtime_id = runtime_id
        self.callback = LangGraphCallback(runtime_id, evidence_dir)

    def get_callback(self) -> LangGraphCallback:
        return self.callback

    def simulate_graph_execution(self, graph_name: str, inputs: Dict) -> Dict:
        """模拟 LangGraph 执行"""

        self.callback.on_graph_start(graph_name, inputs)

        try:
            # 模拟状态机
            state = {"counter": 0, "data": inputs}

            # 模拟节点执行
            nodes = ["init", "process", "validate", "finalize"]
            for i, node_name in enumerate(nodes):
                self.callback.on_node_start(node_name, state)

                # 模拟节点输出
                state["counter"] += 1
                node_output = {
                    "node": node_name,
                    "counter": state["counter"],
                    "status": "completed"
                }
                self.callback.on_node_end(node_name, node_output)

                # 模拟状态转换
                if i < len(nodes) - 1:
                    self.callback.on_state_transition(
                        from_state=node_name,
                        to_state=nodes[i + 1],
                        payload={"counter": state["counter"]}
                    )

            # 模拟条件评估
            self.callback.on_condition_eval(
                condition="counter > 2",
                result=state["counter"] > 2
            )

            result = {"status": "completed", "final_counter": state["counter"]}
            self.callback.on_graph_end(result)
            return result

        except Exception as e:
            self.callback.on_graph_error(e)
            raise

    def get_evidence(self) -> List[Dict[str, Any]]:
        return self.callback.get_evidence()