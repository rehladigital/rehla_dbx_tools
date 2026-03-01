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


def test_workspace_lifecycle_wrappers_use_expected_methods_and_paths():
    client = AccountClient(
        AccountConfig(
            host="https://accounts.cloud.databricks.com",
            account_id="acc-123",
            auth=AuthConfig(token="token"),
        )
    )

    with patch.object(client, "request_account", return_value="ok") as request_account:
        client.get_workspace(101)
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "workspaces/101"

        client.create_workspace({"workspace_name": "prod-ws"})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "workspaces"
        assert request_account.call_args.kwargs["json_body"] == {"workspace_name": "prod-ws"}

        client.update_workspace(101, {"workspace_name": "prod-ws-renamed"})
        assert request_account.call_args.args == ("PATCH",)
        assert request_account.call_args.kwargs["endpoint"] == "workspaces/101"
        assert request_account.call_args.kwargs["json_body"] == {"workspace_name": "prod-ws-renamed"}

        client.delete_workspace(101)
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "workspaces/101"
