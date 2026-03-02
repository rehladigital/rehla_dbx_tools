# Complete Tool Usage Reference (Built So Far)

This document covers every tool method currently shipped in `rehla_dbx_tools` as of version `1.2.17`.

## 1) Quick Start

```python
from rehla_dbx_tools import dbx

client = dbx(
    host="https://dbc-xxxx.cloud.databricks.com",
    token="dapi_xxxxx",  # optional if using guided auth
)
```

### Alternate startup options

```python
from rehla_dbx_tools import DatabricksApiClient, connect

# Explicit simple constructor
client = DatabricksApiClient.simple(host="https://dbc-xxxx.cloud.databricks.com", token="dapi_xxx")

# Guided token flow (browser + prompt)
client = connect(host="https://dbc-xxxx.cloud.databricks.com", open_browser_for_token=True, prompt_for_token=True)

# Windows SSO
client = DatabricksApiClient.from_windows_sso(host="https://dbc-xxxx.cloud.databricks.com")
```

## 2) Response Notes

- Workspace/account methods return API response objects (not plain lists).
- Client convenience methods return plain lists:
  - `client.list_jobs(...)`
  - `client.list_recent_job_runs(...)`
  - `client.list_active_job_runs(...)`
- GET routes auto-paginate when implemented with `paginate=True` in wrappers.

## 3) Client-Level Methods

### Constructors and setup

- `DatabricksApiClient.from_env()`
- `DatabricksApiClient.simple(host=..., token=..., account_id=..., account_host=...)`
- `DatabricksApiClient.from_windows_sso(host=..., profile=...)`
- `DatabricksApiClient.from_env_for_cloud(cloud=...)`
- `DatabricksApiClient.from_notebook_context()`
- `connect(host=..., token=..., open_browser_for_token=..., prompt_for_token=...)`
- `dbx(host=..., token=..., account_id=..., account_host=...)`

### Convenience list helpers

- `DatabricksApiClient.list_jobs(limit=...)`
- `DatabricksApiClient.list_recent_job_runs(limit=..., job_id=...)`
- `DatabricksApiClient.list_active_job_runs(limit=...)`

## 4) Workspace Tools (`client.workspace`)

## Access/Permissions

- `get_object_permissions(object_type, object_id)`
- `set_object_permissions(object_type, object_id, access_control_list)`
- `update_object_permissions(object_type, object_id, access_control_list)`
- `get_object_permission_levels(object_type, object_id)`

## SCIM (Workspace)

- `get_current_user()`
- `list_scim_groups()`
- `create_scim_group(group_spec)`
- `get_scim_group(group_id)`
- `replace_scim_group(group_id, group_spec)`
- `delete_scim_group(group_id)`
- `update_scim_group(group_id, operations_spec)`
- `list_scim_service_principals()`
- `create_scim_service_principal(service_principal_spec)`
- `get_scim_service_principal(service_principal_id)`
- `replace_scim_service_principal(service_principal_id, service_principal_spec)`
- `delete_scim_service_principal(service_principal_id)`
- `update_scim_service_principal(service_principal_id, operations_spec)`
- `get_password_permissions(user_id)`
- `set_password_permissions(user_id, access_control_list)`
- `update_password_permissions(user_id, access_control_list)`
- `get_password_permission_levels(user_id)`
- `list_scim_users()`
- `create_scim_user(user_spec)`
- `get_scim_user(user_id)`
- `replace_scim_user(user_id, user_spec)`
- `delete_scim_user(user_id)`
- `update_scim_user(user_id, operations_spec)`

## Jobs and Runs

- `list_jobs(limit=...)`
- `get_job(job_id)`
- `create_job(job_settings)`
- `update_job(job_id, new_settings)`
- `delete_job(job_id)`
- `run_job_now(job_id, notebook_params=..., python_params=..., python_named_params=..., jar_params=..., spark_submit_params=...)`
- `list_job_runs(job_id=..., active_only=..., completed_only=..., offset=..., limit=...)`
- `get_job_run(run_id)`
- `cancel_job_run(run_id)`
- `cancel_all_job_runs(job_id, all_queued_runs=...)`
- `export_job_run(run_id, views_to_export=...)`
- `get_job_run_output(run_id)`
- `submit_job_run(run_spec)`
- `delete_job_run(run_id)`
- `repair_job_run(run_id, rerun_all_failed_tasks=..., latest_repair_id=...)`

