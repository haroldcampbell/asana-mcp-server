# Spec 007 — CLI Scripts

## Goal
Provide a CLI wrapper per tool for local testing.

## Requirements
- One script per tool in `scripts/`.
- Accept `--payload` or `--payload-file`.
- No secrets embedded in scripts.

## Non-Goals
- Interactive prompts.

## Interfaces
- `python -m scripts.asana_get_task --payload '{"task_gid":"123"}'`

## Security
- Do not print access tokens.

## Tests
- Smoke test each script with mocked responses.

## Acceptance Criteria
- Each script runs and prints JSON output.

## Checklist
- [x] One script per tool in `scripts/`
- [x] Accept `--payload` or `--payload-file`
- [x] No secrets embedded

## Status
Implemented
