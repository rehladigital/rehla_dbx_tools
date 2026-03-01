from unittest.mock import patch

import pytest

from databricks_api.clients.workspace import WorkspaceClient
from databricks_api.config import AuthConfig, WorkspaceConfig
from databricks_api.exceptions import ValidationError


def _workspace_client() -> WorkspaceClient:
    return WorkspaceClient(
        WorkspaceConfig(
            host="https://dbc-test.cloud.databricks.com",
            auth=AuthConfig(token="token"),
        )
    )


def test_jobs_wrappers_route_expected_methods_and_payloads():
    client = _workspace_client()

    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.get_job(123)
        assert request_versioned.call_args.args == ("GET", "jobs")
        assert request_versioned.call_args.kwargs["endpoint"] == "get"
        assert request_versioned.call_args.kwargs["params"] == {"job_id": 123}

        client.create_job({"name": "daily-job"})
        assert request_versioned.call_args.args == ("POST", "jobs")
        assert request_versioned.call_args.kwargs["endpoint"] == "create"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "daily-job"}

        client.update_job(123, {"name": "daily-job-v2"})
        assert request_versioned.call_args.args == ("POST", "jobs")
        assert request_versioned.call_args.kwargs["endpoint"] == "reset"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "job_id": 123,
            "new_settings": {"name": "daily-job-v2"},
        }

        client.run_job_now(123, notebook_params={"date": "2026-02-28"})
        assert request_versioned.call_args.kwargs["endpoint"] == "run-now"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "job_id": 123,
            "notebook_params": {"date": "2026-02-28"},
        }

        client.get_job_run(987)
        assert request_versioned.call_args.kwargs["endpoint"] == "runs/get"
        assert request_versioned.call_args.kwargs["params"] == {"run_id": 987}

        client.cancel_job_run(987)
        assert request_versioned.call_args.kwargs["endpoint"] == "runs/cancel"
        assert request_versioned.call_args.kwargs["json_body"] == {"run_id": 987}

        client.list_job_runs(job_id=123, active_only=True, offset=10, limit=5)
        assert request_versioned.call_args.args == ("GET", "jobs")
        assert request_versioned.call_args.kwargs["endpoint"] == "runs/list"
        assert request_versioned.call_args.kwargs["params"] == {
            "job_id": 123,
            "active_only": True,
            "offset": 10,
            "limit": 5,
        }
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.cancel_all_job_runs(123, all_queued_runs=True)
        assert request_versioned.call_args.args == ("POST", "jobs")
        assert request_versioned.call_args.kwargs["endpoint"] == "runs/cancel-all"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "job_id": 123,
            "all_queued_runs": True,
        }

        client.export_job_run(987, views_to_export="CODE")
        assert request_versioned.call_args.args == ("GET", "jobs")
        assert request_versioned.call_args.kwargs["endpoint"] == "runs/export"
        assert request_versioned.call_args.kwargs["params"] == {"run_id": 987, "views_to_export": "CODE"}

        client.get_job_run_output(987)
        assert request_versioned.call_args.kwargs["endpoint"] == "runs/get-output"
        assert request_versioned.call_args.kwargs["params"] == {"run_id": 987}

        client.submit_job_run({"run_name": "ad-hoc-job"})
        assert request_versioned.call_args.args == ("POST", "jobs")
        assert request_versioned.call_args.kwargs["endpoint"] == "runs/submit"
        assert request_versioned.call_args.kwargs["json_body"] == {"run_name": "ad-hoc-job"}

        client.delete_job_run(987)
        assert request_versioned.call_args.kwargs["endpoint"] == "runs/delete"
        assert request_versioned.call_args.kwargs["json_body"] == {"run_id": 987}

        client.repair_job_run(987, rerun_all_failed_tasks=True, latest_repair_id=2)
        assert request_versioned.call_args.kwargs["endpoint"] == "runs/repair"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "run_id": 987,
            "rerun_all_failed_tasks": True,
            "latest_repair_id": 2,
        }

        client.delete_job(123)
        assert request_versioned.call_args.kwargs["endpoint"] == "delete"
        assert request_versioned.call_args.kwargs["json_body"] == {"job_id": 123}

        client.get_job_permissions(123)
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "jobs/123"

        client.update_job_permissions(
            123,
            [{"user_name": "user@example.com", "permission_level": "CAN_MANAGE"}],
        )
        assert request_versioned.call_args.args == ("PATCH", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "jobs/123"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "access_control_list": [{"user_name": "user@example.com", "permission_level": "CAN_MANAGE"}]
        }

        client.set_job_permissions(
            123,
            [{"group_name": "admins", "permission_level": "CAN_MANAGE"}],
        )
        assert request_versioned.call_args.args == ("PUT", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "jobs/123"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "access_control_list": [{"group_name": "admins", "permission_level": "CAN_MANAGE"}]
        }

        client.get_job_permission_levels(123)
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "jobs/123/permissionLevels"

        client.run_job_now(321)
        assert request_versioned.call_args.kwargs["json_body"] == {"job_id": 321}

        client.list_job_runs()
        assert request_versioned.call_args.kwargs["params"] == {"limit": 25}

        client.export_job_run(123)
        assert request_versioned.call_args.kwargs["params"] == {"run_id": 123}

        client.repair_job_run(456)
        assert request_versioned.call_args.kwargs["json_body"] == {
            "run_id": 456,
            "rerun_all_failed_tasks": False,
        }

        client.submit_job_run({"tasks": [{"task_key": "one-off"}]})
        assert request_versioned.call_args.kwargs["json_body"] == {"tasks": [{"task_key": "one-off"}]}


def test_job_run_wrappers_validate_identifiers_and_pagination_inputs():
    client = _workspace_client()
    with pytest.raises(ValidationError):
        client.get_job_run(0)
    with pytest.raises(ValidationError):
        client.cancel_job_run(-1)
    with pytest.raises(ValidationError):
        client.list_job_runs(job_id=0)
    with pytest.raises(ValidationError):
        client.list_job_runs(offset=-1)
    with pytest.raises(ValidationError):
        client.list_job_runs(limit=0)
    with pytest.raises(ValidationError):
        client.cancel_all_job_runs(0)
    with pytest.raises(ValidationError):
        client.export_job_run(0)
    with pytest.raises(ValidationError):
        client.get_job_run_output(0)
    with pytest.raises(ValidationError):
        client.delete_job_run(0)
    with pytest.raises(ValidationError):
        client.repair_job_run(0)
    with pytest.raises(ValidationError):
        client.repair_job_run(1, latest_repair_id=0)
    with pytest.raises(ValidationError):
        client.delete_job(0)
    with pytest.raises(ValidationError):
        client.get_job_permissions(0)
    with pytest.raises(ValidationError):
        client.update_job_permissions(0, [])
    with pytest.raises(ValidationError):
        client.set_job_permissions(0, [])
    with pytest.raises(ValidationError):
        client.get_job_permission_levels(0)
    with pytest.raises(ValidationError):
        client.get_cluster_permissions("")
    with pytest.raises(ValidationError):
        client.update_cluster_permissions(" ", [])
    with pytest.raises(ValidationError):
        client.get_cluster_permission_levels("")
    with pytest.raises(ValidationError):
        client.get_repo_permissions(0)
    with pytest.raises(ValidationError):
        client.update_repo_permissions(0, [])
    with pytest.raises(ValidationError):
        client.get_repo_permission_levels(0)
    with pytest.raises(ValidationError):
        client.list_jobs(limit=0)
    with pytest.raises(ValidationError):
        client.get_job(0)
    with pytest.raises(ValidationError):
        client.update_job(0, {})
    with pytest.raises(ValidationError):
        client.run_job_now(0)
    with pytest.raises(ValidationError):
        client.get_cluster("")
    with pytest.raises(ValidationError):
        client.edit_cluster("", {})
    with pytest.raises(ValidationError):
        client.start_cluster("")
    with pytest.raises(ValidationError):
        client.restart_cluster("")
    with pytest.raises(ValidationError):
        client.delete_cluster("")
    with pytest.raises(ValidationError):
        client.permanent_delete_cluster("")
    with pytest.raises(ValidationError):
        client.cluster_events("", limit=1)
    with pytest.raises(ValidationError):
        client.cluster_events("c-1", limit=0)


def test_library_wrappers_route_expected_calls_and_validation():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.get_all_library_statuses()
        assert request_versioned.call_args.args == ("GET", "libraries")
        assert request_versioned.call_args.kwargs["endpoint"] == "all-cluster-statuses"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.get_library_status("cluster-1")
        assert request_versioned.call_args.args == ("GET", "libraries")
        assert request_versioned.call_args.kwargs["endpoint"] == "cluster-status"
        assert request_versioned.call_args.kwargs["params"] == {"cluster_id": "cluster-1"}

        libs = [{"pypi": {"package": "pandas==2.3.3"}}]
        client.install_libraries("cluster-1", libs)
        assert request_versioned.call_args.args == ("POST", "libraries")
        assert request_versioned.call_args.kwargs["endpoint"] == "install"
        assert request_versioned.call_args.kwargs["json_body"] == {"cluster_id": "cluster-1", "libraries": libs}

        client.uninstall_libraries("cluster-1", libs)
        assert request_versioned.call_args.args == ("POST", "libraries")
        assert request_versioned.call_args.kwargs["endpoint"] == "uninstall"
        assert request_versioned.call_args.kwargs["json_body"] == {"cluster_id": "cluster-1", "libraries": libs}

    with pytest.raises(ValidationError):
        client.get_library_status("")
    with pytest.raises(ValidationError):
        client.install_libraries("", [])
    with pytest.raises(ValidationError):
        client.uninstall_libraries("", [])