## Job Permissions

- `get_job_permissions(job_id)`
- `set_job_permissions(job_id, access_control_list)`
- `update_job_permissions(job_id, access_control_list)`
- `get_job_permission_levels(job_id)`

## Clusters

- `list_clusters()`
- `get_cluster(cluster_id)`
- `create_cluster(cluster_spec)`
- `edit_cluster(cluster_id, cluster_changes)`
- `start_cluster(cluster_id)`
- `restart_cluster(cluster_id)`
- `delete_cluster(cluster_id)`
- `permanent_delete_cluster(cluster_id)`
- `cluster_events(cluster_id, limit=...)`

## Cluster Permissions

- `get_cluster_permissions(cluster_id)`
- `update_cluster_permissions(cluster_id, access_control_list)`
- `get_cluster_permission_levels(cluster_id)`

## Cluster Policies

- `list_cluster_policies()`
- `get_cluster_policy(policy_id)`
- `create_cluster_policy(policy_spec)`
- `edit_cluster_policy(policy_id, policy_changes)`
- `delete_cluster_policy(policy_id)`

## Unity Catalog Core

- `list_catalogs(max_results=...)`
- `list_schemas(catalog_name=..., max_results=...)`
- `get_catalog(catalog_name)`
- `get_schema(full_name)`

## Unity Catalog Connections/External Locations

- `list_uc_connections()`
- `create_uc_connection(connection_spec)`
- `get_uc_connection(name)`
- `update_uc_connection(name, connection_changes)`
- `delete_uc_connection(name)`
- `list_uc_external_locations()`
- `create_uc_external_location(location_spec)`
- `get_uc_external_location(name)`
- `update_uc_external_location(name, location_changes)`
- `delete_uc_external_location(name)`

## SQL Warehouses

- `list_sql_warehouses()`
- `get_sql_warehouse(warehouse_id)`
- `create_sql_warehouse(warehouse_spec)`
- `edit_sql_warehouse(warehouse_id, warehouse_changes)`
- `delete_sql_warehouse(warehouse_id)`
- `start_sql_warehouse(warehouse_id)`
- `stop_sql_warehouse(warehouse_id)`
- `get_sql_warehouse_permissions(warehouse_id)`
- `set_sql_warehouse_permissions(warehouse_id, access_control_list)`
- `update_sql_warehouse_permissions(warehouse_id, access_control_list)`
- `get_sql_warehouse_permission_levels(warehouse_id)`

## SQL Alerts

- `list_sql_alerts()`
- `create_sql_alert(alert_spec)`
- `get_sql_alert(alert_id)`
- `update_sql_alert(alert_id, alert_changes)`
- `delete_sql_alert(alert_id)`

## SQL Queries

- `list_sql_queries()`
- `create_sql_query(query_spec)`
- `get_sql_query(query_id)`
- `update_sql_query(query_id, query_changes)`
- `delete_sql_query(query_id)`

## Statement Execution

- `execute_sql_statement(statement_payload)`
- `get_sql_statement(statement_id)`
- `cancel_sql_statement(statement_id)`
- `get_sql_statement_result_chunk(statement_id, chunk_index)`

## MLflow (Experiments and Runs)

