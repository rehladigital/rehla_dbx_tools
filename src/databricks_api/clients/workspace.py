"""Workspace-scoped Databricks API client."""

from __future__ import annotations

from typing import Any, Optional

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

    def get_job(self, job_id: int, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "GET",
            "jobs",
            endpoint="get",
            api_version=api_version,
            params={"job_id": job_id},
        )

    def create_job(self, job_settings: dict[str, Any], api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="create",
            api_version=api_version,
            json_body=job_settings,
        )

    def update_job(self, job_id: int, new_settings: dict[str, Any], api_version: str = "2.1") -> Any:
        payload = {"job_id": job_id, "new_settings": new_settings}
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="reset",
            api_version=api_version,
            json_body=payload,
        )

    def run_job_now(
        self,
        job_id: int,
        *,
        notebook_params: Optional[dict[str, str]] = None,
        api_version: str = "2.1",
    ) -> Any:
        payload: dict[str, Any] = {"job_id": job_id}
        if notebook_params:
            payload["notebook_params"] = notebook_params
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="run-now",
            api_version=api_version,
            json_body=payload,
        )

    def get_job_run(self, run_id: int, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "GET",
            "jobs",
            endpoint="runs/get",
            api_version=api_version,
            params={"run_id": run_id},
        )

    def cancel_job_run(self, run_id: int, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="runs/cancel",
            api_version=api_version,
            json_body={"run_id": run_id},
        )

    def delete_job(self, job_id: int, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="delete",
            api_version=api_version,
            json_body={"job_id": job_id},
        )

    def get_cluster(self, cluster_id: str, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "clusters",
            endpoint="get",
            api_version=api_version,
            params={"cluster_id": cluster_id},
        )

    def create_cluster(self, cluster_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "clusters",
            endpoint="create",
            api_version=api_version,
            json_body=cluster_spec,
        )

    def edit_cluster(
        self,
        cluster_id: str,
        cluster_spec: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        payload = {"cluster_id": cluster_id, **cluster_spec}
        return self.request_versioned(
            "POST",
            "clusters",
            endpoint="edit",
            api_version=api_version,
            json_body=payload,
        )

    def start_cluster(self, cluster_id: str, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "clusters",
            endpoint="start",
            api_version=api_version,
            json_body={"cluster_id": cluster_id},
        )

    def restart_cluster(self, cluster_id: str, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "clusters",
            endpoint="restart",
            api_version=api_version,
            json_body={"cluster_id": cluster_id},
        )

    def delete_cluster(self, cluster_id: str, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "clusters",
            endpoint="delete",
            api_version=api_version,
            json_body={"cluster_id": cluster_id},
        )

    def permanent_delete_cluster(self, cluster_id: str, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "clusters",
            endpoint="permanent-delete",
            api_version=api_version,
            json_body={"cluster_id": cluster_id},
        )

    def cluster_events(
        self,
        cluster_id: str,
        *,
        limit: int = 50,
        page_token: Optional[str] = None,
        api_version: str = "2.0",
    ) -> Any:
        params: dict[str, Any] = {"cluster_id": cluster_id, "limit": limit}
        if page_token:
            params["page_token"] = page_token
        return self.request_versioned(
            "GET",
            "clusters",
            endpoint="events",
            api_version=api_version,
            params=params,
        )
