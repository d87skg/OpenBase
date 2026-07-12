"""
OpenBase Runtime MVP
End-to-end integration: Event -> Evidence -> Replay -> Trust -> Certificate
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone

from openbase_core.event import Event, EventFactory, EventValidator
from openbase_core.evidence import EvidenceSigner, Evidence
from openbase_core.replay import ReplayEngine, FidelityLevel
from openbase_core.trust import TrustEngine, TrustScore
from openbase_core.certificate import CertificateEngine, Certificate
from openbase_core.registry import Registry


@dataclass
class RuntimeConfig:
    """Configuration for an OpenBase Runtime."""
    agent_id: str = "agent.openbase.default"
    runtime_name: str = "openbase-runtime"
    runtime_version: str = "0.1.0"
    execution_id: Optional[str] = None

    def get_execution_id(self) -> str:
        if self.execution_id is None:
            from uuid import uuid4
            self.execution_id = f"exec_{uuid4().hex[:8]}"
        return self.execution_id


@dataclass
class ExecutionResult:
    """Result of a complete OpenBase execution."""
    execution_id: str
    events: List[Event] = field(default_factory=list)
    evidence_chain: List[Evidence] = field(default_factory=list)
    trust_score: Optional[TrustScore] = None
    certificate: Optional[Certificate] = None
    replay_result: Optional[Any] = None
    status: str = "pending"
    errors: List[str] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    completed_at: Optional[str] = None

    def to_summary(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "status": self.status,
            "event_count": len(self.events),
            "evidence_count": len(self.evidence_chain),
            "trust_score": self.trust_score.score if self.trust_score else None,
            "trust_level": None,  # computed by TrustEngine
            "certificate_level": self.certificate.level if self.certificate else None,
            "errors": self.errors,
            "duration": f"{self.started_at} -> {self.completed_at}",
        }


class OpenBaseRuntime:
    """End-to-end OpenBase Runtime.

    Integrates all engines into a single execution pipeline:
    Event -> Evidence -> Replay -> Trust -> Certificate
    """

    def __init__(self, config: Optional[RuntimeConfig] = None):
        self.config = config or RuntimeConfig()
        self.event_factory = EventFactory(
            self.config.agent_id,
            self.config.runtime_name,
            self.config.runtime_version,
        )
        self.signer = EvidenceSigner()
        self.validator = EventValidator()
        self.replay_engine = ReplayEngine(self.signer)
        self.trust_engine = TrustEngine(self.signer)
        self.cert_engine = CertificateEngine(signer=self.signer)
        self.registry = Registry()

        self._events: List[Event] = []
        self._evidence_chain: List[Evidence] = []

        # Register this runtime
        self.registry.register("runtime", self.config.runtime_name, self.config.runtime_version)

    def emit(self, event: Event) -> Event:
        """Emit an event and convert to evidence."""
        if not self.validator.is_valid(event):
            raise ValueError(f"Invalid event: {event.event_id}")

        self._events.append(event)
        evidence = self.signer.sign_event(event, self.config.get_execution_id())
        self._evidence_chain.append(evidence)
        return event

    # Convenience methods
    def agent_started(self, task: str, **kwargs) -> Event:
        return self.emit(self.event_factory.agent_started(task, **kwargs))

    def agent_finished(self, result: Any = None) -> Event:
        parent = self._events[-1].event_id if self._events else None
        return self.emit(self.event_factory.agent_finished(result, parent_id=parent))

    def tool_error_event(self, tool_name: str, error: str) -> Event:
        parent = self._events[-1].event_id if self._events else None
        return self.emit(self.event_factory.tool_error(tool_name, error, parent_id=parent))

    def agent_failed(self, error: str) -> Event:
        parent = self._events[-1].event_id if self._events else None
        return self.emit(self.event_factory.agent_failed(error, parent_id=parent))

    def tool_call(self, tool_name: str, tool_input: Dict) -> Event:
        parent = self._events[-1].event_id if self._events else None
        return self.emit(self.event_factory.tool_call(tool_name, tool_input, parent_id=parent))

    def tool_result(self, tool_name: str, result: Any) -> Event:
        parent = self._events[-1].event_id if self._events else None
        return self.emit(self.event_factory.tool_result(tool_name, result, parent_id=parent))

    def llm_request(self, model: str, messages: list, **kwargs) -> Event:
        parent = self._events[-1].event_id if self._events else None
        return self.emit(self.event_factory.llm_request(model, messages, kwargs, parent_id=parent))

    def finish(self) -> ExecutionResult:
        """Complete execution and compute trust + certificate."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        result = ExecutionResult(
            execution_id=self.config.get_execution_id(),
            events=self._events.copy(),
            evidence_chain=self._evidence_chain.copy(),
            status="completed",
        )

        # Replay
        try:
            result.replay_result = self.replay_engine.replay(
                self._evidence_chain,
                self.config.get_execution_id(),
                FidelityLevel.LOGICAL,
            )
        except Exception as e:
            result.errors.append(f"Replay failed: {e}")

        # Trust
        try:
            result.trust_score = self.trust_engine.compute_trust(
                self.config.agent_id,
                "agent",
                self._evidence_chain,
                certificates=self.cert_engine.get_active_certificates(self.config.agent_id),
            )
        except Exception as e:
            result.errors.append(f"Trust computation failed: {e}")

        # Certificate
        try:
            if result.trust_score and result.trust_score.score >= 0.30:
                result.certificate = self.cert_engine.issue(
                    self.config.agent_id,
                    "agent",
                    result.trust_score,
                )
        except Exception as e:
            result.errors.append(f"Certificate issuance failed: {e}")

        if result.errors:
            result.status = "completed_with_errors"

        result.completed_at = now
        return result

    def get_evidence_chain(self) -> List[Evidence]:
        return self._evidence_chain.copy()

    def reset(self):
        """Reset runtime for a new execution."""
        self._events = []
        self._evidence_chain = []
        self.signer.reset_chain()
        self.config.execution_id = None
