import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class CrewAICallback:
    def __init__(self, runtime_id: str, evidence_dir: str = "./evidence"):
        self.runtime_id = runtime_id
        self.evidence_dir = Path(evidence_dir)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self._evidence: List[Dict[str, Any]] = []

    def _generate_evidence(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        evidence_id = f"evid-{uuid.uuid4().hex[:8]}"
        timestamp = datetime.now().isoformat()

        evidence = {
            "evidence_id": evidence_id,
            "spec_version": "1.0",
            "runtime_id": self.runtime_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "payload": payload,
            "proof": {
                "hash": "sha256:crewai_adapter_hash",
                "signature": "ed25519:crewai_adapter_signature"
            }
        }

        filepath = self.evidence_dir / f"{evidence_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)

        self._evidence.append(evidence)
        return evidence

    def on_crew_start(self, crew_name: str, agents: List[str], tasks: List[str]) -> None:
        self._generate_evidence("CREWAI_CREW_START", {
            "crew_name": crew_name,
            "agents": agents,
            "tasks": tasks
        })

    def on_crew_end(self, crew_name: str, results: Dict) -> None:
        self._generate_evidence("CREWAI_CREW_END", {
            "crew_name": crew_name,
            "results": results
        })

    def on_crew_error(self, crew_name: str, error: Exception) -> None:
        self._generate_evidence("ERROR", {
            "crew_name": crew_name,
            "error_type": type(error).__name__,
            "error_message": str(error)
        })

    def on_agent_start(self, agent_name: str, role: str, goal: str) -> None:
        self._generate_evidence("CREWAI_AGENT_START", {
            "agent_name": agent_name,
            "role": role,
            "goal": goal
        })

    def on_agent_end(self, agent_name: str, output: str) -> None:
        self._generate_evidence("CREWAI_AGENT_END", {
            "agent_name": agent_name,
            "output": output
        })

    def on_agent_error(self, agent_name: str, error: Exception) -> None:
        self._generate_evidence("ERROR", {
            "agent_name": agent_name,
            "error_type": type(error).__name__,
            "error_message": str(error)
        })

    def on_task_start(self, task_name: str, description: str, agent: str) -> None:
        self._generate_evidence("CREWAI_TASK_START", {
            "task_name": task_name,
            "description": description,
            "assigned_to": agent
        })

    def on_task_end(self, task_name: str, output: str) -> None:
        self._generate_evidence("CREWAI_TASK_END", {
            "task_name": task_name,
            "output": output
        })

    def on_task_error(self, task_name: str, error: Exception) -> None:
        self._generate_evidence("ERROR", {
            "task_name": task_name,
            "error_type": type(error).__name__,
            "error_message": str(error)
        })

    def on_tool_start(self, tool_name: str, input_data: str) -> None:
        self._generate_evidence("CREWAI_TOOL_START", {
            "tool_name": tool_name,
            "input": input_data
        })

    def on_tool_end(self, tool_name: str, output: str) -> None:
        self._generate_evidence("CREWAI_TOOL_END", {
            "tool_name": tool_name,
            "output": output
        })

    def on_tool_error(self, tool_name: str, error: Exception) -> None:
        self._generate_evidence("ERROR", {
            "tool_name": tool_name,
            "error_type": type(error).__name__,
            "error_message": str(error)
        })

    def get_evidence(self) -> List[Dict[str, Any]]:
        return self._evidence


class CrewAIAdapter:
    def __init__(self, runtime_id: str, evidence_dir: str = "./evidence"):
        self.runtime_id = runtime_id
        self.callback = CrewAICallback(runtime_id, evidence_dir)

    def get_callback(self) -> CrewAICallback:
        return self.callback

    def simulate_crew_execution(self, crew_name: str, agents: List[Dict], tasks: List[Dict]) -> Dict:
        agent_names = [a.get("name", "unknown") for a in agents]
        task_names = [t.get("name", "unknown") for t in tasks]
        self.callback.on_crew_start(crew_name, agent_names, task_names)

        results = {}

        try:
            for agent in agents:
                agent_name = agent.get("name", "unknown")
                role = agent.get("role", "worker")
                goal = agent.get("goal", "complete tasks")

                self.callback.on_agent_start(agent_name, role, goal)

                agent_results = []

                for task in tasks:
                    task_name = task.get("name", "unknown")
                    description = task.get("description", "No description")

                    self.callback.on_task_start(task_name, description, agent_name)

                    tool = task.get("tool")
                    if tool:
                        self.callback.on_tool_start(tool, f"input for {tool}")
                        self.callback.on_tool_end(tool, f"result from {tool}")

                    task_output = f"Task '{task_name}' completed by {agent_name}"
                    self.callback.on_task_end(task_name, task_output)
                    agent_results.append(task_output)

                agent_output = f"Agent {agent_name} completed {len(agent_results)} tasks"
                self.callback.on_agent_end(agent_name, agent_output)
                results[agent_name] = agent_results

            self.callback.on_crew_end(crew_name, results)
            return {"status": "completed", "results": results}

        except Exception as e:
            self.callback.on_crew_error(crew_name, e)
            raise

    def get_evidence(self) -> List[Dict[str, Any]]:
        return self.callback.get_evidence()
