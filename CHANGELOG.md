# Changelog

All notable changes to this project will be documented in this file.

## [2.0.13] - 2026-03-02

### Added

- Delta Sharing provider permissions wrappers:
  - `get_sharing_provider_permissions`
  - `set_sharing_provider_permissions`
  - `update_sharing_provider_permissions`
  - `get_sharing_provider_permission_levels`
- Endpoint catalog entries for provider permissions and permission-level routes.
- Regression test coverage for the new provider permission wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list with sharing provider permission methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with the provider permission operations.
- Bumped package version from `2.0.12` to `2.0.13`.

## [2.0.12] - 2026-03-02

### Added

- Delta Sharing recipient permissions wrappers:
  - `get_share_recipient_permissions`
  - `set_share_recipient_permissions`
  - `update_share_recipient_permissions`
  - `get_share_recipient_permission_levels`
- Delta Sharing share permissions wrappers:
  - `get_share_permissions`
  - `set_share_permissions`
  - `update_share_permissions`
  - `get_share_permission_levels`
- Endpoint catalog entries for recipient/share permissions and permission-level routes.
- Regression test coverage for all new sharing permission wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list with the sharing permission methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with these new Delta Sharing operations.
- Bumped package version from `2.0.11` to `2.0.12`.

## [2.0.11] - 2026-03-02

### Added

- Marketplace installation detail wrapper:
  - `get_marketplace_installation`
- Marketplace provider file update wrapper:
  - `update_marketplace_provider_file`
- Marketplace provider exchange-filter detail wrapper:
  - `get_marketplace_provider_exchange_filter`
- Marketplace provider personalization-request detail wrapper:
  - `get_marketplace_provider_personalization_request`
- Marketplace provider analytics dashboard delete wrapper:
  - `delete_marketplace_provider_analytics_dashboard`
- Endpoint catalog entries for marketplace installation detail, provider file update, exchange-filter detail, personalization-request detail, and analytics-dashboard delete routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list for the expanded marketplace surface.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with the new marketplace operations.
- Bumped package version from `2.0.10` to `2.0.11`.

## [2.0.10] - 2026-03-02

### Added

- Marketplace consumer provider wrappers:
  - `list_marketplace_consumer_providers`
  - `get_marketplace_consumer_provider`
  - `batch_get_marketplace_consumer_providers`
- Marketplace consumer fulfillment wrappers:
  - `list_marketplace_consumer_fulfillments`
  - `get_marketplace_consumer_fulfillment`
- Marketplace provider analytics dashboard wrappers:
  - `get_marketplace_provider_analytics_dashboard`
  - `create_marketplace_provider_analytics_dashboard`
  - `update_marketplace_provider_analytics_dashboard`
  - `get_latest_marketplace_provider_analytics_dashboard`
- Endpoint catalog entries for consumer providers/fulfillments and provider analytics dashboard routes.
- Regression test coverage for these marketplace wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list to include consumer providers, fulfillments, and provider analytics dashboard methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with these new marketplace usage methods.
- Bumped package version from `2.0.9` to `2.0.10`.

## [2.0.9] - 2026-03-02

### Added

- Marketplace provider exchanges wrappers:
  - `list_marketplace_provider_exchanges`
  - `create_marketplace_provider_exchange`
  - `get_marketplace_provider_exchange`
  - `update_marketplace_provider_exchange`
  - `delete_marketplace_provider_exchange`
- Marketplace provider exchange-filters wrappers:
  - `list_marketplace_provider_exchange_filters`
  - `create_marketplace_provider_exchange_filter`
  - `update_marketplace_provider_exchange_filter`
  - `delete_marketplace_provider_exchange_filter`
- Marketplace personalization wrappers:
  - provider: `list_marketplace_provider_personalization_requests`, `update_marketplace_provider_personalization_request`
  - consumer: `list_marketplace_consumer_personalization_requests`, `create_marketplace_consumer_personalization_request`, `get_marketplace_consumer_personalization_request`
- Endpoint catalog entries for marketplace provider exchanges, exchange-filters, and personalization-request routes.
- Regression test coverage for these marketplace wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list to include marketplace exchanges and personalization methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with marketplace exchanges and personalization usage coverage.
- Bumped package version from `2.0.8` to `2.0.9`.

## [2.0.8] - 2026-03-02

### Added

- Marketplace provider listing wrappers:
  - `list_marketplace_provider_listings`
  - `create_marketplace_provider_listing`
  - `get_marketplace_provider_listing`
  - `update_marketplace_provider_listing`
  - `delete_marketplace_provider_listing`
- Marketplace provider provider wrappers:
  - `list_marketplace_provider_providers`
  - `create_marketplace_provider_provider`
  - `get_marketplace_provider_provider`
  - `update_marketplace_provider_provider`
  - `delete_marketplace_provider_provider`
- Marketplace provider file wrappers:
  - `list_marketplace_provider_files`
  - `create_marketplace_provider_file`
  - `get_marketplace_provider_file`
  - `delete_marketplace_provider_file`
- Endpoint catalog entries for marketplace provider listings/providers/files routes.
- Regression test coverage for marketplace provider wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list to include marketplace provider methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with marketplace provider usage coverage.
- Bumped package version from `2.0.7` to `2.0.8`.

