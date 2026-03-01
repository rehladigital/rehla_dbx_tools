import pytest

from databricks_api.client import DatabricksApiClient, connect, dbx
from databricks_api.config import AccountConfig, AuthConfig, UnifiedConfig, WorkspaceConfig
from databricks_api.exceptions import ValidationError
from databricks_api.response import ApiResponse


def test_client_allows_account_only_configuration():
    cfg = UnifiedConfig(
        workspace=WorkspaceConfig(host=None, auth=AuthConfig(token=None)),
        account=AccountConfig(
            host="https://accounts.cloud.databricks.com",
            account_id="acc-123",
            auth=AuthConfig(token="account-token"),
        ),
    )

    client = DatabricksApiClient(cfg)

    assert client.workspace is None
    assert client.account is not None


def test_from_env_for_cloud_overrides_workspace_and_account_cloud(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_TOKEN", "workspace-token")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_HOST", "https://accounts.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_ID", "acc-123")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_TOKEN", "account-token")

    client = DatabricksApiClient.from_env_for_cloud("aws")

    assert client.config.workspace.cloud == "aws"
    assert client.config.account.cloud == "aws"


def test_simple_constructor_accepts_host_token_and_normalizes_host():
    client = DatabricksApiClient.simple(
        host="dbc-test.cloud.databricks.net/",
        token=" workspace-token ",
        cloud="aws",
    )

    assert client.workspace is not None
    assert client.workspace.host == "https://dbc-test.cloud.databricks.com"
    assert client.workspace.auth.token == "workspace-token"


def test_list_active_job_runs_returns_runs_payload(monkeypatch):
    client = DatabricksApiClient.simple(
        host="https://dbc-test.cloud.databricks.com",
        token="workspace-token",
    )

    class _Resp:
        data = {"runs": [{"run_id": 101}, {"run_id": 102}]}

    assert client.workspace is not None
    monkeypatch.setattr(client.workspace, "list_job_runs", lambda **_: _Resp())

    runs = client.list_active_job_runs(limit=10)

    assert [run["run_id"] for run in runs] == [101, 102]


def test_list_active_job_runs_handles_list_payload(monkeypatch):
    client = DatabricksApiClient.simple(
        host="https://dbc-test.cloud.databricks.com",
        token="workspace-token",
    )

    class _Resp:
        data = [{"run_id": 201}, {"run_id": 202}]

    assert client.workspace is not None
    monkeypatch.setattr(client.workspace, "list_job_runs", lambda **_: _Resp())

    runs = client.list_active_job_runs(limit=10)

    assert [run["run_id"] for run in runs] == [201, 202]


def test_list_jobs_returns_plain_list(monkeypatch):
    client = DatabricksApiClient.simple(
        host="https://dbc-test.cloud.databricks.com",
        token="workspace-token",
    )

    class _Resp:
        data = {"jobs": [{"job_id": 1}, {"job_id": 2}]}

    assert client.workspace is not None
    monkeypatch.setattr(client.workspace, "list_jobs", lambda **_: _Resp())

    jobs = client.list_jobs(limit=5)

    assert [job["job_id"] for job in jobs] == [1, 2]


def test_list_recent_job_runs_returns_plain_list(monkeypatch):
    client = DatabricksApiClient.simple(
        host="https://dbc-test.cloud.databricks.com",
        token="workspace-token",
    )

    class _Resp:
        data = {"runs": [{"run_id": 301}, {"run_id": 302}]}

    assert client.workspace is not None
    monkeypatch.setattr(client.workspace, "list_job_runs", lambda **_: _Resp())

    runs = client.list_recent_job_runs(limit=5)

    assert [run["run_id"] for run in runs] == [301, 302]


def test_simple_raises_when_no_token_resolution_available(monkeypatch):
    monkeypatch.delenv("DATABRICKS_TOKEN", raising=False)
    monkeypatch.delenv("DBX_TOKEN", raising=False)

    with pytest.raises(ValidationError):
        DatabricksApiClient.simple(host="https://dbc-test.cloud.databricks.com")


def test_simple_uses_env_token_when_explicit_token_missing(monkeypatch):
    monkeypatch.setenv("DBX_TOKEN", "env-token")

    client = DatabricksApiClient.simple(host="https://dbc-test.cloud.databricks.com")

    assert client.workspace is not None
    assert client.workspace.auth.token == "env-token"


def test_workspace_allows_destructive_calls_when_requested(monkeypatch):
    client = DatabricksApiClient.simple(
        host="https://dbc-test.cloud.databricks.com",
        token="workspace-token",
    )
    assert client.workspace is not None

    captured: dict[str, object] = {}

    def _fake_request_versioned(method, service, **kwargs):
        captured["method"] = method
        captured["service"] = service
        captured["endpoint"] = kwargs.get("endpoint")
        return ApiResponse(status_code=200, url="/api/2.1/jobs/create", data={}, headers={})

    monkeypatch.setattr(client.workspace, "request_versioned", _fake_request_versioned)

    client.workspace.create_job({"name": "allowed"})

    assert captured["method"] == "POST"
    assert captured["service"] == "jobs"
    assert captured["endpoint"] == "create"


def test_account_allows_destructive_calls_when_requested(monkeypatch):
    client = DatabricksApiClient.simple(
        host="https://dbc-test.cloud.databricks.com",
        token="workspace-token",
        account_host="https://accounts.cloud.databricks.com",
        account_id="acc-123",
    )
    assert client.account is not None

    captured: dict[str, object] = {}

    def _fake_request_account(method, **kwargs):
        captured["method"] = method
        captured["endpoint"] = kwargs.get("endpoint")
        return ApiResponse(status_code=200, url="/api/2.0/accounts/acc-123/workspaces", data={}, headers={})

    monkeypatch.setattr(client.account, "request_account", _fake_request_account)

    client.account.create_workspace({"workspace_name": "allowed"})

    assert captured["method"] == "POST"
    assert captured["endpoint"] == "workspaces"


def test_read_only_requests_force_pagination_for_get(monkeypatch):
    client = DatabricksApiClient.simple(
        host="https://dbc-test.cloud.databricks.com",
        token="workspace-token",
    )
    assert client.workspace is not None

    captured: dict[str, object] = {}

    def _fake_http_request(method, path, params=None, json_body=None, paginate=False):
        captured["method"] = method
        captured["paginate"] = paginate
        return ApiResponse(status_code=200, url=path, data={"jobs": []}, headers={})

    monkeypatch.setattr(client.workspace.http, "request", _fake_http_request)

    client.workspace.request_versioned(
        "GET",
        "jobs",
        endpoint="list",
        paginate=False,
    )

    assert captured["method"] == "GET"
    assert captured["paginate"] is True


def test_connect_factory_with_explicit_host_token():
    client = connect("https://dbc-test.cloud.databricks.com", "workspace-token")
    assert isinstance(client, DatabricksApiClient)
    assert client.workspace is not None


def test_dbx_alias_factory_with_explicit_host_token():
    client = dbx("https://dbc-test.cloud.databricks.com", "workspace-token")
    assert isinstance(client, DatabricksApiClient)
    assert client.workspace is not None
