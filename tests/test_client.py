import pytest

from databricks_api.client import DatabricksApiClient
from databricks_api.config import AccountConfig, AuthConfig, UnifiedConfig, WorkspaceConfig
from databricks_api.exceptions import ValidationError


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