- `create_mlflow_experiment(experiment_spec)`
- `delete_mlflow_experiment(experiment_id)`
- `get_mlflow_experiment(experiment_id)`
- `get_mlflow_experiment_by_name(experiment_name)`
- `list_mlflow_experiments(view_type=..., max_results=...)`
- `search_mlflow_experiments(search_spec)`
- `restore_mlflow_experiment(experiment_id)`
- `update_mlflow_experiment(experiment_id, changes)`
- `set_mlflow_experiment_tag(experiment_id, key, value)`
- `create_mlflow_run(run_spec)`
- `delete_mlflow_run(run_id)`
- `restore_mlflow_run(run_id)`
- `get_mlflow_run(run_id)`
- `search_mlflow_runs(search_spec)`
- `log_mlflow_metric(metric_spec)`
- `log_mlflow_param(param_spec)`
- `set_mlflow_run_tag(tag_spec)`
- `create_registered_model(model_spec)`
- `delete_registered_model(name)`
- `get_registered_model(name)`
- `update_registered_model(name, changes)`
- `rename_registered_model(name, new_name)`
- `search_registered_models(search_spec)`
- `set_registered_model_tag(name, key, value)`
- `delete_registered_model_tag(name, key)`
- `get_latest_model_versions(name, stages=...)`
- `create_model_version(version_spec)`
- `delete_model_version(name, version)`
- `get_model_version(name, version)`
- `search_model_versions(search_spec)`
- `update_model_version(name, version, changes)`
- `set_model_version_tag(name, version, key, value)`
- `delete_model_version_tag(name, version, key)`
- `transition_model_version_stage(name, version, stage, archive_existing_versions=...)`
- `get_registered_model_permissions(model_name)`
- `set_registered_model_permissions(model_name, access_control_list)`
- `update_registered_model_permissions(model_name, access_control_list)`
- `get_registered_model_permission_levels(model_name)`
- `create_model_registry_webhook(webhook_spec)`
- `list_model_registry_webhooks(model_name=..., events=..., max_results=..., page_token=...)`
- `update_model_registry_webhook(webhook_id, webhook_changes)`
- `delete_model_registry_webhook(webhook_id)`
- `test_model_registry_webhook(webhook_id)`
- `create_model_registry_comment(name, version, comment)`
- `update_model_registry_comment(comment_id, comment)`
- `delete_model_registry_comment(comment_id)`
- `create_model_version_transition_request(name, version, stage, comment=...)`
- `list_model_version_transition_requests(name, version)`
- `approve_model_version_transition_request(request_id, comment=...)`
- `reject_model_version_transition_request(request_id, comment=...)`
- `delete_model_version_transition_request(request_id)`

## Dashboards (Lakeview)

- `list_dashboards()`
- `create_dashboard(dashboard_spec)`
- `get_dashboard(dashboard_id)`
- `update_dashboard(dashboard_id, dashboard_changes)`
- `trash_dashboard(dashboard_id)`
- `publish_dashboard(dashboard_id)`
- `unpublish_dashboard(dashboard_id)`

## Apps

- `list_apps()`
- `create_app(app_spec)`
- `get_app(app_name)`
- `update_app(app_name, app_changes)`
- `delete_app(app_name)`
- `start_app(app_name)`
- `stop_app(app_name)`

## App Permissions

- `get_app_permissions(app_name)`
- `set_app_permissions(app_name, access_control_list)`
- `update_app_permissions(app_name, access_control_list)`
- `get_app_permission_levels(app_name)`

## Tokens

- `create_token(comment=..., lifetime_seconds=...)`
- `delete_token(token_id)`
- `list_tokens()`
- `revoke_token(token_id)`
- `rotate_token(old_token_id, comment=..., lifetime_seconds=...)`
- `list_all_tokens()`  (token-management)
- `get_token_info(token_id)`  (token-management)

## Repos and Git Credentials

- `list_repos(path_prefix=...)`
- `get_repo(repo_id)`
- `create_repo(url, provider=..., path=..., branch=..., sparse_checkout=...)`
- `update_repo(repo_id, branch=..., tag=...)`
- `delete_repo(repo_id)`
- `list_workspace_objects(path)`
- `create_workspace_directory(path)`
- `get_workspace_object_status(path)`
- `export_workspace_object(path, format=..., direct_download=...)`
- `import_workspace_object(path, content=..., format=..., language=..., overwrite=...)`
- `delete_workspace_object(path, recursive=...)`
- `get_repo_permissions(repo_id)`
- `update_repo_permissions(repo_id, access_control_list)`
- `get_repo_permission_levels(repo_id)`
- `list_git_credentials()`
- `create_git_credential(credential_spec)`
- `get_git_credential(credential_id)`
- `update_git_credential(credential_id, credential_changes)`
- `delete_git_credential(credential_id)`

## Secrets

- `put_secret(scope, key, string_value=..., bytes_value=...)`
- `delete_secret(scope, key)`
- `get_secret(scope, key)`
- `list_secret_keys(scope)`
- `create_secret_scope(scope, initial_manage_principal=...)`
- `list_secret_scopes()`
- `delete_secret_scope(scope)`
- `list_secret_acls(scope)`
- `get_secret_acl(scope, principal)`
- `put_secret_acl(scope, principal, permission)`
- `delete_secret_acl(scope, principal)`

## Command Execution

- `create_execution_context(cluster_id, language=...)`
- `run_command(cluster_id, context_id, language, command)`
- `get_command_status(context_id, command_id)`
- `cancel_command(context_id, command_id)`
- `delete_execution_context(context_id)`

