# Changelog

All notable changes to this project will be documented in this file.

## [1.1.2] - 2026-03-01

### Fixed

- Corrected pagination row extraction for Jobs runs endpoints so `jobs/runs/list` aggregates `runs` across paginated responses.
- Added regression coverage to ensure paginated run payloads are combined correctly.

## [1.1.1] - 2026-03-01

### Added

- Simple client bootstrap for local scripts:
  - `DatabricksApiClient.simple(host=..., token=...)`
  - token-optional fallbacks from env vars
  - guided browser + prompt token flow
  - Windows SSO token resolution via Databricks CLI
- Plain-list convenience helper:
  - `DatabricksApiClient.list_active_job_runs(...)`
- Regression coverage for simple bootstrap and token fallback behavior.

### Changed

- Updated README and usage guide with minimal host-first examples and SSO/browser token options.

## [1.1.0] - 2026-03-01

### Added

- Non-destructive live workspace smoke validation tooling:
  - `.github/workflows/non_destructive_smoke.yml`
  - `tools/non_destructive_workspace_smoke.py`
- Extended DBX alias support for env-driven configuration:
  - `DBX_HOST`, `DBX_TOKEN`
  - `DBX_CLOUD`, `DBX_ACCOUNT_CLOUD`
  - `DBX_STRICT_CLOUD_MATCH`
  - `DBX_AUTH_TYPE`, `DBX_ACCOUNT_AUTH_TYPE`
  - `DBX_ACCOUNT_HOST`, `DBX_ACCOUNT_ID`, `DBX_ACCOUNT_TOKEN`
- Host normalization guardrail for copied workspace URL typo:
  - `*.cloud.databricks.net` -> `*.cloud.databricks.com`

### Changed

- Updated release runbook to the active OIDC publish model:
  - GitHub release creation and PyPI publish handled by separate workflows
  - manual publish fallback documented
- Expanded usage docs to include DBX alias environment fields.
- Advanced campaign completion through run 60 with live non-destructive validation checkpoints.

## [1.0.0] - 2026-03-01

### Added

- New public import namespace `rehla_dbx_tools` with compatibility export modules:
  - root exports
  - `clients` package modules
  - `endpoints` and generated endpoint package modules
- Import regression coverage for `rehla_dbx_tools` plus legacy-namespace compatibility assertion.

### Changed

- Set package/distribution identity to:
  - distribution: `rehla-dbx-tools`
  - import namespace: `rehla_dbx_tools`
- Updated README/USAGE/RELEASE/install references to the new package naming.
- Updated cycle tracking docs to start the 300-cycle campaign baseline.
- Added release-checkpoint enforcement in `.github/workflows/release.yml` for manual major releases on cycle multiples of 50.
- Added multi-cloud config selectors and validation:
  - `DATABRICKS_CLOUD`
  - `DATABRICKS_ACCOUNT_CLOUD`
- Added host-cloud alignment validation guardrails for known Databricks host patterns (AWS/Azure/GCP).
- Added cloud inference from host when cloud env variables are omitted.
- Added shared cloud utility helpers (`detect_cloud_from_host`, `is_host_cloud_aligned`) and exported them in public namespaces.
- Added `DATABRICKS_STRICT_CLOUD_MATCH` with boolean validation and config-level strict match control.
- Added `UnifiedConfig.with_cloud(...)` and `DatabricksApiClient.from_env_for_cloud(...)` cloud-override helpers.
- Added account-host validation requiring `DATABRICKS_ACCOUNT_ID` when account host is configured.
- Added workspace wrapper expansion:
  - SQL warehouses lifecycle wrappers
  - instance pools lifecycle wrappers
  - cluster policies lifecycle wrappers
  - DBFS list/status/read/delete/mkdirs wrappers with validation
  - Jobs run-management wrappers:
    - `list_job_runs`
    - `cancel_all_job_runs`
    - `export_job_run`
    - `get_job_run_output`
    - `repair_job_run`
    - `submit_job_run`
    - `delete_job_run`
