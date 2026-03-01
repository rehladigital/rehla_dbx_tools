"""Base client implementation for Databricks APIs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from ..auth import OAuthTokenProvider, PatTokenProvider, TokenProvider
from ..config import AuthConfig
from ..exceptions import AuthError, ValidationError
from ..http_client import HttpClient
from ..response import ApiResponse


@dataclass
class ClientOptions:
    default_api_version: str = "2.1"
    timeout_seconds: int = 60
    max_retries: int = 3


class BaseDatabricksClient:
    def __init__(self, host: str, auth: AuthConfig, options: ClientOptions):
        if not host:
            raise ValidationError("Client host is required.")
        self.host = host.rstrip("/")
        self.auth = auth
        self.options = options
        self.token_provider = self._build_token_provider()
        self.http = HttpClient(
            host=self.host,
            token_provider=self.token_provider,
            timeout_seconds=options.timeout_seconds,
            max_retries=options.max_retries,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json_body: Optional[dict[str, Any]] = None,
        paginate: bool = False,
    ) -> ApiResponse:
        normalized_method = method.upper().strip()
        return self.http.request(
            method=normalized_method,
            path=path,
            params=params,
            json_body=json_body,
            paginate=True,
        )

    def request_versioned(
        self,
        method: str,
        service: str,
        *,
        endpoint: str,
        api_version: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
        json_body: Optional[dict[str, Any]] = None,
        paginate: bool = False,
    ) -> ApiResponse:
        normalized_method = method.upper().strip()
        version = api_version or self.options.default_api_version
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]
        path = f"/api/{version}/{service}/{endpoint}"
        return self.request(
            method=normalized_method,
            path=path,
            params=params,
            json_body=json_body,
            paginate=True,
        )

    def _build_token_provider(self) -> TokenProvider:
        auth_type = self.auth.auth_type
        if auth_type in {"auto", "pat", "notebook"} and self.auth.token:
            return PatTokenProvider(self.auth.token)
        if auth_type in {"auto", "oauth"} and self.auth.client_id and self.auth.client_secret:
            return OAuthTokenProvider(host=self.host, auth=self.auth)
        if auth_type in {"pat", "notebook"}:
            raise AuthError("PAT/notebook auth requires token.")
        if auth_type == "oauth":
            raise AuthError("OAuth auth requires client_id and client_secret.")
        raise AuthError("Unable to resolve auth provider from current configuration.")
