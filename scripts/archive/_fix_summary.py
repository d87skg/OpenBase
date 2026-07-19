with open(r'D:\OpenBase\openbase_core\registry\runtime.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '"trust_level": self.trust_score.get_trust_level(self.trust_score.score) if self.trust_score else None,'
new = '"trust_level": None,  # computed by TrustEngine'

content = content.replace(old, new)

# Also fix to_summary to use TrustEngine for level
old_summary = '''    def to_summary(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "status": self.status,
            "event_count": len(self.events),
            "evidence_count": len(self.evidence_chain),
            "trust_score": self.trust_score.score if self.trust_score else None,
            "trust_level": self.trust_score.get_trust_level(self.trust_score.score) if self.trust_score else None,
            "certificate_level": self.certificate.level if self.certificate else None,
            "errors": self.errors,
            "duration": f"{self.started_at} -> {self.completed_at}",
        }'''

new_summary = '''    def to_summary(self) -> Dict[str, Any]:
        from openbase_core.trust import TrustEngine
        level = None
        if self.trust_score:
            level = TrustEngine().get_trust_level(self.trust_score.score)
        return {
            "execution_id": self.execution_id,
            "status": self.status,
            "event_count": len(self.events),
            "evidence_count": len(self.evidence_chain),
            "trust_score": self.trust_score.score if self.trust_score else None,
            "trust_level": level,
            "certificate_level": self.certificate.level if self.certificate else None,
            "errors": self.errors,
            "duration": f"{self.started_at} -> {self.completed_at}",
        }'''

content = content.replace(old_summary, new_summary)

with open(r'D:\OpenBase\openbase_core\registry\runtime.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed: to_summary uses TrustEngine.get_trust_level()')
