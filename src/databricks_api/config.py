"""Configuration models and env/notebook loaders."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Literal, Optional

from .exceptions import ValidationError

AuthType = Literal["auto", "pat", "oauth", "notebook"]
CloudType = Literal["aws", "azure", "gcp"]


@dataclass
class AuthConfig:
    auth_type: AuthType = "auto"
    token: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    oauth_scope: str = "all-apis"


@dataclass
class WorkspaceConfig:
    host: Optional[str] = None
    auth: AuthConfig = field(default_factory=AuthConfig)
    default_api_version: str = "2.1"
    cloud: CloudType = "aws"


@dataclass
class AccountConfig:
    host: Optional[str] = None
    account_id: Optional[str] = None
    auth: AuthConfig = field(default_factory=AuthConfig)
    default_api_version: str = "2.0"
    cloud: CloudType = "aws"


@dataclass
class UnifiedConfig:
    workspace: WorkspaceConfig
    account: AccountConfig

    @staticmethod
    def from_env() -> "UnifiedConfig":
        workspace_auth = AuthConfig(
            auth_type=os.getenv("DATABRICKS_AUTH_TYPE", "auto"),  # type: ignore[arg-type]
            token=os.getenv("DATABRICKS_TOKEN"),
            client_id=os.getenv("DATABRICKS_CLIENT_ID"),
            client_secret=os.getenv("DATABRICKS_CLIENT_SECRET"),
            oauth_scope=os.getenv("DATABRICKS_OAUTH_SCOPE", "all-apis"),
        )
        account_auth = AuthConfig(
            auth_type=os.getenv("DATABRICKS_ACCOUNT_AUTH_TYPE", workspace_auth.auth_type),  # type: ignore[arg-type]
            token=os.getenv("DATABRICKS_ACCOUNT_TOKEN", workspace_auth.token),
            client_id=os.getenv("DATABRICKS_ACCOUNT_CLIENT_ID", workspace_auth.client_id),
            client_secret=os.getenv("DATABRICKS_ACCOUNT_CLIENT_SECRET", workspace_auth.client_secret),
            oauth_scope=os.getenv("DATABRICKS_ACCOUNT_OAUTH_SCOPE", workspace_auth.oauth_scope),
        )
        cfg = UnifiedConfig(
            workspace=WorkspaceConfig(
                host=_normalize_host(os.getenv("DATABRICKS_HOST")),
                auth=workspace_auth,
                default_api_version=os.getenv("DATABRICKS_WORKSPACE_API_VERSION", "2.1"),
                cloud=_normalize_cloud(os.getenv("DATABRICKS_CLOUD", "aws")),
            ),
            account=AccountConfig(
                host=_normalize_host(os.getenv("DATABRICKS_ACCOUNT_HOST")),
                account_id=os.getenv("DATABRICKS_ACCOUNT_ID"),
                auth=account_auth,
                default_api_version=os.getenv("DATABRICKS_ACCOUNT_API_VERSION", "2.0"),
                cloud=_normalize_cloud(os.getenv("DATABRICKS_ACCOUNT_CLOUD", os.getenv("DATABRICKS_CLOUD", "aws"))),
            ),
        )
        cfg.validate()
        return cfg

    def validate(self) -> None:
        if not self.workspace.host and not self.account.host:
            raise ValidationError(
                "At least one of DATABRICKS_HOST or DATABRICKS_ACCOUNT_HOST must be configured."
            )
        if self.workspace.cloud not in ("aws", "azure", "gcp"):
            raise ValidationError("Workspace cloud must be one of: aws, azure, gcp.")
        if self.account.cloud not in ("aws", "azure", "gcp"):
            raise ValidationError("Account cloud must be one of: aws, azure, gcp.")


def _normalize_host(host: Optional[str]) -> Optional[str]:
    if not host:
        return host
    host = host.strip()
    if not host:
        return None
    if not host.startswith("http"):
        return f"https://{host}"
    return host.rstrip("/")


def _normalize_cloud(cloud: Optional[str]) -> CloudType:
    normalized = (cloud or "aws").strip().lower()
    if normalized not in ("aws", "azure", "gcp"):
        raise ValidationError("Cloud must be one of: aws, azure, gcp.")
    return normalized  # type: ignore[return-value]
