from unittest.mock import patch

from databricks_api.clients.account import AccountClient
from databricks_api.config import AccountConfig, AuthConfig


def test_request_account_builds_account_scoped_path():
    client = AccountClient(
        AccountConfig(
            host="https://accounts.cloud.databricks.com",
            account_id="acc-123",
            auth=AuthConfig(token="token"),
        )
    )

    with patch.object(client, "request_versioned", return_value="ok") as request_versioned:
        result = client.request_account("GET", service="accounts", endpoint="workspaces")

    assert result == "ok"
    assert request_versioned.call_args.kwargs["endpoint"] == "acc-123/workspaces"
