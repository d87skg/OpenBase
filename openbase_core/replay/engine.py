"""
OpenBase Replay Engine
Replay v1.0 Implementation — reconstructs execution from Evidence Chain.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone


class FidelityLevel(str, Enum):
    STRUCTURAL = "STRUCTURAL"   # Hash chain integrity only
    CAUSAL = "CAUSAL"          # Causal ordering via vector clocks
    LOGICAL = "LOGICAL"        # State transitions without side effects
    EXACT = "EXACT"            # Full bit-exact replay


class ReplayStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ReplayErrorCode(str, Enum):
    E001 = "E001"  # Evidence chain incomplete
    E002 = "E002"  # Hash mismatch
    E003 = "E003"  # Signature verification failed
    E004 = "E004"  # Vector clock violation
    E005 = "E005"  # Invalid state transition
    E006 = "E006"  # Missing genesis evidence


@dataclass
class ReplayStep:
    """A single step in the replay trace."""
    step_index: int
    evidence_id: str
    event_type: str
    state_before: Optional[Dict[str, Any]]
    state_after: Optional[Dict[str, Any]]
    hash_valid: bool
    signature_valid: bool
    causal_valid: bool


@dataclass
class ReplayResult:
    """Result of a replay execution."""
    replay_id: str
    execution_id: str
    fidelity: FidelityLevel
    status: ReplayStatus
    total_steps: int
    steps: List[ReplayStep] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    final_state: Dict[str, Any] = field(default_factory=dict)
    error_code: Optional[ReplayErrorCode] = None
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "replay_id": self.replay_id,
            "execution_id": self.execution_id,
            "fidelity": self.fidelity.value,
            "status": self.status.value,
            "total_steps": self.total_steps,
            "steps": [
                {
                    "step_index": s.step_index,
                    "evidence_id": s.evidence_id,
                    "event_type": s.event_type,
                    "state_before": s.state_before,
                    "state_after": s.state_after,
                    "hash_valid": s.hash_valid,
                    "signature_valid": s.signature_valid,
                    "causal_valid": s.causal_valid,
                }
                for s in self.steps
            ],
            "errors": self.errors,
            "final_state": self.final_state,
            "error_code": self.error_code.value if self.error_code else None,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


class ReplayEngine:
    """Reconstructs Agent execution from an Evidence Chain."""

    def __init__(self, evidence_signer=None):
        """
        Args:
            evidence_signer: EvidenceSigner instance for verification.
                             If None, only structural replay is possible.
        """
        self._signer = evidence_signer

    def replay(
        self,
        evidence_chain: list,
        execution_id: str,
        fidelity: FidelityLevel = FidelityLevel.STRUCTURAL,
    ) -> ReplayResult:
        """Replay an evidence chain and reconstruct execution trace.

        Args:
            evidence_chain: List of Evidence objects in order.
            execution_id: Execution context identifier.
            fidelity: Desired replay fidelity level.

        Returns:
            ReplayResult with full trace, status, and errors.
        """
        from uuid import uuid4

        result = ReplayResult(
            replay_id=f"rpl_{uuid4().hex[:8]}",
            execution_id=execution_id,
            fidelity=fidelity,
            status=ReplayStatus.RUNNING,
            total_steps=len(evidence_chain),
        )

        state: Dict[str, Any] = {"status": "created", "events_processed": 0}
        steps = []

        try:
            # Step 0: Check genesis
            if len(evidence_chain) == 0:
                result.status = ReplayStatus.FAILED
                result.error_code = ReplayErrorCode.E006
                result.errors.append("E006: Missing genesis evidence — empty chain")
                result.completed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                return result

            # Step 1: STRUCTURAL — verify hash chain (always if fidelity >= STRUCTURAL)
            if fidelity in [FidelityLevel.STRUCTURAL, FidelityLevel.CAUSAL, FidelityLevel.LOGICAL, FidelityLevel.EXACT]:
                hash_ok, hash_errors = self._verify_hash_chain(evidence_chain)
                if not hash_ok:
                    result.status = ReplayStatus.FAILED
                    result.error_code = ReplayErrorCode.E002
                    result.errors.extend(hash_errors)
                    # Don't return yet — collect all errors for debugging
                    # But if we need CAUSAL check too, continue

            # Step 2: CAUSAL — verify vector clocks (always if fidelity >= CAUSAL)
            if fidelity in [FidelityLevel.CAUSAL, FidelityLevel.LOGICAL, FidelityLevel.EXACT]:
                causal_ok, causal_errors = self._verify_causal_order(evidence_chain)
                if not causal_ok:
                    result.status = ReplayStatus.FAILED
                    # If E002 not already set, set E004; otherwise chain is already broken
                    if result.error_code is None:
                        result.error_code = ReplayErrorCode.E004
                    result.errors.extend(causal_errors)
                    # Return after collecting errors
                    result.completed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                    return result

            # If STRUCTURAL failed earlier but we continued, return now
            if result.status == ReplayStatus.FAILED:
                result.completed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                return result

            # Step 3: LOGICAL — replay state transitions
            if fidelity in [FidelityLevel.LOGICAL, FidelityLevel.EXACT]:
                for i, evidence in enumerate(evidence_chain):
                    state_before = state.copy()

                    # Apply state transition based on event type
                    state = self._apply_transition(state, evidence)

                    # Verify signature if signer available
                    sig_valid = True
                    if self._signer:
                        sig_valid = self._signer.verify_evidence(evidence)

                    steps.append(ReplayStep(
                        step_index=i,
                        evidence_id=evidence.evidence_id,
                        event_type=evidence.event_type,
                        state_before=state_before,
                        state_after=state.copy(),
                        hash_valid=True,
                        signature_valid=sig_valid,
                        causal_valid=True,
                    ))

            # Step 4: EXACT — would re-execute (placeholder for now)
            if fidelity == FidelityLevel.EXACT:
                # Exact replay requires re-execution environment
                # For now, mark as LOGICAL success with EXACT flag
                pass

            result.steps = steps
            result.final_state = state
            result.status = ReplayStatus.COMPLETED

        except Exception as e:
            result.status = ReplayStatus.FAILED
            result.errors.append(f"Replay error: {str(e)}")
            if result.error_code is None:
                result.error_code = ReplayErrorCode.E001

        result.completed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return result

    def _verify_hash_chain(self, chain: list) -> tuple:
        """Verify SHA-256 hash chain integrity. Returns (ok, errors)."""
        errors = []
        for i, evidence in enumerate(chain):
            if i == 0:
                # Genesis: parent_id must be None
                if evidence.causal.parent_id is not None:
                    errors.append(f"E002 at step {i}: Genesis evidence has non-null parent_id")
            else:
                expected_parent = chain[i - 1].hash
                actual_parent = evidence.causal.parent_id
                if actual_parent != expected_parent:
                    errors.append(
                        f"E002 at step {i}: Hash chain broken. "
                        f"Expected parent {expected_parent[:16]}..., "
                        f"got {actual_parent[:16] if actual_parent else 'None'}..."
                    )

            # Verify individual hash if signer available
            if self._signer:
                if not self._signer.verify_evidence(evidence):
                    errors.append(f"E002 at step {i}: Hash verification failed for {evidence.evidence_id}")

        return len(errors) == 0, errors

    def _verify_causal_order(self, chain: list) -> tuple:
        """Verify vector clock monotonicity. Returns (ok, errors)."""
        errors = []
        for i in range(1, len(chain)):
            prev_vc = chain[i - 1].causal.vector_clock
            curr_vc = chain[i].causal.vector_clock

            # Check: for all actors, curr >= prev
            all_actors = set(list(prev_vc.keys()) + list(curr_vc.keys()))
            has_strict_increase = False
            for actor in all_actors:
                prev_val = prev_vc.get(actor, 0)
                curr_val = curr_vc.get(actor, 0)
                if curr_val < prev_val:
                    errors.append(
                        f"E004 at step {i}: Vector clock decreased for {actor}: "
                        f"{prev_val} -> {curr_val}"
                    )
                if curr_val > prev_val:
                    has_strict_increase = True

            if not has_strict_increase:
                errors.append(
                    f"E004 at step {i}: No vector clock increase between steps"
                )

        return len(errors) == 0, errors

    def _apply_transition(self, state: Dict[str, Any], evidence) -> Dict[str, Any]:
        """Apply a state transition based on event type."""
        new_state = state.copy()
        new_state["events_processed"] = state.get("events_processed", 0) + 1

        event_type = evidence.event_type
        if hasattr(event_type, 'value'):
            event_type = event_type.value

        # Agent lifecycle
        if event_type == "AGENT_STARTED":
            new_state["status"] = "running"
            new_state["task"] = evidence.payload.get("task", "")
        elif event_type == "AGENT_FINISHED":
            new_state["status"] = "completed"
            new_state["result"] = evidence.payload.get("result")
        elif event_type == "AGENT_FAILED":
            new_state["status"] = "failed"
            new_state["error"] = evidence.payload.get("error", "unknown error")

        # Tool execution
        elif event_type == "TOOL_CALL":
            new_state["status"] = "tool_executing"
            new_state["current_tool"] = evidence.payload.get("tool_name", "")
        elif event_type == "TOOL_RESULT":
            new_state["status"] = "running"
            tool_name = evidence.payload.get("tool_name", "unknown")
            new_state[f"tool_{tool_name}_result"] = evidence.payload.get("result")
        elif event_type == "TOOL_ERROR":
            new_state["status"] = "tool_error"
            tool_name = evidence.payload.get("tool_name", "unknown")
            new_state[f"tool_{tool_name}_error"] = evidence.payload.get("error")

        # LLM interaction
        elif event_type == "LLM_REQUEST":
            new_state["last_model"] = evidence.payload.get("model", "")
        elif event_type == "LLM_RESPONSE":
            new_state["last_response"] = evidence.payload.get("content", "")

        # Human interaction
        elif event_type == "APPROVAL_REQUEST":
            new_state["status"] = "awaiting_approval"
        elif event_type == "APPROVAL_GRANTED":
            new_state["status"] = "running"
            new_state["last_approval"] = "granted"
        elif event_type == "APPROVAL_DENIED":
            new_state["status"] = "running"
            new_state["last_approval"] = "denied"

        # Memory operations
        elif event_type == "MEMORY_READ":
            key = evidence.payload.get("key", "")
            new_state[f"memory_read_{key}"] = evidence.payload.get("value")
        elif event_type == "MEMORY_WRITE":
            key = evidence.payload.get("key", "")
            new_state[f"memory_{key}"] = evidence.payload.get("value")

        # File operations
        elif event_type == "FILE_READ":
            new_state["last_file_read"] = evidence.payload.get("path", "")
        elif event_type == "FILE_WRITE":
            new_state["last_file_written"] = evidence.payload.get("path", "")

        return new_state

    def get_execution_summary(self, result: ReplayResult) -> Dict[str, Any]:
        """Generate a human-readable execution summary."""
        if result.status != ReplayStatus.COMPLETED:
            return {
                "status": "failed",
                "error_code": result.error_code.value if result.error_code else "UNKNOWN",
                "errors": result.errors,
                "steps_completed": len(result.steps),
                "total_steps": result.total_steps,
            }

        event_types_seen = set(s.event_type for s in result.steps)
        return {
            "status": "completed",
            "fidelity": result.fidelity.value,
            "total_steps": result.total_steps,
            "duration": result.completed_at,
            "event_types": sorted(event_types_seen),
            "final_state": result.final_state,
            "all_hashes_valid": all(s.hash_valid for s in result.steps),
            "all_signatures_valid": all(s.signature_valid for s in result.steps),
            "all_causal_valid": all(s.causal_valid for s in result.steps),
        }
