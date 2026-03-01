# WordPress Blog Draft

**Title:** Rehla FlightDeck for Databricks on AWS: The Fastest Path From API Calls to DataFrames  
**Slug:** rehla-flightdeck-databricks-aws-dataframe-api  
**Excerpt:** Build AWS Databricks automation with one-liner client setup, forced pagination for analytics, and read-only safety defaults.  
**Categories:** Databricks, AWS, Python, Data Engineering  
**Tags:** databricks, aws, python-sdk, dataframe, api-automation, rehla  
**Author:** Rehla Digital Inc  
**Featured Image Alt:** AWS Databricks automation with Rehla FlightDeck

## Why We Built Rehla FlightDeck

Databricks REST APIs are powerful but repetitive in day-to-day engineering workflows.  
Rehla FlightDeck for Databricks provides a thin, production-oriented layer for AWS teams that need:

- fast setup,
- reliable read pagination,
- DataFrame-ready outputs,
- and safer defaults for operational reporting.

## The One-Liner Start

```python
from rehla_dbx_tools import dbx

client = dbx()  # uses DATABRICKS_HOST/TOKEN or DBX_HOST/TOKEN
print(len(client.list_jobs()))
print(len(client.list_recent_job_runs()))
print(len(client.list_active_job_runs()))
```

## Why This Is Better for Analytics Workloads

For reporting pipelines, engineers usually end up writing the same glue repeatedly:

- handle page tokens,
- merge result batches,
- normalize shape differences,
- convert into DataFrames.

FlightDeck solves this with read-focused defaults:

- GET requests aggregate pagination automatically,
- payloads are consistently easier to consume,
- and conversion helpers stay built-in.

## Read-Only Safety by Default

This build intentionally blocks destructive operations (`POST`, `PATCH`, `PUT`, `DELETE`) to reduce accidental write risk in operational scripts.

That means it is ideal for:

- daily health checks,
- SLA dashboards,
- metadata catalog reporting,
- compliance/visibility pipelines.

## AWS + Databricks Example

```python
from rehla_dbx_tools import dbx

client = dbx("https://dbc-xxxx.cloud.databricks.com", "dapi_xxx")

jobs = client.list_jobs(limit=100)
runs = client.list_recent_job_runs(limit=100)
active = client.list_active_job_runs(limit=100)

print("jobs:", len(jobs), "runs:", len(runs), "active:", len(active))
```

## Where to Go Next

- Full usage: `docs/USAGE.md`
- Detailed tool-by-tool reference (WordPress format): `docs/BLOG_TOOL_REFERENCE_WORDPRESS.md`
- Package metadata in code:

```python
import rehla_dbx_tools as rdt
print(rdt.__version__)
print(rdt.__Help__)
```
