# OBS-MCP Extension v0.1

**Status**: Draft
**Protocol Layer**: OBS Extension
**Depends on**: OBS v1.0, MCP Protocol

---

## 1. Abstract

Defines the mapping between MCP (Model Context Protocol) operations and OBS event types for verifiable Agent-tool interaction evidence.

## 2. Event Mapping

| MCP Operation | OBS Event Type | Payload |
|:---|:---|:---|
| 	ools/call | TOOL_CALL | {tool_name, arguments, request_id} |
| 	ools/list | TOOL_CALL | {operation: "list_tools"} |
| esources/read | FILE_READ | {uri, resource_id} |
| prompts/get | LLM_REQUEST | {prompt_id, arguments} |
| 	ools/call (response) | TOOL_RESULT | {tool_name, result, request_id} |
| Error response | TOOL_ERROR | {tool_name, error, request_id} |

## 3. Attribution Fields

| Field | Source | Required |
|:---|:---|:---|
| gent_id | MCP client identity | Yes |
| user_id | Human-in-the-loop approval | Optional |
| policy_id | OBS-MCP policy reference | Optional |

## 4. Schema

See obs-mcp.schema.json for full JSON Schema.
