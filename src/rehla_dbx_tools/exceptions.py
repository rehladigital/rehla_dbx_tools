"""Compatibility module for exception exports."""

from databricks_api.exceptions import ApiError, AuthError, DatabricksApiError, RateLimitError, ValidationError

__all__ = ["ApiError", "AuthError", "DatabricksApiError", "RateLimitError", "ValidationError"]
