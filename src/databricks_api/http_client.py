"""HTTP client with retries and basic pagination support."""

from __future__ import annotations

import json
import time
from typing import Any, Optional

import requests

from .exceptions import ApiError, RateLimitError
from .response import ApiResponse


class HttpClient:
    def __init__(
        self,
        host: str,
        token_provider: Any,
        timeout_seconds: int = 60,
        max_retries: int = 3,
        backoff_seconds: float = 1.0,
    ):
        self.host = host.rstrip("/")
        self.token_provider = token_provider
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds

    def request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json_body: Optional[dict[str, Any]] = None,
        paginate: bool = False,
    ) -> ApiResponse:
        method = method.upper().strip()
        if not path.startswith("/"):
            path = f"/{path}"
        url = f"{self.host}{path}"

        if not paginate:
            return self._request_once(method, url, params=params, json_body=json_body)
        return self._request_paginated(method, url, params=params, json_body=json_body)

    def _request_once(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        json_body: Optional[dict[str, Any]] = None,
    ) -> ApiResponse:
        attempt = 0
        while True:
            attempt += 1
            headers = {
                "Authorization": f"Bearer {self.token_provider.get_token()}",
                "Content-Type": "application/json",
            }
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=self.timeout_seconds,
            )
            if response.status_code in {429, 500, 502, 503, 504} and attempt <= self.max_retries:
                time.sleep(self.backoff_seconds * attempt)
                continue
            if response.status_code == 429:
                raise RateLimitError(
                    f"Rate limit reached for {url}",
                    status_code=response.status_code,
                    payload=self._safe_json(response.text),
                )
            if response.status_code >= 400:
                raise ApiError(
                    f"API request failed ({response.status_code}) for {url}",
                    status_code=response.status_code,
                    payload=self._safe_json(response.text),
                )

            return ApiResponse(
                status_code=response.status_code,
                url=url,
                data=self._safe_json(response.text),
                headers=dict(response.headers),
            )

    def _request_paginated(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        json_body: Optional[dict[str, Any]] = None,
    ) -> ApiResponse:
        combined: list[Any] = []
        current_params = dict(params or {})
        last_response: Optional[ApiResponse] = None
        seen_tokens: set[str] = set()

        while True:
            response = self._request_once(method, url, params=current_params, json_body=json_body)
            last_response = response
            payload = response.data

            rows = _extract_rows(payload)
            if rows:
                combined.extend(rows)

            next_token = _extract_next_page_token(payload)
            if not next_token:
                break
            if next_token in seen_tokens:
                raise ApiError(f"Detected repeated pagination token while requesting {url}")
            seen_tokens.add(next_token)
            current_params["page_token"] = next_token

        if last_response is None:
            raise ApiError("Pagination completed without responses.")

        last_response.data = combined if combined else last_response.data
        return last_response

    @staticmethod
    def _safe_json(text: str) -> Any:
        if not text:
            return {}
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw_text": text}


def _extract_rows(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "results", "data", "workspaces", "users", "clusters", "jobs"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _extract_next_page_token(payload: Any) -> Optional[str]:
    if isinstance(payload, dict):
        for key in ("next_page_token", "nextPageToken"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value
    return None
