# Release Runbook

## Standard Patch Release Flow

1. Pull latest `main`.
2. Run local quality gates:
   - `python -m pytest -q`
3. Update package version in `pyproject.toml` (patch bump).
4. Update `CHANGELOG.md` with release notes.
5. Commit and push to `main`.
6. Verify remote state and test status.

## Cycle-Oriented Continuous Loop

For each cycle:

1. Plan and prioritize next function batch.
2. Implement wrappers/fixes.
3. Add tests for each added behavior.
4. Run tests and fix regressions.
5. Bump patch version and update changelog.
6. Push to `main`.
7. Append cycle details to `docs/CYCLE_LOG.md`.

## Required Context Preservation

Before ending a cycle:

- Ensure `docs/LOOP_CONTEXT.md` contains the latest instruction snapshot and next queue.
- Ensure `docs/CYCLE_LOG.md` contains completed work and unresolved items.