def test_networking_and_notifications_wrappers_route_expected_calls_and_validation():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_ip_access_lists()
        assert request_versioned.call_args.args == ("GET", "ip-access-lists")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_ip_access_list({"label": "corp-office", "ip_addresses": ["10.0.0.0/24"], "enabled": True})
        assert request_versioned.call_args.args == ("POST", "ip-access-lists")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {
            "label": "corp-office",
            "ip_addresses": ["10.0.0.0/24"],
            "enabled": True,
        }

        client.get_ip_access_list("list-1")
        assert request_versioned.call_args.args == ("GET", "ip-access-lists")
        assert request_versioned.call_args.kwargs["endpoint"] == "list-1"

        client.replace_ip_access_list("list-1", {"label": "corp-office", "ip_addresses": ["10.1.0.0/24"]})
        assert request_versioned.call_args.args == ("PUT", "ip-access-lists")
        assert request_versioned.call_args.kwargs["endpoint"] == "list-1"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "label": "corp-office",
            "ip_addresses": ["10.1.0.0/24"],
        }

        client.update_ip_access_list("list-1", {"enabled": False})
        assert request_versioned.call_args.args == ("PATCH", "ip-access-lists")
        assert request_versioned.call_args.kwargs["endpoint"] == "list-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"enabled": False}

        client.delete_ip_access_list("list-1")
        assert request_versioned.call_args.args == ("DELETE", "ip-access-lists")
        assert request_versioned.call_args.kwargs["endpoint"] == "list-1"

        client.list_notification_destinations()
        assert request_versioned.call_args.args == ("GET", "notification-destinations")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_notification_destination({"display_name": "Slack Alerts"})
        assert request_versioned.call_args.args == ("POST", "notification-destinations")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"display_name": "Slack Alerts"}

        client.get_notification_destination("dest-1")
        assert request_versioned.call_args.args == ("GET", "notification-destinations")
        assert request_versioned.call_args.kwargs["endpoint"] == "dest-1"

        client.update_notification_destination("dest-1", {"display_name": "Slack Alerts v2"})
        assert request_versioned.call_args.args == ("PATCH", "notification-destinations")
        assert request_versioned.call_args.kwargs["endpoint"] == "dest-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"display_name": "Slack Alerts v2"}

        client.delete_notification_destination("dest-1")
        assert request_versioned.call_args.args == ("DELETE", "notification-destinations")
        assert request_versioned.call_args.kwargs["endpoint"] == "dest-1"

    with pytest.raises(ValidationError):
        client.get_ip_access_list("")
    with pytest.raises(ValidationError):
        client.replace_ip_access_list("", {})
    with pytest.raises(ValidationError):
        client.update_ip_access_list("", {})
    with pytest.raises(ValidationError):
        client.delete_ip_access_list("")
    with pytest.raises(ValidationError):
        client.get_notification_destination("")
    with pytest.raises(ValidationError):
        client.update_notification_destination("", {})
    with pytest.raises(ValidationError):
        client.delete_notification_destination("")


def test_pipelines_and_query_history_wrappers_route_expected_calls_and_validation():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.get_pipeline_permissions("pipe-1")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipelines/pipe-1"

        acl = [{"group_name": "admins", "permission_level": "CAN_MANAGE"}]
        client.set_pipeline_permissions("pipe-1", acl)
        assert request_versioned.call_args.args == ("PUT", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipelines/pipe-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"access_control_list": acl}

        client.update_pipeline_permissions("pipe-1", acl)
        assert request_versioned.call_args.args == ("PATCH", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipelines/pipe-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"access_control_list": acl}

        client.get_pipeline_permission_levels("pipe-1")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipelines/pipe-1/permissionLevels"

        client.list_pipelines()
        assert request_versioned.call_args.args == ("GET", "pipelines")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_pipeline({"name": "daily-dlt"})
        assert request_versioned.call_args.args == ("POST", "pipelines")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "daily-dlt"}

        client.get_pipeline("pipe-1")
        assert request_versioned.call_args.args == ("GET", "pipelines")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipe-1"

        client.edit_pipeline("pipe-1", {"name": "daily-dlt-v2"})
        assert request_versioned.call_args.args == ("PUT", "pipelines")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipe-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "daily-dlt-v2"}

        client.delete_pipeline("pipe-1")
        assert request_versioned.call_args.args == ("DELETE", "pipelines")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipe-1"

        client.start_pipeline("pipe-1", {"full_refresh": True})
        assert request_versioned.call_args.args == ("POST", "pipelines")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipe-1/updates"
        assert request_versioned.call_args.kwargs["json_body"] == {"full_refresh": True}

        client.stop_pipeline("pipe-1")
        assert request_versioned.call_args.args == ("POST", "pipelines")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipe-1/stop"

        client.list_pipeline_events("pipe-1")
        assert request_versioned.call_args.args == ("GET", "pipelines")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipe-1/events"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.list_pipeline_updates("pipe-1")
        assert request_versioned.call_args.args == ("GET", "pipelines")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipe-1/updates"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.get_pipeline_update("pipe-1", "update-1")
        assert request_versioned.call_args.args == ("GET", "pipelines")
        assert request_versioned.call_args.kwargs["endpoint"] == "pipe-1/updates/update-1"

        client.list_query_history(max_results=100)
        assert request_versioned.call_args.args == ("GET", "sql/history/queries")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["params"] == {"max_results": 100}
        assert request_versioned.call_args.kwargs["paginate"] is True

    with pytest.raises(ValidationError):
        client.get_pipeline_permissions("")
    with pytest.raises(ValidationError):
        client.set_pipeline_permissions("", [])
    with pytest.raises(ValidationError):
        client.update_pipeline_permissions("", [])
    with pytest.raises(ValidationError):
        client.get_pipeline_permission_levels("")
    with pytest.raises(ValidationError):
        client.get_pipeline("")
    with pytest.raises(ValidationError):
        client.edit_pipeline("", {})
    with pytest.raises(ValidationError):
        client.delete_pipeline("")
    with pytest.raises(ValidationError):
        client.start_pipeline("")
    with pytest.raises(ValidationError):
        client.stop_pipeline("")
    with pytest.raises(ValidationError):
        client.list_pipeline_events("")
    with pytest.raises(ValidationError):
        client.list_pipeline_updates("")
    with pytest.raises(ValidationError):
        client.get_pipeline_update("", "update-1")
    with pytest.raises(ValidationError):
        client.get_pipeline_update("pipe-1", "")
    with pytest.raises(ValidationError):
        client.list_query_history(max_results=0)


def test_marketplace_and_model_serving_wrappers_route_expected_calls_and_validation():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.get_serving_endpoint_permissions("fraud-model")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "serving-endpoints/fraud-model"

        acl = [{"group_name": "ml-team", "permission_level": "CAN_QUERY"}]
        client.set_serving_endpoint_permissions("fraud-model", acl)
        assert request_versioned.call_args.args == ("PUT", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "serving-endpoints/fraud-model"
        assert request_versioned.call_args.kwargs["json_body"] == {"access_control_list": acl}

        client.update_serving_endpoint_permissions("fraud-model", acl)
        assert request_versioned.call_args.args == ("PATCH", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "serving-endpoints/fraud-model"
        assert request_versioned.call_args.kwargs["json_body"] == {"access_control_list": acl}

        client.get_serving_endpoint_permission_levels("fraud-model")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "serving-endpoints/fraud-model/permissionLevels"

        client.list_serving_endpoints()
        assert request_versioned.call_args.args == ("GET", "serving-endpoints")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_serving_endpoint({"name": "fraud-model"})
        assert request_versioned.call_args.args == ("POST", "serving-endpoints")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "fraud-model"}

        client.get_serving_endpoint("fraud-model")
        assert request_versioned.call_args.args == ("GET", "serving-endpoints")
        assert request_versioned.call_args.kwargs["endpoint"] == "fraud-model"

        client.update_serving_endpoint_config("fraud-model", {"served_models": []})
        assert request_versioned.call_args.args == ("PUT", "serving-endpoints")
        assert request_versioned.call_args.kwargs["endpoint"] == "fraud-model/config"
        assert request_versioned.call_args.kwargs["json_body"] == {"served_models": []}

        client.delete_serving_endpoint("fraud-model")
        assert request_versioned.call_args.args == ("DELETE", "serving-endpoints")
        assert request_versioned.call_args.kwargs["endpoint"] == "fraud-model"

        client.query_serving_endpoint("fraud-model", {"dataframe_split": {"columns": ["x"], "data": [[1.0]]}})
        assert request_versioned.call_args.args == ("POST", "serving-endpoints")
        assert request_versioned.call_args.kwargs["endpoint"] == "fraud-model/invocations"

        client.list_marketplace_listings()
        assert request_versioned.call_args.args == ("GET", "marketplace-consumer/listings")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.get_marketplace_listing("listing-1")
        assert request_versioned.call_args.args == ("GET", "marketplace-consumer/listings")
        assert request_versioned.call_args.kwargs["endpoint"] == "listing-1"

        client.search_marketplace_listings({"query": "llm"})
        assert request_versioned.call_args.args == ("POST", "marketplace-consumer/listings")
        assert request_versioned.call_args.kwargs["endpoint"] == "search"
        assert request_versioned.call_args.kwargs["json_body"] == {"query": "llm"}

        client.list_marketplace_installations()
        assert request_versioned.call_args.args == ("GET", "marketplace-consumer/installations")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.install_marketplace_listing({"listing_id": "listing-1"})
        assert request_versioned.call_args.args == ("POST", "marketplace-consumer/installations")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"listing_id": "listing-1"}

        client.uninstall_marketplace_installation("inst-1")
        assert request_versioned.call_args.args == ("DELETE", "marketplace-consumer/installations")
        assert request_versioned.call_args.kwargs["endpoint"] == "inst-1"

    with pytest.raises(ValidationError):
        client.get_serving_endpoint_permissions("")
    with pytest.raises(ValidationError):
        client.set_serving_endpoint_permissions("", [])
    with pytest.raises(ValidationError):
        client.update_serving_endpoint_permissions("", [])
    with pytest.raises(ValidationError):
        client.get_serving_endpoint_permission_levels("")
    with pytest.raises(ValidationError):
        client.get_serving_endpoint("")
    with pytest.raises(ValidationError):
        client.update_serving_endpoint_config("", {})
    with pytest.raises(ValidationError):
        client.delete_serving_endpoint("")
    with pytest.raises(ValidationError):
        client.query_serving_endpoint("", {})
    with pytest.raises(ValidationError):
        client.get_marketplace_listing("")
    with pytest.raises(ValidationError):
        client.uninstall_marketplace_installation("")