## Clean Rooms

- `list_clean_rooms()`
- `create_clean_room(clean_room_spec)`
- `get_clean_room(clean_room_name)`
- `update_clean_room(clean_room_name, clean_room_changes)`
- `delete_clean_room(clean_room_name)`
- `list_clean_room_assets(clean_room_name)`
- `create_clean_room_asset(clean_room_name, asset_spec)`
- `get_clean_room_asset(clean_room_name, asset_name)`
- `update_clean_room_asset(clean_room_name, asset_name, asset_changes)`
- `delete_clean_room_asset(clean_room_name, asset_name)`

## Data Quality Monitoring

- `list_monitors()`
- `create_monitor(monitor_spec)`
- `get_monitor(monitor_id)`
- `update_monitor(monitor_id, monitor_changes)`
- `delete_monitor(monitor_id)`
- `list_monitor_refreshes(monitor_id)`
- `create_monitor_refresh(monitor_id, refresh_spec)`
- `get_monitor_refresh(monitor_id, refresh_id)`
- `update_monitor_refresh(monitor_id, refresh_id, refresh_changes)`
- `delete_monitor_refresh(monitor_id, refresh_id)`
- `cancel_monitor_refresh(monitor_id, refresh_id)`

## Quality Monitor V2

- `list_quality_monitors()`
- `create_quality_monitor(monitor_spec)`
- `get_quality_monitor(monitor_id)`
- `update_quality_monitor(monitor_id, monitor_changes)`
- `delete_quality_monitor(monitor_id)`

## DBFS

- `list_dbfs(path)`
- `get_dbfs_status(path)`
- `read_dbfs(path, offset=..., length=...)`
- `delete_dbfs(path, recursive=...)`
- `mkdirs_dbfs(path)`

## Files API

- `list_files_directory(path)`
- `create_files_directory(path)`
- `delete_files_directory(path)`
- `get_files_directory_metadata(path)`
- `download_file(path)`
- `upload_file(path, contents_base64=..., overwrite=...)`
- `delete_file(path)`
- `get_file_metadata(path)`

## Instance Pools

- `list_instance_pools()`
- `get_instance_pool(instance_pool_id)`
- `create_instance_pool(instance_pool_spec)`
- `edit_instance_pool(instance_pool_id, instance_pool_changes)`
- `delete_instance_pool(instance_pool_id)`
- `get_instance_pool_permissions(instance_pool_id)`
- `set_instance_pool_permissions(instance_pool_id, access_control_list)`
- `update_instance_pool_permissions(instance_pool_id, access_control_list)`
- `get_instance_pool_permission_levels(instance_pool_id)`

## Instance Profiles

- `list_instance_profiles()`
- `add_instance_profile(instance_profile_arn)`
- `edit_instance_profile(instance_profile_arn, skip_validation=..., iam_role_arn=...)`
- `remove_instance_profile(instance_profile_arn)`

## Libraries

- `get_all_library_statuses()`
- `get_library_status(cluster_id)`
- `install_libraries(cluster_id, libraries)`
- `uninstall_libraries(cluster_id, libraries)`

## Networking (IP Access Lists)

- `list_ip_access_lists()`
- `create_ip_access_list(access_list_spec)`
- `get_ip_access_list(list_id)`
- `replace_ip_access_list(list_id, access_list_spec)`
- `update_ip_access_list(list_id, access_list_changes)`
- `delete_ip_access_list(list_id)`

## Notifications

- `list_notification_destinations()`
- `create_notification_destination(destination_spec)`
- `get_notification_destination(destination_id)`
- `update_notification_destination(destination_id, destination_changes)`
- `delete_notification_destination(destination_id)`

## Pipelines

- `get_pipeline_permissions(pipeline_id)`
- `set_pipeline_permissions(pipeline_id, access_control_list)`
- `update_pipeline_permissions(pipeline_id, access_control_list)`
- `get_pipeline_permission_levels(pipeline_id)`
- `list_pipelines()`
- `create_pipeline(pipeline_spec)`
- `get_pipeline(pipeline_id)`
- `edit_pipeline(pipeline_id, pipeline_changes)`
- `delete_pipeline(pipeline_id)`
- `start_pipeline(pipeline_id, start_spec=...)`
- `stop_pipeline(pipeline_id)`
- `list_pipeline_events(pipeline_id)`
- `list_pipeline_updates(pipeline_id)`
- `get_pipeline_update(pipeline_id, update_id)`

