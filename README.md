# Rehla FlightDeck for Databricks

Rehla FlightDeck for Databricks is a unified, DataFrame-first API layer for AWS Databricks workspace and account operations.

## About Rehla Digital Inc

Rehla Digital Inc builds cloud and data engineering solutions that help teams standardize platform operations, accelerate delivery, and reduce integration risk. This package is maintained as part of that effort to provide a practical, production-oriented Databricks API toolkit.

## Install

```bash
pip install rehla_dbx_tools
```

Import in Python with underscores:

```python
from rehla_dbx_tools import DatabricksApiClient
```

Install Spark extras if needed:

```bash
pip install "rehla_dbx_tools[spark]"
```

## Quick Start

```python
from rehla_dbx_tools import dbx

client = dbx()  # uses env vars (DATABRICKS_HOST/TOKEN or DBX_HOST/TOKEN)
print("jobs:", len(client.list_jobs(limit=25)))
print("active:", len(client.list_active_job_runs(limit=25)))
```

Explicit host/token:

```python
from rehla_dbx_tools import dbx

client = dbx("https://dbc-xxxx.cloud.databricks.com", "dapi...token...")
print("runs:", len(client.list_recent_job_runs(limit=25)))
```

Token can be omitted if you want guided auth:

```python
from rehla_dbx_tools import connect

client = connect(
    host="https://dbc-xxxx.cloud.databricks.com",
    open_browser_for_token=True,  # opens Access Tokens page
    prompt_for_token=True,         # prompts to paste token
)
```

Windows SSO flow (Databricks CLI login):

```python
from rehla_dbx_tools import DatabricksApiClient

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

## Operation Coverage Status

This package build supports read and write operations through workspace and account clients.
- GET requests force pagination aggregation for DataFrame-first workflows.
- Delete operations are exposed for full API parity.
- Delete operation paths are not yet fully cycle-validated end-to-end in live environments for this release.

### Version and help metadata

```python
import rehla_dbx_tools as rdt

