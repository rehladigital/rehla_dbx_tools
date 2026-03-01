# Cycle Log

## Cycle 1

- Date: 2026-02-28
- Objective: establish autonomous loop foundation and deliver first expanded API batch.
- Planned focus:
  - baseline capability matrix
  - persistent loop context artifacts
  - first wrapper expansion + tests + fixes
  - patch release and push
- External pain points tracked:
  - pagination token handling reliability
  - account/workspace authentication boundaries
  - endpoint/version drift

### Progress Notes

- Created baseline matrix in `docs/CAPABILITY_MATRIX.md`.
- Initialized persistent loop state files (`docs/LOOP_CONTEXT.md`, `docs/CYCLE_LOG.md`).
- Expanded wrappers in `WorkspaceClient`:
  - Jobs: `get_job`, `create_job`, `update_job`, `run_job_now`, `get_job_run`, `cancel_job_run`, `delete_job`
  - Clusters: `get_cluster`, `create_cluster`, `edit_cluster`, `start_cluster`, `restart_cluster`, `delete_cluster`, `permanent_delete_cluster`, `cluster_events`
- Expanded wrappers in `AccountClient`:
  - `get_workspace`, `create_workspace`, `update_workspace`, `delete_workspace`
- Added endpoint catalog entries for expanded wrapper set.
- Added wrapper behavior tests:
  - `tests/test_workspace_client.py`
  - extended `tests/test_account_client.py`
- Validation: `12 passed` via `pytest -q`.

## Cycle 2

- Date: 2026-02-28
- Objective: establish repeatable automation and execute another release cycle.
- Planned focus:
  - CI workflow
  - release workflow
  - additional reliability test for HTTP retry behavior

### Progress Notes

- Added CI workflow at `.github/workflows/ci.yml` with Python 3.9-3.12 test/build matrix.
- Added release workflow at `.github/workflows/release.yml` for tag/manual GitHub releases.
- Added `test_request_retries_5xx_then_returns_success_response` in `tests/test_http_client.py`.
- Updated runbook and changelog for automation flow.
- Prepared patch bump to `0.1.2`.

## Cycle 3

- Date: 2026-02-28
- Objective: add organization context and package publishing capability.
- Planned focus:
  - Rehla Digital company section in README
  - PyPI publish integration in release workflow
  - patch release bump

### Progress Notes

- Added `About Rehla Digital Inc` section to `README.md`.
- Added PyPI publish step to `.github/workflows/release.yml` using repository secret `PYPI_API_TOKEN`.
- Updated `docs/RELEASE.md` with PyPI setup and verification steps.
- Updated changelog and bumped version to `0.1.3`.

## Cycle 4

- Date: 2026-02-28
- Objective: align published package identity and install command with Rehla branding.
- Planned focus:
  - Rename package for PyPI install (`rehladigital-aws-dbx-tools`)
  - Improve PyPI metadata quality
  - Keep loop cadence active

### Progress Notes

- Renamed distribution package to `rehladigital-aws-dbx-tools`.
- Updated install commands in `README.md` and `docs/USAGE.md`.
- Updated Spark install hint in `src/databricks_api/response.py`.
- Added richer PyPI metadata in `pyproject.toml` (`keywords`, `classifiers`, `project.urls`, improved description).
- Bumped version to `0.1.4`.

## Cycle 5

- Date: 2026-02-28
- Objective: keep loop active with maintainer-agent execution and next API expansion.
- Planned focus:
  - Unity Catalog wrappers
  - Repos/Secrets/Tokens wrappers
  - stronger wrapper tests

### Progress Notes

- Added workspace wrappers: `list_catalogs`, `list_schemas`, `update_repo`, `put_secret`, `create_token`, `delete_token`.
- Expanded endpoint catalog and generated endpoint constants for those routes.
- Added test coverage for new wrappers and payload/path expectations.
- Added loop maintainer reference `docs/LOOP_MAINTAINER_AGENT.md` to formalize continuous agent operation.
- Updated docs examples and bumped version to `0.1.5`.

