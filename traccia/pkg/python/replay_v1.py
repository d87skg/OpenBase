import json
from typing import Dict, Any, List
from .graph import ExecutionGraph

class StateRebuilder:
    def __init__(self):
        self.state = {
            "memory": {},
            "tool_results": {},
            "last_output": None
        }

    def apply(self, event: Dict[str, Any]):
        etype = event.get("event_type")
        payload = event.get("payload", {})
        
        if etype == "MemoryUpdate":
            self.state["memory"][payload.get("key")] = payload.get("value")
        elif etype == "ToolResult":
            self.state["tool_results"][payload.get("tool_name")] = payload.get("output")
        elif etype == "LLMResponse":
            self.state["last_output"] = payload.get("output")
        elif etype == "AgentFinished":
            self.state["last_output"] = payload.get("final_output")
        return self.state.copy()

    def get_snapshot(self):
        return self.state.copy()

class ReplayEngineV1:
    def __init__(self, graph: ExecutionGraph):
        self.graph = graph

    def replay(self) -> Dict[str, Any]:
        builder = StateRebuilder()
        ordered = self.graph.topological_sort()
        for eid in ordered:
            event = self.graph.nodes[eid]
            builder.apply(event)
        return builder.get_snapshot()

    def diff(self, original_state: Dict, replayed_state: Dict) -> Dict:
        diff = {"match": True, "differences": []}
        all_keys = set(original_state.keys()) | set(replayed_state.keys())
        for key in all_keys:
            if original_state.get(key) != replayed_state.get(key):
                diff["match"] = False
                diff["differences"].append({
                    "key": key,
                    "original": original_state.get(key),
                    "replay": replayed_state.get(key)
                })
        return diff