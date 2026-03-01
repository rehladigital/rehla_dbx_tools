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
<<<<<<< HEAD
        params = dict(params or {})
        params.setdefault("account_id", self.account_id)
        return self.request_versioned(
            method=method,
            service=service,
            endpoint=endpoint,
=======
        endpoint = endpoint.lstrip("/")
        account_endpoint = f"{self.account_id}/{endpoint}" if endpoint else self.account_id
        return self.request_versioned(
            method=method,
            service=service,
            endpoint=account_endpoint,
>>>>>>> 95c476f (Build unified Databricks API package with hardening and tests.)
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