## [2.0.7] - 2026-03-02

### Added

- MLflow registry webhooks wrappers:
  - `create_model_registry_webhook`
  - `list_model_registry_webhooks`
  - `update_model_registry_webhook`
  - `delete_model_registry_webhook`
  - `test_model_registry_webhook`
- MLflow model-registry comment wrappers:
  - `create_model_registry_comment`
  - `update_model_registry_comment`
  - `delete_model_registry_comment`
- MLflow transition-request wrappers:
  - `create_model_version_transition_request`
  - `list_model_version_transition_requests`
  - `approve_model_version_transition_request`
  - `reject_model_version_transition_request`
  - `delete_model_version_transition_request`
- Endpoint catalog entries for MLflow webhooks/comments/transition-request routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list to include MLflow webhooks/comments/transition-request methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with MLflow webhooks/comments/transition-request usage coverage.
- Bumped package version from `2.0.6` to `2.0.7`.

## [2.0.6] - 2026-03-02

### Added

- MLflow model registry wrappers in workspace client:
  - `create_registered_model`
  - `delete_registered_model`
  - `get_registered_model`
  - `update_registered_model`
  - `rename_registered_model`
  - `search_registered_models`
  - `set_registered_model_tag`
  - `delete_registered_model_tag`
  - `get_latest_model_versions`
- MLflow model version wrappers in workspace client:
  - `create_model_version`
  - `delete_model_version`
  - `get_model_version`
  - `search_model_versions`
  - `update_model_version`
  - `set_model_version_tag`
  - `delete_model_version_tag`
  - `transition_model_version_stage`
- Registered model permissions wrappers:
  - `get_registered_model_permissions`
  - `set_registered_model_permissions`
  - `update_registered_model_permissions`
  - `get_registered_model_permission_levels`
- Endpoint catalog entries for MLflow model registry/model-version and registered-model permissions routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list to include MLflow model registry and permissions methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with MLflow model registry and permissions usage coverage.
- Bumped package version from `2.0.5` to `2.0.6`.

## [2.0.5] - 2026-03-02

### Added

- MLflow experiments wrappers in workspace client:
  - `create_mlflow_experiment`
  - `delete_mlflow_experiment`
  - `get_mlflow_experiment`
  - `get_mlflow_experiment_by_name`
  - `list_mlflow_experiments`
  - `search_mlflow_experiments`
  - `restore_mlflow_experiment`
  - `update_mlflow_experiment`
  - `set_mlflow_experiment_tag`
- MLflow runs wrappers in workspace client:
  - `create_mlflow_run`
  - `delete_mlflow_run`
  - `restore_mlflow_run`
  - `get_mlflow_run`
  - `search_mlflow_runs`
  - `log_mlflow_metric`
  - `log_mlflow_param`
  - `set_mlflow_run_tag`
- Endpoint catalog entries for MLflow experiments and runs routes.
- Regression test coverage for MLflow wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list to include MLflow experiment/run methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with MLflow usage coverage.
- Bumped package version from `2.0.4` to `2.0.5`.

## [2.0.4] - 2026-03-01

### Added

- Databricks SQL warehouse lifecycle wrappers:
  - `start_sql_warehouse`
  - `stop_sql_warehouse`
- Databricks SQL warehouse permissions wrappers:
  - `get_sql_warehouse_permissions`
  - `set_sql_warehouse_permissions`
  - `update_sql_warehouse_permissions`
  - `get_sql_warehouse_permission_levels`
- Databricks SQL statement execution wrappers:
  - `execute_sql_statement`
  - `get_sql_statement`
  - `cancel_sql_statement`
  - `get_sql_statement_result_chunk`
- Endpoint catalog entries for SQL warehouse start/stop, warehouse permissions, and statement execution routes.
- Regression test coverage for these SQL wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list to include SQL warehouse permissions and statement execution methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with SQL warehouse permissions and statement execution usage coverage.
- Bumped package version from `2.0.3` to `2.0.4`.

## [2.0.3] - 2026-03-01

### Added

- Workspace object wrappers to complete workspace-service object lifecycle operations:
  - `list_workspace_objects`
  - `create_workspace_directory`
  - `get_workspace_object_status`
  - `export_workspace_object`
  - `import_workspace_object`
  - `delete_workspace_object`
- Endpoint catalog entries for `/api/2.0/workspace/*` routes (`list`, `mkdirs`, `get-status`, `export`, `import`, `delete`).
- Regression test coverage for workspace object wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list to include workspace object operations.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with workspace object usage coverage.
- Bumped package version from `2.0.2` to `2.0.3`.

## [2.0.2] - 2026-03-01

### Added

- Workspace secrets-management wrappers to complete the documented secrets scope:
  - `delete_secret`
  - `get_secret`
  - `list_secret_keys`
  - `list_secret_acls`
  - `get_secret_acl`
  - `put_secret_acl`
  - `delete_secret_acl`
- Input validation for secrets methods requiring non-empty identifiers:
  - `put_secret` (`scope`, `key`)
  - all new secret and ACL helper methods
