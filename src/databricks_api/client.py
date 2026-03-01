"""Top-level unified client entrypoint."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Optional

from .clients.account import AccountClient
from .clients.workspace import WorkspaceClient
from .config import AuthConfig, CloudType, UnifiedConfig
from .notebook_context import resolve_notebook_context


class DatabricksApiClient:
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.workspace = WorkspaceClient(config.workspace) if config.workspace.host else None
        self.account = (
            AccountClient(config.account) if config.account.host and config.account.account_id else None
        )

    @classmethod
    def from_env(cls) -> "DatabricksApiClient":
        return cls(UnifiedConfig.from_env())

    @classmethod
    def from_env_for_cloud(cls, cloud: CloudType) -> "DatabricksApiClient":
        cfg = UnifiedConfig.from_env().with_cloud(cloud)
        return cls(cfg)

    @classmethod
    def from_notebook_context(
        cls,
        config: Optional[UnifiedConfig] = None,
        dbutils: Optional[Any] = None,
    ) -> "DatabricksApiClient":
        cfg = config or UnifiedConfig.from_env()
        ctx = resolve_notebook_context(dbutils=dbutils)

        workspace = cfg.workspace
        if ctx.host and not workspace.host:
            workspace = replace(workspace, host=ctx.host)
        if ctx.token and not workspace.auth.token:
            workspace = replace(workspace, auth=_with_token(workspace.auth, ctx.token))

        account = cfg.account
        if ctx.token and account.auth.token is None:
            account = replace(account, auth=_with_token(account.auth, ctx.token))

        return cls(UnifiedConfig(workspace=workspace, account=account))


def _with_token(auth: AuthConfig, token: str) -> AuthConfig:
    return AuthConfig(
        auth_type="notebook" if auth.auth_type == "auto" else auth.auth_type,
        token=token,
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        oauth_scope=auth.oauth_scope,
    )
