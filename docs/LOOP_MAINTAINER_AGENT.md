# Loop Maintainer Agent

## Purpose

Operate continuous improvement cycles without stalling:

1. Plan next batch
2. Build
3. Test
4. Fix
5. Release
6. Push
7. Log and repeat

## Agent Team (Minimum 5)

- Planner/Research Agent
- API Builder Agent
- Test Engineer Agent
- Bug Hunter Agent
- Release Manager Agent
- Docs/Quality Agent

## Mandatory Outputs Per Cycle

- Updated code and tests
- Passing local test run
- Version bump and changelog entry
- Pushed commit SHA
- Updated `docs/CYCLE_LOG.md`

## Context Retention

- Keep source instruction snapshot in `docs/LOOP_CONTEXT.md`.
- Keep cycle-by-cycle execution history in `docs/CYCLE_LOG.md`.
- Before context pressure, append compact handoff:
  - current version
  - last pushed SHA
  - open defects
  - next batch queue

## Safety Rules

- Do not force push.
- Do not skip tests before release.
- Keep secrets out of code and docs.