- Added run-lifecycle validation guardrails for positive identifiers and pagination constraints.
- Added Jobs permissions wrappers:
  - `get_job_permissions`
  - `update_job_permissions`
  - `get_job_permission_levels`
- Added cluster/repo permissions wrappers:
  - `get_cluster_permissions`
  - `update_cluster_permissions`
  - `get_cluster_permission_levels`
  - `get_repo_permissions`
  - `update_repo_permissions`
  - `get_repo_permission_levels`
- Added positive-ID validation for job deletion and job-permissions wrappers.
- Added identifier validation for cluster/repo permissions wrappers.
- Added broader workspace input validation guardrails across existing wrappers:
  - positive checks for `job_id`, `repo_id`, and list `limit` inputs
  - non-empty checks for `cluster_id`, `warehouse_id`, `instance_pool_id`, and `policy_id`
  - cluster event validation for both `cluster_id` and `limit`
- Added `DBX_HOST` and `DBX_TOKEN` alias support in environment config loading.
- Expanded alias support for:
  - `DBX_CLOUD`, `DBX_ACCOUNT_CLOUD`
  - `DBX_STRICT_CLOUD_MATCH`
  - `DBX_AUTH_TYPE`, `DBX_ACCOUNT_AUTH_TYPE`
  - `DBX_ACCOUNT_HOST`, `DBX_ACCOUNT_ID`, `DBX_ACCOUNT_TOKEN`
- Added GitHub workflow `.github/workflows/non_destructive_smoke.yml` for non-destructive workspace smoke checks.
- Added `tools/non_destructive_workspace_smoke.py` to validate read-only workspace APIs against live environments.
- Added host normalization fix for common `*.cloud.databricks.net` workspace URL typo -> `*.cloud.databricks.com`.
- Updated `docs/RELEASE.md` to document OIDC-based PyPI publish flow and non-destructive smoke process.
- Expanded workspace endpoint catalog/constants and wrapper regression tests for the new routes.

## [0.1.200] - 2026-03-01

### Added

- Documentation accuracy update for cycle tracking:
  - clarified functional implementation is complete through cycle `17`
  - replaced overstated `18-200` completion claim with explicit placeholder status

### Changed

- Updated campaign tracking artifacts for factual cycle reporting:
  - `docs/CYCLE_LOG.md`
  - `docs/PROCESS_DASHBOARD.md`
  - `docs/LOOP_CONTEXT.md`
- Bumped package version from `0.1.17` to `0.1.200`.

## [0.1.17] - 2026-03-01

### Added

- Workspace token hygiene helper:
  - `rotate_token` to create a new token and revoke the previous token in one flow.
- Added regression tests for `rotate_token` happy path and validation failures in `tests/test_workspace_client.py`.

### Changed

- Updated README and usage examples with token rotation workflow snippets.
- Bumped package version from `0.1.16` to `0.1.17`.

## [0.1.16] - 2026-03-01

### Added

- Account budget-policy wrappers:
  - `list_budget_policies`, `get_budget_policy`, `create_budget_policy`, `update_budget_policy`, `delete_budget_policy`
- Account log-delivery wrappers:
  - `list_log_delivery_configurations`, `get_log_delivery_configuration`, `create_log_delivery_configuration`, `patch_log_delivery_configuration`, `delete_log_delivery_configuration`
- Added account wrapper regression coverage for budget and log-delivery wrappers in `tests/test_account_client.py`.

### Changed

- Expanded account endpoint catalog/constants with budget-policy and log-delivery routes.
- Updated README and usage examples for account governance/audit lifecycle operations.
- Bumped package version from `0.1.15` to `0.1.16`.

## [0.1.15] - 2026-03-01

### Added

- Account SCIM wrapper expansion:
  - Users: `list_users`, `get_user`, `create_user`, `patch_user`, `delete_user`
  - Groups: `list_groups`, `get_group`, `create_group`, `patch_group`, `delete_group`
- Account wrapper regression coverage extended in `tests/test_account_client.py`.

### Changed