print(rdt.__version__)
print(rdt.__Help__)
```

### Available tools (current build)

Workspace (`client.workspace`):
- `list_jobs`, `get_job`
- `list_job_runs`, `get_job_run`, `get_job_run_output`, `export_job_run`
- `get_job_permissions`, `set_job_permissions`, `update_job_permissions`, `get_job_permission_levels`
- `get_object_permissions`, `set_object_permissions`, `update_object_permissions`, `get_object_permission_levels`
- `list_sql_alerts`, `create_sql_alert`, `get_sql_alert`, `update_sql_alert`, `delete_sql_alert`
- `list_sql_queries`, `create_sql_query`, `get_sql_query`, `update_sql_query`, `delete_sql_query`
- `list_dashboards`, `create_dashboard`, `get_dashboard`, `update_dashboard`, `trash_dashboard`, `publish_dashboard`, `unpublish_dashboard`
- `list_apps`, `create_app`, `get_app`, `update_app`, `delete_app`, `start_app`, `stop_app`
- `get_app_permissions`, `set_app_permissions`, `update_app_permissions`, `get_app_permission_levels`
- `list_all_tokens`, `get_token_info`
- `create_execution_context`, `run_command`, `get_command_status`, `cancel_command`, `delete_execution_context`
- `list_clean_rooms`, `create_clean_room`, `get_clean_room`, `update_clean_room`, `delete_clean_room`
- `list_clean_room_assets`, `create_clean_room_asset`, `get_clean_room_asset`, `update_clean_room_asset`, `delete_clean_room_asset`
- `list_monitors`, `create_monitor`, `get_monitor`, `update_monitor`, `delete_monitor`
- `list_monitor_refreshes`, `create_monitor_refresh`, `get_monitor_refresh`, `update_monitor_refresh`, `delete_monitor_refresh`, `cancel_monitor_refresh`
- `list_clusters`, `get_cluster`, `cluster_events`
- `get_cluster_permissions`, `get_cluster_permission_levels`
- `list_catalogs`, `list_schemas`, `get_catalog`, `get_schema`
- `list_uc_connections`, `create_uc_connection`, `get_uc_connection`, `update_uc_connection`, `delete_uc_connection`
- `list_uc_external_locations`, `create_uc_external_location`, `get_uc_external_location`, `update_uc_external_location`, `delete_uc_external_location`
- `list_vector_search_endpoints`, `create_vector_search_endpoint`, `get_vector_search_endpoint`, `update_vector_search_endpoint`, `delete_vector_search_endpoint`
- `list_vector_search_indexes`, `create_vector_search_index`, `get_vector_search_index`, `delete_vector_search_index`, `query_vector_search_index`
- `list_sharing_providers`, `create_sharing_provider`, `get_sharing_provider`, `update_sharing_provider`, `delete_sharing_provider`
- `list_share_recipients`, `create_share_recipient`, `get_share_recipient`, `update_share_recipient`, `delete_share_recipient`
- `list_shares`, `create_share`, `get_share`, `update_share`, `delete_share`
- `list_sql_warehouses`, `get_sql_warehouse`
- `list_instance_pools`, `get_instance_pool`
- `get_instance_pool_permissions`, `set_instance_pool_permissions`, `update_instance_pool_permissions`, `get_instance_pool_permission_levels`
- `list_instance_profiles`, `add_instance_profile`, `edit_instance_profile`, `remove_instance_profile`
- `get_all_library_statuses`, `get_library_status`, `install_libraries`, `uninstall_libraries`
- `list_ip_access_lists`, `create_ip_access_list`, `get_ip_access_list`, `replace_ip_access_list`, `update_ip_access_list`, `delete_ip_access_list`
- `list_notification_destinations`, `create_notification_destination`, `get_notification_destination`, `update_notification_destination`, `delete_notification_destination`
- `get_pipeline_permissions`, `set_pipeline_permissions`, `update_pipeline_permissions`, `get_pipeline_permission_levels`
- `list_pipelines`, `create_pipeline`, `get_pipeline`, `edit_pipeline`, `delete_pipeline`, `start_pipeline`, `stop_pipeline`, `list_pipeline_events`, `list_pipeline_updates`, `get_pipeline_update`
- `list_query_history`
- `get_serving_endpoint_permissions`, `set_serving_endpoint_permissions`, `update_serving_endpoint_permissions`, `get_serving_endpoint_permission_levels`
- `list_serving_endpoints`, `create_serving_endpoint`, `get_serving_endpoint`, `update_serving_endpoint_config`, `delete_serving_endpoint`, `query_serving_endpoint`
- `list_marketplace_listings`, `get_marketplace_listing`, `search_marketplace_listings`, `list_marketplace_installations`, `install_marketplace_listing`, `uninstall_marketplace_installation`
- `list_genie_spaces`, `create_genie_space`, `get_genie_space`, `update_genie_space`, `delete_genie_space`
- `list_global_init_scripts`, `create_global_init_script`, `get_global_init_script`, `update_global_init_script`, `delete_global_init_script`
- `list_setting_keys_metadata`, `get_workspace_setting`, `update_workspace_setting`, `get_workspace_conf`, `set_workspace_conf`
- `list_tag_policies`, `create_tag_policy`, `get_tag_policy`, `update_tag_policy`, `delete_tag_policy`
- `list_tag_assignments`, `create_tag_assignment`, `get_tag_assignment`, `update_tag_assignment`, `delete_tag_assignment`
- `list_quality_monitors`, `create_quality_monitor`, `get_quality_monitor`, `update_quality_monitor`, `delete_quality_monitor`
- `list_postgres_projects`, `create_postgres_project`, `get_postgres_project`, `update_postgres_project`, `delete_postgres_project`
- `list_postgres_branches`, `create_postgres_branch`, `get_postgres_branch`, `delete_postgres_branch`
- `list_cluster_policies`, `get_cluster_policy`
- `list_dbfs`, `get_dbfs_status`, `read_dbfs`
- `list_files_directory`, `create_files_directory`, `delete_files_directory`, `get_files_directory_metadata`
- `download_file`, `upload_file`, `delete_file`, `get_file_metadata`
- `list_repos`, `get_repo`
- `list_git_credentials`, `create_git_credential`, `get_git_credential`, `update_git_credential`, `delete_git_credential`
- `list_secret_scopes`
- `list_tokens`

Client-level convenience:
- `list_jobs`
- `list_recent_job_runs`
- `list_active_job_runs`

Account (`client.account`):
- `get_assignable_roles_for_resource`, `get_rule_set`, `update_rule_set`
- `list_workspaces`, `get_workspace`
- `list_credentials`
- `list_storage_configurations`
- `list_networks`
- `list_private_access_settings`
- `list_vpc_endpoints`
- `list_customer_managed_keys`
- `list_users`, `get_user`
- `list_groups`, `get_group`
- `resolve_external_user`, `resolve_external_service_principal`, `resolve_external_group`, `get_workspace_access_details`
- `list_budget_policies`, `get_budget_policy`
- `list_log_delivery_configurations`, `get_log_delivery_configuration`

For detailed setup and examples, see `docs/USAGE.md`.

## How This Differs From Databricks SDK/API

- **Less boilerplate**: one-liner bootstrap (`dbx(...)` / `connect(...)`) for quick scripts.
- **DataFrame-first**: normalized payloads and built-in Pandas/Spark conversion paths.
- **Forced read pagination**: GET calls aggregate paginated records automatically for analysis workloads.
- **Broad API surface**: supports both read and mutation workflows from one client.
- **Operational ergonomics**: host normalization, env aliases, browser-guided token flow, and Windows SSO helper.

## WordPress-Style Docs

- AWS + Databricks blog draft: `docs/BLOG_AWS_DATABRICKS_WORDPRESS.md`
- Complete tool-by-tool blog reference: `docs/BLOG_TOOL_REFERENCE_WORDPRESS.md`
- Complete built-tools usage reference: `docs/COMPLETE_TOOL_USAGE_REFERENCE.md`