- Endpoint catalog entries for secret ACL and key/list/get/delete routes.
- Regression test coverage for secrets scope wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list to include full secrets scope methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with full secrets scope usage coverage.
- Bumped package version from `2.0.1` to `2.0.2`.

## [2.0.1] - 2026-03-01

### Added

- Workspace SCIM wrappers covering all SCIM scope operations:
  - current user: `get_current_user`
  - groups: `list_scim_groups`, `create_scim_group`, `get_scim_group`, `replace_scim_group`, `delete_scim_group`, `update_scim_group`
  - service principals: `list_scim_service_principals`, `create_scim_service_principal`, `get_scim_service_principal`, `replace_scim_service_principal`, `delete_scim_service_principal`, `update_scim_service_principal`
  - users: `list_scim_users`, `create_scim_user`, `get_scim_user`, `replace_scim_user`, `delete_scim_user`, `update_scim_user`
  - password permissions: `get_password_permissions`, `set_password_permissions`, `update_password_permissions`, `get_password_permission_levels`
- Endpoint catalog entries for workspace SCIM and password-permissions routes.
- Regression test coverage for workspace SCIM wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README available-tools list to include workspace SCIM methods.
- Updated `docs/COMPLETE_TOOL_USAGE_REFERENCE.md` with workspace SCIM usage coverage.
- Bumped package version from `2.0.0` to `2.0.1`.

## [2.0.0] - 2026-03-01

### Changed

- Promoted release version from `1.2.17` to `2.0.0` per major-version transition request.
- Carried forward current built tool surface and documentation set, including:
  - cycle 77 Unity Catalog and Vector Search wrapper additions
  - complete usage reference at `docs/COMPLETE_TOOL_USAGE_REFERENCE.md`

## [1.2.17] - 2026-03-01

### Added

- Unity Catalog wrappers on workspace client:
  - `list_uc_connections`
  - `create_uc_connection`
  - `get_uc_connection`
  - `update_uc_connection`
  - `delete_uc_connection`
  - `list_uc_external_locations`
  - `create_uc_external_location`
  - `get_uc_external_location`
  - `update_uc_external_location`
  - `delete_uc_external_location`
- Vector Search wrappers on workspace client:
  - `list_vector_search_endpoints`
  - `create_vector_search_endpoint`
  - `get_vector_search_endpoint`
  - `update_vector_search_endpoint`
  - `delete_vector_search_endpoint`
  - `list_vector_search_indexes`
  - `create_vector_search_index`
  - `get_vector_search_index`
  - `delete_vector_search_index`
  - `query_vector_search_index`
- Endpoint catalog entries for Unity Catalog connections/external-locations and Vector Search routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include new Unity Catalog and Vector Search methods.
- Added complete built-tools usage document at `docs/COMPLETE_TOOL_USAGE_REFERENCE.md`.
- Bumped package version from `1.2.16` to `1.2.17`.

## [1.2.16] - 2026-03-01

### Added

- Quality Monitor wrappers on workspace client:
  - `list_quality_monitors`
  - `create_quality_monitor`
  - `get_quality_monitor`
  - `update_quality_monitor`
  - `delete_quality_monitor`
- Postgres wrappers on workspace client:
  - `list_postgres_projects`
  - `create_postgres_project`
  - `get_postgres_project`
  - `update_postgres_project`
  - `delete_postgres_project`
  - `list_postgres_branches`
  - `create_postgres_branch`
  - `get_postgres_branch`
  - `delete_postgres_branch`
- Endpoint catalog entries for quality-monitor and postgres routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include quality-monitor and postgres methods.
- Bumped package version from `1.2.15` to `1.2.16`.

## [1.2.15] - 2026-03-01

### Added

- Settings wrappers on workspace client:
  - `list_setting_keys_metadata`
  - `get_workspace_setting`
  - `update_workspace_setting`
  - `get_workspace_conf`
  - `set_workspace_conf`
- Tags wrappers on workspace client:
  - `list_tag_policies`
  - `create_tag_policy`
  - `get_tag_policy`
  - `update_tag_policy`
  - `delete_tag_policy`
  - `list_tag_assignments`
  - `create_tag_assignment`
  - `get_tag_assignment`
  - `update_tag_assignment`
  - `delete_tag_assignment`
- Endpoint catalog entries for settings and tags routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include settings and tags methods.
- Bumped package version from `1.2.14` to `1.2.15`.

## [1.2.14] - 2026-03-01

### Added

- Genie wrappers on workspace client:
  - `list_genie_spaces`
  - `create_genie_space`
  - `get_genie_space`
  - `update_genie_space`
  - `delete_genie_space`
- Global init scripts wrappers on workspace client:
  - `list_global_init_scripts`
  - `create_global_init_script`
  - `get_global_init_script`
  - `update_global_init_script`
  - `delete_global_init_script`
- Endpoint catalog entries for genie and global-init-scripts routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include genie and global-init-scripts methods.
- Bumped package version from `1.2.13` to `1.2.14`.

## [1.2.13] - 2026-03-01

### Added

- Model-serving wrappers on workspace client:
  - `get_serving_endpoint_permissions`
  - `set_serving_endpoint_permissions`
  - `update_serving_endpoint_permissions`
  - `get_serving_endpoint_permission_levels`
  - `list_serving_endpoints`
  - `create_serving_endpoint`
  - `get_serving_endpoint`
  - `update_serving_endpoint_config`
  - `delete_serving_endpoint`
  - `query_serving_endpoint`
