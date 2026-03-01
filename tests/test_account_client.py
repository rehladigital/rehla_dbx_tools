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


def test_access_management_wrappers_use_expected_methods_and_paths():
    client = AccountClient(
        AccountConfig(
            host="https://accounts.cloud.databricks.com",
            account_id="acc-123",
            auth=AuthConfig(token="token"),
        )
    )

    with patch.object(client, "request_account", return_value="ok") as request_account:
        client.get_assignable_roles_for_resource("accounts/acc-123")
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["service"] == "iam"
        assert request_account.call_args.kwargs["endpoint"] == "assignable-roles"
        assert request_account.call_args.kwargs["params"] == {"resource": "accounts/acc-123"}

        client.get_rule_set("accounts/acc-123/rule-sets/default")
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["service"] == "access-control/rule-sets"
        assert request_account.call_args.kwargs["endpoint"] == "accounts/acc-123/rule-sets/default"

        client.update_rule_set(
            "accounts/acc-123/rule-sets/default",
            {"name": "default", "grant_rules": []},
        )
        assert request_account.call_args.args == ("PUT",)
        assert request_account.call_args.kwargs["service"] == "access-control/rule-sets"
        assert request_account.call_args.kwargs["endpoint"] == "accounts/acc-123/rule-sets/default"
        assert request_account.call_args.kwargs["json_body"] == {"name": "default", "grant_rules": []}

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


def test_vpc_endpoints_and_customer_managed_keys_wrappers_use_expected_methods_and_paths():
    client = AccountClient(
        AccountConfig(
            host="https://accounts.cloud.databricks.com",
            account_id="acc-123",
            auth=AuthConfig(token="token"),
        )
    )

    with patch.object(client, "request_account", return_value="ok") as request_account:
        client.list_vpc_endpoints()
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "vpc-endpoints"
        assert request_account.call_args.kwargs["paginate"] is True

        client.create_vpc_endpoint({"vpc_endpoint_name": "prod-vpce"})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "vpc-endpoints"
        assert request_account.call_args.kwargs["json_body"] == {"vpc_endpoint_name": "prod-vpce"}

        client.delete_vpc_endpoint("vpce-101")
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "vpc-endpoints/vpce-101"

        client.list_customer_managed_keys()
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "customer-managed-keys"
        assert request_account.call_args.kwargs["paginate"] is True

        client.create_customer_managed_key({"use_cases": ["MANAGED_SERVICES"], "aws_key_info": {"key_arn": "arn"}})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "customer-managed-keys"
        assert request_account.call_args.kwargs["json_body"] == {
            "use_cases": ["MANAGED_SERVICES"],
            "aws_key_info": {"key_arn": "arn"},
        }

        client.delete_customer_managed_key("cmk-101")
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "customer-managed-keys/cmk-101"


def test_scim_user_and_group_wrappers_use_expected_methods_and_paths():
    client = AccountClient(
        AccountConfig(
            host="https://accounts.cloud.databricks.com",
            account_id="acc-123",
            auth=AuthConfig(token="token"),
        )
    )

    user_patch_payload = {"Operations": [{"op": "replace", "path": "active", "value": False}]}
    group_patch_payload = {
        "Operations": [{"op": "add", "path": "members", "value": [{"value": "123", "display": "alice"}]}]
    }

    with patch.object(client, "request_account", return_value="ok") as request_account:
        client.list_users()
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "scim/v2/Users"
        assert request_account.call_args.kwargs["paginate"] is True

        client.get_user("user-101")
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "scim/v2/Users/user-101"

        client.create_user({"userName": "alice@example.com", "active": True})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "scim/v2/Users"
        assert request_account.call_args.kwargs["json_body"] == {"userName": "alice@example.com", "active": True}

        client.patch_user("user-101", user_patch_payload)
        assert request_account.call_args.args == ("PATCH",)
        assert request_account.call_args.kwargs["endpoint"] == "scim/v2/Users/user-101"
        assert request_account.call_args.kwargs["json_body"] == user_patch_payload

        client.delete_user("user-101")
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "scim/v2/Users/user-101"

        client.list_groups()
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "scim/v2/Groups"
        assert request_account.call_args.kwargs["paginate"] is True

        client.get_group("group-101")
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "scim/v2/Groups/group-101"

        client.create_group({"displayName": "data-eng"})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "scim/v2/Groups"
        assert request_account.call_args.kwargs["json_body"] == {"displayName": "data-eng"}

        client.patch_group("group-101", group_patch_payload)
        assert request_account.call_args.args == ("PATCH",)
        assert request_account.call_args.kwargs["endpoint"] == "scim/v2/Groups/group-101"
        assert request_account.call_args.kwargs["json_body"] == group_patch_payload

        client.delete_group("group-101")
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "scim/v2/Groups/group-101"