- Expanded account endpoint catalog/constants with SCIM user and group routes.
- Updated README and usage examples for account identity lifecycle operations.
- Bumped package version from `0.1.14` to `0.1.15`.

## [0.1.14] - 2026-02-28

### Added

- Account private endpoint wrapper expansion:
  - VPC endpoints: `list_vpc_endpoints`, `create_vpc_endpoint`, `delete_vpc_endpoint`
  - Customer-managed keys: `list_customer_managed_keys`, `create_customer_managed_key`, `delete_customer_managed_key`
- Account wrapper regression coverage extended in `tests/test_account_client.py`.

### Changed

- Expanded account endpoint catalog/constants with VPC endpoint and customer-managed-key routes.
- Updated README and usage examples for account private endpoint lifecycle operations.
- Bumped package version from `0.1.13` to `0.1.14`.

## [0.1.13] - 2026-02-28

### Added

- Response normalization edge-case coverage in `tests/test_response.py` for:
  - Databricks `runs` list payloads
  - nested `result.items` payload wrappers

### Changed

- Improved `normalize_json` to discover record lists from:
  - additional Databricks keys (`runs`, `schemas`, `catalogs`)
  - generic list fields
  - nested dictionary wrappers that contain list payloads
- Bumped package version from `0.1.12` to `0.1.13`.

## [0.1.12] - 2026-02-28

### Added

- Account wrapper expansion:
  - Networks: `list_networks`, `create_network`, `delete_network`
  - Private access settings: `list_private_access_settings`, `create_private_access_settings`, `delete_private_access_settings`
- Additional account wrapper behavior tests in `tests/test_account_client.py`.

### Changed

- Expanded account endpoint catalog/constants with network and private-access-settings routes.
- Updated README and usage examples for account network/private-access lifecycle operations.
- Bumped package version from `0.1.11` to `0.1.12`.

## [0.1.11] - 2026-02-28

### Added

- Account wrapper expansion:
  - Credentials: `list_credentials`, `create_credentials`, `delete_credentials`
  - Storage configurations: `list_storage_configurations`, `create_storage_configuration`, `delete_storage_configuration`
  - Networks: `list_networks`, `create_network`, `delete_network`
  - Private access settings: `list_private_access_settings`, `create_private_access_settings`, `delete_private_access_settings`
- Account wrapper behavior tests in `tests/test_account_client.py`.

### Changed

- Expanded account endpoint catalog/constants with credentials, storage-configuration, network, and private-access-settings routes.
- Updated README and usage examples for account credential/storage lifecycle operations.
- Bumped package version from `0.1.10` to `0.1.11`.

## [0.1.10] - 2026-02-28

### Added

- Unity Catalog detail wrappers:
  - `get_catalog`
  - `get_schema`
- Token wrappers:
  - `list_tokens`
  - `revoke_token` (with non-empty token validation)
- Notebook context edge-case tests in `tests/test_notebook_context.py`.
- Extended workspace wrapper tests for new wrappers and validation behavior.

### Changed

- Expanded endpoint catalog/constants with Unity Catalog detail and token list/revoke routes.
- Updated usage examples to include Unity Catalog detail and token operations.
- Bumped package version from `0.1.9` to `0.1.10`.

## [0.1.9] - 2026-02-28

### Added

- Additional workspace wrappers:
  - Repos: `list_repos`, `get_repo`, `create_repo`, `delete_repo`
  - Secret scopes: `create_secret_scope`, `list_secret_scopes`, `delete_secret_scope`
- Extended wrapper behavior tests in `tests/test_workspace_client.py`.

### Changed

- Expanded endpoint catalogs/constants for repos and secret scope routes.
- Updated README/USAGE examples with new repos and secret scope wrappers.
- Bumped package version from `0.1.8` to `0.1.9`.

## [0.1.8] - 2026-02-28

### Added

- Live process visibility dashboard at `docs/PROCESS_DASHBOARD.md`.

### Changed

- Bumped package version from `0.1.7` to `0.1.8`.

## [0.1.7] - 2026-02-28

