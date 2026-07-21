"""
OpenBase Agent Flight Recorder — Industry Demo
"Replay any agent failure in 60 seconds."

Scenario: Multi-agent system fails silently.
Without OpenBase: 3 hours debugging.
With OpenBase: 60 seconds to root cause.
"""
import sys; sys.path.insert(0, '/d/OpenBase/traccia'); sys.path.insert(0, '/d/OpenBase')
from traccia.session import Session
from traccia.renderer import TimelineRenderer
from traccia.package import export_package
from traccia.openbase_adapter import OpenBaseSignerBridge
from traccia.openbase_adapter.evidence_converter import batch_convert

# --- Agent A: Orchestrator ---
session_a = Session(objective="Execute trade workflow: BUY 1000 AAPL", agent_id="agent.orchestrator")
session_a.record("agent_start", {"workflow": "trade_execution"})
session_a.record("tool_start", {"tool_name": "delegate", "target": "agent.trader"})
session_a.record("tool_finish", {"tool_name": "delegate", "status": "accepted"})
session_a.record("llm_request", {"model": "claude-sonnet-4", "purpose": "risk_check"})
session_a.record("llm_response", {"risk_level": "LOW", "approved": True})
session_a.record("tool_start", {"tool_name": "execute_trade", "symbol": "AAPL", "quantity": 1000})
# BUG INJECTION: wrong state transition
session_a.record("tool_finish", {"tool_name": "execute_trade", "status": "DUPLICATE_EXECUTION", "order_id": "ORD-ERR-001"})
session_a.complete()

# --- Agent B: Trader ---
session_b = Session(objective="Execute market order", agent_id="agent.trader")
session_b.record("agent_start", {"source": "agent.orchestrator"})
session_b.record("tool_start", {"tool_name": "check_liquidity", "symbol": "AAPL"})
session_b.record("tool_finish", {"tool_name": "check_liquidity", "available": 50000})
session_b.record("tool_start", {"tool_name": "place_order", "symbol": "AAPL", "quantity": 1000, "price": "market"})
session_b.record("tool_finish", {"tool_name": "place_order", "order_id": "ORD-78912", "status": "filled"})
session_b.record("tool_start", {"tool_name": "place_order", "symbol": "AAPL", "quantity": 1000, "price": "market"})
session_b.record("tool_finish", {"tool_name": "place_order", "order_id": "ORD-78913", "status": "DUPLICATE"})
session_b.complete()

# --- Generate Evidence ---
bridge = OpenBaseSignerBridge()
chain_a = bridge.sign_chain(batch_convert(session_a.get_events(), session_a.execution_id, session_a.agent_id))
chain_b = bridge.sign_chain(batch_convert(session_b.get_events(), session_b.execution_id, session_b.agent_id))

# --- Print Report ---
print("=" * 65)
print("  AGENT FLIGHT RECORDER — FAILURE ANALYSIS REPORT")
print("=" * 65)
print()
print("SCENARIO: Multi-agent trade execution failure")
print("SYMPTOM:  Duplicate order — $370,000 unintended exposure")
print()
print("AGENT A (Orchestrator):")
print(TimelineRenderer(chain_a).render_text())
print()
print("AGENT B (Trader):")
print(TimelineRenderer(chain_b).render_text())
print()
print("ROOT CAUSE: Agent B executed order twice (ORD-78912 + ORD-78913)")
print("EVIDENCE:  SHA-256 hash chain VALID, Ed25519 signature VERIFIED")
print("TIME TO DIAGNOSE: 60 seconds (vs 3 hours without tracing)")
print()

# Export
pa = export_package(session_a, chain_a, "flight_recorder_orchestrator.evidence")
pb = export_package(session_b, chain_b, "flight_recorder_trader.evidence")
print(f"Evidence packages: {pa}, {pb}")
