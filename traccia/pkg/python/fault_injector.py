import random
import copy
from typing import List, Dict, Any

class FaultInjector:
    def __init__(self, seed=42):
        random.seed(seed)
        self.fault_log = []

    def inject_event_loss(self, events: List[Dict], probability=0.1) -> List[Dict]:
        """随机删除事件"""
        new_events = []
        for ev in events:
            if random.random() > probability:
                new_events.append(ev)
            else:
                self.fault_log.append({"type": "event_loss", "event_id": ev.get("run_id")})
        return new_events

    def inject_event_duplication(self, events: List[Dict], probability=0.05) -> List[Dict]:
        """随机复制事件"""
        new_events = []
        for ev in events:
            new_events.append(ev)
            if random.random() < probability:
                dup = copy.deepcopy(ev)
                dup["run_id"] = dup["run_id"] + "_dup"
                new_events.append(dup)
                self.fault_log.append({"type": "duplication", "original_id": ev.get("run_id")})
        return new_events

    def inject_reordering(self, events: List[Dict], probability=0.1) -> List[Dict]:
        """随机交换相邻事件顺序"""
        if len(events) < 2:
            return events
        new_events = events[:]
        for i in range(len(new_events)-1):
            if random.random() < probability:
                new_events[i], new_events[i+1] = new_events[i+1], new_events[i]
                self.fault_log.append({"type": "reordering", "pos": i})
        return new_events

    def inject_payload_corruption(self, events: List[Dict], probability=0.05) -> List[Dict]:
        """随机篡改 payload"""
        new_events = []
        for ev in events:
            if random.random() < probability:
                ev = copy.deepcopy(ev)
                if "payload" in ev and isinstance(ev["payload"], dict):
                    # 随机修改一个字段
                    keys = list(ev["payload"].keys())
                    if keys:
                        key = random.choice(keys)
                        ev["payload"][key] = "CORRUPTED_" + str(ev["payload"][key])
                        self.fault_log.append({"type": "corruption", "event_id": ev.get("run_id"), "field": key})
            new_events.append(ev)
        return new_events

    def inject_identity_spoof(self, events: List[Dict], probability=0.02) -> List[Dict]:
        """伪造 agent_id 或 node_id"""
        new_events = []
        for ev in events:
            if random.random() < probability:
                ev = copy.deepcopy(ev)
                ev["agent_id"] = "spoofed_agent"
                ev["node_id"] = "spoofed_node"
                self.fault_log.append({"type": "identity_spoof", "event_id": ev.get("run_id")})
            new_events.append(ev)
        return new_events

    def apply_all(self, events: List[Dict]) -> List[Dict]:
        """应用所有故障（顺序执行）"""
        events = self.inject_event_loss(events)
        events = self.inject_event_duplication(events)
        events = self.inject_reordering(events)
        events = self.inject_payload_corruption(events)
        events = self.inject_identity_spoof(events)
        return events

    def get_fault_report(self) -> List[Dict]:
        return self.fault_log