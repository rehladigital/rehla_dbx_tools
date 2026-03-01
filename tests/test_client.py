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
