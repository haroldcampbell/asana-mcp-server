# Spec 002 — Auth + Config

## Goal
Define environment-based configuration and validate required settings.

## Requirements
- `ASANA_TOKEN_FILE` preferred, `ASANA_ACCESS_TOKEN` fallback.
- Optional config for API base URL, timeout, retries, log level.
- Clear error if required env var missing.

## Non-Goals
- Secrets manager integration.

## Interfaces
- `src/config.py` provides a cached settings object.

## Security
- Never log tokens.
- Redact sensitive fields in audit logs.

## Tests
- Unit test verifies missing token raises an error.

## Acceptance Criteria
- Invalid config fails fast with readable error.
- Token is not printed in logs or errors.
 - `ASANA_TOKEN_FILE` is preferred when set.

## Checklist
- [x] `ASANA_TOKEN_FILE` preferred, `ASANA_ACCESS_TOKEN` fallback
- [x] Optional config for API base URL, timeout, retries, log level
- [x] Clear error if required env var missing
- [x] No token leakage in logs

## Status
Implemented