def test_genie_and_global_init_script_wrappers_route_expected_calls_and_validation():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_genie_spaces()
        assert request_versioned.call_args.args == ("GET", "genie/spaces")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_genie_space({"display_name": "Ops Analyst"})
        assert request_versioned.call_args.args == ("POST", "genie/spaces")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"display_name": "Ops Analyst"}

        client.get_genie_space("space-1")
        assert request_versioned.call_args.args == ("GET", "genie/spaces")
        assert request_versioned.call_args.kwargs["endpoint"] == "space-1"

        client.update_genie_space("space-1", {"display_name": "Ops Analyst V2"})
        assert request_versioned.call_args.args == ("PATCH", "genie/spaces")
        assert request_versioned.call_args.kwargs["endpoint"] == "space-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"display_name": "Ops Analyst V2"}

        client.delete_genie_space("space-1")
        assert request_versioned.call_args.args == ("DELETE", "genie/spaces")
        assert request_versioned.call_args.kwargs["endpoint"] == "space-1"

        client.list_global_init_scripts()
        assert request_versioned.call_args.args == ("GET", "global-init-scripts")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_global_init_script({"name": "setup-env", "enabled": True})
        assert request_versioned.call_args.args == ("POST", "global-init-scripts")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "setup-env", "enabled": True}

        client.get_global_init_script("script-1")
        assert request_versioned.call_args.args == ("GET", "global-init-scripts")
        assert request_versioned.call_args.kwargs["endpoint"] == "script-1"

        client.update_global_init_script("script-1", {"enabled": False})
        assert request_versioned.call_args.args == ("PATCH", "global-init-scripts")
        assert request_versioned.call_args.kwargs["endpoint"] == "script-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"enabled": False}

        client.delete_global_init_script("script-1")
        assert request_versioned.call_args.args == ("DELETE", "global-init-scripts")
        assert request_versioned.call_args.kwargs["endpoint"] == "script-1"

    with pytest.raises(ValidationError):
        client.get_genie_space("")
    with pytest.raises(ValidationError):
        client.update_genie_space("", {})
    with pytest.raises(ValidationError):
        client.delete_genie_space("")
    with pytest.raises(ValidationError):
        client.get_global_init_script("")
    with pytest.raises(ValidationError):
        client.update_global_init_script("", {})
    with pytest.raises(ValidationError):
        client.delete_global_init_script("")


def test_settings_and_tags_wrappers_route_expected_calls_and_validation():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_setting_keys_metadata()
        assert request_versioned.call_args.args == ("GET", "settings-v2")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.get_workspace_setting("sql_results_download")
        assert request_versioned.call_args.args == ("GET", "settings-v2")
        assert request_versioned.call_args.kwargs["endpoint"] == "sql_results_download"

        client.update_workspace_setting("sql_results_download", {"setting": {"enabled": False}})
        assert request_versioned.call_args.args == ("PATCH", "settings-v2")
        assert request_versioned.call_args.kwargs["endpoint"] == "sql_results_download"
        assert request_versioned.call_args.kwargs["json_body"] == {"setting": {"enabled": False}}

        client.get_workspace_conf(["enableWorkspaceAcls", "maxTokenLifetimeDays"])
        assert request_versioned.call_args.args == ("GET", "workspace-conf")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["params"] == {"keys": "enableWorkspaceAcls,maxTokenLifetimeDays"}

        client.set_workspace_conf({"enableWorkspaceAcls": "true"})
        assert request_versioned.call_args.args == ("PATCH", "workspace-conf")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"custom_config": {"enableWorkspaceAcls": "true"}}

        client.list_tag_policies()
        assert request_versioned.call_args.args == ("GET", "tags/policies")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_tag_policy({"name": "pii-policy"})
        assert request_versioned.call_args.args == ("POST", "tags/policies")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "pii-policy"}

        client.get_tag_policy("policy-1")
        assert request_versioned.call_args.args == ("GET", "tags/policies")
        assert request_versioned.call_args.kwargs["endpoint"] == "policy-1"

        client.update_tag_policy("policy-1", {"name": "pii-policy-v2"})
        assert request_versioned.call_args.args == ("PATCH", "tags/policies")
        assert request_versioned.call_args.kwargs["endpoint"] == "policy-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "pii-policy-v2"}

        client.delete_tag_policy("policy-1")
        assert request_versioned.call_args.args == ("DELETE", "tags/policies")
        assert request_versioned.call_args.kwargs["endpoint"] == "policy-1"

        client.list_tag_assignments("clusters", "cluster-1")
        assert request_versioned.call_args.args == ("GET", "tags/assignments")
        assert request_versioned.call_args.kwargs["endpoint"] == "clusters/cluster-1"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_tag_assignment("clusters", "cluster-1", {"tag_policy_id": "policy-1"})
        assert request_versioned.call_args.args == ("POST", "tags/assignments")
        assert request_versioned.call_args.kwargs["endpoint"] == "clusters/cluster-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"tag_policy_id": "policy-1"}

        client.get_tag_assignment("clusters", "cluster-1", "assignment-1")
        assert request_versioned.call_args.args == ("GET", "tags/assignments")
        assert request_versioned.call_args.kwargs["endpoint"] == "clusters/cluster-1/assignment-1"

        client.update_tag_assignment("clusters", "cluster-1", "assignment-1", {"tag_policy_id": "policy-2"})
        assert request_versioned.call_args.args == ("PATCH", "tags/assignments")
        assert request_versioned.call_args.kwargs["endpoint"] == "clusters/cluster-1/assignment-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"tag_policy_id": "policy-2"}

        client.delete_tag_assignment("clusters", "cluster-1", "assignment-1")
        assert request_versioned.call_args.args == ("DELETE", "tags/assignments")
        assert request_versioned.call_args.kwargs["endpoint"] == "clusters/cluster-1/assignment-1"

    with pytest.raises(ValidationError):
        client.get_workspace_setting("")
    with pytest.raises(ValidationError):
        client.update_workspace_setting("", {})
    with pytest.raises(ValidationError):
        client.get_tag_policy("")
    with pytest.raises(ValidationError):
        client.update_tag_policy("", {})
    with pytest.raises(ValidationError):
        client.delete_tag_policy("")
    with pytest.raises(ValidationError):
        client.list_tag_assignments("", "cluster-1")
    with pytest.raises(ValidationError):
        client.list_tag_assignments("clusters", "")
    with pytest.raises(ValidationError):
        client.get_tag_assignment("", "cluster-1", "assignment-1")
    with pytest.raises(ValidationError):
        client.get_tag_assignment("clusters", "", "assignment-1")
    with pytest.raises(ValidationError):
        client.get_tag_assignment("clusters", "cluster-1", "")
    with pytest.raises(ValidationError):
        client.update_tag_assignment("", "cluster-1", "assignment-1", {})
    with pytest.raises(ValidationError):
        client.update_tag_assignment("clusters", "", "assignment-1", {})
    with pytest.raises(ValidationError):
        client.update_tag_assignment("clusters", "cluster-1", "", {})
    with pytest.raises(ValidationError):
        client.delete_tag_assignment("", "cluster-1", "assignment-1")
    with pytest.raises(ValidationError):
        client.delete_tag_assignment("clusters", "", "assignment-1")
    with pytest.raises(ValidationError):
        client.delete_tag_assignment("clusters", "cluster-1", "")


