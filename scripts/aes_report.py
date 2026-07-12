import sys
import os
import glob
from openbase_core.governance import ReportGenerator

def find_latest_evidence(pattern="evidence_*.jsonl"):
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

if __name__ == "__main__":
    # 如果命令行指定了文件，使用它；否则找最新的 evidence_*.jsonl
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = find_latest_evidence()
        if not file_path:
            print("❌ No evidence files found. Run an Agent first!")
            sys.exit(1)
    
    print(f"📂 Processing: {file_path}")
    
    generator = ReportGenerator(file_path)
    json_path, md_path = generator.generate()
    
    print(f"✅ JSON report: {json_path}")
    print(f"✅ Markdown report: {md_path}")
    
    # 打印摘要
    result = generator.result
    print("\n" + "="*50)
    print(f"🔍 AES Governance Summary")
    print("="*50)
    print(f"Risk Score: {result['score']}/100 ({result['risk_level']})")
    print(f"Violations: {result['violation_count']}")
    print(f"Tool Calls: {result['tool_call_count']}")
    print(f"Total Events: {result['total_events']}")
    print("="*50)