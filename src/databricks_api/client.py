"""Top-level unified client entrypoint."""

from __future__ import annotations

import getpass
import json
import os
import re
import subprocess
import webbrowser
from dataclasses import replace
from typing import Any, Optional

from .clients.account import AccountClient
from .clients.workspace import WorkspaceClient
from .config import AccountConfig, AuthConfig, CloudType, UnifiedConfig, WorkspaceConfig
from .exceptions import ValidationError
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
    def simple(
        cls,
        host: str,
        token: Optional[str] = None,
        *,
        cloud: CloudType = "aws",
        account_host: Optional[str] = None,
        account_id: Optional[str] = None,
        account_token: Optional[str] = None,
        strict_cloud_match: bool = False,
        open_browser_for_token: bool = False,
        prompt_for_token: bool = False,
        use_windows_sso: bool = False,
        databricks_cli_profile: Optional[str] = None,
    ) -> "DatabricksApiClient":
        """Create a client from just host/token (+ optional account fields)."""
        clean_workspace_host = _normalize_host_input(host)
        clean_workspace_token = _resolve_workspace_token(
            host=clean_workspace_host,
            token=token,
            open_browser_for_token=open_browser_for_token,
            prompt_for_token=prompt_for_token,
            use_windows_sso=use_windows_sso,
            databricks_cli_profile=databricks_cli_profile,
        )
        if not clean_workspace_token:
            raise ValidationError(
                "Workspace token is required. Pass token=..., set DATABRICKS_TOKEN/DBX_TOKEN, "
                "or enable prompt_for_token/use_windows_sso."
            )

        clean_account_host = _normalize_host_input(account_host) if account_host else None
        clean_account_token = (account_token or clean_workspace_token or "").strip() or None

        cfg = UnifiedConfig(
            workspace=WorkspaceConfig(
                host=clean_workspace_host,
                auth=AuthConfig(auth_type="pat", token=clean_workspace_token),
                cloud=cloud,
            ),
            account=AccountConfig(
                host=clean_account_host,
                account_id=account_id,
                auth=AuthConfig(auth_type="pat", token=clean_account_token),
                cloud=cloud,
            ),
            strict_cloud_match=strict_cloud_match,
        )
        return cls(cfg)

    @classmethod
    def from_windows_sso(
        cls,
        host: str,
        *,
        cloud: CloudType = "aws",
        account_host: Optional[str] = None,
        account_id: Optional[str] = None,
        account_token: Optional[str] = None,
        strict_cloud_match: bool = False,
        databricks_cli_profile: Optional[str] = None,
    ) -> "DatabricksApiClient":
        """Create a client using Databricks CLI SSO token resolution."""
        token = _token_from_windows_sso(_normalize_host_input(host), databricks_cli_profile)
        return cls.simple(
            host=host,
            token=token,
            cloud=cloud,
            account_host=account_host,
            account_id=account_id,
            account_token=account_token,
            strict_cloud_match=strict_cloud_match,
        )

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

    def list_active_job_runs(self, *, limit: int = 25) -> list[dict[str, Any]]:
        """Return active job runs as a plain list for simple scripts."""
        if self.workspace is None:
            raise ValidationError("Workspace client is not configured.")
        response = self.workspace.list_job_runs(active_only=True, limit=limit)
        data = response.data or {}
        if isinstance(data, dict):
            runs = data.get("runs")
            if isinstance(runs, list):
                return runs
        return []


def _with_token(auth: AuthConfig, token: str) -> AuthConfig:
    return AuthConfig(
        auth_type="notebook" if auth.auth_type == "auto" else auth.auth_type,
        token=token,
        client_id=auth.client_id,
        client_secret=auth.client_secret,
        oauth_scope=auth.oauth_scope,
    )


def _normalize_host_input(host: str) -> str:
    normalized = (host or "").strip()
    normalized = normalized.replace(".cloud.databricks.net", ".cloud.databricks.com")
    normalized = normalized.rstrip("/")
    if normalized and not normalized.startswith("http"):
        normalized = f"https://{normalized}"
    return normalized


def _resolve_workspace_token(
    *,
    host: str,
    token: Optional[str],
    open_browser_for_token: bool,
    prompt_for_token: bool,
    use_windows_sso: bool,
    databricks_cli_profile: Optional[str],
) -> str:
    explicit = (token or "").strip()
    if explicit:
        return explicit

    env_token = (os.getenv("DATABRICKS_TOKEN") or os.getenv("DBX_TOKEN") or "").strip()
    if env_token:
        return env_token

    if use_windows_sso:
        return _token_from_windows_sso(host, databricks_cli_profile)

    if open_browser_for_token:
        _open_access_token_page(host)

    if prompt_for_token:
        return getpass.getpass("Enter Databricks token: ").strip()

    return ""


def _open_access_token_page(host: str) -> None:
    webbrowser.open(f"{host.rstrip('/')}/settings/developer/access-tokens", new=2)


def _token_from_windows_sso(host: str, databricks_cli_profile: Optional[str]) -> str:
    candidates: list[list[str]] = [
        ["databricks", "auth", "token", "--host", host, "--output", "json"],
        ["databricks", "auth", "token", "--host", host, "-o", "json"],
        ["databricks", "auth", "token", "--host", host],
    ]
    if databricks_cli_profile:
        candidates = [cmd + ["--profile", databricks_cli_profile] for cmd in candidates]

    for cmd in candidates:
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        except FileNotFoundError as exc:
            raise ValidationError(
                "Databricks CLI not found. Install CLI and run `databricks auth login --host <workspace-host>`."
            ) from exc

        if proc.returncode != 0:
            continue

        token = _extract_token_from_cli_output(proc.stdout)
        if token:
            return token

    raise ValidationError(
        "Unable to resolve token from Databricks CLI SSO. Run "
        "`databricks auth login --host <workspace-host>` and retry."
    )


def _extract_token_from_cli_output(output: str) -> str:
    content = (output or "").strip()
    if not content:
        return ""

    # Preferred path: parse JSON output from `databricks auth token`.
    try:
        payload = json.loads(content)
        if isinstance(payload, dict):
            direct = payload.get("token") or payload.get("access_token") or payload.get("token_value")
            if isinstance(direct, str) and direct.strip():
                return direct.strip()
            credentials = payload.get("credentials")
            if isinstance(credentials, dict):
                nested = (
                    credentials.get("token")
                    or credentials.get("access_token")
                    or credentials.get("token_value")
                )
                if isinstance(nested, str) and nested.strip():
                    return nested.strip()
    except Exception:
        pass

    # Fallback for plain-text output.
    match = re.search(r"(dapi[a-zA-Z0-9]+)", content)
    return match.group(1) if match else ""