def test_quality_monitor_and_postgres_wrappers_route_expected_calls_and_validation():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_quality_monitors()
        assert request_versioned.call_args.args == ("GET", "quality-monitor-v2/monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_quality_monitor({"table_name": "main.prod.sales"})
        assert request_versioned.call_args.args == ("POST", "quality-monitor-v2/monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"table_name": "main.prod.sales"}

        client.get_quality_monitor("qm-1")
        assert request_versioned.call_args.args == ("GET", "quality-monitor-v2/monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "qm-1"

        client.update_quality_monitor("qm-1", {"status": "DISABLED"})
        assert request_versioned.call_args.args == ("PATCH", "quality-monitor-v2/monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "qm-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"status": "DISABLED"}

        client.delete_quality_monitor("qm-1")
        assert request_versioned.call_args.args == ("DELETE", "quality-monitor-v2/monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "qm-1"

        client.list_postgres_projects()
        assert request_versioned.call_args.args == ("GET", "postgres/projects")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_postgres_project({"name": "analytics-db"})
        assert request_versioned.call_args.args == ("POST", "postgres/projects")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "analytics-db"}

        client.get_postgres_project("project-1")
        assert request_versioned.call_args.args == ("GET", "postgres/projects")
        assert request_versioned.call_args.kwargs["endpoint"] == "project-1"

        client.update_postgres_project("project-1", {"name": "analytics-db-v2"})
        assert request_versioned.call_args.args == ("PATCH", "postgres/projects")
        assert request_versioned.call_args.kwargs["endpoint"] == "project-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "analytics-db-v2"}

        client.delete_postgres_project("project-1")
        assert request_versioned.call_args.args == ("DELETE", "postgres/projects")
        assert request_versioned.call_args.kwargs["endpoint"] == "project-1"

        client.list_postgres_branches("project-1")
        assert request_versioned.call_args.args == ("GET", "postgres/projects")
        assert request_versioned.call_args.kwargs["endpoint"] == "project-1/branches"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_postgres_branch("project-1", {"name": "feature-branch"})
        assert request_versioned.call_args.args == ("POST", "postgres/projects")
        assert request_versioned.call_args.kwargs["endpoint"] == "project-1/branches"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "feature-branch"}

        client.get_postgres_branch("project-1", "branch-1")
        assert request_versioned.call_args.args == ("GET", "postgres/projects")
        assert request_versioned.call_args.kwargs["endpoint"] == "project-1/branches/branch-1"

        client.delete_postgres_branch("project-1", "branch-1")
        assert request_versioned.call_args.args == ("DELETE", "postgres/projects")
        assert request_versioned.call_args.kwargs["endpoint"] == "project-1/branches/branch-1"

    with pytest.raises(ValidationError):
        client.get_quality_monitor("")
    with pytest.raises(ValidationError):
        client.update_quality_monitor("", {})
    with pytest.raises(ValidationError):
        client.delete_quality_monitor("")
    with pytest.raises(ValidationError):
        client.get_postgres_project("")
    with pytest.raises(ValidationError):
        client.update_postgres_project("", {})
    with pytest.raises(ValidationError):
        client.delete_postgres_project("")
    with pytest.raises(ValidationError):
        client.list_postgres_branches("")
    with pytest.raises(ValidationError):
        client.create_postgres_branch("", {})
    with pytest.raises(ValidationError):
        client.get_postgres_branch("", "branch-1")
    with pytest.raises(ValidationError):
        client.get_postgres_branch("project-1", "")
    with pytest.raises(ValidationError):
        client.delete_postgres_branch("", "branch-1")
    with pytest.raises(ValidationError):
        client.delete_postgres_branch("project-1", "")

    with pytest.raises(ValidationError):
        client.update_repo(0, branch="main")
    with pytest.raises(ValidationError):
        client.get_repo(0)
    with pytest.raises(ValidationError):
        client.delete_repo(0)
    with pytest.raises(ValidationError):
        client.get_sql_warehouse("")
    with pytest.raises(ValidationError):
        client.edit_sql_warehouse("", {})
    with pytest.raises(ValidationError):
        client.delete_sql_warehouse("")
    with pytest.raises(ValidationError):
        client.get_instance_pool("")
    with pytest.raises(ValidationError):
        client.edit_instance_pool("", {})
    with pytest.raises(ValidationError):
        client.delete_instance_pool("")
    with pytest.raises(ValidationError):
        client.get_cluster_policy("")
    with pytest.raises(ValidationError):
        client.edit_cluster_policy("", {})
    with pytest.raises(ValidationError):
        client.delete_cluster_policy("")


def test_cluster_wrappers_route_expected_methods_and_payloads():
    client = _workspace_client()

    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.get_cluster("c-1")
        assert request_versioned.call_args.args == ("GET", "clusters")
        assert request_versioned.call_args.kwargs["endpoint"] == "get"
        assert request_versioned.call_args.kwargs["params"] == {"cluster_id": "c-1"}

        client.create_cluster({"cluster_name": "etl-cluster"})
        assert request_versioned.call_args.kwargs["endpoint"] == "create"
        assert request_versioned.call_args.kwargs["json_body"] == {"cluster_name": "etl-cluster"}

        client.edit_cluster("c-1", {"num_workers": 3})
        assert request_versioned.call_args.kwargs["endpoint"] == "edit"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "cluster_id": "c-1",
            "num_workers": 3,
        }

        client.start_cluster("c-1")
        assert request_versioned.call_args.kwargs["endpoint"] == "start"
        assert request_versioned.call_args.kwargs["json_body"] == {"cluster_id": "c-1"}

        client.restart_cluster("c-1")
        assert request_versioned.call_args.kwargs["endpoint"] == "restart"
        assert request_versioned.call_args.kwargs["json_body"] == {"cluster_id": "c-1"}

        client.delete_cluster("c-1")
        assert request_versioned.call_args.kwargs["endpoint"] == "delete"
        assert request_versioned.call_args.kwargs["json_body"] == {"cluster_id": "c-1"}

        client.permanent_delete_cluster("c-1")
        assert request_versioned.call_args.kwargs["endpoint"] == "permanent-delete"
        assert request_versioned.call_args.kwargs["json_body"] == {"cluster_id": "c-1"}

        client.cluster_events("c-1", limit=20, page_token="tok-1")
        assert request_versioned.call_args.kwargs["endpoint"] == "events"
        assert request_versioned.call_args.kwargs["params"] == {
            "cluster_id": "c-1",
            "limit": 20,
            "page_token": "tok-1",
        }

        client.cluster_events("c-1")
        assert request_versioned.call_args.kwargs["params"] == {
            "cluster_id": "c-1",
            "limit": 50,
        }

        client.get_cluster_permissions("c-1")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "clusters/c-1"

        client.update_cluster_permissions(
            "c-1",
            [{"group_name": "admins", "permission_level": "CAN_MANAGE"}],
        )
        assert request_versioned.call_args.args == ("PATCH", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "clusters/c-1"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "access_control_list": [{"group_name": "admins", "permission_level": "CAN_MANAGE"}]
        }

        client.get_cluster_permission_levels("c-1")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "clusters/c-1/permissionLevels"


def test_generic_object_permission_wrappers_route_expected_methods_and_payloads():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.get_object_permissions("warehouses", "wh-1")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "warehouses/wh-1"

        acl = [{"group_name": "data-team", "permission_level": "CAN_USE"}]
        client.set_object_permissions("warehouses", "wh-1", acl)
        assert request_versioned.call_args.args == ("PUT", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "warehouses/wh-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"access_control_list": acl}

        client.update_object_permissions("warehouses", "wh-1", acl)
        assert request_versioned.call_args.args == ("PATCH", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "warehouses/wh-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"access_control_list": acl}

        client.get_object_permission_levels("warehouses", "wh-1")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "warehouses/wh-1/permissionLevels"

    with pytest.raises(ValidationError):
        client.get_object_permissions("", "wh-1")
    with pytest.raises(ValidationError):
        client.get_object_permissions("warehouses", "")
    with pytest.raises(ValidationError):
        client.set_object_permissions("", "wh-1", [])
    with pytest.raises(ValidationError):
        client.set_object_permissions("warehouses", "", [])
    with pytest.raises(ValidationError):
        client.update_object_permissions("", "wh-1", [])
    with pytest.raises(ValidationError):
        client.update_object_permissions("warehouses", "", [])
    with pytest.raises(ValidationError):
        client.get_object_permission_levels("", "wh-1")
    with pytest.raises(ValidationError):
        client.get_object_permission_levels("warehouses", "")


def test_catalog_repo_secret_token_wrappers_route_expected_calls():
    client = _workspace_client()

    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_catalogs(max_results=25, page_token="pg-1")
        assert request_versioned.call_args.args == ("GET", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "catalogs"
        assert request_versioned.call_args.kwargs["params"] == {
            "max_results": 25,
            "page_token": "pg-1",
        }
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.list_schemas(catalog_name="main", max_results=10)
        assert request_versioned.call_args.args == ("GET", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "schemas"
        assert request_versioned.call_args.kwargs["params"] == {
            "catalog_name": "main",
            "max_results": 10,
        }
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.update_repo(12345, branch="main")
        assert request_versioned.call_args.args == ("PATCH", "repos")
        assert request_versioned.call_args.kwargs["endpoint"] == "12345"
        assert request_versioned.call_args.kwargs["json_body"] == {"branch": "main"}

        client.put_secret("app-prod", "token", string_value="abc")
        assert request_versioned.call_args.args == ("POST", "secrets")
        assert request_versioned.call_args.kwargs["endpoint"] == "put"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "scope": "app-prod",
            "key": "token",
            "string_value": "abc",
        }

        client.create_token(lifetime_seconds=3600, comment="ci token")
        assert request_versioned.call_args.args == ("POST", "token")
        assert request_versioned.call_args.kwargs["endpoint"] == "create"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "lifetime_seconds": 3600,
            "comment": "ci token",
        }

        client.delete_token("tok-123")
        assert request_versioned.call_args.args == ("POST", "token")
        assert request_versioned.call_args.kwargs["endpoint"] == "delete"
        assert request_versioned.call_args.kwargs["json_body"] == {"token_id": "tok-123"}


def test_repo_and_secret_scope_wrappers_route_expected_calls():
    client = _workspace_client()

    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_repos(path_prefix="/Repos/team")
        assert request_versioned.call_args.args == ("GET", "repos")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["params"] == {"path_prefix": "/Repos/team"}
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.get_repo(12345)
        assert request_versioned.call_args.args == ("GET", "repos")
        assert request_versioned.call_args.kwargs["endpoint"] == "12345"

        client.create_repo(
            url="https://github.com/rehladigital/repo.git",
            provider="gitHub",
            path="/Repos/team/repo",
        )
        assert request_versioned.call_args.args == ("POST", "repos")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {
            "url": "https://github.com/rehladigital/repo.git",
            "provider": "gitHub",
            "path": "/Repos/team/repo",
        }

        client.delete_repo(12345)
        assert request_versioned.call_args.args == ("DELETE", "repos")
        assert request_versioned.call_args.kwargs["endpoint"] == "12345"

        client.list_git_credentials()
        assert request_versioned.call_args.args == ("GET", "git-credentials")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_git_credential({"git_username": "svc-user", "git_provider": "gitHub"})
        assert request_versioned.call_args.args == ("POST", "git-credentials")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {
            "git_username": "svc-user",
            "git_provider": "gitHub",
        }

        client.get_git_credential(101)
        assert request_versioned.call_args.args == ("GET", "git-credentials")
        assert request_versioned.call_args.kwargs["endpoint"] == "101"

        client.update_git_credential(101, {"personal_access_token": "new-token"})
        assert request_versioned.call_args.args == ("PATCH", "git-credentials")
        assert request_versioned.call_args.kwargs["endpoint"] == "101"
        assert request_versioned.call_args.kwargs["json_body"] == {"personal_access_token": "new-token"}

        client.delete_git_credential(101)
        assert request_versioned.call_args.args == ("DELETE", "git-credentials")
        assert request_versioned.call_args.kwargs["endpoint"] == "101"

        client.get_repo_permissions(12345)
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "repos/12345"

        client.update_repo_permissions(
            12345,
            [{"user_name": "user@example.com", "permission_level": "CAN_READ"}],
        )
        assert request_versioned.call_args.args == ("PATCH", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "repos/12345"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "access_control_list": [{"user_name": "user@example.com", "permission_level": "CAN_READ"}]
        }

        client.get_repo_permission_levels(12345)
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "repos/12345/permissionLevels"

        client.create_secret_scope("app-prod", initial_manage_principal="users")
        assert request_versioned.call_args.args == ("POST", "secrets")
        assert request_versioned.call_args.kwargs["endpoint"] == "scopes/create"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "scope": "app-prod",
            "initial_manage_principal": "users",
        }

        client.list_secret_scopes()
        assert request_versioned.call_args.args == ("GET", "secrets")
        assert request_versioned.call_args.kwargs["endpoint"] == "scopes/list"

        client.delete_secret_scope("app-prod")
        assert request_versioned.call_args.args == ("POST", "secrets")
        assert request_versioned.call_args.kwargs["endpoint"] == "scopes/delete"
        assert request_versioned.call_args.kwargs["json_body"] == {"scope": "app-prod"}

    with pytest.raises(ValidationError):
        client.get_git_credential(0)
    with pytest.raises(ValidationError):
        client.update_git_credential(0, {})
    with pytest.raises(ValidationError):
        client.delete_git_credential(0)


def test_unity_catalog_detail_and_token_wrappers_route_expected_calls():
    client = _workspace_client()

    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.get_catalog("main")
        assert request_versioned.call_args.args == ("GET", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "catalogs/main"

        client.get_schema("main.default")
        assert request_versioned.call_args.args == ("GET", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "schemas/main.default"

        client.list_tokens()
        assert request_versioned.call_args.args == ("GET", "token")
        assert request_versioned.call_args.kwargs["endpoint"] == "list"

        client.revoke_token("tok-321")
        assert request_versioned.call_args.args == ("POST", "token")
        assert request_versioned.call_args.kwargs["endpoint"] == "delete"
        assert request_versioned.call_args.kwargs["json_body"] == {"token_id": "tok-321"}


def test_revoke_token_requires_non_empty_token_id():
    client = _workspace_client()
    with pytest.raises(ValidationError):
        client.revoke_token("")


def test_rotate_token_creates_new_token_then_revokes_previous_token():
    client = _workspace_client()

    with (
        patch.object(client, "create_token", return_value={"token_value": "new-token"}) as create_token,
        patch.object(client, "revoke_token", return_value=None) as revoke_token,
    ):
        created_token = client.rotate_token(
            "old-token-id",
            lifetime_seconds=3600,
            comment="rotated by automation",
        )

    assert created_token == {"token_value": "new-token"}
    create_token.assert_called_once_with(
        lifetime_seconds=3600,
        comment="rotated by automation",
        api_version="2.0",
    )
    revoke_token.assert_called_once_with(token_id="old-token-id", api_version="2.0")


def test_rotate_token_requires_non_empty_token_id_to_revoke():
    client = _workspace_client()
    with pytest.raises(ValidationError):
        client.rotate_token("")


def test_sql_warehouse_wrappers_route_expected_calls():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_sql_warehouses()
        assert request_versioned.call_args.args == ("GET", "sql/warehouses")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.get_sql_warehouse("wh-1")
        assert request_versioned.call_args.args == ("GET", "sql/warehouses")
        assert request_versioned.call_args.kwargs["endpoint"] == "wh-1"

        client.create_sql_warehouse({"name": "analytics-wh"})
        assert request_versioned.call_args.args == ("POST", "sql/warehouses")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "analytics-wh"}

        client.edit_sql_warehouse("wh-1", {"cluster_size": "2X-Small"})
        assert request_versioned.call_args.args == ("POST", "sql/warehouses/wh-1")
        assert request_versioned.call_args.kwargs["endpoint"] == "edit"
        assert request_versioned.call_args.kwargs["json_body"] == {"cluster_size": "2X-Small"}

        client.delete_sql_warehouse("wh-1")
        assert request_versioned.call_args.args == ("DELETE", "sql/warehouses")
        assert request_versioned.call_args.kwargs["endpoint"] == "wh-1"


def test_alerts_and_dashboards_wrappers_route_expected_calls():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_sql_alerts()
        assert request_versioned.call_args.args == ("GET", "sql/alerts")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_sql_alert({"name": "daily-failure-alert"})
        assert request_versioned.call_args.args == ("POST", "sql/alerts")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "daily-failure-alert"}

        client.get_sql_alert("alert-1")
        assert request_versioned.call_args.args == ("GET", "sql/alerts")
        assert request_versioned.call_args.kwargs["endpoint"] == "alert-1"

        client.update_sql_alert("alert-1", {"name": "daily-failure-alert-v2"})
        assert request_versioned.call_args.args == ("PATCH", "sql/alerts")
        assert request_versioned.call_args.kwargs["endpoint"] == "alert-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "daily-failure-alert-v2"}

        client.delete_sql_alert("alert-1")
        assert request_versioned.call_args.args == ("DELETE", "sql/alerts")
        assert request_versioned.call_args.kwargs["endpoint"] == "alert-1"

        client.list_sql_queries()
        assert request_versioned.call_args.args == ("GET", "sql/queries")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_sql_query({"name": "daily-revenue", "query": "SELECT 1"})
        assert request_versioned.call_args.args == ("POST", "sql/queries")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "daily-revenue", "query": "SELECT 1"}

        client.get_sql_query("query-1")
        assert request_versioned.call_args.args == ("GET", "sql/queries")
        assert request_versioned.call_args.kwargs["endpoint"] == "query-1"

        client.update_sql_query("query-1", {"name": "daily-revenue-v2"})
        assert request_versioned.call_args.args == ("PATCH", "sql/queries")
        assert request_versioned.call_args.kwargs["endpoint"] == "query-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "daily-revenue-v2"}

        client.delete_sql_query("query-1")
        assert request_versioned.call_args.args == ("DELETE", "sql/queries")
        assert request_versioned.call_args.kwargs["endpoint"] == "query-1"

        client.list_dashboards()
        assert request_versioned.call_args.args == ("GET", "lakeview/dashboards")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_dashboard({"display_name": "Ops Dashboard"})
        assert request_versioned.call_args.args == ("POST", "lakeview/dashboards")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"display_name": "Ops Dashboard"}

        client.get_dashboard("dash-1")
        assert request_versioned.call_args.args == ("GET", "lakeview/dashboards")
        assert request_versioned.call_args.kwargs["endpoint"] == "dash-1"

        client.update_dashboard("dash-1", {"display_name": "Ops Dashboard V2"})
        assert request_versioned.call_args.args == ("PATCH", "lakeview/dashboards")
        assert request_versioned.call_args.kwargs["endpoint"] == "dash-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"display_name": "Ops Dashboard V2"}

        client.trash_dashboard("dash-1")
        assert request_versioned.call_args.args == ("POST", "lakeview/dashboards")
        assert request_versioned.call_args.kwargs["endpoint"] == "dash-1/trash"

        client.publish_dashboard("dash-1")
        assert request_versioned.call_args.args == ("POST", "lakeview/dashboards")
        assert request_versioned.call_args.kwargs["endpoint"] == "dash-1/published"

        client.unpublish_dashboard("dash-1")
        assert request_versioned.call_args.args == ("DELETE", "lakeview/dashboards")
        assert request_versioned.call_args.kwargs["endpoint"] == "dash-1/published"

    with pytest.raises(ValidationError):
        client.get_sql_alert("")
    with pytest.raises(ValidationError):
        client.update_sql_alert("", {})
    with pytest.raises(ValidationError):
        client.delete_sql_alert("")
    with pytest.raises(ValidationError):
        client.get_sql_query("")
    with pytest.raises(ValidationError):
        client.update_sql_query("", {})
    with pytest.raises(ValidationError):
        client.delete_sql_query("")
    with pytest.raises(ValidationError):
        client.get_dashboard("")
    with pytest.raises(ValidationError):
        client.update_dashboard("", {})
    with pytest.raises(ValidationError):
        client.trash_dashboard("")
    with pytest.raises(ValidationError):
        client.publish_dashboard("")
    with pytest.raises(ValidationError):
        client.unpublish_dashboard("")


