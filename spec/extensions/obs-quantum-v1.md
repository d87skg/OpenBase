# OBS Quantum Extension v1.0

## Status: Draft — interface frozen, implementation deferred

## Purpose
Define canonical event types for quantum computing jobs within OpenBase execution traces.

## Event Types

| Event | Description |
|-------|-------------|
| `quantum.job.start` | QPU job submitted |
| `quantum.job.finish` | QPU job completed |
| `quantum.job.error` | QPU job failed |
| `quantum.backend` | Target backend (ionq, ibm, quera, qinghe, etc.) |
| `quantum.result_hash` | Verifiable hash of quantum output |

## Payload Schema

```json
{
  "event_type": "quantum.job.start",
  "payload": {
    "backend": "qinghe-1",
    "shots": 4096,
    "circuit_hash": "sha256:...",
    "estimated_cost_usd": 12.50
  }
}
Integration Rule
This is an Extension, NOT Core OBS.

Implementations create Quantum Adapters that emit these events.

No runtime dependency on any quantum platform.

Freeze Period
Interface frozen until first real quantum agent integration.
