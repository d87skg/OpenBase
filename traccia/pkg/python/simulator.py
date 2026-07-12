import random
import copy
from typing import Dict, Any, List, Callable
from .graph import ExecutionGraph

class LLMSimulator:
    def __init__(self, seed=42):
        random.seed(seed)
    
    def sample(self, prompt: str, candidates: List[str]) -> str:
        # 模拟 LLM 输出分布（加权随机）
        weights = [0.6, 0.3, 0.1]  # 假设 top-3 概率
        return random.choices(candidates, weights=weights, k=1)[0]

class ToolSimulator:
    def __init__(self, fail_rate=0.1):
        self.fail_rate = fail_rate
    
    def call(self, tool_name: str, input_data: str) -> Dict:
        if random.random() < self.fail_rate:
            return {"status": "error", "message": "Tool timeout"}
        return {"status": "success", "output": f"Result of {tool_name} on {input_data}"}

class ProbabilisticReplayer:
    def __init__(self, graph: ExecutionGraph, samples=5):
        self.graph = graph
        self.samples = samples
        self.llm = LLMSimulator()
        self.tool = ToolSimulator()

    def run_single(self) -> Dict:
        state = {"memory": {}, "outputs": []}
        ordered = self.graph.topological_sort()
        for eid in ordered:
            event = self.graph.nodes[eid]
            etype = event.get("event_type")
            payload = event.get("payload", {})
            
            if etype == "LLMRequest":
                candidates = payload.get("candidates", ["A", "B", "C"])
                result = self.llm.sample(payload.get("prompt", ""), candidates)
                state["outputs"].append(result)
            elif etype == "ToolCall":
                result = self.tool.call(payload.get("tool_name", "unknown"), payload.get("input", ""))
                state["tool_results"] = result
            elif etype == "MemoryUpdate":
                state["memory"][payload.get("key")] = payload.get("value")
        return state

    def run_distribution(self) -> List[Dict]:
        results = []
        for _ in range(self.samples):
            results.append(self.run_single())
        return results