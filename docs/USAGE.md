# Usage Guide

This guide explains how to use the package for:
- Workspace and Account APIs
- Authentication from env variables, notebook context, PAT, and OAuth SP
- API version selection (GA and preview)
- Converting JSON responses into Pandas or PySpark DataFrames

## Install

```bash
pip install rehla-dbx-tools
```

For Spark DataFrame conversion support:

```bash
pip install "rehla-dbx-tools[spark]"
```

## 1) Configuration Model

The package supports two API scopes:
- `workspace` APIs (per workspace host)
- `account` APIs (account-level host + account ID)

Configuration precedence:
1. Explicit Python config
2. Notebook context (`dbutils.notebook.entry_point`) when using `from_notebook_context()`
3. Environment variables

## 2) Environment Variables

### Workspace

- `DATABRICKS_HOST` (required for local usage if not from notebook context)
- `DATABRICKS_AUTH_TYPE` (`auto`, `pat`, `oauth`, `notebook`; default `auto`)
- `DATABRICKS_TOKEN` (PAT)
- `DATABRICKS_CLIENT_ID` (OAuth service principal)
- `DATABRICKS_CLIENT_SECRET` (OAuth service principal)
- `DATABRICKS_OAUTH_SCOPE` (default `all-apis`)
- `DATABRICKS_WORKSPACE_API_VERSION` (default `2.1`)
- `DATABRICKS_CLOUD` (`aws`, `azure`, `gcp`; default `aws`)

### Account

- `DATABRICKS_ACCOUNT_HOST` (required for account APIs)
- `DATABRICKS_ACCOUNT_ID` (required for account APIs)
- `DATABRICKS_ACCOUNT_AUTH_TYPE` (default fallback from workspace auth type)
- `DATABRICKS_ACCOUNT_TOKEN`
- `DATABRICKS_ACCOUNT_CLIENT_ID`
- `DATABRICKS_ACCOUNT_CLIENT_SECRET`
- `DATABRICKS_ACCOUNT_OAUTH_SCOPE`
- `DATABRICKS_ACCOUNT_API_VERSION` (default `2.0`)
- `DATABRICKS_ACCOUNT_CLOUD` (`aws`, `azure`, `gcp`; defaults to `DATABRICKS_CLOUD`)

Cloud-host alignment guardrail:
- If host pattern clearly indicates a cloud (for example `*.azuredatabricks.net` or `*.gcp.databricks.com`), the corresponding cloud env value must match.
- If cloud env values are omitted, cloud is inferred from host pattern when possible; otherwise fallback is `aws`.

## 3) Create Client from Environment

```python
from rehla_dbx_tools import DatabricksApiClient

client = DatabricksApiClient.from_env()
```

## 4) Create Client from Notebook Context

When running inside Databricks, host/token can be inferred:

```python
from rehla_dbx_tools import DatabricksApiClient

client = DatabricksApiClient.from_notebook_context()
```

You can still pass explicit config to override values:

```python
from rehla_dbx_tools import DatabricksApiClient, UnifiedConfig

cfg = UnifiedConfig.from_env()
client = DatabricksApiClient.from_notebook_context(config=cfg)
```

## 5) Workspace API Calls

### Built-in convenience wrappers

