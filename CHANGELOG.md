# Changelog

All notable changes to this project will be documented in this file.

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
