import sys
sys.path.insert(0, r'D:\OpenBase')

"""Demo 3: Multi-Agent Collaboration — Two agents with causal ordering."""
from traccia.traccia.session.manager import Session
from traccia.traccia.renderer.timeline import TimelineRenderer
from traccia.traccia.package.exporter import export_package
from traccia.traccia.openbase_adapter import OpenBaseSignerBridge
from traccia.traccia.openbase_adapter.evidence_converter import batch_convert

session_a = Session(objective="Research AI safety papers", agent_id="agent.researcher")
session_a.record("agent_start", {"topic": "AI safety"})
session_a.record("tool_start", {"tool_name": "search_papers", "query": "AI safety 2026"})
session_a.record("tool_finish", {"tool_name": "search_papers", "results": 23})
session_a.record("llm_request", {"model": "claude-sonnet-4", "purpose": "summarize findings"})
session_a.record("llm_response", {"summary": "Key risks: alignment, robustness, interpretability"})
session_a.complete()

session_b = Session(objective="Review research findings", agent_id="agent.reviewer")
session_b.record("agent_start", {"source": "agent.researcher"})
session_b.record("file_read", {"path": "/research/safety_findings.md"})
session_b.record("llm_request", {"model": "gpt-5", "purpose": "validate methodology"})
session_b.record("llm_response", {"validation": "Methodology sound, sample size adequate"})
session_b.record("approval_request", {"action": "publish findings"})
session_b.record("approval_granted", {"approver": "human.editor"})
session_b.complete()

bridge = OpenBaseSignerBridge()
chain_a = bridge.sign_chain(batch_convert(session_a.get_events(), session_a.execution_id, session_a.agent_id))
chain_b = bridge.sign_chain(batch_convert(session_b.get_events(), session_b.execution_id, session_b.agent_id))

print("=== Agent A: Researcher ===")
print(TimelineRenderer(chain_a).render_text())
print("\n=== Agent B: Reviewer ===")
print(TimelineRenderer(chain_b).render_text())

pa = export_package(session_a, chain_a, "multi_agent_researcher.evidence")
pb = export_package(session_b, chain_b, "multi_agent_reviewer.evidence")
print(f"Packages: {pa}, {pb}")
