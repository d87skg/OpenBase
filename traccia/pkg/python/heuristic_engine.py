import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

class HeuristicScorer:
    def __init__(self, evidence_list: List[Dict[str, Any]]):
        self.evidence = evidence_list
        self.total_events = len(evidence_list)
        self.violations = [e for e in evidence_list if e.get("event_type") == "PolicyViolation"]
        self.tool_calls = [e for e in evidence_list if e.get("event_type") == "ToolCall"]
        self.agent_ids = list(set(e.get("agent_id") for e in evidence_list if e.get("agent_id")))
        self.execution_ids = list(set(e.get("execution_id") for e in evidence_list if e.get("execution_id")))
        self.unique_tools = list(set(
            e.get("payload", {}).get("tool_name") 
            for e in self.tool_calls 
            if e.get("payload", {}).get("tool_name")
        ))
    
    def calculate(self) -> Dict[str, Any]:
        # 基础�?100
        score = 100.0
        
        # 扣分项：每次违规�?15 �?        violation_count = len(self.violations)
        score -= violation_count * 15
        
        # 扣分项：工具调用过多（超�?10 次扣 5 分）
        tool_count = len(self.tool_calls)
        if tool_count > 10:
            score -= 5
        
        # 加分项：有证据签名（安全�?        signed_count = sum(1 for e in self.evidence if e.get("signature"))
        if signed_count == self.total_events and self.total_events > 0:
            score += 5
        
        # 确保分数�?0-100 之间
        score = max(0, min(100, score))
        
        risk_level = "Low" if score >= 80 else "Medium" if score >= 50 else "High"
        
        return {
            "score": round(score, 1),
            "risk_level": risk_level,
            "violation_count": violation_count,
            "tool_call_count": tool_count,
            "unique_tools": self.unique_tools,
            "agent_ids": self.agent_ids,
            "execution_ids": self.execution_ids,
            "total_events": self.total_events,
            "signed_events": signed_count,
            "details": {
                "violations": [
                    {
                        "tool_name": v.get("payload", {}).get("tool_name"),
                        "reason": v.get("payload", {}).get("reason"),
                        "timestamp": v.get("timestamp")
                    }
                    for v in self.violations
                ]
            }
        }

class ExperimentalReportBuilder:
    def __init__(self, evidence_path: str, output_dir: str = "reports"):
        self.evidence_path = evidence_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        with open(evidence_path, 'r', encoding='utf-8') as f:
            self.evidence_list = [json.loads(line) for line in f if line.strip()]
        
        self.scorer = HeuristicScorer(self.evidence_list)
        self.result = self.scorer.calculate()
    
    def generate_json(self) -> str:
        path = os.path.join(self.output_dir, f"governance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.result, f, indent=2, ensure_ascii=False)
        return path
    
    def generate_markdown(self) -> str:
        path = os.path.join(self.output_dir, f"governance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        
        score = self.result["score"]
        risk = self.result["risk_level"]
        # �?ASCII 简易图�?        bar_length = int(score / 2)  # 0-50 个字�?        bar = "�? * bar_length + "�? * (50 - bar_length)
        
        lines = [
            "# 🔍 AES Governance Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Evidence File:** `{os.path.basename(self.evidence_path)}`",
            "",
            "## 📊 Risk Score",
            "",
            f"**Score: `{score}/100`**",
            f"**Risk Level: `{risk}`**",
            "",
            f"```",
            f"[{bar}]  {score}%",
            f"```",
            "",
            "## 📈 Metrics",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Events | {self.result['total_events']} |",
            f"| Tool Calls | {self.result['tool_call_count']} |",
            f"| Unique Tools | {len(self.result['unique_tools'])} |",
            f"| Policy Violations | {self.result['violation_count']} |",
            f"| Signed Events | {self.result['signed_events']} |",
            f"| Agents | {', '.join(self.result['agent_ids'])} |",
            "",
            "## ⚠️ Violation Details",
            ""
        ]
        
        if self.result["details"]["violations"]:
            for v in self.result["details"]["violations"]:
                lines.append(f"- **{v.get('tool_name', 'unknown')}**: {v.get('reason', 'No reason')} (at {v.get('timestamp', 'N/A')})")
        else:
            lines.append("�?No policy violations detected.")
        
        lines.append("")
        lines.append("---")
        lines.append("*Report generated by OpenBase AES Governance Engine v0.1*")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        return path
    
    def generate(self):
        json_path = self.generate_json()
        md_path = self.generate_markdown()
        return json_path, md_path