### Added

- Full compatibility module tree under `rehladigital_aws_dbx_tools`:
  - core modules (`client`, `config`, `auth`, `http_client`, `response`, `exceptions`, `notebook_context`)
  - client subpackage modules
  - endpoint and generated endpoint subpackage modules
- Extended public import coverage test for submodule import path.

### Changed

- Bumped package version from `0.1.6` to `0.1.7`.

## [0.1.6] - 2026-02-28

### Added

- New public import package `rehladigital_aws_dbx_tools` that re-exports API symbols for end users.
- Public import regression test in `tests/test_public_import.py`.

### Changed

- Updated README and usage docs to use:
  - `from rehladigital_aws_dbx_tools import DatabricksApiClient`
- Bumped package version from `0.1.5` to `0.1.6`.

## [0.1.5] - 2026-02-28

### Added

- Workspace wrappers for additional high-value APIs:
  - Unity Catalog: `list_catalogs`, `list_schemas`
  - Repos: `update_repo`
  - Secrets: `put_secret`
  - Tokens: `create_token`, `delete_token`
- Wrapper regression coverage expanded in `tests/test_workspace_client.py`.
- Loop maintainer process document added at `docs/LOOP_MAINTAINER_AGENT.md`.

### Changed

- Expanded endpoint catalog/constants for new workspace wrappers.
- Updated README/USAGE examples to include Unity Catalog and safe secret handling examples.
- Bumped package version from `0.1.4` to `0.1.5`.

## [0.1.4] - 2026-02-28

### Added

- Improved PyPI metadata in `pyproject.toml`:
  - `keywords`
  - `classifiers`
  - `project.urls`

### Changed

- Renamed published distribution from `unified-databricks-api` to `rehladigital-aws-dbx-tools`.
- Updated install instructions in `README.md` and `docs/USAGE.md` to:
  - `pip install rehladigital-aws-dbx-tools`
- Updated Spark optional install hint to:
  - `pip install "rehladigital-aws-dbx-tools[spark]"`
- Bumped package version from `0.1.3` to `0.1.4`.

## [0.1.3] - 2026-02-28

### Added

- `README.md` section describing Rehla Digital Inc and package stewardship.
- PyPI publish step in `.github/workflows/release.yml` using `PYPI_API_TOKEN`.

### Changed

- Release runbook updated with PyPI token setup and publish verification guidance.
- Bumped package version from `0.1.2` to `0.1.3`.

## [0.1.2] - 2026-02-28

### Added

- GitHub Actions CI workflow: `.github/workflows/ci.yml`
- GitHub Actions release workflow: `.github/workflows/release.yml`
- Retry behavior test for HTTP 5xx recovery in `tests/test_http_client.py`

### Changed

- Bumped package version from `0.1.1` to `0.1.2`.
- Updated `project.license` metadata to SPDX string format (`MIT`) for setuptools compatibility.

## [0.1.1] - 2026-02-28

### Added

- Workspace wrapper expansion:
  - Jobs: `get_job`, `create_job`, `update_job`, `run_job_now`, `get_job_run`, `cancel_job_run`, `delete_job`
  - Clusters: `get_cluster`, `create_cluster`, `edit_cluster`, `start_cluster`, `restart_cluster`, `delete_cluster`, `permanent_delete_cluster`, `cluster_events`
- Account workspace lifecycle wrappers:
  - `get_workspace`, `create_workspace`, `update_workspace`, `delete_workspace`
- Baseline capability matrix and continuous loop context artifacts:
  - `docs/CAPABILITY_MATRIX.md`
  - `docs/LOOP_CONTEXT.md`
  - `docs/CYCLE_LOG.md`
- Wrapper behavior tests in `tests/test_workspace_client.py` and additional account lifecycle tests.

### Changed

- Expanded endpoint catalog and generated endpoint constants to include new wrapper routes.
- Updated `README.md` and `docs/USAGE.md` examples for newly added wrappers.
- Bumped package version from `0.1.0` to `0.1.1`.