## Query History

- `list_query_history(filter_by=..., max_results=..., include_metrics=...)`

## Model Serving

- `get_serving_endpoint_permissions(endpoint_name)`
- `set_serving_endpoint_permissions(endpoint_name, access_control_list)`
- `update_serving_endpoint_permissions(endpoint_name, access_control_list)`
- `get_serving_endpoint_permission_levels(endpoint_name)`
- `list_serving_endpoints()`
- `create_serving_endpoint(endpoint_spec)`
- `get_serving_endpoint(endpoint_name)`
- `update_serving_endpoint_config(endpoint_name, config_changes)`
- `delete_serving_endpoint(endpoint_name)`
- `query_serving_endpoint(endpoint_name, query_payload)`

## Marketplace

- `list_marketplace_listings()`
- `get_marketplace_listing(listing_id)`
- `search_marketplace_listings(search_payload)`
  - `search_payload` must be a non-empty object.
- `list_marketplace_installations()`
- `get_marketplace_installation(installation_id)`
- `install_marketplace_listing(install_payload)`
  - `install_payload` must be a non-empty object.
- `create_marketplace_installation(install_payload)`
  - `install_payload` must be a non-empty object.
- `uninstall_marketplace_installation(installation_id)`
- `delete_marketplace_installation(installation_id)`
- `list_marketplace_provider_listings()`
- `create_marketplace_provider_listing(listing_spec)`
  - `listing_spec` must be a non-empty object.
- `get_marketplace_provider_listing(listing_id)`
- `update_marketplace_provider_listing(listing_id, listing_changes)`
  - `listing_changes` must be a non-empty object.
- `delete_marketplace_provider_listing(listing_id)`
- `list_marketplace_provider_providers()`
- `create_marketplace_provider_provider(provider_spec)`
  - `provider_spec` must be a non-empty object.
- `get_marketplace_provider_provider(provider_id)`
- `update_marketplace_provider_provider(provider_id, provider_changes)`
  - `provider_changes` must be a non-empty object.
- `delete_marketplace_provider_provider(provider_id)`
- `list_marketplace_provider_files()`
- `create_marketplace_provider_file(file_spec)`
  - `file_spec` must be a non-empty object.
- `get_marketplace_provider_file(file_id)`
- `update_marketplace_provider_file(file_id, file_changes)`
  - `file_changes` must be a non-empty object.
- `delete_marketplace_provider_file(file_id)`
- `list_marketplace_provider_exchanges()`
- `create_marketplace_provider_exchange(exchange_spec)`
- `get_marketplace_provider_exchange(exchange_id)`
- `update_marketplace_provider_exchange(exchange_id, exchange_changes)`
- `delete_marketplace_provider_exchange(exchange_id)`
- `list_marketplace_provider_exchange_filters()`
- `create_marketplace_provider_exchange_filter(filter_spec)`
- `get_marketplace_provider_exchange_filter(filter_id)`
- `update_marketplace_provider_exchange_filter(filter_id, filter_changes)`
- `delete_marketplace_provider_exchange_filter(filter_id)`
- `list_marketplace_provider_personalization_requests()`
- `get_marketplace_provider_personalization_request(request_id)`
- `update_marketplace_provider_personalization_request(request_id, request_changes)`
- `delete_marketplace_provider_personalization_request(request_id)`
- `list_marketplace_consumer_personalization_requests()`
- `create_marketplace_consumer_personalization_request(request_spec)`
- `get_marketplace_consumer_personalization_request(request_id)`
- `update_marketplace_consumer_personalization_request(request_id, request_changes)`
- `delete_marketplace_consumer_personalization_request(request_id)`
- `list_marketplace_consumer_providers()`
- `get_marketplace_consumer_provider(provider_id)`
- `batch_get_marketplace_consumer_providers(provider_ids)`
  - Requires a non-empty list of non-empty string provider IDs.
- `list_marketplace_consumer_fulfillments()`
- `get_marketplace_consumer_fulfillment(fulfillment_id)`
- `get_marketplace_provider_analytics_dashboard(provider_id)`
- `create_marketplace_provider_analytics_dashboard(provider_id, dashboard_spec)`
- `update_marketplace_provider_analytics_dashboard(provider_id, dashboard_changes)`
- `get_latest_marketplace_provider_analytics_dashboard(provider_id)`
- `delete_marketplace_provider_analytics_dashboard(provider_id)`

