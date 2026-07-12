from typing import List, Dict, Any
from .byzantine_detector import ByzantineDetector
from .fault_injector import FaultInjector

class InconsistencyProver:
    def __init__(self, original_events: List[Dict], corrupted_events: List[Dict]):
        self.original = original_events
        self.corrupted = corrupted_events
        self.detector = ByzantineDetector()

    def prove(self) -> Dict:
        """生成不一致证明报告"""
        # 1. 检测原始事件是否有异常（基线）
        base_check = self.detector.full_check(self.original)

        # 2. 检测损坏事件
        self.detector = ByzantineDetector()  # 重置
        corrupted_check = self.detector.full_check(self.corrupted)

        # 3. 比较节点、执行ID等
        orig_ids = {e.get("run_id") for e in self.original if e.get("run_id")}
        corr_ids = {e.get("run_id") for e in self.corrupted if e.get("run_id")}
        missing = orig_ids - corr_ids
        extra = corr_ids - orig_ids

        # 4. 检测签名不一致
        orig_signed = sum(1 for e in self.original if "signature" in e)
        corr_signed = sum(1 for e in self.corrupted if "signature" in e)

        return {
            "inconsistency_found": corrupted_check["anomaly_count"] > 0 or missing or extra,
            "base_anomalies": base_check["anomalies"],
            "corrupted_anomalies": corrupted_check["anomalies"],
            "missing_events": list(missing),
            "extra_events": list(extra),
            "signature_discrepancy": {
                "original_signed": orig_signed,
                "corrupted_signed": corr_signed
            },
            "malicious_suspicion": corrupted_check["malicious_suspicion"]
        }