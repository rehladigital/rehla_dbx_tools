"""Configuration models and env/notebook loaders."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Literal, Optional

from .cloud import detect_cloud_from_host
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
    strict_cloud_match: bool = True

    @staticmethod
    def from_env() -> "UnifiedConfig":
        workspace_host = _normalize_host(_first_env("DATABRICKS_HOST", "DBX_HOST"))
        account_host = _normalize_host(_first_env("DATABRICKS_ACCOUNT_HOST", "DBX_ACCOUNT_HOST"))
        workspace_cloud = _resolve_cloud(
            configured_cloud=_first_env("DATABRICKS_CLOUD", "DBX_CLOUD"),
            host=workspace_host,
            fallback="aws",
        )
        account_cloud = _resolve_cloud(
            configured_cloud=(
                _first_env("DATABRICKS_ACCOUNT_CLOUD", "DBX_ACCOUNT_CLOUD")
                or _first_env("DATABRICKS_CLOUD", "DBX_CLOUD")
            ),
            host=account_host,
            fallback=workspace_cloud,
        )
        strict_cloud_match = _normalize_bool(
            _first_env("DATABRICKS_STRICT_CLOUD_MATCH", "DBX_STRICT_CLOUD_MATCH"),
            default=True,
        )

        workspace_auth = AuthConfig(
            auth_type=_first_env("DATABRICKS_AUTH_TYPE", "DBX_AUTH_TYPE") or "auto",  # type: ignore[arg-type]
            token=_first_env("DATABRICKS_TOKEN", "DBX_TOKEN"),
            client_id=os.getenv("DATABRICKS_CLIENT_ID"),
            client_secret=os.getenv("DATABRICKS_CLIENT_SECRET"),
            oauth_scope=os.getenv("DATABRICKS_OAUTH_SCOPE", "all-apis"),
        )
        account_auth = AuthConfig(
            auth_type=(_first_env("DATABRICKS_ACCOUNT_AUTH_TYPE", "DBX_ACCOUNT_AUTH_TYPE") or workspace_auth.auth_type),  # type: ignore[arg-type]
            token=_first_env("DATABRICKS_ACCOUNT_TOKEN", "DBX_ACCOUNT_TOKEN") or workspace_auth.token,
            client_id=os.getenv("DATABRICKS_ACCOUNT_CLIENT_ID", workspace_auth.client_id),
            client_secret=os.getenv("DATABRICKS_ACCOUNT_CLIENT_SECRET", workspace_auth.client_secret),
            oauth_scope=os.getenv("DATABRICKS_ACCOUNT_OAUTH_SCOPE", workspace_auth.oauth_scope),
        )
        cfg = UnifiedConfig(
            workspace=WorkspaceConfig(
                host=workspace_host,
                auth=workspace_auth,
                default_api_version=os.getenv("DATABRICKS_WORKSPACE_API_VERSION", "2.1"),
                cloud=workspace_cloud,
            ),
            account=AccountConfig(
                host=account_host,
                account_id=_first_env("DATABRICKS_ACCOUNT_ID", "DBX_ACCOUNT_ID"),
                auth=account_auth,
                default_api_version=os.getenv("DATABRICKS_ACCOUNT_API_VERSION", "2.0"),
                cloud=account_cloud,
            ),
            strict_cloud_match=strict_cloud_match,
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
        if self.account.host and not self.account.account_id:
            raise ValidationError("DATABRICKS_ACCOUNT_ID is required when DATABRICKS_ACCOUNT_HOST is configured.")

        if self.strict_cloud_match:
            workspace_inferred = detect_cloud_from_host(self.workspace.host)
            if workspace_inferred and workspace_inferred != self.workspace.cloud:
                raise ValidationError(
                    f"Workspace host appears to be '{workspace_inferred}' but DATABRICKS_CLOUD is '{self.workspace.cloud}'."
                )

            account_inferred = detect_cloud_from_host(self.account.host)
            if account_inferred and account_inferred != self.account.cloud:
                raise ValidationError(
                    f"Account host appears to be '{account_inferred}' but DATABRICKS_ACCOUNT_CLOUD is '{self.account.cloud}'."
                )

    def with_cloud(self, cloud: CloudType) -> "UnifiedConfig":
        normalized = _normalize_cloud(cloud)
        cfg = UnifiedConfig(
            workspace=WorkspaceConfig(
                host=self.workspace.host,
                auth=self.workspace.auth,
                default_api_version=self.workspace.default_api_version,
                cloud=normalized,
            ),
            account=AccountConfig(
                host=self.account.host,
                account_id=self.account.account_id,
                auth=self.account.auth,
                default_api_version=self.account.default_api_version,
                cloud=normalized,
            ),
            strict_cloud_match=self.strict_cloud_match,
        )
        cfg.validate()
        return cfg


def _normalize_host(host: Optional[str]) -> Optional[str]:
    if not host:
        return host
    host = host.strip()
    if not host:
        return None
    # Common typo in copied workspace URLs: ".cloud.databricks.net" vs ".com".
    host = host.replace(".cloud.databricks.net", ".cloud.databricks.com")
    if not host.startswith("http"):
        return f"https://{host}"
    return host.rstrip("/")


def _normalize_cloud(cloud: Optional[str]) -> CloudType:
    normalized = (cloud or "aws").strip().lower()
    if normalized not in ("aws", "azure", "gcp"):
        raise ValidationError("Cloud must be one of: aws, azure, gcp.")
    return normalized  # type: ignore[return-value]


def _resolve_cloud(configured_cloud: Optional[str], host: Optional[str], fallback: CloudType = "aws") -> CloudType:
    if configured_cloud:
        return _normalize_cloud(configured_cloud)
    inferred = detect_cloud_from_host(host)
    if inferred:
        return inferred
    return fallback


def _normalize_bool(value: Optional[str], default: bool) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in ("1", "true", "yes", "y", "on"):
        return True
    if normalized in ("0", "false", "no", "n", "off"):
        return False
    raise ValidationError("DATABRICKS_STRICT_CLOUD_MATCH must be a boolean value.")


def _first_env(*keys: str) -> Optional[str]:
    for key in keys:
        value = os.getenv(key)
        if value is not None:
            return value
    return None