def test_apps_and_authentication_wrappers_route_expected_calls():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_apps()
        assert request_versioned.call_args.args == ("GET", "apps")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_app({"name": "ops-app"})
        assert request_versioned.call_args.args == ("POST", "apps")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "ops-app"}

        client.get_app("ops-app")
        assert request_versioned.call_args.args == ("GET", "apps")
        assert request_versioned.call_args.kwargs["endpoint"] == "ops-app"

        client.update_app("ops-app", {"description": "ops app v2"})
        assert request_versioned.call_args.args == ("PATCH", "apps")
        assert request_versioned.call_args.kwargs["endpoint"] == "ops-app"
        assert request_versioned.call_args.kwargs["json_body"] == {"description": "ops app v2"}

        client.delete_app("ops-app")
        assert request_versioned.call_args.args == ("DELETE", "apps")
        assert request_versioned.call_args.kwargs["endpoint"] == "ops-app"

        client.start_app("ops-app")
        assert request_versioned.call_args.args == ("POST", "apps")
        assert request_versioned.call_args.kwargs["endpoint"] == "ops-app/start"

        client.stop_app("ops-app")
        assert request_versioned.call_args.args == ("POST", "apps")
        assert request_versioned.call_args.kwargs["endpoint"] == "ops-app/stop"

        acl = [{"user_name": "user@example.com", "permission_level": "CAN_MANAGE"}]
        client.get_app_permissions("ops-app")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "apps/ops-app"

        client.set_app_permissions("ops-app", acl)
        assert request_versioned.call_args.args == ("PUT", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "apps/ops-app"
        assert request_versioned.call_args.kwargs["json_body"] == {"access_control_list": acl}

        client.update_app_permissions("ops-app", acl)
        assert request_versioned.call_args.args == ("PATCH", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "apps/ops-app"
        assert request_versioned.call_args.kwargs["json_body"] == {"access_control_list": acl}

        client.get_app_permission_levels("ops-app")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "apps/ops-app/permissionLevels"

        client.list_all_tokens()
        assert request_versioned.call_args.args == ("GET", "token-management")
        assert request_versioned.call_args.kwargs["endpoint"] == "tokens"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.get_token_info("token-123")
        assert request_versioned.call_args.args == ("GET", "token-management")
        assert request_versioned.call_args.kwargs["endpoint"] == "tokens/token-123"

    with pytest.raises(ValidationError):
        client.get_app("")
    with pytest.raises(ValidationError):
        client.update_app("", {})
    with pytest.raises(ValidationError):
        client.delete_app("")
    with pytest.raises(ValidationError):
        client.start_app("")
    with pytest.raises(ValidationError):
        client.stop_app("")
    with pytest.raises(ValidationError):
        client.get_app_permissions("")
    with pytest.raises(ValidationError):
        client.set_app_permissions("", [])
    with pytest.raises(ValidationError):
        client.update_app_permissions("", [])
    with pytest.raises(ValidationError):
        client.get_app_permission_levels("")
    with pytest.raises(ValidationError):
        client.get_token_info("")


def test_cleanrooms_and_command_execution_wrappers_route_expected_calls():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.create_execution_context("cluster-1", language="python")
        assert request_versioned.call_args.args == ("POST", "command-execution")
        assert request_versioned.call_args.kwargs["endpoint"] == "contexts/create"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "cluster_id": "cluster-1",
            "language": "python",
        }

        client.run_command("ctx-1", "print(1)", language="python")
        assert request_versioned.call_args.args == ("POST", "command-execution")
        assert request_versioned.call_args.kwargs["endpoint"] == "commands/execute"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "context_id": "ctx-1",
            "command": "print(1)",
            "language": "python",
        }

        client.get_command_status("ctx-1", "cmd-1")
        assert request_versioned.call_args.args == ("GET", "command-execution")
        assert request_versioned.call_args.kwargs["endpoint"] == "commands/status"
        assert request_versioned.call_args.kwargs["params"] == {"context_id": "ctx-1", "command_id": "cmd-1"}

        client.cancel_command("ctx-1", "cmd-1")
        assert request_versioned.call_args.args == ("POST", "command-execution")
        assert request_versioned.call_args.kwargs["endpoint"] == "commands/cancel"
        assert request_versioned.call_args.kwargs["json_body"] == {"context_id": "ctx-1", "command_id": "cmd-1"}

        client.delete_execution_context("ctx-1")
        assert request_versioned.call_args.args == ("POST", "command-execution")
        assert request_versioned.call_args.kwargs["endpoint"] == "contexts/destroy"
        assert request_versioned.call_args.kwargs["json_body"] == {"context_id": "ctx-1"}

        client.list_clean_rooms()
        assert request_versioned.call_args.args == ("GET", "clean-rooms")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_clean_room({"name": "cr-prod"})
        assert request_versioned.call_args.args == ("POST", "clean-rooms")
        assert request_versioned.call_args.kwargs["endpoint"] == ""
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "cr-prod"}

        client.get_clean_room("cr-prod")
        assert request_versioned.call_args.args == ("GET", "clean-rooms")
        assert request_versioned.call_args.kwargs["endpoint"] == "cr-prod"

        client.update_clean_room("cr-prod", {"description": "secure room"})
        assert request_versioned.call_args.args == ("PATCH", "clean-rooms")
        assert request_versioned.call_args.kwargs["endpoint"] == "cr-prod"
        assert request_versioned.call_args.kwargs["json_body"] == {"description": "secure room"}

        client.delete_clean_room("cr-prod")
        assert request_versioned.call_args.args == ("DELETE", "clean-rooms")
        assert request_versioned.call_args.kwargs["endpoint"] == "cr-prod"

        client.list_clean_room_assets("cr-prod")
        assert request_versioned.call_args.args == ("GET", "clean-rooms")
        assert request_versioned.call_args.kwargs["endpoint"] == "cr-prod/assets"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_clean_room_asset("cr-prod", {"name": "asset-1"})
        assert request_versioned.call_args.args == ("POST", "clean-rooms")
        assert request_versioned.call_args.kwargs["endpoint"] == "cr-prod/assets"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "asset-1"}

        client.get_clean_room_asset("cr-prod", "asset-1")
        assert request_versioned.call_args.args == ("GET", "clean-rooms")
        assert request_versioned.call_args.kwargs["endpoint"] == "cr-prod/assets/asset-1"

        client.update_clean_room_asset("cr-prod", "asset-1", {"description": "v2"})
        assert request_versioned.call_args.args == ("PATCH", "clean-rooms")
        assert request_versioned.call_args.kwargs["endpoint"] == "cr-prod/assets/asset-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"description": "v2"}

        client.delete_clean_room_asset("cr-prod", "asset-1")
        assert request_versioned.call_args.args == ("DELETE", "clean-rooms")
        assert request_versioned.call_args.kwargs["endpoint"] == "cr-prod/assets/asset-1"

    with pytest.raises(ValidationError):
        client.create_execution_context("")
    with pytest.raises(ValidationError):
        client.run_command("", "print(1)")
    with pytest.raises(ValidationError):
        client.run_command("ctx-1", "")
    with pytest.raises(ValidationError):
        client.get_command_status("", "cmd-1")
    with pytest.raises(ValidationError):
        client.get_command_status("ctx-1", "")
    with pytest.raises(ValidationError):
        client.cancel_command("", "cmd-1")
    with pytest.raises(ValidationError):
        client.cancel_command("ctx-1", "")
    with pytest.raises(ValidationError):
        client.delete_execution_context("")
    with pytest.raises(ValidationError):
        client.get_clean_room("")
    with pytest.raises(ValidationError):
        client.update_clean_room("", {})
    with pytest.raises(ValidationError):
        client.delete_clean_room("")
    with pytest.raises(ValidationError):
        client.list_clean_room_assets("")
    with pytest.raises(ValidationError):
        client.create_clean_room_asset("", {})
    with pytest.raises(ValidationError):
        client.get_clean_room_asset("", "asset-1")
    with pytest.raises(ValidationError):
        client.get_clean_room_asset("cr-prod", "")
    with pytest.raises(ValidationError):
        client.update_clean_room_asset("", "asset-1", {})
    with pytest.raises(ValidationError):
        client.update_clean_room_asset("cr-prod", "", {})
    with pytest.raises(ValidationError):
        client.delete_clean_room_asset("", "asset-1")
    with pytest.raises(ValidationError):
        client.delete_clean_room_asset("cr-prod", "")