## Cycle 6

- Date: 2026-02-28
- Objective: align Python import path with rehladigital package identity.
- Planned focus:
  - user-facing import namespace
  - docs import updates
  - regression coverage

### Progress Notes

- Added new package export module `src/rehladigital_aws_dbx_tools/__init__.py`.
- Updated docs to use `from rehladigital_aws_dbx_tools import DatabricksApiClient`.
- Added import validation test `tests/test_public_import.py`.
- Bumped version to `0.1.6`.

## Cycle 7

- Date: 2026-02-28
- Objective: make package namespace fully match `rehladigital_aws_dbx_tools`.
- Planned focus:
  - full module namespace compatibility
  - submodule import support
  - release continuation

### Progress Notes

- Added compatibility module tree under `src/rehladigital_aws_dbx_tools/` for core modules, clients, and endpoints.
- Added submodule import test coverage to ensure `rehladigital_aws_dbx_tools.clients.workspace` works.
- Bumped version to `0.1.7`.

## Cycle 8

- Date: 2026-02-28
- Objective: make loop execution status visibly trackable to the user.
- Planned focus:
  - add one-file process dashboard
  - keep release cadence consistent

### Progress Notes

- Added `docs/PROCESS_DASHBOARD.md` with status, last cycle, current version, last SHA, and next queue.
- Bumped version to `0.1.8`.

## Cycle 9

- Date: 2026-02-28
- Objective: continue 200-loop campaign with next planned wrapper batch.
- Planned focus:
  - repos wrappers
  - secret scope lifecycle wrappers
  - wrapper test expansion

### Progress Notes

- Added repos wrappers: `list_repos`, `get_repo`, `create_repo`, `delete_repo`.
- Added secret scope wrappers: `create_secret_scope`, `list_secret_scopes`, `delete_secret_scope`.
- Expanded endpoint catalog/constants and tests.
- Updated README/USAGE examples and bumped version to `0.1.9`.

## Cycle 10

- Date: 2026-02-28
- Objective: execute queued loop tasks for Unity Catalog details, token guardrails, and notebook context tests.
- Planned focus:
  - Unity Catalog detail wrappers
  - token list/revoke wrappers with validation
  - notebook context edge-case tests

### Progress Notes

- Added wrappers: `get_catalog`, `get_schema`, `list_tokens`, `revoke_token`.
- Added non-empty guard for `revoke_token` to prevent invalid delete requests.
- Added notebook context tests (`tests/test_notebook_context.py`) and expanded workspace wrapper tests.
- Expanded endpoint catalog/constants and usage docs.
- Bumped version to `0.1.10`.

## Cycle 11

- Date: 2026-02-28
- Objective: expand high-value account onboarding wrappers and keep release cadence active.
- Planned focus:
  - account credentials wrappers
  - account storage-configuration wrappers
  - regression tests for new account wrapper paths

### Progress Notes

- Added account credentials wrappers:
  - `list_credentials`
  - `create_credentials`
  - `delete_credentials`
- Added account storage configuration wrappers:
  - `list_storage_configurations`
  - `create_storage_configuration`
  - `delete_storage_configuration`
- Added account network wrappers:
  - `list_networks`
  - `create_network`
  - `delete_network`
- Added account private access settings wrappers:
  - `list_private_access_settings`
  - `create_private_access_settings`
  - `delete_private_access_settings`
- Expanded account endpoint catalog and regenerated endpoint constants.
- Added account wrapper path/payload tests in `tests/test_account_client.py`.
- Updated README and usage examples for new account wrappers.
- Validation: `22 passed` via `pytest -q`.
- Bumped version to `0.1.11`.

## Cycle 12

- Date: 2026-02-28
- Objective: expand account networking wrappers and keep the repeat loop moving.
- Planned focus:
  - account networks wrappers
  - account private-access-settings wrappers
  - tests/docs/version bump

