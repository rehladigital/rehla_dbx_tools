from databricks_api.client import DatabricksApiClient
from databricks_api.config import AccountConfig, AuthConfig, UnifiedConfig, WorkspaceConfig


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
