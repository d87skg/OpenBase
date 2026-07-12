from typing import List, Dict, Any
from .graph import ExecutionGraph
from .vector_clock import VectorClock

class ConsensusEngine:
    def __init__(self, graphs: List[ExecutionGraph]):
        self.graphs = graphs

    def merge(self) -> ExecutionGraph:
        """合并多个图，形成单一共识图"""
        merged = ExecutionGraph()
        all_events = {}
        for g in self.graphs:
            for eid, ev in g.nodes.items():
                if eid not in all_events:
                    all_events[eid] = ev
                    merged.add_event(ev)
        # 注意：实际生产需要解决冲突，这里简化：直接合并，保留首次出现
        return merged

    def detect_divergence(self) -> List[Dict]:
        """检测分歧点"""
        divergences = []
        # 比较每个图的根和边
        for i, g in enumerate(self.graphs):
            for j, h in enumerate(self.graphs):
                if i >= j: continue
                if set(g.nodes.keys()) != set(h.nodes.keys()):
                    divergences.append({
                        "graph_a": i,
                        "graph_b": j,
                        "reason": "node_id_mismatch",
                        "extra_nodes": list(set(g.nodes.keys()) - set(h.nodes.keys()))
                    })
        return divergences