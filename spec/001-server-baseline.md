# Spec 001 — MCP Server Baseline

## Goal
Establish the FastMCP server entrypoint, logging, and tool registry skeleton.

## Requirements
- FastMCP server in `src/server.py`.
- Tool registration in `src/tools.py`.
- Logging to `logs/` with file + console handlers.
- No secrets in repo.

## Non-Goals
- Implement Asana API tools.

## Interfaces
- MCP server launched via `python -m src.server`.

## Security
- No secrets stored on disk.

## Tests
- Basic unit test for logging setup (optional).

## Acceptance Criteria
- Server starts without error when `ASANA_ACCESS_TOKEN` is set.
- Logs are written to `logs/asana-mcp.log`.

## Checklist
- [x] FastMCP server entrypoint in `src/server.py`
- [x] Tool registry in `src/tools.py`
- [x] Logging to `logs/` with file + console handlers
- [x] No secrets stored in repo

## Status
Implemented
