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


def test_credentials_and_storage_wrappers_use_expected_methods_and_paths():
    client = AccountClient(
        AccountConfig(
            host="https://accounts.cloud.databricks.com",
            account_id="acc-123",
            auth=AuthConfig(token="token"),
        )
    )

    with patch.object(client, "request_account", return_value="ok") as request_account:
        client.list_credentials()
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "credentials"
        assert request_account.call_args.kwargs["paginate"] is True

        client.create_credentials({"credentials_name": "prod-cross-account-role"})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "credentials"
        assert request_account.call_args.kwargs["json_body"] == {
            "credentials_name": "prod-cross-account-role",
        }

        client.delete_credentials("cred-101")
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "credentials/cred-101"

        client.list_storage_configurations()
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "storage-configurations"
        assert request_account.call_args.kwargs["paginate"] is True

        client.create_storage_configuration({"storage_configuration_name": "prod-root-bucket"})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "storage-configurations"
        assert request_account.call_args.kwargs["json_body"] == {
            "storage_configuration_name": "prod-root-bucket",
        }

        client.delete_storage_configuration("sc-101")
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "storage-configurations/sc-101"


def test_network_and_private_access_wrappers_use_expected_methods_and_paths():
    client = AccountClient(
        AccountConfig(
            host="https://accounts.cloud.databricks.com",
            account_id="acc-123",
            auth=AuthConfig(token="token"),
        )
    )

    with patch.object(client, "request_account", return_value="ok") as request_account:
        client.list_networks()
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "networks"
        assert request_account.call_args.kwargs["paginate"] is True

        client.create_network({"network_name": "prod-vpc"})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "networks"
        assert request_account.call_args.kwargs["json_body"] == {"network_name": "prod-vpc"}

        client.delete_network("net-101")
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "networks/net-101"

        client.list_private_access_settings()
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "private-access-settings"
        assert request_account.call_args.kwargs["paginate"] is True

        client.create_private_access_settings({"private_access_settings_name": "prod-private-link"})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "private-access-settings"
        assert request_account.call_args.kwargs["json_body"] == {
            "private_access_settings_name": "prod-private-link",
        }

        client.delete_private_access_settings("pas-101")
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "private-access-settings/pas-101"
