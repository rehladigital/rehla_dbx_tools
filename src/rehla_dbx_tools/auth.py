"""Compatibility module for auth exports."""

from databricks_api.auth import OAuthTokenProvider, PatTokenProvider, TokenProvider

__all__ = ["OAuthTokenProvider", "PatTokenProvider", "TokenProvider"]
