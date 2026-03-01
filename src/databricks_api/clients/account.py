"""Account-scoped Databricks API client."""

from __future__ import annotations

from typing import Any, Optional

from ..config import AccountConfig
from ..exceptions import ValidationError
from .base import BaseDatabricksClient, ClientOptions


class AccountClient(BaseDatabricksClient):
    def __init__(self, config: AccountConfig):
        if not config.account_id:
            raise ValidationError("account_id is required for account APIs.")
        self.account_id = config.account_id
        options = ClientOptions(default_api_version=config.default_api_version)
        super().__init__(host=config.host or "", auth=config.auth, options=options)

    def request_account(
        self,
        method: str,
        service: str,
        endpoint: str,
        *,
        api_version: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
        json_body: Optional[dict[str, Any]] = None,
        paginate: bool = False,
    ) -> Any:
        endpoint = endpoint.lstrip("/")
        account_endpoint = f"{self.account_id}/{endpoint}" if endpoint else self.account_id
        return self.request_versioned(
            method=method,
            service=service,
            endpoint=account_endpoint,
            api_version=api_version,
            params=params,
            json_body=json_body,
            paginate=paginate,
        )

    def list_workspaces(self, api_version: str = "2.0") -> Any:
        return self.request_account(
            "GET",
            service="accounts",
            endpoint="workspaces",
            api_version=api_version,
            paginate=True,
        )

    def get_workspace(self, workspace_id: int, api_version: str = "2.0") -> Any:
        return self.request_account(
            "GET",
            service="accounts",
            endpoint=f"workspaces/{workspace_id}",
            api_version=api_version,
        )

    def create_workspace(self, workspace_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_account(
            "POST",
            service="accounts",
            endpoint="workspaces",
            api_version=api_version,
            json_body=workspace_spec,
        )

    def update_workspace(
        self,
        workspace_id: int,
        workspace_changes: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        return self.request_account(
            "PATCH",
            service="accounts",
            endpoint=f"workspaces/{workspace_id}",
            api_version=api_version,
            json_body=workspace_changes,
        )

    def delete_workspace(self, workspace_id: int, api_version: str = "2.0") -> Any:
        return self.request_account(
            "DELETE",
            service="accounts",
            endpoint=f"workspaces/{workspace_id}",
            api_version=api_version,
        )

    def list_credentials(self, api_version: str = "2.0") -> Any:
        return self.request_account(
            "GET",
            service="accounts",
            endpoint="credentials",
            api_version=api_version,
            paginate=True,
        )

    def create_credentials(self, credentials_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_account(
            "POST",
            service="accounts",
            endpoint="credentials",
            api_version=api_version,
            json_body=credentials_spec,
        )

    def delete_credentials(self, credentials_id: str, api_version: str = "2.0") -> Any:
        return self.request_account(
            "DELETE",
            service="accounts",
            endpoint=f"credentials/{credentials_id}",
            api_version=api_version,
        )

    def list_storage_configurations(self, api_version: str = "2.0") -> Any:
        return self.request_account(
            "GET",
            service="accounts",
            endpoint="storage-configurations",
            api_version=api_version,
            paginate=True,
        )

    def create_storage_configuration(
        self,
        storage_configuration_spec: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        return self.request_account(
            "POST",
            service="accounts",
            endpoint="storage-configurations",
            api_version=api_version,
            json_body=storage_configuration_spec,
        )

    def delete_storage_configuration(self, storage_configuration_id: str, api_version: str = "2.0") -> Any:
        return self.request_account(
            "DELETE",
            service="accounts",
            endpoint=f"storage-configurations/{storage_configuration_id}",
            api_version=api_version,
        )

    def list_networks(self, api_version: str = "2.0") -> Any:
        return self.request_account(
            "GET",
            service="accounts",
            endpoint="networks",
            api_version=api_version,
            paginate=True,
        )

    def create_network(self, network_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_account(
            "POST",
            service="accounts",
            endpoint="networks",
            api_version=api_version,
            json_body=network_spec,
        )

    def delete_network(self, network_id: str, api_version: str = "2.0") -> Any:
        return self.request_account(
            "DELETE",
            service="accounts",
            endpoint=f"networks/{network_id}",
            api_version=api_version,
        )

    def list_private_access_settings(self, api_version: str = "2.0") -> Any:
        return self.request_account(
            "GET",
            service="accounts",
            endpoint="private-access-settings",
            api_version=api_version,
            paginate=True,
        )

    def create_private_access_settings(
        self,
        private_access_spec: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        return self.request_account(
            "POST",
            service="accounts",
            endpoint="private-access-settings",
            api_version=api_version,
            json_body=private_access_spec,
        )

    def delete_private_access_settings(self, private_access_settings_id: str, api_version: str = "2.0") -> Any:
        return self.request_account(
            "DELETE",
            service="accounts",
            endpoint=f"private-access-settings/{private_access_settings_id}",
            api_version=api_version,
        )
