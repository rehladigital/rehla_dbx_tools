"""Workspace-scoped Databricks API client."""

from __future__ import annotations

from typing import Any

from ..config import WorkspaceConfig
from .base import BaseDatabricksClient, ClientOptions


class WorkspaceClient(BaseDatabricksClient):
    def __init__(self, config: WorkspaceConfig):
        options = ClientOptions(default_api_version=config.default_api_version)
        super().__init__(host=config.host or "", auth=config.auth, options=options)

    def list_jobs(self, api_version: str = "2.1", limit: int = 25) -> Any:
        return self.request_versioned(
            "GET",
            "jobs",
            endpoint="list",
            api_version=api_version,
            params={"limit": limit},
            paginate=True,
        )

    def list_clusters(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "clusters",
            endpoint="list",
            api_version=api_version,
            paginate=False,
        )
