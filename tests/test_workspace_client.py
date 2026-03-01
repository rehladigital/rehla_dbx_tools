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
