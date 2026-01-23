# Asana MCP Server

MCP server that provides Asana tools for tasks, projects, and workspace discovery.

## Requirements
- Python 3.10+
- `uv` for environment management
- Asana personal access token (PAT)

## Environment Variables
- `ASANA_TOKEN_FILE` (preferred, required if `ASANA_ACCESS_TOKEN` not set)
- `ASANA_ACCESS_TOKEN` (fallback)
- `ASANA_API_BASE` (optional, default `https://app.asana.com/api/1.0`)
- `ASANA_TIMEOUT_SECONDS` (optional, default `30`)
- `ASANA_MAX_RETRIES` (optional, default `3`)
- `LOG_LEVEL` (optional, default `INFO`)
- `LOG_FILE` (optional, default `logs/asana-mcp.log`)

## Tools
- `asana_get_current_user`
- `asana_list_workspaces`
- `asana_list_projects`
- `asana_get_task`
- `asana_search_tasks`
- `asana_create_task`
- `asana_update_task`
- `asana_delete_task`

## Quickstart
```bash
uv sync
ASANA_TOKEN_FILE=.secrets/asana.token uv run python -m src.server
```

## Runtime Flags
- `--version` prints the server version and exits.
- `--health-check` validates configuration and exits.

## Codex CLI MCP Server Install
Example `~/.codex/config.toml` entry:
```toml
[mcp_servers.asana]
command = "uv"
args = ["--project", "/path/to/repo", "run", "python", "-m", "src.server"]

[mcp_servers.asana.env]
PYTHONPATH = "/path/to/repo"
ASANA_TOKEN_FILE = "${HOME}/path/to/repo/.secrets/asana.token"
```

## CLI Scripts
Each script accepts `--payload` or `--payload-file` with JSON input.

Example:
```bash
ASANA_ACCESS_TOKEN=*** \
  uv run python -m scripts.asana_get_task --payload '{"task_gid":"123"}'
```
