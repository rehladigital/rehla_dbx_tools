# Capability Matrix

## Current Coverage Snapshot

Date: 2026-02-28

### Clients and Convenience Wrappers

| Scope | Client | Convenience wrappers | Generic request path |
|---|---|---|---|
| Workspace | `WorkspaceClient` | `list_jobs`, `list_clusters` | `request_versioned(...)` |
| Account | `AccountClient` | `list_workspaces` | `request_account(...)` |
| Unified | `DatabricksApiClient` | construction only (`from_env`, `from_notebook_context`) | delegates to workspace/account |

### Endpoint Catalog Coverage

| Scope | API version | Catalog entries |
|---|---|---|
| Workspace | `2.0` | `clusters_list` |
| Workspace | `2.1` | `jobs_list` |
| Account | `2.0` | `workspaces_list` |

### Test Coverage

| Area | Status | Notes |
|---|---|---|
| Config load/normalize | Covered | `tests/test_config.py` |
| Auth edge case | Covered | invalid `expires_in` in OAuth |
| HTTP pagination guard | Covered | repeated token fails fast |
| Response normalization | Covered | nested/list/scalar to DataFrame |
| Account path shaping | Covered | account-scoped endpoint composition |
| Account-only client init | Covered | no forced workspace requirement |
| Workspace wrappers | Gap | no direct wrapper behavior tests |
| Notebook context resolver | Gap | no direct extraction tests |
| Retry success/failure matrix | Gap | limited HTTP retry assertions |

## Prioritized Missing Functionality

1. Jobs wrappers: `get`, `create`, `update/reset`, `run-now`, `get-run`, `cancel-run`, `delete`
2. Clusters wrappers: `get`, `create`, `edit`, `start`, `restart`, `delete`, `permanent-delete`, `events`
3. Account workspaces lifecycle: `create`, `get`, `update`, `delete`
4. Endpoint catalog expansion and consistency with convenience wrappers
5. CI/release automation (`ci.yml`, `release.yml`, changelog/runbook)

## Online Pain Points to Keep Addressed

- Pagination regressions and parameter handling drift.
- Account vs workspace auth/context mismatch in notebook environments.
- Endpoint/version drift requiring stable generic fallback paths.
- Retry/timeout behavior consistency under throttling and 5xx failures.
