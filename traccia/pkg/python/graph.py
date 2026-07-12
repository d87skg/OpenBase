import json
from typing import Dict, List, Optional, Any
from collections import defaultdict

class ExecutionGraph:
    def __init__(self):
        self.nodes: Dict[str, Dict] = {}  # event_id -> event_dict
        self.edges: Dict[str, List[str]] = defaultdict(list)  # parent_id -> [child_ids]
        self.roots: List[str] = []

    def add_event(self, event: Dict[str, Any]):
        eid = event.get("run_id") or event.get("event_id")
        if not eid:
            return
        self.nodes[eid] = event
        parent = event.get("parent_id")
        if parent:
            self.edges[parent].append(eid)
        else:
            self.roots.append(eid)

    def topological_sort(self) -> List[str]:
        """返回按因果顺序排列的 event_ids"""
        visited = set()
        order = []
        temp = set()

        def dfs(nid):
            if nid in temp:
                raise ValueError("Cycle detected in execution graph!")
            if nid in visited:
                return
            temp.add(nid)
            for child in self.edges.get(nid, []):
                dfs(child)
            temp.remove(nid)
            visited.add(nid)
            order.append(nid)

        for root in self.roots:
            if root not in visited:
                dfs(root)
        return order

    def to_json(self) -> str:
        return json.dumps({
            "nodes": self.nodes,
            "edges": dict(self.edges),
            "roots": self.roots
        }, indent=2)

    @staticmethod
    def from_evidence_file(path: str) -> "ExecutionGraph":
        graph = ExecutionGraph()
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    ev = json.loads(line)
                    graph.add_event(ev)
        return graph