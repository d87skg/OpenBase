with open(r'D:\OpenBase\openbase_core\tests\test_trust.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    def test_should_renew_gold_when_score_high(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        chain = [signer.sign_event(factory.agent_started("task"), "exec_001")] * 200

        engine = TrustEngine(signer)
        score = engine.compute_trust("agent.test", "agent", chain)

        assert engine.should_renew_certificate(score, "GOLD") is True'''

new = '''    def test_should_renew_gold_when_score_high(self):
        signer = EvidenceSigner()
        factory = EventFactory("agent.test", "openclaw", "0.1.0")
        engine = TrustEngine(signer)

        # Build a chain with many successful agent completions to boost consistency
        chain = []
        for i in range(200):
            chain.append(signer.sign_event(factory.agent_started(f"task_{i}"), "exec_001"))
            chain.append(signer.sign_event(factory.agent_finished(f"success_{i}"), "exec_001"))

        score = engine.compute_trust("agent.test", "agent", chain)

        # With 400 evidence (200 start + 200 finish), score should exceed GOLD threshold
        assert score.score >= 0.70, f"Expected score >= 0.70, got {score.score}"
        assert engine.should_renew_certificate(score, "GOLD") is True'''

content = content.replace(old, new)

with open(r'D:\OpenBase\openbase_core\tests\test_trust.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed: test_should_renew_gold now uses successful completions')
