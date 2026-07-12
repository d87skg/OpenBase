from typing import List, Dict, Any
from .graph import ExecutionGraph
from .replay_v1 import StateRebuilder
import copy

class AdversarialReplayEngine:
    def __init__(self, events: List[Dict]):
        self.events = events
        self.graph = self._build_graph(events)

    def _build_graph(self, events):
        g = ExecutionGraph()
        for ev in events:
            g.add_event(ev)
        return g

    def reconstruct(self) -> Dict[str, Any]:
        """在存在故障的情况下重建最可能的状态"""
        # 策略：忽略孤立节点，优先信任有签名的节点
        # 1. 过滤掉无签名的可疑事件
        trusted_events = [ev for ev in self.events if "signature" in ev]
        if not trusted_events:
            return {"error": "No trusted events available"}

        # 2. 构建只包含可信事件的图
        g = ExecutionGraph()
        for ev in trusted_events:
            g.add_event(ev)

        # 3. 拓扑排序
        try:
            order = g.topological_sort()
        except ValueError:
            # 有环，尝试移除环
            order = self._break_cycles(g)

        # 4. 重放
        builder = StateRebuilder()
        for eid in order:
            ev = g.nodes[eid]
            builder.apply(ev)
        return builder.get_snapshot()

    def _break_cycles(self, graph):
        # 简单策略：按 logical_time 排序
        nodes = list(graph.nodes.values())
        nodes.sort(key=lambda x: x.get("logical_time", 0))
        return [n.get("run_id") for n in nodes if n.get("run_id")]

    def compare_with_original(self, original_state: Dict) -> Dict:
        replayed = self.reconstruct()
        diff = {"match": True, "differences": []}
        for key in set(original_state.keys()) | set(replayed.keys()):
            if original_state.get(key) != replayed.get(key):
                diff["match"] = False
                diff["differences"].append({
                    "key": key,
                    "original": original_state.get(key),
                    "replayed": replayed.get(key)
                })
        return diff