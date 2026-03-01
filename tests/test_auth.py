from unittest.mock import patch

import pytest

from databricks_api.auth import OAuthTokenProvider
from databricks_api.config import AuthConfig
from databricks_api.exceptions import AuthError


class _FakeResponse:
    status_code = 200
    text = ""

    @staticmethod
    def json():
        return {"access_token": "abc", "expires_in": "not-a-number"}


def test_oauth_provider_raises_auth_error_for_invalid_expires_in():
    provider = OAuthTokenProvider(
        host="https://example.cloud.databricks.com",
        auth=AuthConfig(auth_type="oauth", client_id="id", client_secret="secret"),
    )

    with patch("databricks_api.auth.requests.post", return_value=_FakeResponse()):
        with pytest.raises(AuthError):
            provider.get_token()