def test_instance_pool_wrappers_route_expected_calls():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_instance_pools()
        assert request_versioned.call_args.args == ("GET", "instance-pools")
        assert request_versioned.call_args.kwargs["endpoint"] == "list"

        client.get_instance_pool("pool-1")
        assert request_versioned.call_args.kwargs["endpoint"] == "get"
        assert request_versioned.call_args.kwargs["params"] == {"instance_pool_id": "pool-1"}

        client.create_instance_pool({"instance_pool_name": "etl-pool"})
        assert request_versioned.call_args.args == ("POST", "instance-pools")
        assert request_versioned.call_args.kwargs["endpoint"] == "create"
        assert request_versioned.call_args.kwargs["json_body"] == {"instance_pool_name": "etl-pool"}

        client.edit_instance_pool("pool-1", {"min_idle_instances": 1})
        assert request_versioned.call_args.kwargs["endpoint"] == "edit"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "instance_pool_id": "pool-1",
            "min_idle_instances": 1,
        }

        client.delete_instance_pool("pool-1")
        assert request_versioned.call_args.kwargs["endpoint"] == "delete"
        assert request_versioned.call_args.kwargs["json_body"] == {"instance_pool_id": "pool-1"}

        client.get_instance_pool_permissions("pool-1")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "instance-pools/pool-1"

        client.set_instance_pool_permissions("pool-1", [{"group_name": "users", "permission_level": "CAN_ATTACH_TO"}])
        assert request_versioned.call_args.args == ("PUT", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "instance-pools/pool-1"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "access_control_list": [{"group_name": "users", "permission_level": "CAN_ATTACH_TO"}]
        }

        client.update_instance_pool_permissions("pool-1", [{"group_name": "admins", "permission_level": "CAN_MANAGE"}])
        assert request_versioned.call_args.args == ("PATCH", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "instance-pools/pool-1"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "access_control_list": [{"group_name": "admins", "permission_level": "CAN_MANAGE"}]
        }

        client.get_instance_pool_permission_levels("pool-1")
        assert request_versioned.call_args.args == ("GET", "permissions")
        assert request_versioned.call_args.kwargs["endpoint"] == "instance-pools/pool-1/permissionLevels"

    with pytest.raises(ValidationError):
        client.get_instance_pool_permissions("")
    with pytest.raises(ValidationError):
        client.set_instance_pool_permissions("", [])
    with pytest.raises(ValidationError):
        client.update_instance_pool_permissions("", [])
    with pytest.raises(ValidationError):
        client.get_instance_pool_permission_levels("")


