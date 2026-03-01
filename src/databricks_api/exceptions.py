"""Package-specific exception hierarchy."""

from typing import Optional


class DatabricksApiError(Exception):
    """Base package error."""


class AuthError(DatabricksApiError):
    """Raised when authentication fails or credentials are missing."""


class ApiError(DatabricksApiError):
    """Raised when API requests fail."""

    def __init__(self, message: str, status_code: Optional[int] = None, payload: Optional[object] = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class RateLimitError(ApiError):
    """Raised when API rate-limits requests."""


class ValidationError(DatabricksApiError):
    """Raised when inputs are invalid."""
