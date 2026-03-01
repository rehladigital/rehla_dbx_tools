# Unified Databricks API

Single Python package to call Databricks Workspace and Account APIs and convert JSON responses into Pandas or PySpark DataFrames.

## Install

```bash
pip install -e .
```

Install Spark extras if needed:

```bash
pip install -e .[spark]
```

## Quick Start

```python
from databricks_api import DatabricksApiClient

client = DatabricksApiClient.from_env()
if client.workspace is not None:
    jobs = client.workspace.list_jobs()
    df = jobs.to_pandas()
    print(df.head())
```

## Notebook Context Bootstrap

Inside Databricks notebooks:

```python
from databricks_api import DatabricksApiClient

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

For detailed setup and examples, see `docs/USAGE.md`.
