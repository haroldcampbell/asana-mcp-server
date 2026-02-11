# Spec 009 — Task Sections

## Goal
Allow adding or moving a task into a specific section within a project.

## Requirements
- Tools: move task to section; create task in section.
- Input validation for tool payload.
- Normalized response envelope.
- Audit logging for tool usage.

## Non-Goals
- Full section management (create/update/delete sections).

## Interfaces
- MCP tool registered in `src/tools.py`.
- Tool implementation in `src/tool_impl.py`.
- CLI wrapper in `scripts/`.

## Security
- Redact secrets and PII in logs.

## Tests
- Unit tests for validation and redaction as applicable.

## Acceptance Criteria
- Tool returns `{"status":"ok","data":...}` on success.
- Errors return `{"status":"error","error":...}` with no secret leakage.

## Checklist
- [x] Tool implemented in `src/tool_impl.py`
- [x] Input validation
- [x] Normalized response envelope
- [x] Audit logging
- [x] CLI script

## Status
Implemented
