from .graph import ExecutionGraph
from .replay_v1 import ReplayEngineV1, StateRebuilder
import copy

class CounterfactualEngine:
    def __init__(self, graph: ExecutionGraph):
        self.graph = graph

    def what_if(self, target_event_id: str, new_payload: dict) -> dict:
        # 克隆图结构
        new_graph = ExecutionGraph()
        for eid, ev in self.graph.nodes.items():
            copied = copy.deepcopy(ev)
            if eid == target_event_id:
                copied["payload"] = new_payload
            new_graph.add_event(copied)
        
        # 重放修改后的图
        engine = ReplayEngineV1(new_graph)
        return engine.replay()

    def compare(self, original_state: dict, new_state: dict) -> dict:
        diff = {"changed": False, "diffs": []}
        for key in set(original_state.keys()) | set(new_state.keys()):
            if original_state.get(key) != new_state.get(key):
                diff["changed"] = True
                diff["diffs"].append({
                    "key": key,
                    "original": original_state.get(key),
                    "new": new_state.get(key)
                })
        return diff