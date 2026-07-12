from typing import Dict, List
from collections import defaultdict

class TrustGraph:
    def __init__(self):
        self.nodes = set()  # agent_ids
        self.edges = defaultdict(dict)  # from_agent -> {to_agent: trust_score}

    def add_trust(self, from_agent: str, to_agent: str, score: float):
        self.nodes.add(from_agent)
        self.nodes.add(to_agent)
        self.edges[from_agent][to_agent] = score

    def propagate(self, initial_scores: Dict[str, float], iterations: int = 3) -> Dict[str, float]:
        """PageRank-like 信任传播"""
        scores = initial_scores.copy()
        for _ in range(iterations):
            new_scores = {}
            for node in self.nodes:
                incoming = [scores.get(src, 0.5) * self.edges[src].get(node, 0) 
                            for src in self.nodes if node in self.edges[src]]
                new_scores[node] = max(0.1, sum(incoming) / max(1, len(incoming)) * 0.9 + 0.1)
            scores = new_scores
        return scores

    @staticmethod
    def from_evidence_files(paths: List[str]) -> "TrustGraph":
        import json
        graph = TrustGraph()
        for path in paths:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip(): continue
                    ev = json.loads(line)
                    agent = ev.get("agent_id")
                    if agent:
                        graph.nodes.add(agent)
        # 添加随机信任边用于演示
        nodes_list = list(graph.nodes)
        for i, src in enumerate(nodes_list):
            for j, dst in enumerate(nodes_list):
                if i != j:
                    graph.add_trust(src, dst, 0.7 if i < j else 0.5)
        return graph