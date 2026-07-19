import os
import sys
import glob
from openbase_core.heuristic_engine import ReportGenerator  # 改名

def find_latest_evidence(pattern="evidence_*.jsonl"):
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def run_report(args):
    if len(args) >= 1:
        file_path = args[0]
    else:
        file_path = find_latest_evidence()
        if not file_path:
            print("❌ No evidence files found. Run an Agent first!")
            return 1
    print(f"📂 Processing: {file_path}")
    try:
        generator = ReportGenerator(file_path)
        json_path, md_path = generator.generate()
        print(f"✅ JSON report: {json_path}")
        print(f"✅ Markdown report: {md_path}")
        result = generator.result
        print("\n" + "="*50)
        print("🔍 AES Governance Summary")
        print("="*50)
        print(f"Risk Score: {result['score']}/100 ({result['risk_level']})")
        print(f"Violations: {result['violation_count']}")
        print(f"Tool Calls: {result['tool_call_count']}")
        print(f"Total Events: {result['total_events']}")
        print("="*50)
        return 0
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return 1