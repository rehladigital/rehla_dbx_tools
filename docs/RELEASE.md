# Release Runbook

## Standard Release Flow

1. Pull latest `main`.
2. Run local quality gates:
   - `python -m pytest -q`
   - `python -m build`
3. Update package version in `pyproject.toml` when required by checkpoint policy.
4. Update `CHANGELOG.md` with release notes.
5. Commit and push to `main`.
6. Verify remote state and test status.
7. Confirm install command for release:
   - `pip install rehla_dbx_tools`

## Version and Milestone Policy

- Campaign baseline starts at `1.0.0`.
- Major GitHub Release milestone: every `50` cycles.
- Minor version checkpoint: every `100` cycles.

## CI and Release Automation

- CI workflow: `.github/workflows/ci.yml`
  - Runs on PRs and pushes to `main`
  - Python matrix: 3.9, 3.10, 3.11, 3.12
  - Executes tests and package build
- Release workflow: `.github/workflows/release.yml`
  - Runs on `v*.*.*` tags and manual dispatch
  - Manual dispatch requires:
    - `cycle_number`
    - `version`
  - Workflow enforces major milestone dispatch only on cycle multiples of `50`
  - Builds distribution artifacts and creates GitHub release
- PyPI publish workflow: `.github/workflows/workflow.yml`
  - Runs on `release.published`
  - Also supports manual dispatch (`workflow_dispatch`) for recovery/retry
  - Publishes to PyPI using OIDC trusted publishing (no API token required)

## PyPI Publish Setup

1. Configure PyPI Trusted Publisher for this repository/workflow/environment.
2. Create/push release tag (for example `v1.0.0`) and ensure GitHub release is published.
3. Verify `Publish to PyPI` workflow succeeds (or trigger it manually via `workflow_dispatch` if needed).
4. Verify package appears on PyPI and release artifacts are attached to GitHub Release.
5. Validate install from a clean environment:
   - `pip install rehla_dbx_tools`

## Non-Destructive Live Validation

- Workflow: `.github/workflows/non_destructive_smoke.yml`
- Trigger: manual dispatch
- Secrets used:
  - `DBX_HOST`
  - `DBX_TOKEN`
- Behavior:
  - runs read-only list/get smoke checks via `tools/non_destructive_workspace_smoke.py`
  - does not call mutation endpoints

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
