import sys, os, glob, json
from openbase_core.verifier import ProofVerifier

def find_latest_proof():
    files = glob.glob("proof_*.json")
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def run_proof_verify(proof_file=None, full_mode=False):
    # 如果未指定文件，尝试查找最新的 proof
    if proof_file is None:
        proof_file = find_latest_proof()
        if proof_file is None:
            print("❌ No proof files found. Run 'openbase prove' first.")
            return 1
        print(f"🔍 Using latest proof: {proof_file}")
    else:
        # 如果包含通配符，进行 glob 并选择最新的
        if '*' in proof_file or '?' in proof_file:
            matches = glob.glob(proof_file)
            if not matches:
                print(f"❌ No files matching: {proof_file}")
                return 1
            # 选择最新的
            proof_file = max(matches, key=os.path.getmtime)
            print(f"🔍 Using latest match: {proof_file}")
        elif not os.path.exists(proof_file):
            print(f"❌ Proof file not found: {proof_file}")
            return 1

    print(f"🔍 Verifying proof: {proof_file}")
    
    try:
        with open(proof_file, 'r', encoding='utf-8') as f:
            proof = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in proof file: {proof_file}")
        return 1

    verifier = ProofVerifier(proof)
    
    if full_mode:
        result = verifier.verify_full()
        print("\n📊 Full Verification Result:")
        print(f"  Valid: {result['valid']}")
        if result.get('verified_events'):
            print(f"  Verified events: {len(result['verified_events'])}")
            for ev in result['verified_events'][:5]:
                print(f"    - Event {ev['index']}: {ev['event_type']} ✅")
        if result.get('errors'):
            print(f"  Errors: {len(result['errors'])}")
            for err in result['errors']:
                print(f"    - {err}")
    else:
        result = verifier.verify()
        print("\n📊 Verification Result:")
        print(f"  Valid: {result['valid']}")
        for check in result.get('checks', []):
            status = "✅" if check.get('status') == "passed" else "❌"
            print(f"  {status} {check['name']}: {check.get('detail', '')}")
        for err in result.get('errors', []):
            print(f"  ❌ ERROR: {err}")

    return 0 if result['valid'] else 1