- Marketplace wrappers on workspace client:
  - `list_marketplace_listings`
  - `get_marketplace_listing`
  - `search_marketplace_listings`
  - `list_marketplace_installations`
  - `install_marketplace_listing`
  - `uninstall_marketplace_installation`
- Endpoint catalog entries for model-serving and marketplace routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include model-serving and marketplace methods.
- Bumped package version from `1.2.12` to `1.2.13`.

## [1.2.12] - 2026-03-01

### Added

- Pipelines wrappers on workspace client:
  - `get_pipeline_permissions`
  - `set_pipeline_permissions`
  - `update_pipeline_permissions`
  - `get_pipeline_permission_levels`
  - `list_pipelines`
  - `create_pipeline`
  - `get_pipeline`
  - `edit_pipeline`
  - `delete_pipeline`
  - `start_pipeline`
  - `stop_pipeline`
  - `list_pipeline_events`
  - `list_pipeline_updates`
  - `get_pipeline_update`
- Query History wrapper on workspace client:
  - `list_query_history`
- Endpoint catalog entries for pipelines and query-history routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include pipelines and query-history methods.
- Bumped package version from `1.2.11` to `1.2.12`.

## [1.2.11] - 2026-03-01

### Added

- Networking wrappers on workspace client:
  - `list_ip_access_lists`
  - `create_ip_access_list`
  - `get_ip_access_list`
  - `replace_ip_access_list`
  - `update_ip_access_list`
  - `delete_ip_access_list`
- Notifications wrappers on workspace client:
  - `list_notification_destinations`
  - `create_notification_destination`
  - `get_notification_destination`
  - `update_notification_destination`
  - `delete_notification_destination`
- Endpoint catalog entries for networking and notifications routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include networking and notifications methods.
- Bumped package version from `1.2.10` to `1.2.11`.

## [1.2.10] - 2026-03-01

### Added

- Jobs scope additions on workspace client:
  - `set_job_permissions`
- Libraries scope wrappers on workspace client:
  - `get_all_library_statuses`
  - `get_library_status`
  - `install_libraries`
  - `uninstall_libraries`
- Endpoint catalog entries for permissions `PUT` and libraries routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include jobs-permissions setter and libraries methods.
- Bumped package version from `1.2.9` to `1.2.10`.

## [1.2.9] - 2026-03-01

### Added

- Instance profiles wrappers on workspace client:
  - `list_instance_profiles`
  - `add_instance_profile`
  - `edit_instance_profile`
  - `remove_instance_profile`
- Identity wrappers on account client:
  - `resolve_external_user`
  - `resolve_external_service_principal`
  - `resolve_external_group`
  - `get_workspace_access_details`
- Endpoint catalog entries for instance-profiles and identity routes.
- Regression test coverage in:
  - `tests/test_workspace_client.py`
  - `tests/test_account_client.py`

### Changed

- Updated README tool list to include identity and instance-profiles methods.
- Bumped package version from `1.2.8` to `1.2.9`.

## [1.2.8] - 2026-03-01

### Added

- Delta Sharing wrappers on workspace client:
  - `list_sharing_providers`
  - `create_sharing_provider`
  - `get_sharing_provider`
  - `update_sharing_provider`
  - `delete_sharing_provider`
  - `list_share_recipients`
  - `create_share_recipient`
  - `get_share_recipient`
  - `update_share_recipient`
  - `delete_share_recipient`
  - `list_shares`
  - `create_share`
  - `get_share`
  - `update_share`
  - `delete_share`
- Files wrappers on workspace client:
  - `list_files_directory`
  - `create_files_directory`
  - `delete_files_directory`
  - `get_files_directory_metadata`
  - `download_file`
  - `upload_file`
  - `delete_file`
  - `get_file_metadata`
- Endpoint catalog entries for sharing and files routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include sharing and files methods.
- Bumped package version from `1.2.7` to `1.2.8`.

## [1.2.7] - 2026-03-01

### Added

- Databricks Workspace git-credentials wrappers on workspace client:
  - `list_git_credentials`
  - `create_git_credential`
  - `get_git_credential`
  - `update_git_credential`
  - `delete_git_credential`
- Databricks SQL query wrappers on workspace client:
  - `list_sql_queries`
  - `create_sql_query`
  - `get_sql_query`
  - `update_sql_query`
  - `delete_sql_query`
- Endpoint catalog entries for git-credentials and sql-queries routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include git-credentials and SQL-query methods.
- Bumped package version from `1.2.6` to `1.2.7`.

## [1.2.6] - 2026-03-01

### Added

- Data quality monitoring wrappers on workspace client:
  - `list_monitors`
  - `create_monitor`
  - `get_monitor`
  - `update_monitor`
  - `delete_monitor`
  - `list_monitor_refreshes`
  - `create_monitor_refresh`
  - `get_monitor_refresh`
  - `update_monitor_refresh`
  - `delete_monitor_refresh`
  - `cancel_monitor_refresh`
