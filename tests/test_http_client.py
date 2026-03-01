from unittest.mock import patch
from typing import Optional

import pytest

from databricks_api.exceptions import ApiError
from databricks_api.http_client import HttpClient, _extract_next_page_token
from databricks_api.response import ApiResponse


class _TokenProvider:
    def get_token(self) -> str:
        return "token"


class _FakeResponse:
    def __init__(self, status_code: int, text: str = "{}", headers: Optional[dict[str, str]] = None):
        self.status_code = status_code
        self.text = text
        self.headers = headers or {}


def test_extract_next_page_token_ignores_current_page_token():
    assert _extract_next_page_token({"page_token": "same-token"}) is None


def test_paginated_request_raises_on_repeated_next_page_token():
    client = HttpClient(host="https://example.com", token_provider=_TokenProvider(), max_retries=0)
    page = ApiResponse(
        status_code=200,
        url="https://example.com/api/2.1/jobs/list",
        data={"items": [{"id": 1}], "next_page_token": "same-token"},
        headers={},
    )

    with patch.object(client, "_request_once", side_effect=[page, page]):
        with pytest.raises(ApiError):
            client.request(
                method="GET",
                path="/api/2.1/jobs/list",
                paginate=True,
            )


def test_paginated_request_combines_runs_payloads():
    client = HttpClient(host="https://example.com", token_provider=_TokenProvider(), max_retries=0)
    page1 = ApiResponse(
        status_code=200,
        url="https://example.com/api/2.1/jobs/runs/list",
        data={"runs": [{"run_id": 1}], "next_page_token": "token-2"},
        headers={},
    )
    page2 = ApiResponse(
        status_code=200,
        url="https://example.com/api/2.1/jobs/runs/list",
        data={"runs": [{"run_id": 2}]},
        headers={},
    )

    with patch.object(client, "_request_once", side_effect=[page1, page2]):
        response = client.request(
            method="GET",
            path="/api/2.1/jobs/runs/list",
            paginate=True,
        )

    assert response.data == [{"run_id": 1}, {"run_id": 2}]


def test_request_retries_5xx_then_returns_success_response():
    client = HttpClient(host="https://example.com", token_provider=_TokenProvider(), max_retries=1)
    first = _FakeResponse(503, text='{"message":"unavailable"}')
    second = _FakeResponse(200, text='{"items":[{"id":1}]}', headers={"x-test": "ok"})

    with patch("databricks_api.http_client.requests.request", side_effect=[first, second]) as request:
        with patch("databricks_api.http_client.time.sleep") as sleep:
            response = client.request(method="GET", path="/api/2.1/jobs/list")

    assert request.call_count == 2
    sleep.assert_called_once()
    assert response.status_code == 200
    assert response.data == {"items": [{"id": 1}]}
