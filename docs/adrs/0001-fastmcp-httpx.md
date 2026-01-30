# ADR 0001 - FastMCP + httpx

## Status
Accepted

## Context
We need an MCP server with a minimal, maintainable HTTP client for the Asana API.

## Decision
Use FastMCP for server/tool registration and httpx for Asana API calls.

## Consequences
- FastMCP provides a clear tool interface.
- httpx provides async-ready HTTP with straightforward retries.
