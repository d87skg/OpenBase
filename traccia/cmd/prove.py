import sys, os, glob, json
from openbase_core.proof_generator import ProofGenerator

def load_events(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def find_latest_evidence():
    files = glob.glob("evidence_*.jsonl")
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def run_prove(file_path, output_path):
    if not file_path:
        file_path = find_latest_evidence()
        if not file_path:
            print("❌ No evidence files found. Run an Agent first!")
            return 1

    print(f"📂 Generating proof from: {file_path}")
    events = load_events(file_path)
    if not events:
        print("❌ No events found.")
        return 1

    # 获取 execution_id（从第一个事件）
    execution_id = events[0].get("execution_id", "unknown")
    
    generator = ProofGenerator(events, execution_id)
    proof = generator.generate_full_proof()

    if not output_path:
        output_path = f"proof_{execution_id[:8]}_{os.path.basename(file_path).replace('.jsonl', '')}.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(proof, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Proof generated: {output_path}")
    print(f"   Root hash: {proof['root_hash'][:32]}...")
    print(f"   Events: {proof['event_count']}")
    print(f"   State commitment: {proof['state_commitment'][:32]}...")
    return 0