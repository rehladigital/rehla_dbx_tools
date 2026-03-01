"""Unified Databricks API package."""

from importlib.metadata import PackageNotFoundError, version

from .client import DatabricksApiClient
from .cloud import detect_cloud_from_host, is_host_cloud_aligned
from .config import AccountConfig, AuthConfig, CloudType, UnifiedConfig, WorkspaceConfig
from .exceptions import ApiError, AuthError, DatabricksApiError, RateLimitError, ValidationError
from .response import ApiResponse, normalize_json, to_pandas_df, to_spark_df

try:
    __version__ = version("rehla-dbx-tools")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

__Help__ = (
    "rehla_dbx_tools is read-only by design in this build.\n"
    "Use DatabricksApiClient.simple(host=..., token=...) for quick setup.\n"
    "Core helpers: list_jobs(), list_recent_job_runs(), list_active_job_runs().\n"
    "Destructive HTTP methods (POST/PATCH/PUT/DELETE) are disabled."
)

__all__ = [
    "AccountConfig",
    "ApiError",
    "ApiResponse",
    "AuthConfig",
    "AuthError",
    "CloudType",
    "DatabricksApiClient",
    "DatabricksApiError",
    "RateLimitError",
    "UnifiedConfig",
    "ValidationError",
    "WorkspaceConfig",
    "__Help__",
    "__version__",
    "detect_cloud_from_host",
    "is_host_cloud_aligned",
    "normalize_json",
    "to_pandas_df",
    "to_spark_df",
]