## Genie

- `list_genie_spaces()`
- `create_genie_space(space_spec)`
- `get_genie_space(space_id)`
- `update_genie_space(space_id, space_changes)`
- `delete_genie_space(space_id)`

## Global Init Scripts

- `list_global_init_scripts()`
- `create_global_init_script(script_spec)`
- `get_global_init_script(script_id)`
- `update_global_init_script(script_id, script_changes)`
- `delete_global_init_script(script_id)`

## Settings and Workspace Conf

- `list_setting_keys_metadata(max_results=..., page_token=...)`
- `get_workspace_setting(setting_key, etag=...)`
- `update_workspace_setting(setting_key, setting_payload, allow_missing=..., field_mask=...)`
- `get_workspace_conf(keys)`
- `set_workspace_conf(conf)`

## Tags

- `list_tag_policies()`
- `create_tag_policy(policy_spec)`
- `get_tag_policy(policy_id)`
- `update_tag_policy(policy_id, policy_changes)`
- `delete_tag_policy(policy_id)`
- `list_tag_assignments(entity_type, entity_id)`
- `create_tag_assignment(entity_type, entity_id, assignment_spec)`
- `get_tag_assignment(entity_type, entity_id, assignment_id)`
- `update_tag_assignment(entity_type, entity_id, assignment_id, assignment_changes)`
- `delete_tag_assignment(entity_type, entity_id, assignment_id)`

## Postgres

- `list_postgres_projects()`
- `create_postgres_project(project_spec)`
- `get_postgres_project(project_id)`
- `update_postgres_project(project_id, project_changes)`
- `delete_postgres_project(project_id)`
- `list_postgres_branches(project_id)`
- `create_postgres_branch(project_id, branch_spec)`
- `get_postgres_branch(project_id, branch_id)`
- `delete_postgres_branch(project_id, branch_id)`

## Vector Search

- `list_vector_search_endpoints()`
- `create_vector_search_endpoint(endpoint_spec)`
- `get_vector_search_endpoint(endpoint_name)`
- `update_vector_search_endpoint(endpoint_name, endpoint_changes)`
- `delete_vector_search_endpoint(endpoint_name)`
- `list_vector_search_indexes(endpoint_name)`
- `create_vector_search_index(endpoint_name, index_spec)`
- `get_vector_search_index(endpoint_name, index_name)`
- `delete_vector_search_index(endpoint_name, index_name)`
- `query_vector_search_index(endpoint_name, index_name, query_payload)`

## Delta Sharing

- `list_sharing_providers()`
- `create_sharing_provider(provider_spec)`
  - `provider_spec` must be a non-empty object.
- `get_sharing_provider(name)`
- `update_sharing_provider(name, provider_changes)`
  - `provider_changes` must be a non-empty object.
- `delete_sharing_provider(name)`
- `get_sharing_provider_permissions(name)`
- `set_sharing_provider_permissions(name, access_control_list)`
- `update_sharing_provider_permissions(name, access_control_list)`
- `get_sharing_provider_permission_levels(name)`
- `list_sharing_provider_shares(name)`
- `get_sharing_provider_share(name, share_name)`
- `create_sharing_provider_share(name, share_link_spec)`
- `delete_sharing_provider_share(name, share_name)`
- `update_sharing_provider_share(name, share_name, share_link_changes)`
  - `share_link_spec` and `share_link_changes` must be non-empty objects.
- `list_share_recipients()`
- `create_share_recipient(recipient_spec)`
  - `recipient_spec` must be a non-empty object.
- `get_share_recipient(name)`
- `update_share_recipient(name, recipient_changes)`
  - `recipient_changes` must be a non-empty object.
- `delete_share_recipient(name)`
- `rotate_share_recipient_token(name, rotation_spec=None)`
- `get_share_recipient_permissions(name)`
- `set_share_recipient_permissions(name, access_control_list)`
- `update_share_recipient_permissions(name, access_control_list)`
- `get_share_recipient_permission_levels(name)`
- `list_share_recipient_shares(name)`
- `get_share_recipient_share(name, share_name)`
- `create_share_recipient_share(name, share_link_spec)`
- `delete_share_recipient_share(name, share_name)`
- `update_share_recipient_share(name, share_name, share_link_changes)`
  - `share_link_spec` and `share_link_changes` must be non-empty objects.