def test_budget_policy_and_log_delivery_wrappers_use_expected_methods_and_paths():
    client = AccountClient(
        AccountConfig(
            host="https://accounts.cloud.databricks.com",
            account_id="acc-123",
            auth=AuthConfig(token="token"),
        )
    )

    with patch.object(client, "request_account", return_value="ok") as request_account:
        client.list_budget_policies()
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "budget-policies"
        assert request_account.call_args.kwargs["paginate"] is True

        client.get_budget_policy("bp-101")
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "budget-policies/bp-101"

        client.create_budget_policy({"name": "core-platform-budget", "custom_tags": {"env": "prod"}})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "budget-policies"
        assert request_account.call_args.kwargs["json_body"] == {
            "name": "core-platform-budget",
            "custom_tags": {"env": "prod"},
        }

        client.update_budget_policy("bp-101", {"name": "core-platform-budget-v2"})
        assert request_account.call_args.args == ("PATCH",)
        assert request_account.call_args.kwargs["endpoint"] == "budget-policies/bp-101"
        assert request_account.call_args.kwargs["json_body"] == {"name": "core-platform-budget-v2"}

        client.delete_budget_policy("bp-101")
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "budget-policies/bp-101"

        client.list_log_delivery_configurations()
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "log-delivery"
        assert request_account.call_args.kwargs["paginate"] is True

        client.create_log_delivery_configuration({"config_name": "audit-logs", "output_format": "JSON"})
        assert request_account.call_args.args == ("POST",)
        assert request_account.call_args.kwargs["endpoint"] == "log-delivery"
        assert request_account.call_args.kwargs["json_body"] == {
            "config_name": "audit-logs",
            "output_format": "JSON",
        }

        client.get_log_delivery_configuration("ld-101")
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["endpoint"] == "log-delivery/ld-101"

        client.patch_log_delivery_configuration("ld-101", {"status": "DISABLED"})
        assert request_account.call_args.args == ("PATCH",)
        assert request_account.call_args.kwargs["endpoint"] == "log-delivery/ld-101"
        assert request_account.call_args.kwargs["json_body"] == {"status": "DISABLED"}

        client.delete_log_delivery_configuration("ld-101")
        assert request_account.call_args.args == ("DELETE",)
        assert request_account.call_args.kwargs["endpoint"] == "log-delivery/ld-101"


def test_identity_wrappers_use_expected_methods_and_paths():
    client = AccountClient(
        AccountConfig(
            host="https://accounts.cloud.databricks.com",
            account_id="acc-123",
            auth=AuthConfig(token="token"),
        )
    )

    with patch.object(client, "request_account", return_value="ok") as request_account:
        client.resolve_external_user("ext-user-101")
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["service"] == "iam/v2"
        assert request_account.call_args.kwargs["endpoint"] == "external-users/ext-user-101"

        client.resolve_external_service_principal("ext-sp-101")
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["service"] == "iam/v2"
        assert request_account.call_args.kwargs["endpoint"] == "external-service-principals/ext-sp-101"

        client.resolve_external_group("ext-group-101")
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["service"] == "iam/v2"
        assert request_account.call_args.kwargs["endpoint"] == "external-groups/ext-group-101"

        client.get_workspace_access_details("principal-101", workspace_id=1234)
        assert request_account.call_args.args == ("GET",)
        assert request_account.call_args.kwargs["service"] == "iam/v2"
        assert request_account.call_args.kwargs["endpoint"] == "workspace-access/principal-101"
        assert request_account.call_args.kwargs["params"] == {"workspace_id": 1234}
