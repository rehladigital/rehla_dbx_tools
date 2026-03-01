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

## Expanded Convenience Wrappers

```python
import getpass

if client.workspace is not None:
    run = client.workspace.run_job_now(job_id=123)
    runs = client.workspace.list_job_runs(job_id=123, active_only=True, limit=10)
    run_export = client.workspace.export_job_run(run_id=987, views_to_export="CODE")
    run_output = client.workspace.get_job_run_output(run_id=987)
    run_submit = client.workspace.submit_job_run({"run_name": "ad-hoc-check"})
    run_delete = client.workspace.delete_job_run(run_id=987)
    job_permissions = client.workspace.get_job_permissions(job_id=123)
    permission_levels = client.workspace.get_job_permission_levels(job_id=123)
    permission_update = client.workspace.update_job_permissions(
        job_id=123,
        access_control_list=[{"group_name": "admins", "permission_level": "CAN_MANAGE"}],
    )
    repair = client.workspace.repair_job_run(run_id=987, rerun_all_failed_tasks=True)
    cancel_all = client.workspace.cancel_all_job_runs(job_id=123, all_queued_runs=True)
    cluster = client.workspace.get_cluster(cluster_id="0123-abc")
    catalogs = client.workspace.list_catalogs(max_results=25)
    warehouses = client.workspace.list_sql_warehouses()
    dbfs_files = client.workspace.list_dbfs("dbfs:/tmp")
    token = client.workspace.create_token(lifetime_seconds=3600, comment="ci-short-lived")
    rotated_token = client.workspace.rotate_token(
        token_id_to_revoke="old-token-id",
        lifetime_seconds=3600,
        comment="ci-rotation",
    )
    repos = client.workspace.list_repos(path_prefix="/Repos/team")
    repo = client.workspace.get_repo(repo_id=12345)
    client.workspace.put_secret(
        scope="app-prod",
        key="api-token",
        string_value=getpass.getpass("Secret value: "),
    )

if client.account is not None:
    ws = client.account.get_workspace(workspace_id=101)
    creds = client.account.list_credentials()
    storage_cfgs = client.account.list_storage_configurations()
    networks = client.account.list_networks()
    private_access = client.account.list_private_access_settings()
    vpc_endpoints = client.account.list_vpc_endpoints()
    cmks = client.account.list_customer_managed_keys()
    users = client.account.list_users()
    user = client.account.get_user("user-101")
    groups = client.account.list_groups()
    group = client.account.get_group("group-101")
    budgets = client.account.list_budget_policies()
    log_delivery_configs = client.account.list_log_delivery_configurations()
```

For detailed setup and examples, see `docs/USAGE.md`.