### Progress Notes

- Added account network wrappers:
  - `list_networks`
  - `create_network`
  - `delete_network`
- Added account private access settings wrappers:
  - `list_private_access_settings`
  - `create_private_access_settings`
  - `delete_private_access_settings`
- Expanded account endpoint catalog and regenerated endpoint constants.
- Added tests for account network/private-access wrapper paths and payloads.
- Updated README and usage examples for account network/private-access operations.
- Validation: `23 passed` via `pytest -q`.
- Bumped version to `0.1.12`.

## Cycle 13

- Date: 2026-02-28
- Objective: harden response normalization for common Databricks wrapper payload edge cases.
- Planned focus:
  - nested list payload extraction
  - additional key support (`runs`)
  - regression tests

### Progress Notes

- Improved `normalize_json` to extract row payloads from:
  - known Databricks list keys (`runs`, `schemas`, `catalogs` added),
  - generic list-valued fields,
  - nested dictionary wrappers containing list payloads.
- Added response regression tests for `runs` and nested `result.items` patterns.
- Validation: `25 passed` via `pytest -q`.
- Bumped version to `0.1.13`.

## Cycle 14

- Date: 2026-02-28
- Objective: expand account private endpoint coverage for networking and key management.
- Planned focus:
  - account VPC endpoint wrappers
  - account customer-managed-key wrappers
  - tests/docs/version bump

### Progress Notes

- Added account VPC endpoint wrappers:
  - `list_vpc_endpoints`
  - `create_vpc_endpoint`
  - `delete_vpc_endpoint`
- Added account customer-managed-key wrappers:
  - `list_customer_managed_keys`
  - `create_customer_managed_key`
  - `delete_customer_managed_key`
- Expanded account endpoint catalog and regenerated endpoint constants.
- Added tests for VPC endpoint/CMK wrapper paths and payloads.
- Updated README and usage examples for account private endpoint operations.
- Validation: `26 passed` via `pytest -q`.
- Bumped version to `0.1.14`.

## Cycle 15

- Date: 2026-03-01
- Objective: expand account identity lifecycle coverage for SCIM users and groups.
- Planned focus:
  - account SCIM user wrappers
  - account SCIM group wrappers
  - tests/docs/version bump

### Progress Notes

- Added account SCIM user wrappers:
  - `list_users`
  - `get_user`
  - `create_user`
  - `patch_user`
  - `delete_user`
- Added account SCIM group wrappers:
  - `list_groups`
  - `get_group`
  - `create_group`
  - `patch_group`
  - `delete_group`
- Expanded account endpoint catalog and regenerated endpoint constants.
- Added tests for SCIM user/group wrapper paths and payloads.
- Updated README and usage examples for account identity lifecycle operations.
- Validation: `27 passed` via `pytest -q`.
- Bumped version to `0.1.15`.

## Cycle 16

- Date: 2026-03-01
- Objective: expand account governance and audit wrappers for budget and log-delivery lifecycle.
- Planned focus:
  - account budget-policy wrappers
  - account log-delivery wrappers
  - tests/docs/version bump

### Progress Notes

- Added account budget-policy wrappers:
  - `list_budget_policies`
  - `get_budget_policy`
  - `create_budget_policy`
  - `update_budget_policy`
  - `delete_budget_policy`
- Added account log-delivery wrappers:
  - `list_log_delivery_configurations`
  - `get_log_delivery_configuration`
  - `create_log_delivery_configuration`
  - `patch_log_delivery_configuration`
  - `delete_log_delivery_configuration`
- Expanded account endpoint catalog and regenerated endpoint constants.
- Added tests for budget-policy/log-delivery wrapper paths and payloads.
- Updated README and usage examples for account governance and audit operations.
- Validation: `28 passed` via `pytest -q`.
- Bumped version to `0.1.16`.

