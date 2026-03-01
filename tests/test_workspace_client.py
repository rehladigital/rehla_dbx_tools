from unittest.mock import patch

from databricks_api.clients.workspace import WorkspaceClient
from databricks_api.config import AuthConfig, WorkspaceConfig


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

        client.delete_job(123)
        assert request_versioned.call_args.kwargs["endpoint"] == "delete"
        assert request_versioned.call_args.kwargs["json_body"] == {"job_id": 123}

        client.run_job_now(321)
        assert request_versioned.call_args.kwargs["json_body"] == {"job_id": 321}


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
