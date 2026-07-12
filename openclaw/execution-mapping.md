# Execution Lifecycle Mapping

**Asset-Type:** Reference Runtime
**Category:** Mapping
**Status:** Draft
**Version:** 1.0.0
**Date:** 2026-07-03
**Related:** mapping-rules.md, runtime-inventory.md, execution.md

## 1. Purpose

This document maps OpenClaw Runtime states and behaviors to OpenBase Execution Semantics v1.0.

All mappings follow the rules defined in  + "mapping-rules.md" + .

## 2. Runtime → Spec State Mapping

| Runtime State | Source | Execution State | Quality | Notes |
| :--- | :--- | :--- | :--- | :--- |
| STARTING | Verified | CREATED | DIRECT | Runtime initialization |
| RUNNING | Verified | RUNNING | DIRECT | Active execution loop |
| PLANNING | Pending | RUNNING | GRANULAR | Internal phase within RUNNING |
| THINKING | Pending | RUNNING | GRANULAR | Internal reasoning phase |
| TOOL_SELECTING | Pending | RUNNING | GRANULAR | Pre-tool decision phase |
| TOOL_EXECUTING | Pending | RUNNING | GRANULAR | Observable via TOOL_CALL/TOOL_RESULT |
| MEMORY_LOADING | Pending | RUNNING | GRANULAR | Observable via MEMORY_UPDATE |
| MEMORY_SAVING | Pending | RUNNING | GRANULAR | Internal persistence phase |
| WAITING | Verified | WAITING | DIRECT | Explicit wait for external input |
| INTERRUPTED | Pending | SUSPENDED | SEMANTIC | Depends on interruption recovery model |
| RETRYING | Pending | RUNNING | SEMANTIC | Recovery behavior, not standalone state |
| RESUMING | Pending | RESUMED | DIRECT | Lifecycle resumes |
| FINISHING | Verified | COMPLETED | SEMANTIC | Transitional implementation detail |
| SHUTDOWN | Verified | COMPLETED | GRANULAR | Runtime teardown |
| ERROR | Verified | FAILED | DIRECT | Terminal failure state |

## 3. Observable Actions

| Runtime Hook | Source | Observable Action | Evidence Event | Quality |
| :--- | :--- | :--- | :--- | :--- |
| before_llm | Verified | LLM Request | LLM_CALL | DIRECT |
| after_llm | Verified | LLM Response | LLM_RESPONSE | DIRECT |
| before_tool | Verified | Tool Invocation | TOOL_CALL | DIRECT |
| after_tool | Verified | Tool Result | TOOL_RESULT | DIRECT |
| before_memory | Pending | Memory Read | MEMORY_READ | MISSING |
| after_memory | Verified | Memory Write | MEMORY_UPDATE | DIRECT |
| on_retry | Pending | Retry Attempt | RETRY | MISSING |
| on_interrupt | Pending | Interrupt | ERROR | SEMANTIC |
| on_resume | Pending | Resume | RESUMED | MISSING |
| on_complete | Verified | Execution Finish | AGENT_FINISHED | DIRECT |
| on_error | Verified | Error | ERROR | DIRECT |

## 4. Gap Summary

Refer to  + "eference-runtime/gap-analysis.md" +  for all gaps.

## 5. References

- Execution Semantics: protocol/specs/execution.md
- Mapping Rules: reference-runtime/mapping-rules.md
- Runtime Inventory: reference-runtime/runtime-inventory.md
- Gap Analysis: reference-runtime/gap-analysis.md