- `list_shares()`
- `create_share(share_spec)`
  - `share_spec` must be a non-empty object.
- `get_share(name)`
- `list_share_providers(name)`
- `get_share_provider(name, provider_name)`
- `create_share_provider_link(name, provider_link_spec)`
- `update_share_provider_link(name, provider_name, provider_link_changes)`
- `delete_share_provider_link(name, provider_name)`
- `list_share_recipients_for_share(name)`
- `get_share_recipient_for_share(name, recipient_name)`
- `create_share_recipient_link(name, recipient_link_spec)`
- `update_share_recipient_link(name, recipient_name, recipient_link_changes)`
- `delete_share_recipient_link(name, recipient_name)`
  - `provider_link_spec`, `provider_link_changes`, `recipient_link_spec`, and `recipient_link_changes` must be non-empty objects.
- `update_share(name, share_changes)`
  - `share_changes` must be a non-empty object.
- `delete_share(name)`
- `get_share_permissions(name)`
- `set_share_permissions(name, access_control_list)`
- `update_share_permissions(name, access_control_list)`
- `get_share_permission_levels(name)`

## 5) Account Tools (`client.account`)

## Access Management

- `get_assignable_roles_for_resource(resource)`
- `get_rule_set(name)`
- `update_rule_set(name, rule_set_spec)`

## Workspaces

- `list_workspaces()`
- `get_workspace(workspace_id)`
- `create_workspace(workspace_spec)`
- `update_workspace(workspace_id, workspace_spec)`
- `delete_workspace(workspace_id)`

## Credentials / Storage / Network

- `list_credentials()`
- `create_credentials(credentials_spec)`
- `delete_credentials(credentials_id)`
- `list_storage_configurations()`
- `create_storage_configuration(storage_configuration_spec)`
- `delete_storage_configuration(storage_configuration_id)`
- `list_networks()`
- `create_network(network_spec)`
- `delete_network(network_id)`
- `list_private_access_settings()`
- `create_private_access_settings(private_access_settings_spec)`
- `delete_private_access_settings(private_access_settings_id)`
- `list_vpc_endpoints()`
- `create_vpc_endpoint(vpc_endpoint_spec)`
- `delete_vpc_endpoint(vpc_endpoint_id)`
- `list_customer_managed_keys()`
- `create_customer_managed_key(key_spec)`
- `delete_customer_managed_key(customer_managed_key_id)`

## SCIM

- `list_users()`
- `get_user(user_id)`
- `create_user(user_spec)`
- `patch_user(user_id, operations_spec)`
- `delete_user(user_id)`
- `list_groups()`
- `get_group(group_id)`
- `create_group(group_spec)`
- `patch_group(group_id, operations_spec)`
- `delete_group(group_id)`

## Budget / Log Delivery

- `list_budget_policies()`
- `get_budget_policy(budget_policy_id)`
- `create_budget_policy(budget_policy_spec)`
- `update_budget_policy(budget_policy_id, budget_policy_spec)`
- `delete_budget_policy(budget_policy_id)`
- `list_log_delivery_configurations()`
- `create_log_delivery_configuration(log_delivery_spec)`
- `get_log_delivery_configuration(log_delivery_configuration_id)`
- `patch_log_delivery_configuration(log_delivery_configuration_id, patch_spec)`
- `delete_log_delivery_configuration(log_delivery_configuration_id)`

## Identity

- `resolve_external_user(external_id)`
- `resolve_external_service_principal(external_id)`
- `resolve_external_group(external_id)`
- `get_workspace_access_details(principal_id, workspace_id=...)`

## 6) Example End-to-End Snippet

```python
from rehla_dbx_tools import dbx

client = dbx(host="https://dbc-xxxx.cloud.databricks.com", token="dapi_xxx")
ws = client.workspace

# Simple read helpers
jobs = client.list_jobs(limit=25)
active = client.list_active_job_runs(limit=25)

# Workspace response-style call
runs_resp = ws.list_job_runs(limit=25)

# Unity Catalog + Vector Search examples
uc_connections = ws.list_uc_connections()
vs_endpoints = ws.list_vector_search_endpoints()

print(len(jobs), len(active), runs_resp.data is not None)
```

