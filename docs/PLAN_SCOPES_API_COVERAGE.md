# Main Plan: All API Scopes Execution TODO

## Goal

Execute scope-by-scope implementation across the full Databricks API scope list in one main plan file, with all tool families visible as TODO items.

Reference:
- Databricks Workspace API scopes: https://docs.databricks.com/api/workspace/api/scopes

## Execution Stages

- [ ] research
- [ ] plan
- [ ] develop
- [ ] implement
- [ ] test
- [ ] release
- [ ] next

## Agent Handoff Rule

Before each stage, every agent must read:
- `docs/LOOP_CONTEXT.md`
- `docs/CYCLE_LOG.md`
- `docs/PROCESS_DASHBOARD.md`

After each stage, update all three files with completed work and next queue.

## All Scopes TODO (Main Execution Index)

Each line is a required scope family in the active execution backlog. Operation counts use the source list provided by user.

- [ ] `access-management` (7 operations)
- [ ] `dashboards` (19 operations)
- [ ] `alerts` (5 operations)
- [ ] `apps` (16 operations)
- [ ] `authentication` (14 operations)
- [ ] `cleanrooms` (20 operations)
- [ ] `clusters` (35 operations)
- [ ] `command-execution` (6 operations)
- [ ] `dataquality` (11 operations)
- [ ] `sql` (52 operations)
- [ ] `workspace` (24 operations)
- [ ] `sharing` (27 operations)
- [ ] `files` (18 operations)
- [ ] `genie` (17 operations)
- [ ] `global-init-scripts` (5 operations)
- [ ] `identity` (4 operations)
- [ ] `instance-pools` (9 operations)
- [ ] `instance-profiles` (4 operations)
- [ ] `jobs` (23 operations)
- [ ] `libraries` (4 operations)
- [ ] `marketplace` (50 operations)
- [ ] `mlflow` (75 operations)
- [ ] `model-serving` (20 operations)
- [ ] `networking` (6 operations)
- [ ] `notifications` (5 operations)
- [ ] `pipelines` (15 operations)
- [ ] `postgres` (33 operations)
- [ ] `qualitymonitor` (5 operations)
- [ ] `query-history` (1 operation)
- [ ] `scim` (23 operations)
- [ ] `secrets` (11 operations)
- [ ] `settings` (41 operations)
- [ ] `tags` (10 operations)
- [ ] `unity-catalog` (121 operations)
- [ ] `vector-search` (17 operations)

## Operation-Level TODO Expansion Rule

For each scope marked in progress, expand into operation-level checkboxes directly in this file under a new subsection:

`### <scope>-operations`

Example:

- [ ] list_<scope_item>
- [ ] get_<scope_item>
- [ ] create_<scope_item>
- [ ] update_<scope_item>
- [ ] delete_<scope_item> (if applicable)

## Notes For Current Release Cycle

- Delete operations are available in this package version.
- Delete operations are not yet fully cycle-tested end-to-end in live validation.

## Exit Criteria

- [ ] All scope families above have operation-level expansion sections.
- [ ] Scope implementation status is tracked in this file.
- [ ] README and usage docs reflect current operation support and test caveats.
- [ ] Security scan results are recorded in cycle log before release.
- [ ] PyPI publish is completed as the final release step.
