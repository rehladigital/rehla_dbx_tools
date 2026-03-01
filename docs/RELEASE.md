# Release Runbook

## Standard Patch Release Flow

1. Pull latest `main`.
2. Run local quality gates:
   - `python -m pytest -q`
   - `python -m build`
3. Update package version in `pyproject.toml` (patch bump).
4. Update `CHANGELOG.md` with release notes.
5. Commit and push to `main`.
6. Verify remote state and test status.

## CI and Release Automation

- CI workflow: `.github/workflows/ci.yml`
  - Runs on PRs and pushes to `main`
  - Python matrix: 3.9, 3.10, 3.11, 3.12
  - Executes tests and package build
- Release workflow: `.github/workflows/release.yml`
  - Runs on `v*.*.*` tags and manual dispatch
  - Builds distribution artifacts and creates GitHub release

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