```python
import getpass

jobs_resp = client.workspace.list_jobs(api_version="2.1", limit=50)
clusters_resp = client.workspace.list_clusters(api_version="2.0")
job_resp = client.workspace.get_job(job_id=123)
run_resp = client.workspace.run_job_now(job_id=123, notebook_params={"date": "2026-02-28"})
cluster_resp = client.workspace.get_cluster(cluster_id="0123-abc")
catalogs_resp = client.workspace.list_catalogs(max_results=25)
schemas_resp = client.workspace.list_schemas(catalog_name="main", max_results=100)
catalog_detail = client.workspace.get_catalog("main")
schema_detail = client.workspace.get_schema("main.default")
repo_resp = client.workspace.update_repo(repo_id=12345, branch="main")
secret_resp = client.workspace.put_secret(
    scope="app-prod",
    key="db-password",
    string_value=getpass.getpass("Secret value: "),
)
token_resp = client.workspace.create_token(lifetime_seconds=3600, comment="short-lived-ci-token")
token_list = client.workspace.list_tokens()
token_revoke = client.workspace.revoke_token(token_id="token-id")
token_rotate = client.workspace.rotate_token(
    token_id_to_revoke="old-token-id",
    lifetime_seconds=3600,
    comment="rotation-run",
)
repos_resp = client.workspace.list_repos(path_prefix="/Repos/team")
repo_get = client.workspace.get_repo(repo_id=12345)
repo_create = client.workspace.create_repo(
    url="https://github.com/rehladigital/repo.git",
    provider="gitHub",
    path="/Repos/team/repo",
)
repo_delete = client.workspace.delete_repo(repo_id=12345)
scope_create = client.workspace.create_secret_scope(scope="app-prod", initial_manage_principal="users")
scope_list = client.workspace.list_secret_scopes()
scope_delete = client.workspace.delete_secret_scope(scope="app-prod")
```

### Generic versioned request (recommended for full endpoint coverage)

```python
resp = client.workspace.request_versioned(
    method="GET",
    service="unity-catalog",
    endpoint="metastores",
    api_version="2.1",  # e.g., "2.0", "2.1", "preview"
)
```

### Preview endpoint example

```python
preview_resp = client.workspace.request_versioned(
    "GET",
    service="some-service",
    endpoint="some-preview-endpoint",
    api_version="preview",
)
```

## 6) Account API Calls

```python
if client.account is not None:
    ws_resp = client.account.list_workspaces(api_version="2.0")
    ws_get = client.account.get_workspace(workspace_id=101)
    ws_create = client.account.create_workspace({"workspace_name": "finance-prod"})
    ws_update = client.account.update_workspace(101, {"workspace_name": "finance-prod-v2"})
    ws_delete = client.account.delete_workspace(101)
    creds_list = client.account.list_credentials()
    creds_create = client.account.create_credentials({"credentials_name": "prod-cross-account-role"})
    creds_delete = client.account.delete_credentials("cred-101")
    storage_list = client.account.list_storage_configurations()
    storage_create = client.account.create_storage_configuration(
        {"storage_configuration_name": "prod-root-bucket"}
    )
    storage_delete = client.account.delete_storage_configuration("sc-101")
    network_list = client.account.list_networks()
    network_create = client.account.create_network({"network_name": "prod-vpc"})
    network_delete = client.account.delete_network("net-101")
    pas_list = client.account.list_private_access_settings()
    pas_create = client.account.create_private_access_settings(
        {"private_access_settings_name": "prod-private-link"}
    )
    pas_delete = client.account.delete_private_access_settings("pas-101")
    vpce_list = client.account.list_vpc_endpoints()
    vpce_create = client.account.create_vpc_endpoint({"vpc_endpoint_name": "prod-vpce"})
    vpce_delete = client.account.delete_vpc_endpoint("vpce-101")
    cmk_list = client.account.list_customer_managed_keys()
    cmk_create = client.account.create_customer_managed_key(
        {"use_cases": ["MANAGED_SERVICES"], "aws_key_info": {"key_arn": "arn:aws:kms:region:acct:key/id"}}
    )
    cmk_delete = client.account.delete_customer_managed_key("cmk-101")
    users_list = client.account.list_users()
    user_get = client.account.get_user("user-101")
    user_create = client.account.create_user({"userName": "alice@example.com", "active": True})
    user_patch = client.account.patch_user(
        "user-101",
        {"Operations": [{"op": "replace", "path": "active", "value": False}]},
    )
    user_delete = client.account.delete_user("user-101")
    groups_list = client.account.list_groups()
    group_get = client.account.get_group("group-101")
    group_create = client.account.create_group({"displayName": "data-eng"})
    group_patch = client.account.patch_group(
        "group-101",
        {"Operations": [{"op": "add", "path": "members", "value": [{"value": "123", "display": "alice"}]}]},
    )
    group_delete = client.account.delete_group("group-101")
    budgets_list = client.account.list_budget_policies()
    budget_get = client.account.get_budget_policy("bp-101")
    budget_create = client.account.create_budget_policy(
        {"name": "core-platform-budget", "custom_tags": {"env": "prod"}}
    )
    budget_update = client.account.update_budget_policy("bp-101", {"name": "core-platform-budget-v2"})
    budget_delete = client.account.delete_budget_policy("bp-101")
    log_delivery_list = client.account.list_log_delivery_configurations()
    log_delivery_create = client.account.create_log_delivery_configuration(
        {"config_name": "audit-logs", "output_format": "JSON"}
    )
    log_delivery_get = client.account.get_log_delivery_configuration("ld-101")
    log_delivery_patch = client.account.patch_log_delivery_configuration("ld-101", {"status": "DISABLED"})
    log_delivery_delete = client.account.delete_log_delivery_configuration("ld-101")
```