def test_data_quality_monitor_wrappers_route_expected_calls():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_monitors()
        assert request_versioned.call_args.args == ("GET", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_monitor({"table_name": "main.prod.sales"})
        assert request_versioned.call_args.args == ("POST", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors"
        assert request_versioned.call_args.kwargs["json_body"] == {"table_name": "main.prod.sales"}

        client.get_monitor("m-1")
        assert request_versioned.call_args.args == ("GET", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors/m-1"

        client.update_monitor("m-1", {"output_schema_name": "dq"})
        assert request_versioned.call_args.args == ("PATCH", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors/m-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"output_schema_name": "dq"}

        client.delete_monitor("m-1")
        assert request_versioned.call_args.args == ("DELETE", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors/m-1"

        client.list_monitor_refreshes("m-1")
        assert request_versioned.call_args.args == ("GET", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors/m-1/refreshes"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_monitor_refresh("m-1", {"full_refresh": True})
        assert request_versioned.call_args.args == ("POST", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors/m-1/refreshes"
        assert request_versioned.call_args.kwargs["json_body"] == {"full_refresh": True}

        client.get_monitor_refresh("m-1", "r-1")
        assert request_versioned.call_args.args == ("GET", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors/m-1/refreshes/r-1"

        client.delete_monitor_refresh("m-1", "r-1")
        assert request_versioned.call_args.args == ("DELETE", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors/m-1/refreshes/r-1"

        client.update_monitor_refresh("m-1", "r-1", {"priority": "high"})
        assert request_versioned.call_args.args == ("PATCH", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors/m-1/refreshes/r-1"
        assert request_versioned.call_args.kwargs["json_body"] == {"priority": "high"}

        client.cancel_monitor_refresh("m-1", "r-1")
        assert request_versioned.call_args.args == ("POST", "data-quality-monitors")
        assert request_versioned.call_args.kwargs["endpoint"] == "monitors/m-1/refreshes/r-1/cancel"

    with pytest.raises(ValidationError):
        client.get_monitor("")
    with pytest.raises(ValidationError):
        client.update_monitor("", {})
    with pytest.raises(ValidationError):
        client.delete_monitor("")
    with pytest.raises(ValidationError):
        client.list_monitor_refreshes("")
    with pytest.raises(ValidationError):
        client.create_monitor_refresh("", {})
    with pytest.raises(ValidationError):
        client.get_monitor_refresh("", "r-1")
    with pytest.raises(ValidationError):
        client.get_monitor_refresh("m-1", "")
    with pytest.raises(ValidationError):
        client.delete_monitor_refresh("", "r-1")
    with pytest.raises(ValidationError):
        client.delete_monitor_refresh("m-1", "")
    with pytest.raises(ValidationError):
        client.update_monitor_refresh("", "r-1", {})
    with pytest.raises(ValidationError):
        client.update_monitor_refresh("m-1", "", {})
    with pytest.raises(ValidationError):
        client.cancel_monitor_refresh("", "r-1")
    with pytest.raises(ValidationError):
        client.cancel_monitor_refresh("m-1", "")


def test_cluster_policy_wrappers_route_expected_calls():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_cluster_policies()
        assert request_versioned.call_args.args == ("GET", "policies/clusters")
        assert request_versioned.call_args.kwargs["endpoint"] == "list"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.get_cluster_policy("policy-1")
        assert request_versioned.call_args.kwargs["endpoint"] == "get"
        assert request_versioned.call_args.kwargs["params"] == {"policy_id": "policy-1"}

        client.create_cluster_policy({"name": "job-policy"})
        assert request_versioned.call_args.args == ("POST", "policies/clusters")
        assert request_versioned.call_args.kwargs["endpoint"] == "create"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "job-policy"}

        client.edit_cluster_policy("policy-1", {"name": "job-policy-v2"})
        assert request_versioned.call_args.kwargs["endpoint"] == "edit"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "policy_id": "policy-1",
            "name": "job-policy-v2",
        }

        client.delete_cluster_policy("policy-1")
        assert request_versioned.call_args.kwargs["endpoint"] == "delete"
        assert request_versioned.call_args.kwargs["json_body"] == {"policy_id": "policy-1"}


def test_dbfs_wrappers_route_expected_calls_and_validation():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_dbfs("dbfs:/tmp")
        assert request_versioned.call_args.args == ("GET", "dbfs")
        assert request_versioned.call_args.kwargs["endpoint"] == "list"
        assert request_versioned.call_args.kwargs["params"] == {"path": "dbfs:/tmp"}

        client.get_dbfs_status("dbfs:/tmp/file.txt")
        assert request_versioned.call_args.kwargs["endpoint"] == "get-status"
        assert request_versioned.call_args.kwargs["params"] == {"path": "dbfs:/tmp/file.txt"}

        client.read_dbfs("dbfs:/tmp/file.txt", offset=10, length=128)
        assert request_versioned.call_args.kwargs["endpoint"] == "read"
        assert request_versioned.call_args.kwargs["params"] == {
            "path": "dbfs:/tmp/file.txt",
            "offset": 10,
            "length": 128,
        }

        client.delete_dbfs("dbfs:/tmp/file.txt")
        assert request_versioned.call_args.args == ("POST", "dbfs")
        assert request_versioned.call_args.kwargs["endpoint"] == "delete"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "path": "dbfs:/tmp/file.txt",
            "recursive": False,
        }

        client.mkdirs_dbfs("dbfs:/tmp/new-dir")
        assert request_versioned.call_args.kwargs["endpoint"] == "mkdirs"
        assert request_versioned.call_args.kwargs["json_body"] == {"path": "dbfs:/tmp/new-dir"}

    with pytest.raises(ValidationError):
        client.list_dbfs("")
    with pytest.raises(ValidationError):
        client.get_dbfs_status("")
    with pytest.raises(ValidationError):
        client.read_dbfs("", offset=0, length=1)
    with pytest.raises(ValidationError):
        client.read_dbfs("dbfs:/tmp/file.txt", offset=-1, length=1)
    with pytest.raises(ValidationError):
        client.read_dbfs("dbfs:/tmp/file.txt", offset=0, length=0)
    with pytest.raises(ValidationError):
        client.delete_dbfs("")
    with pytest.raises(ValidationError):
        client.mkdirs_dbfs("")


def test_files_and_sharing_wrappers_route_expected_calls_and_validation():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_files_directory("/Volumes/main/default")
        assert request_versioned.call_args.args == ("GET", "files")
        assert request_versioned.call_args.kwargs["endpoint"] == "directories"
        assert request_versioned.call_args.kwargs["params"] == {"path": "/Volumes/main/default"}
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_files_directory("/Volumes/main/default/new-dir")
        assert request_versioned.call_args.args == ("POST", "files")
        assert request_versioned.call_args.kwargs["endpoint"] == "directories"
        assert request_versioned.call_args.kwargs["json_body"] == {"path": "/Volumes/main/default/new-dir"}

        client.delete_files_directory("/Volumes/main/default/new-dir")
        assert request_versioned.call_args.args == ("DELETE", "files")
        assert request_versioned.call_args.kwargs["endpoint"] == "directories"
        assert request_versioned.call_args.kwargs["params"] == {"path": "/Volumes/main/default/new-dir"}

        client.get_files_directory_metadata("/Volumes/main/default")
        assert request_versioned.call_args.args == ("GET", "files")
        assert request_versioned.call_args.kwargs["endpoint"] == "directories/metadata"
        assert request_versioned.call_args.kwargs["params"] == {"path": "/Volumes/main/default"}

        client.download_file("/Volumes/main/default/data.csv")
        assert request_versioned.call_args.args == ("GET", "files")
        assert request_versioned.call_args.kwargs["endpoint"] == "files"
        assert request_versioned.call_args.kwargs["params"] == {"path": "/Volumes/main/default/data.csv"}

        client.upload_file("/Volumes/main/default/data.csv", "SGVsbG8=", overwrite=True)
        assert request_versioned.call_args.args == ("POST", "files")
        assert request_versioned.call_args.kwargs["endpoint"] == "files"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "path": "/Volumes/main/default/data.csv",
            "contents": "SGVsbG8=",
            "overwrite": True,
        }

        client.delete_file("/Volumes/main/default/data.csv")
        assert request_versioned.call_args.args == ("DELETE", "files")
        assert request_versioned.call_args.kwargs["endpoint"] == "files"
        assert request_versioned.call_args.kwargs["params"] == {"path": "/Volumes/main/default/data.csv"}

        client.get_file_metadata("/Volumes/main/default/data.csv")
        assert request_versioned.call_args.args == ("GET", "files")
        assert request_versioned.call_args.kwargs["endpoint"] == "files/metadata"
        assert request_versioned.call_args.kwargs["params"] == {"path": "/Volumes/main/default/data.csv"}

        client.list_sharing_providers()
        assert request_versioned.call_args.args == ("GET", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "providers"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_sharing_provider({"name": "partner-a"})
        assert request_versioned.call_args.args == ("POST", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "providers"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "partner-a"}

        client.get_sharing_provider("partner-a")
        assert request_versioned.call_args.kwargs["endpoint"] == "providers/partner-a"

        client.update_sharing_provider("partner-a", {"comment": "trusted provider"})
        assert request_versioned.call_args.args == ("PATCH", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "providers/partner-a"
        assert request_versioned.call_args.kwargs["json_body"] == {"comment": "trusted provider"}

        client.delete_sharing_provider("partner-a")
        assert request_versioned.call_args.args == ("DELETE", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "providers/partner-a"

        client.list_share_recipients()
        assert request_versioned.call_args.args == ("GET", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "recipients"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_share_recipient({"name": "consumer-a"})
        assert request_versioned.call_args.args == ("POST", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "recipients"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "consumer-a"}

        client.get_share_recipient("consumer-a")
        assert request_versioned.call_args.kwargs["endpoint"] == "recipients/consumer-a"

        client.update_share_recipient("consumer-a", {"comment": "new comment"})
        assert request_versioned.call_args.args == ("PATCH", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "recipients/consumer-a"
        assert request_versioned.call_args.kwargs["json_body"] == {"comment": "new comment"}

        client.delete_share_recipient("consumer-a")
        assert request_versioned.call_args.args == ("DELETE", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "recipients/consumer-a"

        client.list_shares()
        assert request_versioned.call_args.args == ("GET", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "shares"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.create_share({"name": "sales_share"})
        assert request_versioned.call_args.args == ("POST", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "shares"
        assert request_versioned.call_args.kwargs["json_body"] == {"name": "sales_share"}

        client.get_share("sales_share")
        assert request_versioned.call_args.kwargs["endpoint"] == "shares/sales_share"

        client.update_share("sales_share", {"comment": "updated"})
        assert request_versioned.call_args.args == ("PATCH", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "shares/sales_share"
        assert request_versioned.call_args.kwargs["json_body"] == {"comment": "updated"}

        client.delete_share("sales_share")
        assert request_versioned.call_args.args == ("DELETE", "unity-catalog")
        assert request_versioned.call_args.kwargs["endpoint"] == "shares/sales_share"

    with pytest.raises(ValidationError):
        client.list_files_directory("")
    with pytest.raises(ValidationError):
        client.create_files_directory("")
    with pytest.raises(ValidationError):
        client.delete_files_directory("")
    with pytest.raises(ValidationError):
        client.get_files_directory_metadata("")
    with pytest.raises(ValidationError):
        client.download_file("")
    with pytest.raises(ValidationError):
        client.upload_file("", "SGVsbG8=")
    with pytest.raises(ValidationError):
        client.upload_file("/Volumes/main/default/data.csv", "")
    with pytest.raises(ValidationError):
        client.delete_file("")
    with pytest.raises(ValidationError):
        client.get_file_metadata("")
    with pytest.raises(ValidationError):
        client.get_sharing_provider("")
    with pytest.raises(ValidationError):
        client.update_sharing_provider("", {})
    with pytest.raises(ValidationError):
        client.delete_sharing_provider("")
    with pytest.raises(ValidationError):
        client.get_share_recipient("")
    with pytest.raises(ValidationError):
        client.update_share_recipient("", {})
    with pytest.raises(ValidationError):
        client.delete_share_recipient("")
    with pytest.raises(ValidationError):
        client.get_share("")
    with pytest.raises(ValidationError):
        client.update_share("", {})
    with pytest.raises(ValidationError):
        client.delete_share("")


def test_instance_profile_wrappers_route_expected_calls_and_validation():
    client = _workspace_client()
    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        client.list_instance_profiles()
        assert request_versioned.call_args.args == ("GET", "instance-profiles")
        assert request_versioned.call_args.kwargs["endpoint"] == "list"
        assert request_versioned.call_args.kwargs["paginate"] is True

        client.add_instance_profile("arn:aws:iam::111122223333:instance-profile/databricks-prod")
        assert request_versioned.call_args.args == ("POST", "instance-profiles")
        assert request_versioned.call_args.kwargs["endpoint"] == "add"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "instance_profile_arn": "arn:aws:iam::111122223333:instance-profile/databricks-prod"
        }

        client.edit_instance_profile(
            "arn:aws:iam::111122223333:instance-profile/databricks-prod",
            is_meta_instance_profile=True,
        )
        assert request_versioned.call_args.args == ("POST", "instance-profiles")
        assert request_versioned.call_args.kwargs["endpoint"] == "edit"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "instance_profile_arn": "arn:aws:iam::111122223333:instance-profile/databricks-prod",
            "is_meta_instance_profile": True,
        }

        client.remove_instance_profile("arn:aws:iam::111122223333:instance-profile/databricks-prod")
        assert request_versioned.call_args.args == ("POST", "instance-profiles")
        assert request_versioned.call_args.kwargs["endpoint"] == "remove"
        assert request_versioned.call_args.kwargs["json_body"] == {
            "instance_profile_arn": "arn:aws:iam::111122223333:instance-profile/databricks-prod"
        }

    with pytest.raises(ValidationError):
        client.add_instance_profile("")
    with pytest.raises(ValidationError):
        client.edit_instance_profile("")
    with pytest.raises(ValidationError):
        client.remove_instance_profile("")
