#!/usr/bin/env python3
"""
OpenAI SDK Adapter

自动记录 OpenAI API 调用为 OpenBase Evidence
"""

import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path


class OpenAICallback:
    """OpenAI 回调适配器"""

    def __init__(self, runtime_id: str, evidence_dir: str = "./evidence"):
        self.runtime_id = runtime_id
        self.evidence_dir = Path(evidence_dir)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self._evidence: List[Dict[str, Any]] = []

    def _generate_evidence(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """生成 Evidence"""
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
                "hash": "sha256:openai_adapter_hash",
                "signature": "ed25519:openai_adapter_signature"
            }
        }

        # 保存到文件
        filepath = self.evidence_dir / f"{evidence_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)

        self._evidence.append(evidence)
        return evidence

    def before_request(self, model: str, messages: List[Dict], **kwargs) -> None:
        """在 OpenAI 请求前调用"""
        self._generate_evidence("LLM_REQUEST", {
            "model": model,
            "messages": messages,
            "params": kwargs
        })

    def after_response(self, response: Dict[str, Any]) -> None:
        """在 OpenAI 响应后调用"""
        self._generate_evidence("LLM_RESPONSE", {
            "response": response
        })

    def on_error(self, error: Exception) -> None:
        """在错误发生时调用"""
        self._generate_evidence("ERROR", {
            "error_type": type(error).__name__,
            "error_message": str(error)
        })

    def get_evidence(self) -> List[Dict[str, Any]]:
        """获取所有证据"""
        return self._evidence


class OpenAIClient:
    """包装 OpenAI 客户端，自动记录"""

    def __init__(self, callback: OpenAICallback):
        self.callback = callback

    def chat_completion(self, model: str, messages: List[Dict], **kwargs) -> Dict[str, Any]:
        """
        模拟 OpenAI chat.completions.create

        实际使用时应替换为真正的 OpenAI 客户端调用
        """
        self.callback.before_request(model, messages, kwargs)

        try:
            # 模拟响应
            response = {
                "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
                "model": model,
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": f"Hello! This is a simulated response for {model}"
                        }
                    }
                ]
            }
            self.callback.after_response(response)
            return response
        except Exception as e:
            self.callback.on_error(e)
            raise