Generic account call:

```python
resp = client.account.request_account(
    method="GET",
    service="accounts",
    endpoint="workspaces",
    api_version="2.0",
)
```

## 7) Convert Response to DataFrame

Every API call returns `ApiResponse`:

```python
resp = client.workspace.list_jobs()
raw = resp.data
```

### Pandas

```python
pdf = resp.to_pandas()
```

### Spark

```python
sdf = resp.to_spark()  # uses active SparkSession or creates one
```

You may pass your own Spark session:

```python
sdf = resp.to_spark(spark_session=spark)
```

## 8) JSON Normalization Behavior

Normalization follows deterministic rules:
- list of dicts -> rows
- dict with list keys (`items`, `results`, `data`, `workspaces`, etc.) -> rows from list
- nested dicts -> flattened column names with dot notation
- scalar -> one-row DataFrame with `value` column

## 9) Pagination

Use `paginate=True` in generic requests when endpoint supports page tokens:

```python
resp = client.workspace.request_versioned(
    "GET",
    service="jobs",
    endpoint="list",
    params={"limit": 25},
    paginate=True,
)
```

The client checks for `next_page_token` and appends results.

## 10) Error Handling

Key exceptions:
- `AuthError` for auth failures
- `ApiError` for HTTP errors
- `RateLimitError` for throttling
- `ValidationError` for config/input issues

```python
from rehla_dbx_tools import AuthError, ApiError, RateLimitError, ValidationError
```

## 11) Troubleshooting

### Missing host error

Set at least one of:
- `DATABRICKS_HOST`
- `DATABRICKS_ACCOUNT_HOST`

### Notebook token not found

`from_notebook_context()` depends on Databricks runtime context; if token is unavailable, set env or explicit config.

### Account client is `None`

Ensure both are set:
- `DATABRICKS_ACCOUNT_HOST`
- `DATABRICKS_ACCOUNT_ID`

### Spark conversion fails

Install spark extra:

```bash
pip install "rehla-dbx-tools[spark]"
```

## 12) Suggested Usage Pattern

- Use notebook context inside Databricks notebooks/jobs
- Use environment variables for local scripts and CI/CD
- Use generic `request_versioned(...)` for full endpoint coverage (GA + preview)
- Convert to Pandas for local analysis, Spark DataFrame for large-scale transformations

## 13) Endpoint Expansion Workflow

1. Add or update endpoint definitions in `src/databricks_api/endpoints/catalog.py`.
2. Add corresponding wrapper methods in client modules.
3. Cover added endpoints with focused tests under `tests/`.

This allows gradual expansion toward broad endpoint coverage while keeping behavior explicit and testable.
