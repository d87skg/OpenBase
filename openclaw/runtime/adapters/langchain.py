#!/usr/bin/env python3
"""
LangChain Adapter - 位于 openclaw/runtime/adapters/langchain.py
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Union


class LangChainCallback:
    """
    LangChain Callback Handler

    通过 LangChain 的 callback 机制拦截链执行过程
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
                "hash": "sha256:langchain_adapter_hash",
                "signature": "ed25519:langchain_adapter_signature"
            }
        }

        filepath = self.evidence_dir / f"{evidence_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)

        self._evidence.append(evidence)
        return evidence

    # ============================================================
    # Chain 生命周期回调
    # ============================================================

    def on_chain_start(self, serialized: Dict, inputs: Dict, **kwargs) -> None:
        """链开始执行"""
        chain_name = serialized.get("name", "unknown_chain")
        self._generate_evidence("LANGCHAIN_CHAIN_START", {
            "chain_name": chain_name,
            "inputs": inputs
        })

    def on_chain_end(self, outputs: Dict, **kwargs) -> None:
        """链执行完成"""
        self._generate_evidence("LANGCHAIN_CHAIN_END", {
            "outputs": outputs
        })

    def on_chain_error(self, error: Exception, **kwargs) -> None:
        """链执行出错"""
        self._generate_evidence("ERROR", {
            "error_type": type(error).__name__,
            "error_message": str(error)
        })

    # ============================================================
    # LLM 回调
    # ============================================================

    def on_llm_start(self, serialized: Dict, prompts: List[str], **kwargs) -> None:
        """LLM 开始调用"""
        model_name = serialized.get("name", "unknown_model")
        self._generate_evidence("LANGCHAIN_LLM_START", {
            "model": model_name,
            "prompts": prompts
        })

    def on_llm_end(self, response: Dict, **kwargs) -> None:
        """LLM 调用完成"""
        self._generate_evidence("LANGCHAIN_LLM_END", {
            "response": response
        })

    def on_llm_error(self, error: Exception, **kwargs) -> None:
        """LLM 调用出错"""
        self._generate_evidence("ERROR", {
            "error_type": type(error).__name__,
            "error_message": str(error)
        })

    # ============================================================
    # Tool 回调
    # ============================================================

    def on_tool_start(self, serialized: Dict, input_str: str, **kwargs) -> None:
        """工具开始执行"""
        tool_name = serialized.get("name", "unknown_tool")
        self._generate_evidence("LANGCHAIN_TOOL_START", {
            "tool_name": tool_name,
            "input": input_str
        })

    def on_tool_end(self, output: str, **kwargs) -> None:
        """工具执行完成"""
        self._generate_evidence("LANGCHAIN_TOOL_END", {
            "output": output
        })

    def on_tool_error(self, error: Exception, **kwargs) -> None:
        """工具执行出错"""
        self._generate_evidence("ERROR", {
            "error_type": type(error).__name__,
            "error_message": str(error)
        })

    # ============================================================
    # 获取证据
    # ============================================================

    def get_evidence(self) -> List[Dict[str, Any]]:
        return self._evidence


class LangChainAdapter:
    """
    LangChain 适配器包装类

    提供类似 LangChain 的 callback handler 接口
    """

    def __init__(self, runtime_id: str, evidence_dir: str = "./evidence"):
        self.runtime_id = runtime_id
        self.callback = LangChainCallback(runtime_id, evidence_dir)

    def get_callback(self) -> LangChainCallback:
        """获取 callback 实例，用于 LangChain"""
        return self.callback

    def simulate_chain_execution(self, chain_name: str, inputs: Dict) -> Dict:
        """模拟 LangChain 链执行"""

        # 链开始
        self.callback.on_chain_start({"name": chain_name}, inputs)

        try:
            # 模拟 LLM 调用
            self.callback.on_llm_start(
                {"name": "gpt-4"},
                [str(inputs.get("input", "Hello"))]
            )
            # 模拟 LLM 响应
            self.callback.on_llm_end({
                "generations": [
                    [{"text": f"LLM response from {chain_name}: {inputs.get('input', 'Hello')}"}]
                ]
            })

            # 模拟 Tool 调用
            self.callback.on_tool_start({"name": "search_tool"}, "search query")
            self.callback.on_tool_end("Search result: found something")

            # 链结束
            output = {"output": f"Chain {chain_name} completed successfully"}
            self.callback.on_chain_end(output)

            return output

        except Exception as e:
            self.callback.on_chain_error(e)
            raise

    def get_evidence(self) -> List[Dict[str, Any]]:
        return self.callback.get_evidence()