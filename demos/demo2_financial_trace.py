import sys
sys.path.insert(0, r'D:\OpenBase')

"""Demo 2: Financial Agent Trace — Responsibility chain for financial transactions."""
from traccia.traccia.session.manager import Session
from traccia.traccia.renderer.timeline import TimelineRenderer
from traccia.traccia.package.exporter import export_package
from traccia.traccia.openbase_adapter import OpenBaseSignerBridge
from traccia.traccia.openbase_adapter.evidence_converter import batch_convert

session = Session(objective="Execute trade: BUY 1000 AAPL at market", agent_id="agent.trading.desk")
session.record("agent_start", {"portfolio": "growth-fund", "risk_level": "moderate"})
session.record("llm_request", {"model": "gpt-5", "purpose": "market analysis"})
session.record("llm_response", {"recommendation": "BUY", "confidence": 0.87})
session.record("tool_start", {"tool_name": "check_balance", "account": "growth-fund"})
session.record("tool_finish", {"tool_name": "check_balance", "balance": ".5M"})
session.record("approval_request", {"action": "BUY 1000 AAPL", "amount": ",000"})
session.record("approval_granted", {"approver": "human.supervisor"})
session.record("tool_start", {"tool_name": "execute_trade", "symbol": "AAPL", "quantity": 1000})
session.record("tool_finish", {"tool_name": "execute_trade", "order_id": "ORD-78912", "status": "filled"})
session.complete()

bridge = OpenBaseSignerBridge()
chain = bridge.sign_chain(batch_convert(session.get_events(), session.execution_id, session.agent_id))
renderer = TimelineRenderer(chain)
print(renderer.render_markdown())
path = export_package(session, chain, "financial_trace.evidence", attribution={"executor": "agent.trading.desk", "supervisor": "human.supervisor"})
print(f"Evidence package: {path}")