- Instance pool permissions wrappers on workspace client:
  - `get_instance_pool_permissions`
  - `set_instance_pool_permissions`
  - `update_instance_pool_permissions`
  - `get_instance_pool_permission_levels`
- Endpoint catalog entries for data-quality-monitors and instance-pools permissions routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include data-quality and instance-pool-permissions methods.
- Bumped package version from `1.2.5` to `1.2.6`.

## [1.2.5] - 2026-03-01

### Added

- Command execution wrappers on workspace client:
  - `create_execution_context`
  - `run_command`
  - `get_command_status`
  - `cancel_command`
  - `delete_execution_context`
- Clean rooms wrappers on workspace client:
  - `list_clean_rooms`
  - `create_clean_room`
  - `get_clean_room`
  - `update_clean_room`
  - `delete_clean_room`
  - `list_clean_room_assets`
  - `create_clean_room_asset`
  - `get_clean_room_asset`
  - `update_clean_room_asset`
  - `delete_clean_room_asset`
- Endpoint catalog entries for command-execution and clean-rooms routes.
- Regression test coverage for these wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include command-execution and clean-rooms methods.
- Bumped package version from `1.2.4` to `1.2.5`.

## [1.2.4] - 2026-03-01

### Added

- Apps scope wrappers on workspace client:
  - `list_apps`
  - `create_app`
  - `get_app`
  - `update_app`
  - `delete_app`
  - `start_app`
  - `stop_app`
  - `get_app_permissions`
  - `set_app_permissions`
  - `update_app_permissions`
  - `get_app_permission_levels`
- Authentication scope wrappers on workspace client:
  - `list_all_tokens` (token-management)
  - `get_token_info` (token-management)
- Endpoint catalog entries for apps and token-management routes.
- Regression test coverage for apps/authentication wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include apps and token-management methods.
- Bumped package version from `1.2.3` to `1.2.4`.

## [1.2.3] - 2026-03-01

### Added

- Alerts scope wrappers on workspace client:
  - `list_sql_alerts`
  - `create_sql_alert`
  - `get_sql_alert`
  - `update_sql_alert`
  - `delete_sql_alert`
- Dashboards scope wrappers on workspace client:
  - `list_dashboards`
  - `create_dashboard`
  - `get_dashboard`
  - `update_dashboard`
  - `trash_dashboard`
  - `publish_dashboard`
  - `unpublish_dashboard`
- Endpoint catalog entries for SQL alerts and Lakeview dashboards routes.
- Regression test coverage for alerts and dashboards wrappers in `tests/test_workspace_client.py`.

### Changed

- Updated README tool list to include alerts and dashboards methods.
- Bumped package version from `1.2.2` to `1.2.3`.

## [1.2.2] - 2026-03-01

### Added

- Access-management wrappers on account client:
  - `get_assignable_roles_for_resource`
  - `get_rule_set`
  - `update_rule_set`
- Generic permission wrappers on workspace client:
  - `get_object_permissions`
  - `set_object_permissions`
  - `update_object_permissions`
  - `get_object_permission_levels`
- Endpoint catalog entries for access-management and generic object-permissions paths.
- Regression coverage for the new wrappers in:
  - `tests/test_account_client.py`
  - `tests/test_workspace_client.py`

### Changed

- Updated README tool list to include newly added access-management and generic permissions methods.
- Bumped package version from `1.2.1` to `1.2.2`.

## [1.2.1] - 2026-03-01

### Changed

- Removed read-only enforcement in base client request path so POST/PATCH/PUT/DELETE calls are supported again.
- Updated package help metadata and README to reflect full operation support.
- Added explicit release note that delete operations are available but not fully cycle-tested end-to-end yet.
- Reworked plan/TODO docs to use main-plan-driven all-scope execution tracking with agent handoff continuity.

### Security

- Ran static and dependency security scans:
  - Bandit: 4 low-severity findings (subprocess usage and broad exception handling patterns).
  - pip-audit: environment package advisories for `filelock`, `pip`, and `setuptools`.

## [1.2.0] - 2026-03-01

### Changed

- Renamed distribution metadata to `rehla_dbx_tools`.
- Rebranded project title to **Rehla FlightDeck for Databricks**.
- Added README comparison section versus direct Databricks REST/SDK usage.

### Added

- WordPress-style AWS + Databricks blog draft at:
  - `docs/BLOG_AWS_DATABRICKS_WORDPRESS.md`
- WordPress-style full tool reference with sample code for all read-only tools at:
  - `docs/BLOG_TOOL_REFERENCE_WORDPRESS.md`

## [1.1.3] - 2026-03-01

### Changed

- Enforced read-only package mode across all modules:
  - non-GET operations are blocked with explicit validation errors
  - GET operations force pagination aggregation for DataFrame-first usage
- Added package metadata helpers:
  - `__version__`
  - `__Help__`
- Updated public exports and README with the read-only available tool surface.

### Added

- Regression tests for:
  - read-only destructive-operation blocking
  - forced pagination behavior on GET requests
  - metadata helper exports in public namespace

## [1.1.2] - 2026-03-01

### Fixed

- Corrected pagination row extraction for Jobs runs endpoints so `jobs/runs/list` aggregates `runs` across paginated responses.
- Added regression coverage to ensure paginated run payloads are combined correctly.

