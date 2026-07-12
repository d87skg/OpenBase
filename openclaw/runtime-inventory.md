# OpenClaw Runtime Inventory

## Purpose

This document inventories the observable behaviors of OpenClaw Runtime as they relate to Execution Semantics.

This is a **factual record** of what OpenClaw actually does. No interpretation, no mapping.

## Execution Lifecycle

### States

- STARTING
- RUNNING
- PLANNING
- THINKING
- TOOL_SELECTING
- TOOL_EXECUTING
- MEMORY_LOADING
- MEMORY_SAVING
- WAITING
- INTERRUPTED
- RETRYING
- RESUMING
- FINISHING
- SHUTDOWN
- ERROR

### Actions / Hooks

- before_llm
- after_llm
- before_tool
- after_tool
- before_memory
- after_memory
- before_planning
- after_planning
- on_retry
- on_interrupt
- on_resume
- on_complete
- on_error
- before_loop
- after_loop

## Context Metadata

### Fields

- execution_id
- parent_execution_id
- root_execution_id
- session_id
- workflow_id
- agent_name
- agent_version
- model
- temperature
- max_tokens
- tools (list)
- memory (state)
- prompt (content)

## Event Types (Current)

### Events emitted

- STARTED
- LLM_REQUEST
- LLM_RESPONSE
- TOOL_INVOKED
- TOOL_RESULT
- MEMORY_READ
- MEMORY_WRITE
- PLAN_CREATED
- PLAN_UPDATED
- RETRY
- ERROR
- COMPLETED
- CANCELLED

## Failure Modes

### Observed failures

- LLM timeout
- Tool execution error
- Memory read failure
- Memory write failure
- Invalid state transition
- Interrupted by user
- Resource exhaustion

## Non-Determinism Sources

### Identified sources

- LLM (temperature, model, prompt)
- Tool (external API, network latency)
- Memory (external DB, cache)
- Clock (system time)
- Random (UUID, seeds)
- Filesystem (file content)
- Network (request/response)
