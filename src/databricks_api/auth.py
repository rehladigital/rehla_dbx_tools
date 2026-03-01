"""Authentication providers for PAT/OAuth/notebook context."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

import requests

from .config import AuthConfig
from .exceptions import AuthError


@dataclass
class TokenState:
    access_token: str
    expires_at_epoch: float

    @property
    def is_expired(self) -> bool:
        # Refresh slightly early to avoid race conditions.
        return time.time() >= self.expires_at_epoch - 30


class TokenProvider:
    def get_token(self) -> str:
        raise NotImplementedError


class PatTokenProvider(TokenProvider):
    def __init__(self, token: Optional[str]):
        self._token = token

    def get_token(self) -> str:
        if not self._token:
            raise AuthError("PAT token is missing.")
        return self._token


class OAuthTokenProvider(TokenProvider):
    """OAuth client credentials flow against Databricks OAuth endpoint."""

    def __init__(self, host: str, auth: AuthConfig, timeout_seconds: int = 30):
        self._host = host.rstrip("/")
        self._auth = auth
        self._timeout_seconds = timeout_seconds
        self._state: Optional[TokenState] = None

    def get_token(self) -> str:
        if self._state is None or self._state.is_expired:
            self._state = self._refresh_token()
        return self._state.access_token

    def _refresh_token(self) -> TokenState:
        if not self._auth.client_id or not self._auth.client_secret:
            raise AuthError("OAuth requires client_id and client_secret.")

        endpoint = f"{self._host}/oidc/v1/token"
        payload = {
            "grant_type": "client_credentials",
            "scope": self._auth.oauth_scope or "all-apis",
        }
        response = requests.post(
            endpoint,
            auth=(self._auth.client_id, self._auth.client_secret),
            data=payload,
            timeout=self._timeout_seconds,
        )
        if response.status_code >= 400:
            raise AuthError(
                f"OAuth token request failed with status {response.status_code}: {response.text}"
            )
        data = response.json()
        access_token = data.get("access_token")
        try:
            expires_in = int(data.get("expires_in", 3600))
        except (TypeError, ValueError) as exc:
            raise AuthError("OAuth response included invalid expires_in value.") from exc
        if not access_token:
            raise AuthError("OAuth response did not include access_token.")
        return TokenState(access_token=access_token, expires_at_epoch=time.time() + expires_in)
