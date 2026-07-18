import sys
sys.path.insert(0, r'D:\OpenBase')

"""Demo 1: Coding Agent Audit — Tracks file edits with full evidence chain."""
from traccia.traccia.session.manager import Session
from traccia.traccia.renderer.timeline import TimelineRenderer
from traccia.traccia.package.exporter import export_package
from traccia.traccia.openbase_adapter import OpenBaseSignerBridge
from traccia.traccia.openbase_adapter.evidence_converter import batch_convert

session = Session(objective="Refactor authentication module", agent_id="agent.coding.audit")
session.record("file_read", {"path": "/src/auth.py", "lines": 150})
session.record("tool_start", {"tool_name": "edit_file", "path": "/src/auth.py"})
session.record("file_write", {"path": "/src/auth.py", "changes": "+45 lines, -12 lines"})
session.record("execute_shell", {"command": "pytest tests/test_auth.py"})
session.record("tool_finish", {"tool_name": "edit_file", "success": True})
session.record("llm_request", {"model": "claude-sonnet-4", "purpose": "code review"})
session.record("llm_response", {"verdict": "Changes approved, no security issues"})
session.complete()

bridge = OpenBaseSignerBridge()
chain = bridge.sign_chain(batch_convert(session.get_events(), session.execution_id, session.agent_id))
renderer = TimelineRenderer(chain)
print(renderer.render_text())
path = export_package(session, chain, "coding_audit.evidence")
print(f"Evidence package: {path}")
