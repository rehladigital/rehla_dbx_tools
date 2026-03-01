# Usage Guide

This guide explains how to use the package for:
- Workspace and Account APIs
- Authentication from env variables, notebook context, PAT, and OAuth SP
- API version selection (GA and preview)
- Converting JSON responses into Pandas or PySpark DataFrames

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

### Account

- `DATABRICKS_ACCOUNT_HOST` (required for account APIs)
- `DATABRICKS_ACCOUNT_ID` (required for account APIs)
- `DATABRICKS_ACCOUNT_AUTH_TYPE` (default fallback from workspace auth type)
- `DATABRICKS_ACCOUNT_TOKEN`
- `DATABRICKS_ACCOUNT_CLIENT_ID`
- `DATABRICKS_ACCOUNT_CLIENT_SECRET`
- `DATABRICKS_ACCOUNT_OAUTH_SCOPE`
- `DATABRICKS_ACCOUNT_API_VERSION` (default `2.0`)

## 3) Create Client from Environment

```python
from databricks_api import DatabricksApiClient

client = DatabricksApiClient.from_env()
```

## 4) Create Client from Notebook Context

When running inside Databricks, host/token can be inferred:

```python
from databricks_api import DatabricksApiClient

client = DatabricksApiClient.from_notebook_context()
```

You can still pass explicit config to override values:

```python
from databricks_api import DatabricksApiClient, UnifiedConfig

cfg = UnifiedConfig.from_env()
client = DatabricksApiClient.from_notebook_context(config=cfg)
```

## 5) Workspace API Calls

### Built-in convenience wrappers

```python
jobs_resp = client.workspace.list_jobs(api_version="2.1", limit=50)
clusters_resp = client.workspace.list_clusters(api_version="2.0")
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
from databricks_api import AuthError, ApiError, RateLimitError, ValidationError
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
pip install -e .[spark]
```

## 12) Suggested Usage Pattern

- Use notebook context inside Databricks notebooks/jobs
- Use environment variables for local scripts and CI/CD
- Use generic `request_versioned(...)` for full endpoint coverage (GA + preview)
- Convert to Pandas for local analysis, Spark DataFrame for large-scale transformations

## 13) Endpoint Generation Workflow

1. Update endpoint definitions in `src/databricks_api/endpoints/catalog.py`.
2. Generate constants:

```bash
py tools/generate_endpoints.py
```

3. Import generated constants from `src/databricks_api/endpoints/generated/` in wrapper modules.

This allows gradual expansion toward broad endpoint coverage while keeping version maps explicit.