## Cycle 17

- Date: 2026-03-01
- Objective: add token hygiene helper flow for safer token rotation in automation contexts.
- Planned focus:
  - workspace token rotation helper
  - regression tests for helper behavior
  - docs/version/log update

### Progress Notes

- Added `rotate_token` to `WorkspaceClient` to create a replacement token and revoke an old token in one helper flow.
- Added tests for rotate-token success behavior and validation on missing token ID.
- Updated README and usage examples with token rotation snippets.
- Validation: `30 passed` via `pytest -q`.
- Bumped version to `0.1.17`.

## Cycles 18-200

- Date range: 2026-03-01
- Status: **not implemented as distinct code cycles yet**
- Objective: document state accurately and avoid overstating shipped functionality.

### Accuracy Notes

- Functional code additions currently completed through cycle **17** only.
- No additional concrete API wrapper/test implementation has been recorded yet for cycles **18-200**.
- Prior entry overstated campaign completion and has been corrected.
- This section now serves as a tracking placeholder for future cycle-by-cycle implementation.

### Implemented Functionality Through Cycle 17

- Cycle 15: account SCIM identity wrappers + tests
  - Users: `list_users`, `get_user`, `create_user`, `patch_user`, `delete_user`
  - Groups: `list_groups`, `get_group`, `create_group`, `patch_group`, `delete_group`
- Cycle 16: account governance/audit wrappers + tests
  - Budget policies: `list_budget_policies`, `get_budget_policy`, `create_budget_policy`, `update_budget_policy`, `delete_budget_policy`
  - Log delivery: `list_log_delivery_configurations`, `get_log_delivery_configuration`, `create_log_delivery_configuration`, `patch_log_delivery_configuration`, `delete_log_delivery_configuration`
- Cycle 17: workspace token hygiene helper + tests
  - `rotate_token` helper added with validation coverage

## Run 1 (Cycle 1 of 300 campaign)

- Date: 2026-03-01
- Cloud track: AWS (round-robin assignment)
- Objective: initialize 300-cycle campaign baseline and rename public package namespace to `rehla_dbx_tools`.

### Progress Notes

- Added new public package namespace tree under `src/rehla_dbx_tools/` with compatibility exports for:
  - root package exports
  - `clients` subpackage
  - `endpoints` and generated endpoint subpackages
- Kept legacy namespace `rehladigital_aws_dbx_tools` available for backward compatibility.
- Updated docs/import examples to use:
  - distribution: `rehla-dbx-tools`
  - import namespace: `rehla_dbx_tools`
- Updated import regression tests for new namespace and added legacy import compatibility assertion.
- Updated campaign tracking docs for 300-cycle execution baseline.
- Set package version to `1.0.0`.

## Run 2 (Cycle 2 of 300 campaign)

- Date: 2026-03-01
- Cloud track: Azure (round-robin assignment)
- Objective: enforce release checkpoint policy (major every 50 cycles, minor every 100 cycles) in automation and runbook.

### Progress Notes

- Updated `.github/workflows/release.yml` manual dispatch inputs to require:
  - `cycle_number`
  - `version`
- Added release-workflow checkpoint validation that blocks manual major-release execution unless `cycle_number % 50 == 0`.
- Added deterministic release tag resolution for both tag-push and manual dispatch paths.
- Updated `docs/RELEASE.md` with campaign version/release policy and manual-dispatch requirements.
- Updated loop/dashboard context pointers for next run.
- Package version remains `1.0.0` (no 50/100-cycle checkpoint reached in run 2).

## Run 3 (Cycle 3 of 300 campaign)

- Date: 2026-03-01
- Cloud track: GCP (round-robin assignment)
- Objective: add explicit cloud-target configuration support to improve multi-cloud execution control.

### Progress Notes

- Added cloud target fields to configuration models:
  - `WorkspaceConfig.cloud`
  - `AccountConfig.cloud`
