# Spec 003 — Core CRUD + Search Tools

## Goal
Implement core Asana task tools and discovery tools.

## Requirements
- Tools: get current user, list workspaces, list projects, get task, search tasks, create task, update task, delete task.
- Input validation for all tools.
- Normalized response envelope.
- Audit logging for all tools.

## Non-Goals
- Full Asana API coverage.

## Interfaces
- MCP tools registered in `src/tools.py`.
- Tool implementations in `src/tool_impl.py`.

## Security
- Redact secrets and PII in logs.
- Retry backoff for rate limits.

## Tests
- Unit tests for redaction and validation.

## Acceptance Criteria
- Each tool returns `{"status":"ok","data":...}` on success.
- Errors return `{"status":"error","error":...}` with no secret leakage.

## Checklist
- [x] Tools implemented in `src/tool_impl.py`
- [x] Input validation for all tools
- [x] Normalized response envelope
- [x] Audit logging for all tools
- [x] Retry/backoff on rate limits

## Status
Implemented
