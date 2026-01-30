# Spec 008 — Tests

## Goal
Add unit tests for config and redaction logic.

## Requirements
- Tests in `tests/`.
- Mock external API calls by default.

## Non-Goals
- Full integration tests against live Asana.

## Interfaces
- `pytest` used for running tests.

## Security
- No secrets in test fixtures.

## Acceptance Criteria
- Tests pass locally without Asana credentials.

## Checklist
- [x] Unit tests for config and redaction
- [x] Mocked-by-default (no live Asana calls)

## Status
Implemented