- Added environment variable support:
  - `DATABRICKS_CLOUD` (`aws`, `azure`, `gcp`; default `aws`)
  - `DATABRICKS_ACCOUNT_CLOUD` (defaults to `DATABRICKS_CLOUD`)
- Added validation to reject unsupported cloud values.
- Added regression tests for cloud parsing, overrides, and invalid-value handling in `tests/test_config.py`.
- Updated `docs/USAGE.md` environment variable documentation for cloud selectors.
- Package version remains `1.0.0` (no 50/100-cycle checkpoint reached in run 3).

## Run 4 (Cycle 4 of 300 campaign)

- Date: 2026-03-01
- Cloud track: AWS (round-robin assignment)
- Objective: add host-cloud alignment guardrails to prevent misconfigured multi-cloud environments.

### Progress Notes

- Added host inference guardrails in config validation:
  - `*.azuredatabricks.net` -> `azure`
  - `*.gcp.databricks.com` -> `gcp`
  - `*.cloud.databricks.com` -> `aws`
- Added validation errors when configured cloud env values conflict with inferred host cloud.
- Added regression tests for workspace and account host/cloud mismatch scenarios in `tests/test_config.py`.
- Updated `docs/USAGE.md` with cloud-host alignment guidance.
- Package version remains `1.0.0` (no 50/100-cycle checkpoint reached in run 4).

## Run 5 (Cycle 5 of 300 campaign)

- Date: 2026-03-01
- Cloud track: Azure (round-robin assignment)
- Objective: improve cloud selector ergonomics by inferring cloud from host when cloud env values are not set.

### Progress Notes

- Added cloud resolution helper in config to prioritize:
  1. explicit cloud env var
  2. cloud inferred from host pattern
  3. fallback cloud default
- Updated `UnifiedConfig.from_env()` to use host-based cloud inference for workspace/account when cloud env vars are absent.
- Added regression tests for cloud inference behavior in `tests/test_config.py`.
- Updated `docs/USAGE.md` to document fallback/inference behavior.
- Package version remains `1.0.0` (no 50/100-cycle checkpoint reached in run 5).

## Run 6 (Cycle 6 of 300 campaign)

- Date: 2026-03-01
- Cloud track: GCP (round-robin assignment)
- Objective: centralize cloud host detection logic for reuse across config and public API.

### Progress Notes

- Added `src/databricks_api/cloud.py` with:
  - `detect_cloud_from_host(...)`
  - `is_host_cloud_aligned(...)`
- Reused shared cloud detection helper in config validation path.

## Run 7 (Cycle 7 of 300 campaign)

- Date: 2026-03-01
- Cloud track: AWS (round-robin assignment)
- Objective: add strict-cloud-match switch for controlled rollout and migration scenarios.

### Progress Notes

- Added `strict_cloud_match` on `UnifiedConfig`.
- Added env support:
  - `DATABRICKS_STRICT_CLOUD_MATCH` (`true`/`false`, default `true`)
- Added boolean parsing with validation for invalid values.

## Run 8 (Cycle 8 of 300 campaign)

- Date: 2026-03-01
- Cloud track: Azure (round-robin assignment)
- Objective: harden account configuration validity for account-host scenarios.

### Progress Notes

- Added validation requiring `DATABRICKS_ACCOUNT_ID` when `DATABRICKS_ACCOUNT_HOST` is configured.
- Added regression test coverage for missing account ID validation.

## Run 9 (Cycle 9 of 300 campaign)

- Date: 2026-03-01
- Cloud track: GCP (round-robin assignment)
- Objective: support deterministic cloud override from already-loaded unified config.

### Progress Notes

- Added `UnifiedConfig.with_cloud(cloud)` to override both workspace/account cloud targets in one call.
- Added regression test coverage for `with_cloud(...)`.

## Run 10 (Cycle 10 of 300 campaign)

