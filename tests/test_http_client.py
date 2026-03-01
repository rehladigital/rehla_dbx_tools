from unittest.mock import patch

import pytest

from databricks_api.exceptions import ApiError
from databricks_api.http_client import HttpClient, _extract_next_page_token
from databricks_api.response import ApiResponse


class _TokenProvider:
    def get_token(self) -> str:
        return "token"


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
