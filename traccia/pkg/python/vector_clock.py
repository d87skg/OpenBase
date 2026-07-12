from typing import Dict, Optional

class VectorClock:
    def __init__(self, node_id: str):
        self.clock: Dict[str, int] = {node_id: 0}
        self.node_id = node_id

    def tick(self) -> Dict[str, int]:
        """当前节点发生事件，自增并返回新时钟"""
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1
        return self.clock.copy()

    def update(self, received_clock: Dict[str, int]) -> Dict[str, int]:
        """收到其他节点的时钟，合并（取最大值）"""
        for node, time in received_clock.items():
            self.clock[node] = max(self.clock.get(node, 0), time)
        # 自己的时钟也要递增（接收事件）
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1
        return self.clock.copy()

    def get_clock(self) -> Dict[str, int]:
        return self.clock.copy()

    @staticmethod
    def compare(a: Dict[str, int], b: Dict[str, int]) -> str:
        if a == b:
            return "equal"
        a_less_or_equal = all(a.get(k, 0) <= b.get(k, 0) for k in a)
        b_less_or_equal = all(b.get(k, 0) <= a.get(k, 0) for k in b)
        if a_less_or_equal and not b_less_or_equal:
            return "causal_a_before_b"
        elif b_less_or_equal and not a_less_or_equal:
            return "causal_b_before_a"
        else:
            return "concurrent"