- Date: 2026-03-01
- Cloud track: AWS (round-robin assignment)
- Objective: add client-level cloud override constructor for cross-cloud execution pipelines.

### Progress Notes

- Added `DatabricksApiClient.from_env_for_cloud(cloud)` to force both workspace/account cloud values.
- Added regression test coverage in `tests/test_client.py`.

## Run 11 (Cycle 11 of 300 campaign)

- Date: 2026-03-01
- Cloud track: Azure (round-robin assignment)
- Objective: expose cloud helpers and types through top-level package exports.

### Progress Notes

- Exported `CloudType`, `detect_cloud_from_host`, and `is_host_cloud_aligned` via:
  - `databricks_api`
  - `rehla_dbx_tools`
  - `rehladigital_aws_dbx_tools` (compat namespace)
- Added public-import regression test for cloud helper visibility.

## Run 12 (Cycle 12 of 300 campaign)

- Date: 2026-03-01
- Cloud track: GCP (round-robin assignment)
- Objective: improve configuration robustness for strict-match setting parsing.

### Progress Notes

- Added explicit validation error path for invalid `DATABRICKS_STRICT_CLOUD_MATCH` values.
- Added regression test for invalid strict-match env value.

## Run 13 (Cycle 13 of 300 campaign)

- Date: 2026-03-01
- Cloud track: AWS (round-robin assignment)
- Objective: keep operator docs aligned with advanced cloud configuration controls.

### Progress Notes

- Updated `docs/USAGE.md` with strict-match env option and cloud-override examples.
- Added `from_env_for_cloud("azure")` usage snippet.

## Run 14 (Cycle 14 of 300 campaign)

- Date: 2026-03-01
- Cloud track: Azure (round-robin assignment)
- Objective: improve end-user discoverability of cloud-aware startup patterns.

### Progress Notes

- Updated `README.md` quick-start to include forced cloud-target example.
- Synced docs with new cloud override semantics.

## Run 15 (Cycle 15 of 300 campaign)

- Date: 2026-03-01
- Cloud track: GCP (round-robin assignment)
- Objective: finalize the run 6-15 hardening batch with full test validation and factual log updates.

### Progress Notes

- Full test suite passed after cumulative changes.
- Validation: `43 passed` via `pytest -q`.
- Package version remains `1.0.0` (no 50/100-cycle checkpoint reached in run 15).

## Run 16 (Cycle 16 of 300 campaign)

- Date: 2026-03-01
- Cloud track: AWS (round-robin assignment)
- Objective: expand workspace SQL warehouse wrappers for analytics workflows.

### Progress Notes

- Added SQL warehouse wrappers:
  - `list_sql_warehouses`
  - `get_sql_warehouse`
  - `create_sql_warehouse`
  - `edit_sql_warehouse`
  - `delete_sql_warehouse`
- Added endpoint catalog/constants for SQL warehouse routes.

## Run 17 (Cycle 17 of 300 campaign)

- Date: 2026-03-01
- Cloud track: Azure (round-robin assignment)
- Objective: expand instance-pool lifecycle wrappers for compute capacity management.

### Progress Notes

- Added instance pool wrappers:
  - `list_instance_pools`
  - `get_instance_pool`
  - `create_instance_pool`
  - `edit_instance_pool`
  - `delete_instance_pool`
- Added endpoint catalog/constants for instance-pool routes.

## Run 18 (Cycle 18 of 300 campaign)

- Date: 2026-03-01
- Cloud track: GCP (round-robin assignment)
- Objective: expand cluster-policy wrappers for governance controls.

### Progress Notes

- Added cluster policy wrappers:
  - `list_cluster_policies`
  - `get_cluster_policy`
  - `create_cluster_policy`
  - `edit_cluster_policy`
  - `delete_cluster_policy`
- Added endpoint catalog/constants for cluster-policy routes.

## Run 19 (Cycle 19 of 300 campaign)