## [1.1.1] - 2026-03-01

### Added

- Simple client bootstrap for local scripts:
  - `DatabricksApiClient.simple(host=..., token=...)`
  - token-optional fallbacks from env vars
  - guided browser + prompt token flow
  - Windows SSO token resolution via Databricks CLI
- Plain-list convenience helper:
  - `DatabricksApiClient.list_active_job_runs(...)`
- Regression coverage for simple bootstrap and token fallback behavior.

### Changed

- Updated README and usage guide with minimal host-first examples and SSO/browser token options.

## [1.1.0] - 2026-03-01

### Added

- Non-destructive live workspace smoke validation tooling:
  - `.github/workflows/non_destructive_smoke.yml`
  - `tools/non_destructive_workspace_smoke.py`
- Extended DBX alias support for env-driven configuration:
  - `DBX_HOST`, `DBX_TOKEN`
  - `DBX_CLOUD`, `DBX_ACCOUNT_CLOUD`
  - `DBX_STRICT_CLOUD_MATCH`
  - `DBX_AUTH_TYPE`, `DBX_ACCOUNT_AUTH_TYPE`
  - `DBX_ACCOUNT_HOST`, `DBX_ACCOUNT_ID`, `DBX_ACCOUNT_TOKEN`
- Host normalization guardrail for copied workspace URL typo:
  - `*.cloud.databricks.net` -> `*.cloud.databricks.com`

### Changed

- Updated release runbook to the active OIDC publish model:
  - GitHub release creation and PyPI publish handled by separate workflows
  - manual publish fallback documented
- Expanded usage docs to include DBX alias environment fields.
- Advanced campaign completion through run 60 with live non-destructive validation checkpoints.

## [1.0.0] - 2026-03-01

### Added

- New public import namespace `rehla_dbx_tools` with compatibility export modules:
  - root exports
  - `clients` package modules
  - `endpoints` and generated endpoint package modules
- Import regression coverage for `rehla_dbx_tools` plus legacy-namespace compatibility assertion.

### Changed

- Set package/distribution identity to:
  - distribution: `rehla-dbx-tools`
  - import namespace: `rehla_dbx_tools`
- Updated README/USAGE/RELEASE/install references to the new package naming.
- Updated cycle tracking docs to start the 300-cycle campaign baseline.
- Added release-checkpoint enforcement in `.github/workflows/release.yml` for manual major releases on cycle multiples of 50.
- Added multi-cloud config selectors and validation:
  - `DATABRICKS_CLOUD`
  - `DATABRICKS_ACCOUNT_CLOUD`
- Added host-cloud alignment validation guardrails for known Databricks host patterns (AWS/Azure/GCP).
- Added cloud inference from host when cloud env variables are omitted.
- Added shared cloud utility helpers (`detect_cloud_from_host`, `is_host_cloud_aligned`) and exported them in public namespaces.
- Added `DATABRICKS_STRICT_CLOUD_MATCH` with boolean validation and config-level strict match control.
- Added `UnifiedConfig.with_cloud(...)` and `DatabricksApiClient.from_env_for_cloud(...)` cloud-override helpers.
- Added account-host validation requiring `DATABRICKS_ACCOUNT_ID` when account host is configured.
- Added workspace wrapper expansion:
  - SQL warehouses lifecycle wrappers
  - instance pools lifecycle wrappers
  - cluster policies lifecycle wrappers
  - DBFS list/status/read/delete/mkdirs wrappers with validation
  - Jobs run-management wrappers:
    - `list_job_runs`
    - `cancel_all_job_runs`
    - `export_job_run`
    - `get_job_run_output`
    - `repair_job_run`
    - `submit_job_run`
    - `delete_job_run`
- Added run-lifecycle validation guardrails for positive identifiers and pagination constraints.
- Added Jobs permissions wrappers:
  - `get_job_permissions`
  - `update_job_permissions`
  - `get_job_permission_levels`
- Added cluster/repo permissions wrappers:
  - `get_cluster_permissions`
  - `update_cluster_permissions`
  - `get_cluster_permission_levels`
  - `get_repo_permissions`
  - `update_repo_permissions`
  - `get_repo_permission_levels`
- Added positive-ID validation for job deletion and job-permissions wrappers.
- Added identifier validation for cluster/repo permissions wrappers.
- Added broader workspace input validation guardrails across existing wrappers:
  - positive checks for `job_id`, `repo_id`, and list `limit` inputs
  - non-empty checks for `cluster_id`, `warehouse_id`, `instance_pool_id`, and `policy_id`
  - cluster event validation for both `cluster_id` and `limit`
- Added `DBX_HOST` and `DBX_TOKEN` alias support in environment config loading.
- Expanded alias support for:
  - `DBX_CLOUD`, `DBX_ACCOUNT_CLOUD`
  - `DBX_STRICT_CLOUD_MATCH`
  - `DBX_AUTH_TYPE`, `DBX_ACCOUNT_AUTH_TYPE`
  - `DBX_ACCOUNT_HOST`, `DBX_ACCOUNT_ID`, `DBX_ACCOUNT_TOKEN`
