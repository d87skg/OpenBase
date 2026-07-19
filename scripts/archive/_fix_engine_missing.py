with open(r'D:\OpenBase\openbase_core\tests\test_replay.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = "        broken_chain = [ev1, broken_ev2]\n\n        result = engine.replay(broken_chain, \"exec_001\", FidelityLevel.CAUSAL)"
new = "        engine = ReplayEngine(signer1)\n        broken_chain = [ev1, broken_ev2]\n\n        result = engine.replay(broken_chain, \"exec_001\", FidelityLevel.CAUSAL)"

content = content.replace(old, new)

with open(r'D:\OpenBase\openbase_core\tests\test_replay.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed: added engine = ReplayEngine(signer1)')
