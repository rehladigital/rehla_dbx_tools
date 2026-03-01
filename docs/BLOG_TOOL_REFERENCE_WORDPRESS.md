# WordPress Blog Draft

**Title:** Complete Rehla FlightDeck Tool Reference (AWS Databricks, Read-Only Edition)  
**Slug:** rehla-flightdeck-complete-tool-reference-aws-databricks  
**Excerpt:** A practical, sample-driven reference for every read-only tool in Rehla FlightDeck for Databricks.  
**Categories:** Databricks, AWS, Python, Developer Tools  
**Tags:** databricks, aws, sdk, api, python, reference, cheatsheet  
**Author:** Rehla Digital Inc  
**Featured Image Alt:** Databricks tool reference with Python code examples

## Setup Once

```python
from rehla_dbx_tools import dbx

client = dbx("https://dbc-xxxx.cloud.databricks.com", "dapi_xxx")
```

---

## Client-Level Tools

### `list_jobs(limit=25)`
**Purpose:** Return workspace jobs as a plain list of dicts.  
**Sample:**

```python
jobs = client.list_jobs(limit=50)
```

### `list_recent_job_runs(limit=25, job_id=None)`
**Purpose:** Return recent runs as a plain list.  
**Sample:**

```python
runs = client.list_recent_job_runs(limit=100)
```

### `list_active_job_runs(limit=25)`
**Purpose:** Return currently active runs only.  
**Sample:**

```python
active = client.list_active_job_runs(limit=100)
```

---

## Workspace Tools (`client.workspace`)

### Jobs

- `list_jobs(limit=...)`
- `get_job(job_id=...)`
- `list_job_runs(...)`
- `get_job_run(run_id=...)`
- `get_job_run_output(run_id=...)`
- `export_job_run(run_id=..., views_to_export="CODE")`

```python
ws = client.workspace
jobs_resp = ws.list_jobs(limit=50)
job_resp = ws.get_job(job_id=123)
runs_resp = ws.list_job_runs(limit=50)
run_resp = ws.get_job_run(run_id=456)
output_resp = ws.get_job_run_output(run_id=456)
export_resp = ws.export_job_run(run_id=456, views_to_export="CODE")
```

### Job Permissions

- `get_job_permissions(job_id=...)`
- `get_job_permission_levels(job_id=...)`

```python
perm_resp = ws.get_job_permissions(job_id=123)
perm_levels_resp = ws.get_job_permission_levels(job_id=123)
```

### Clusters

- `list_clusters()`
- `get_cluster(cluster_id=...)`
- `cluster_events(cluster_id=..., limit=...)`

```python
clusters_resp = ws.list_clusters()
cluster_resp = ws.get_cluster(cluster_id="0123-abc")
events_resp = ws.cluster_events(cluster_id="0123-abc", limit=100)
```

### Cluster Permissions

- `get_cluster_permissions(cluster_id=...)`
- `get_cluster_permission_levels(cluster_id=...)`

```python
cluster_perm_resp = ws.get_cluster_permissions(cluster_id="0123-abc")
cluster_perm_levels_resp = ws.get_cluster_permission_levels(cluster_id="0123-abc")
```

### Unity Catalog

- `list_catalogs(max_results=...)`
- `list_schemas(catalog_name=..., max_results=...)`
- `get_catalog(catalog_name=...)`
- `get_schema(full_name=...)`

```python
catalogs_resp = ws.list_catalogs(max_results=100)
schemas_resp = ws.list_schemas(catalog_name="main", max_results=100)
catalog_resp = ws.get_catalog("main")
schema_resp = ws.get_schema("main.default")
```

### SQL Warehouses

- `list_sql_warehouses()`
- `get_sql_warehouse(warehouse_id=...)`

```python
wh_list_resp = ws.list_sql_warehouses()
wh_resp = ws.get_sql_warehouse("warehouse-id")
```

### Instance Pools

- `list_instance_pools()`
- `get_instance_pool(instance_pool_id=...)`

```python
pool_list_resp = ws.list_instance_pools()
pool_resp = ws.get_instance_pool("pool-id")
```

### Cluster Policies

- `list_cluster_policies()`
- `get_cluster_policy(policy_id=...)`

```python
policy_list_resp = ws.list_cluster_policies()
policy_resp = ws.get_cluster_policy("policy-id")
```

### DBFS

- `list_dbfs(path=...)`
- `get_dbfs_status(path=...)`
- `read_dbfs(path=..., offset=..., length=...)`

```python
dbfs_list_resp = ws.list_dbfs("dbfs:/tmp")
dbfs_status_resp = ws.get_dbfs_status("dbfs:/tmp/file.txt")
dbfs_read_resp = ws.read_dbfs("dbfs:/tmp/file.txt", offset=0, length=1024)
```

### Repos

- `list_repos(path_prefix=...)`
- `get_repo(repo_id=...)`

```python
repos_resp = ws.list_repos(path_prefix="/Repos/team")
repo_resp = ws.get_repo(repo_id=12345)
```

### Secrets and Tokens (Read-Only)

- `list_secret_scopes()`
- `list_tokens()`

```python
scopes_resp = ws.list_secret_scopes()
tokens_resp = ws.list_tokens()
```

---

## Account Tools (`client.account`)

> Account client is available when account host + account ID are configured.

### Workspaces

- `list_workspaces()`
- `get_workspace(workspace_id=...)`

```python
acc = client.account
workspaces_resp = acc.list_workspaces()
workspace_resp = acc.get_workspace(workspace_id=101)
```

### Infrastructure Configuration

- `list_credentials()`
- `list_storage_configurations()`
- `list_networks()`
- `list_private_access_settings()`
- `list_vpc_endpoints()`
- `list_customer_managed_keys()`

```python
creds_resp = acc.list_credentials()
storage_resp = acc.list_storage_configurations()
networks_resp = acc.list_networks()
pas_resp = acc.list_private_access_settings()
vpce_resp = acc.list_vpc_endpoints()
cmk_resp = acc.list_customer_managed_keys()
```

### SCIM Identity

- `list_users()`
- `get_user(user_id=...)`
- `list_groups()`
- `get_group(group_id=...)`

```python
users_resp = acc.list_users()
user_resp = acc.get_user("user-101")
groups_resp = acc.list_groups()
group_resp = acc.get_group("group-101")
```

### Cost & Logging

- `list_budget_policies()`
- `get_budget_policy(budget_policy_id=...)`
- `list_log_delivery_configurations()`
- `get_log_delivery_configuration(log_delivery_configuration_id=...)`

```python
budget_list_resp = acc.list_budget_policies()
budget_resp = acc.get_budget_policy("bp-101")
logs_list_resp = acc.list_log_delivery_configurations()
logs_resp = acc.get_log_delivery_configuration("ld-101")
```

---

## Package Metadata + Help

```python
import rehla_dbx_tools as rdt

print(rdt.__version__)
print(rdt.__Help__)
```

---

## Notes for DataFrame Pipelines

- GET requests force pagination aggregation by default.
- Responses can be used directly as raw JSON or converted to DataFrames:

```python
resp = client.workspace.list_jobs(limit=100)
pdf = resp.to_pandas()
```

- For quick script ergonomics, prefer client-level helpers (`list_jobs`, `list_recent_job_runs`, `list_active_job_runs`).