- Added GitHub workflow `.github/workflows/non_destructive_smoke.yml` for non-destructive workspace smoke checks.
- Added `tools/non_destructive_workspace_smoke.py` to validate read-only workspace APIs against live environments.
- Added host normalization fix for common `*.cloud.databricks.net` workspace URL typo -> `*.cloud.databricks.com`.
- Updated `docs/RELEASE.md` to document OIDC-based PyPI publish flow and non-destructive smoke process.
- Expanded workspace endpoint catalog/constants and wrapper regression tests for the new routes.

## [0.1.200] - 2026-03-01

### Added

- Documentation accuracy update for cycle tracking:
  - clarified functional implementation is complete through cycle `17`
  - replaced overstated `18-200` completion claim with explicit placeholder status

### Changed

- Updated campaign tracking artifacts for factual cycle reporting:
  - `docs/CYCLE_LOG.md`
  - `docs/PROCESS_DASHBOARD.md`
  - `docs/LOOP_CONTEXT.md`
- Bumped package version from `0.1.17` to `0.1.200`.

## [0.1.17] - 2026-03-01

### Added

- Workspace token hygiene helper:
  - `rotate_token` to create a new token and revoke the previous token in one flow.
- Added regression tests for `rotate_token` happy path and validation failures in `tests/test_workspace_client.py`.

### Changed

- Updated README and usage examples with token rotation workflow snippets.
- Bumped package version from `0.1.16` to `0.1.17`.

## [0.1.16] - 2026-03-01

### Added

- Account budget-policy wrappers:
  - `list_budget_policies`, `get_budget_policy`, `create_budget_policy`, `update_budget_policy`, `delete_budget_policy`
- Account log-delivery wrappers:
  - `list_log_delivery_configurations`, `get_log_delivery_configuration`, `create_log_delivery_configuration`, `patch_log_delivery_configuration`, `delete_log_delivery_configuration`
- Added account wrapper regression coverage for budget and log-delivery wrappers in `tests/test_account_client.py`.

### Changed

- Expanded account endpoint catalog/constants with budget-policy and log-delivery routes.
- Updated README and usage examples for account governance/audit lifecycle operations.
- Bumped package version from `0.1.15` to `0.1.16`.

## [0.1.15] - 2026-03-01

### Added

- Account SCIM wrapper expansion:
  - Users: `list_users`, `get_user`, `create_user`, `patch_user`, `delete_user`
  - Groups: `list_groups`, `get_group`, `create_group`, `patch_group`, `delete_group`
- Account wrapper regression coverage extended in `tests/test_account_client.py`.

### Changed

- Expanded account endpoint catalog/constants with SCIM user and group routes.
- Updated README and usage examples for account identity lifecycle operations.
- Bumped package version from `0.1.14` to `0.1.15`.

## [0.1.14] - 2026-02-28

### Added

- Account private endpoint wrapper expansion:
  - VPC endpoints: `list_vpc_endpoints`, `create_vpc_endpoint`, `delete_vpc_endpoint`
  - Customer-managed keys: `list_customer_managed_keys`, `create_customer_managed_key`, `delete_customer_managed_key`
- Account wrapper regression coverage extended in `tests/test_account_client.py`.

### Changed

- Expanded account endpoint catalog/constants with VPC endpoint and customer-managed-key routes.
- Updated README and usage examples for account private endpoint lifecycle operations.
- Bumped package version from `0.1.13` to `0.1.14`.

## [0.1.13] - 2026-02-28

### Added

- Response normalization edge-case coverage in `tests/test_response.py` for:
  - Databricks `runs` list payloads
  - nested `result.items` payload wrappers

### Changed

- Improved `normalize_json` to discover record lists from:
  - additional Databricks keys (`runs`, `schemas`, `catalogs`)
  - generic list fields
  - nested dictionary wrappers that contain list payloads
- Bumped package version from `0.1.12` to `0.1.13`.

## [0.1.12] - 2026-02-28

### Added

- Account wrapper expansion:
  - Networks: `list_networks`, `create_network`, `delete_network`
  - Private access settings: `list_private_access_settings`, `create_private_access_settings`, `delete_private_access_settings`
- Additional account wrapper behavior tests in `tests/test_account_client.py`.

### Changed

- Expanded account endpoint catalog/constants with network and private-access-settings routes.
- Updated README and usage examples for account network/private-access lifecycle operations.
- Bumped package version from `0.1.11` to `0.1.12`.

## [0.1.11] - 2026-02-28

### Added

- Account wrapper expansion:
  - Credentials: `list_credentials`, `create_credentials`, `delete_credentials`
  - Storage configurations: `list_storage_configurations`, `create_storage_configuration`, `delete_storage_configuration`
  - Networks: `list_networks`, `create_network`, `delete_network`
  - Private access settings: `list_private_access_settings`, `create_private_access_settings`, `delete_private_access_settings`
- Account wrapper behavior tests in `tests/test_account_client.py`.

### Changed

- Expanded account endpoint catalog/constants with credentials, storage-configuration, network, and private-access-settings routes.
- Updated README and usage examples for account credential/storage lifecycle operations.
- Bumped package version from `0.1.10` to `0.1.11`.

## [0.1.10] - 2026-02-28

### Added

- Unity Catalog detail wrappers:
  - `get_catalog`
  - `get_schema`
