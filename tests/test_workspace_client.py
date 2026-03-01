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
        client.get_job_permission_levels(0)


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
