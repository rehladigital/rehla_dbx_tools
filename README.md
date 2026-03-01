<<<<<<< HEAD
# rehla-aw-databricks-tools
=======
# Unified Databricks API
>>>>>>> 95c476f (Build unified Databricks API package with hardening and tests.)

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
<<<<<<< HEAD
jobs = client.workspace.list_jobs()
df = jobs.to_pandas()
print(df.head())
=======
if client.workspace is not None:
    jobs = client.workspace.list_jobs()
    df = jobs.to_pandas()
    print(df.head())
>>>>>>> 95c476f (Build unified Databricks API package with hardening and tests.)
```

## Notebook Context Bootstrap

Inside Databricks notebooks:

```python
from databricks_api import DatabricksApiClient

client = DatabricksApiClient.from_notebook_context()
<<<<<<< HEAD
clusters = client.workspace.list_clusters()
spark_df = clusters.to_spark()
display(spark_df)
=======
if client.workspace is not None:
    clusters = client.workspace.list_clusters()
    spark_df = clusters.to_spark()
    display(spark_df)
>>>>>>> 95c476f (Build unified Databricks API package with hardening and tests.)
```

## Account API

`account` client is enabled when `DATABRICKS_ACCOUNT_HOST` and `DATABRICKS_ACCOUNT_ID` are set.

```python
<<<<<<< HEAD
workspaces = client.account.list_workspaces()
print(workspaces.to_pandas().head())
=======
if client.account is not None:
    workspaces = client.account.list_workspaces()
    print(workspaces.to_pandas().head())
>>>>>>> 95c476f (Build unified Databricks API package with hardening and tests.)
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

<<<<<<< HEAD
## Endpoint Wrapper Generation

Starter generator is included:

```bash
py tools/generate_endpoints.py
```

Update `src/databricks_api/endpoints/catalog.py` and regenerate wrappers under `src/databricks_api/endpoints/generated/`.

=======
>>>>>>> 95c476f (Build unified Databricks API package with hardening and tests.)
For detailed setup and examples, see `docs/USAGE.md`.
