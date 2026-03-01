# Unified Databricks API

Single Python package to call Databricks Workspace and Account APIs and convert JSON responses into Pandas or PySpark DataFrames.

## About Rehla Digital Inc

Rehla Digital Inc builds cloud and data engineering solutions that help teams standardize platform operations, accelerate delivery, and reduce integration risk. This package is maintained as part of that effort to provide a practical, production-oriented Databricks API toolkit.

## Install

```bash
pip install rehla-dbx-tools
```

Import in Python with underscores:

```python
from rehla_dbx_tools import DatabricksApiClient
```

Install Spark extras if needed:

```bash
pip install "rehla-dbx-tools[spark]"
```

## Quick Start

```python
from rehla_dbx_tools import DatabricksApiClient

client = DatabricksApiClient.from_env()
if client.workspace is not None:
    jobs = client.workspace.list_jobs()
    df = jobs.to_pandas()
    print(df.head())

# Force both workspace/account config to a target cloud
client = DatabricksApiClient.from_env_for_cloud("azure")
```

Simple host/token setup:

```python
from rehla_dbx_tools import DatabricksApiClient

client = DatabricksApiClient.simple(
    host="https://dbc-xxxx.cloud.databricks.com",
    token="dapi...token...",
)

jobs = client.list_jobs(limit=25)
print("jobs:", len(jobs))

for run in client.list_recent_job_runs(limit=25):
    print(run.get("run_id"))
```

Token can be omitted if you want guided auth:

```python
client = DatabricksApiClient.simple(
    host="https://dbc-xxxx.cloud.databricks.com",
    open_browser_for_token=True,  # opens Access Tokens page
    prompt_for_token=True,         # prompts to paste token
)
```

Windows SSO flow (Databricks CLI login):

```python
client = DatabricksApiClient.from_windows_sso(
    host="https://dbc-xxxx.cloud.databricks.com",
)
```

## Notebook Context Bootstrap

Inside Databricks notebooks:

```python
from rehla_dbx_tools import DatabricksApiClient

client = DatabricksApiClient.from_notebook_context()
if client.workspace is not None:
    clusters = client.workspace.list_clusters()
    spark_df = clusters.to_spark()
    display(spark_df)
```

## Account API

`account` client is enabled when `DATABRICKS_ACCOUNT_HOST` and `DATABRICKS_ACCOUNT_ID` are set.

```python
if client.account is not None:
    workspaces = client.account.list_workspaces()
    print(workspaces.to_pandas().head())
```

## Version-Aware Generic Request

```python
response = client.workspace.request_versioned(
    "GET",
    service="unity-catalog",
    endpoint="metastores",
    api_version="2.1",
)
```

## Read-Only Package Mode

This package build is read-only by design:
- Destructive HTTP methods (`POST`, `PATCH`, `PUT`, `DELETE`) are blocked.
- GET requests force pagination aggregation for DataFrame-first workflows.

### Version and help metadata

```python
import rehla_dbx_tools as rdt

print(rdt.__version__)
print(rdt.__Help__)
```

### Available read-only tools

Workspace (`client.workspace`):
- `list_jobs`, `get_job`
- `list_job_runs`, `get_job_run`, `get_job_run_output`, `export_job_run`
- `get_job_permissions`, `get_job_permission_levels`
- `list_clusters`, `get_cluster`, `cluster_events`
- `get_cluster_permissions`, `get_cluster_permission_levels`
- `list_catalogs`, `list_schemas`, `get_catalog`, `get_schema`
- `list_sql_warehouses`, `get_sql_warehouse`
- `list_instance_pools`, `get_instance_pool`
- `list_cluster_policies`, `get_cluster_policy`
- `list_dbfs`, `get_dbfs_status`, `read_dbfs`
- `list_repos`, `get_repo`
- `list_secret_scopes`
- `list_tokens`

Client-level convenience:
- `list_jobs`
- `list_recent_job_runs`
- `list_active_job_runs`

Account (`client.account`):
- `list_workspaces`, `get_workspace`
- `list_credentials`
- `list_storage_configurations`
- `list_networks`
- `list_private_access_settings`
- `list_vpc_endpoints`
- `list_customer_managed_keys`
- `list_users`, `get_user`
- `list_groups`, `get_group`
- `list_budget_policies`, `get_budget_policy`
- `list_log_delivery_configurations`, `get_log_delivery_configuration`

For detailed setup and examples, see `docs/USAGE.md`.
