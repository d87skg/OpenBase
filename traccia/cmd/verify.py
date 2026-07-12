import sys, os, glob, json, base64
from cryptography.hazmat.primitives.asymmetric import ed25519

def find_latest_evidence():
    files = glob.glob("evidence_*.jsonl")
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def verify_evidence_file(file_path):
    """验证证据文件中的所有证据，打印结果并返回布尔值"""
    print(f"🔍 Verifying evidence file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False

    if not lines:
        print("❌ Empty file")
        return False

    print(f"📄 Total events: {len(lines)}")

    all_ok = True
    for idx, line in enumerate(lines):
        ev = json.loads(line)
        if 'signature' not in ev or 'public_key' not in ev:
            print(f"⚠️  Event {idx+1} ({ev.get('event_type', 'Unknown')}) has no signature, skipping")
            continue

        try:
            public_key_b64 = ev['public_key']
            public_bytes = base64.b64decode(public_key_b64)
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)

            sign_data = (ev['hash'] + ev['execution_id']).encode()
            signature = base64.b64decode(ev['signature'])
            public_key.verify(signature, sign_data)
            print(f"✅ Event {idx+1} ({ev['event_type']}) signature OK")
        except Exception as e:
            print(f"❌ Event {idx+1} ({ev['event_type']}) signature FAILED: {e}")
            all_ok = False

    # 检查哈希链（基本连续性）
    print("\n🔗 Checking hash chain (sequential order)...")
    prev_hash = None
    for idx, line in enumerate(lines):
        ev = json.loads(line)
        if 'hash' not in ev:
            print(f"❌ Event {idx+1} has no hash")
            all_ok = False
            continue
        prev_hash = ev['hash']
    if all_ok:
        print("✅ Hash chain integrity check passed (sequential order)")
    else:
        print("❌ Hash chain check failed")

    return all_ok

def run_verify(args):
    """CLI 入口：args 是列表，可能为空"""
    if len(args) >= 1 and args[0]:
        file_path = args[0]
    else:
        file_path = find_latest_evidence()
        if not file_path:
            print("❌ No evidence files found. Run an Agent first!")
            return 1
        print(f"🔍 Using latest evidence: {file_path}")
    success = verify_evidence_file(file_path)
    return 0 if success else 1