from typing import List, Dict, Any, Optional
import base64
from cryptography.hazmat.primitives.asymmetric import ed25519

class ByzantineDetector:
    def __init__(self):
        self.anomalies = []

    def verify_signatures(self, events: List[Dict]) -> List[Dict]:
        """检查签名是否有效"""
        anomalies = []
        for ev in events:
            if "signature" not in ev or "public_key" not in ev:
                anomalies.append({
                    "event_id": ev.get("run_id"),
                    "type": "missing_signature",
                    "detail": "Event lacks signature or public key"
                })
                continue
            try:
                public_key_b64 = ev["public_key"]
                public_bytes = base64.b64decode(public_key_b64)
                public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)
                sign_data = (ev["hash"] + ev["execution_id"]).encode()
                signature = base64.b64decode(ev["signature"])
                public_key.verify(signature, sign_data)
            except Exception:
                anomalies.append({
                    "event_id": ev.get("run_id"),
                    "type": "invalid_signature",
                    "detail": "Signature verification failed"
                })
        self.anomalies.extend(anomalies)
        return anomalies

    def detect_causal_contradiction(self, events: List[Dict]) -> List[Dict]:
        """检测因果矛盾：如 parent_id 指向不存在的事件"""
        anomalies = []
        event_ids = {ev.get("run_id") for ev in events if ev.get("run_id")}
        for ev in events:
            parent = ev.get("parent_id")
            if parent and parent not in event_ids and not parent.startswith("spoofed"):
                anomalies.append({
                    "event_id": ev.get("run_id"),
                    "type": "causal_contradiction",
                    "detail": f"Parent {parent} not found"
                })
        self.anomalies.extend(anomalies)
        return anomalies

    def detect_temporal_drift(self, events: List[Dict]) -> List[Dict]:
        """检测时间戳异常：顺序与逻辑时间不一致"""
        anomalies = []
        # 按 logical_time 排序，检查 timestamp 是否递增
        sorted_events = sorted(events, key=lambda x: x.get("logical_time", 0))
        for i in range(len(sorted_events)-1):
            t1 = sorted_events[i].get("timestamp")
            t2 = sorted_events[i+1].get("timestamp")
            if t1 and t2 and t1 > t2:
                anomalies.append({
                    "type": "temporal_drift",
                    "event1": sorted_events[i].get("run_id"),
                    "event2": sorted_events[i+1].get("run_id"),
                    "detail": "Physical time decreases while logical time increases"
                })
        self.anomalies.extend(anomalies)
        return anomalies

    def detect_duplicate_events(self, events: List[Dict]) -> List[Dict]:
        """检测重复的 run_id"""
        seen = set()
        anomalies = []
        for ev in events:
            rid = ev.get("run_id")
            if rid and rid in seen:
                anomalies.append({
                    "event_id": rid,
                    "type": "duplicate_event",
                    "detail": "Duplicate run_id found"
                })
            seen.add(rid)
        self.anomalies.extend(anomalies)
        return anomalies

    def full_check(self, events: List[Dict]) -> Dict:
        """执行所有检查"""
        self.anomalies = []
        self.verify_signatures(events)
        self.detect_causal_contradiction(events)
        self.detect_temporal_drift(events)
        self.detect_duplicate_events(events)
        return {
            "total_events": len(events),
            "anomaly_count": len(self.anomalies),
            "anomalies": self.anomalies,
            "malicious_suspicion": len([a for a in self.anomalies if a["type"] in ["invalid_signature", "identity_spoof", "causal_contradiction"]]) > 0
        }