- Date: 2026-03-01
- Cloud track: AWS (round-robin assignment)
- Objective: add DBFS file-system wrappers and input validation guardrails.

### Progress Notes

- Added DBFS wrappers:
  - `list_dbfs`
  - `get_dbfs_status`
  - `read_dbfs`
  - `delete_dbfs`
  - `mkdirs_dbfs`
- Added path/offset/length validation for DBFS wrappers.
- Added endpoint catalog/constants for DBFS routes.

## Run 20 (Cycle 20 of 300 campaign)

- Date: 2026-03-01
- Cloud track: Azure (round-robin assignment)
- Objective: complete wrapper regression coverage and usage docs for new workspace capabilities.

### Progress Notes

- Expanded `tests/test_workspace_client.py` with behavior assertions for:
  - SQL warehouses
  - instance pools
  - cluster policies
  - DBFS wrappers and validation paths
- Updated `README.md` and `docs/USAGE.md` with new workspace wrapper examples.
- Validation: `47 passed` via `pytest -q`.
- Package version remains `1.0.0` (no 50/100-cycle checkpoint reached in run 20).

## Run 21 (Cycle 21 of 300 campaign)

- Date: 2026-03-01
- Cloud track: GCP (round-robin assignment)
- Objective: add workspace wrapper for listing job runs with filterable params and pagination.

### Progress Notes

- Added `list_job_runs(...)` wrapper to `WorkspaceClient` with optional filters:
  - `job_id`
  - `active_only`
  - `completed_only`
  - `offset`
  - `limit`
- Added endpoint-catalog route for `/api/2.1/jobs/runs/list`.

## Run 22 (Cycle 22 of 300 campaign)

- Date: 2026-03-01
- Cloud track: AWS (round-robin assignment)
- Objective: add run export/output wrappers for easier troubleshooting and artifact capture.

### Progress Notes

- Added `export_job_run(run_id, views_to_export=...)` wrapper.
- Added `get_job_run_output(run_id)` wrapper.
- Added endpoint-catalog routes for:
  - `/api/2.1/jobs/runs/export`
  - `/api/2.1/jobs/runs/get-output`

## Run 23 (Cycle 23 of 300 campaign)

- Date: 2026-03-01
- Cloud track: Azure (round-robin assignment)
- Objective: add run-level control wrappers for fleet cancellation and repair operations.

### Progress Notes

- Added `cancel_all_job_runs(job_id, all_queued_runs=...)` wrapper.
- Added `repair_job_run(run_id, rerun_all_failed_tasks=..., latest_repair_id=...)` wrapper.
- Added endpoint-catalog routes for:
  - `/api/2.1/jobs/runs/cancel-all`
  - `/api/2.1/jobs/runs/repair`

## Run 24 (Cycle 24 of 300 campaign)

- Date: 2026-03-01
- Cloud track: GCP (round-robin assignment)
- Objective: extend workspace wrapper regression coverage for new job-run operations.

### Progress Notes

- Expanded `tests/test_workspace_client.py` to assert method/path/payload behavior for:
  - `list_job_runs`
  - `cancel_all_job_runs`
  - `export_job_run`
  - `get_job_run_output`
  - `repair_job_run`
- Included default-parameter coverage for list/export/repair calls.

## Run 25 (Cycle 25 of 300 campaign)

- Date: 2026-03-01
- Cloud track: AWS (round-robin assignment)
- Objective: sync generated endpoints and user docs for the run-management wrapper expansion.

### Progress Notes

- Regenerated endpoint constants from catalog updates:
  - `src/databricks_api/endpoints/generated/workspace_endpoints.py`
  - `src/databricks_api/endpoints/generated/account_endpoints.py`
- Updated examples in `README.md` and `docs/USAGE.md` to include new Jobs run-management wrappers.
- Validation: `47 passed` via `pytest -q`.
- Package version remains `1.0.0` (no 50/100-cycle checkpoint reached in run 25).