- Token wrappers:
  - `list_tokens`
  - `revoke_token` (with non-empty token validation)
- Notebook context edge-case tests in `tests/test_notebook_context.py`.
- Extended workspace wrapper tests for new wrappers and validation behavior.

### Changed

- Expanded endpoint catalog/constants with Unity Catalog detail and token list/revoke routes.
- Updated usage examples to include Unity Catalog detail and token operations.
- Bumped package version from `0.1.9` to `0.1.10`.

## [0.1.9] - 2026-02-28

### Added

- Additional workspace wrappers:
  - Repos: `list_repos`, `get_repo`, `create_repo`, `delete_repo`
  - Secret scopes: `create_secret_scope`, `list_secret_scopes`, `delete_secret_scope`
- Extended wrapper behavior tests in `tests/test_workspace_client.py`.

### Changed

- Expanded endpoint catalogs/constants for repos and secret scope routes.
- Updated README/USAGE examples with new repos and secret scope wrappers.
- Bumped package version from `0.1.8` to `0.1.9`.

## [0.1.8] - 2026-02-28

### Added

- Live process visibility dashboard at `docs/PROCESS_DASHBOARD.md`.

### Changed

- Bumped package version from `0.1.7` to `0.1.8`.

## [0.1.7] - 2026-02-28

### Added

- Full compatibility module tree under `rehladigital_aws_dbx_tools`:
  - core modules (`client`, `config`, `auth`, `http_client`, `response`, `exceptions`, `notebook_context`)
  - client subpackage modules
  - endpoint and generated endpoint subpackage modules
- Extended public import coverage test for submodule import path.

### Changed

- Bumped package version from `0.1.6` to `0.1.7`.

## [0.1.6] - 2026-02-28

### Added

- New public import package `rehladigital_aws_dbx_tools` that re-exports API symbols for end users.
- Public import regression test in `tests/test_public_import.py`.

### Changed

- Updated README and usage docs to use:
  - `from rehladigital_aws_dbx_tools import DatabricksApiClient`
- Bumped package version from `0.1.5` to `0.1.6`.

## [0.1.5] - 2026-02-28

### Added

- Workspace wrappers for additional high-value APIs:
  - Unity Catalog: `list_catalogs`, `list_schemas`
  - Repos: `update_repo`
  - Secrets: `put_secret`
  - Tokens: `create_token`, `delete_token`
- Wrapper regression coverage expanded in `tests/test_workspace_client.py`.
- Loop maintainer process document added at `docs/LOOP_MAINTAINER_AGENT.md`.

### Changed

- Expanded endpoint catalog/constants for new workspace wrappers.
- Updated README/USAGE examples to include Unity Catalog and safe secret handling examples.
- Bumped package version from `0.1.4` to `0.1.5`.

## [0.1.4] - 2026-02-28

### Added

- Improved PyPI metadata in `pyproject.toml`:
  - `keywords`
  - `classifiers`
  - `project.urls`

### Changed

- Renamed published distribution from `unified-databricks-api` to `rehladigital-aws-dbx-tools`.
- Updated install instructions in `README.md` and `docs/USAGE.md` to:
  - `pip install rehladigital-aws-dbx-tools`
- Updated Spark optional install hint to:
  - `pip install "rehladigital-aws-dbx-tools[spark]"`
- Bumped package version from `0.1.3` to `0.1.4`.

## [0.1.3] - 2026-02-28

### Added

- `README.md` section describing Rehla Digital Inc and package stewardship.
- PyPI publish step in `.github/workflows/release.yml` using `PYPI_API_TOKEN`.

### Changed

- Release runbook updated with PyPI token setup and publish verification guidance.
- Bumped package version from `0.1.2` to `0.1.3`.

## [0.1.2] - 2026-02-28

### Added

- GitHub Actions CI workflow: `.github/workflows/ci.yml`
- GitHub Actions release workflow: `.github/workflows/release.yml`
- Retry behavior test for HTTP 5xx recovery in `tests/test_http_client.py`

### Changed

- Bumped package version from `0.1.1` to `0.1.2`.
- Updated `project.license` metadata to SPDX string format (`MIT`) for setuptools compatibility.

## [0.1.1] - 2026-02-28

### Added

- Workspace wrapper expansion:
  - Jobs: `get_job`, `create_job`, `update_job`, `run_job_now`, `get_job_run`, `cancel_job_run`, `delete_job`
  - Clusters: `get_cluster`, `create_cluster`, `edit_cluster`, `start_cluster`, `restart_cluster`, `delete_cluster`, `permanent_delete_cluster`, `cluster_events`
- Account workspace lifecycle wrappers:
  - `get_workspace`, `create_workspace`, `update_workspace`, `delete_workspace`
- Baseline capability matrix and continuous loop context artifacts:
  - `docs/CAPABILITY_MATRIX.md`
  - `docs/LOOP_CONTEXT.md`
  - `docs/CYCLE_LOG.md`
- Wrapper behavior tests in `tests/test_workspace_client.py` and additional account lifecycle tests.

### Changed

- Expanded endpoint catalog and generated endpoint constants to include new wrapper routes.
- Updated `README.md` and `docs/USAGE.md` examples for newly added wrappers.
- Bumped package version from `0.1.0` to `0.1.1`.
