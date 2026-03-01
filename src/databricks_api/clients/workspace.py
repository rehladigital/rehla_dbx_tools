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

    def list_catalogs(
        self,
        *,
        max_results: Optional[int] = None,
        page_token: Optional[str] = None,
        api_version: str = "2.1",
    ) -> Any:
        params: dict[str, Any] = {}
        if max_results is not None:
            params["max_results"] = max_results
        if page_token:
            params["page_token"] = page_token
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint="catalogs",
            api_version=api_version,
            params=params or None,
            paginate=True,
        )

    def list_schemas(
        self,
        *,
        catalog_name: Optional[str] = None,
        max_results: Optional[int] = None,
        page_token: Optional[str] = None,
        api_version: str = "2.1",
    ) -> Any:
        params: dict[str, Any] = {}
        if catalog_name:
            params["catalog_name"] = catalog_name
        if max_results is not None:
            params["max_results"] = max_results
        if page_token:
            params["page_token"] = page_token
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint="schemas",
            api_version=api_version,
            params=params or None,
            paginate=True,
        )

    def update_repo(
        self,
        repo_id: int,
        *,
        branch: Optional[str] = None,
        tag: Optional[str] = None,
        sparse_checkout: Optional[dict[str, Any]] = None,
        api_version: str = "2.0",
    ) -> Any:
        payload: dict[str, Any] = {}
        if branch:
            payload["branch"] = branch
        if tag:
            payload["tag"] = tag
        if sparse_checkout is not None:
            payload["sparse_checkout"] = sparse_checkout
        return self.request_versioned(
            "PATCH",
            "repos",
            endpoint=f"{repo_id}",
            api_version=api_version,
            json_body=payload or None,
        )

    def put_secret(
        self,
        scope: str,
        key: str,
        *,
        string_value: Optional[str] = None,
        bytes_value: Optional[str] = None,
        api_version: str = "2.0",
    ) -> Any:
        payload: dict[str, Any] = {"scope": scope, "key": key}
        if string_value is not None:
            payload["string_value"] = string_value
        if bytes_value is not None:
            payload["bytes_value"] = bytes_value
        return self.request_versioned(
            "POST",
            "secrets",
            endpoint="put",
            api_version=api_version,
            json_body=payload,
        )

    def create_token(
        self,
        *,
        lifetime_seconds: Optional[int] = None,
        comment: Optional[str] = None,
        api_version: str = "2.0",
    ) -> Any:
        payload: dict[str, Any] = {}
        if lifetime_seconds is not None:
            payload["lifetime_seconds"] = lifetime_seconds
        if comment:
            payload["comment"] = comment
        return self.request_versioned(
            "POST",
            "token",
            endpoint="create",
            api_version=api_version,
            json_body=payload or None,
        )

    def delete_token(self, token_id: str, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "token",
            endpoint="delete",
            api_version=api_version,
            json_body={"token_id": token_id},
        )

    def list_repos(
        self,
        *,
        path_prefix: Optional[str] = None,
        next_page_token: Optional[str] = None,
        api_version: str = "2.0",
    ) -> Any:
        params: dict[str, Any] = {}
        if path_prefix:
            params["path_prefix"] = path_prefix
        if next_page_token:
            params["next_page_token"] = next_page_token
        return self.request_versioned(
            "GET",
            "repos",
            endpoint="",
            api_version=api_version,
            params=params or None,
            paginate=True,
        )

    def get_repo(self, repo_id: int, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "repos",
            endpoint=f"{repo_id}",
            api_version=api_version,
        )

    def create_repo(
        self,
        url: str,
        provider: str,
        *,
        path: Optional[str] = None,
        sparse_checkout: Optional[dict[str, Any]] = None,
        api_version: str = "2.0",
    ) -> Any:
        payload: dict[str, Any] = {"url": url, "provider": provider}
        if path:
            payload["path"] = path
        if sparse_checkout is not None:
            payload["sparse_checkout"] = sparse_checkout
        return self.request_versioned(
            "POST",
            "repos",
            endpoint="",
            api_version=api_version,
            json_body=payload,
        )

    def delete_repo(self, repo_id: int, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "DELETE",
            "repos",
            endpoint=f"{repo_id}",
            api_version=api_version,
        )

    def create_secret_scope(
        self,
        scope: str,
        *,
        initial_manage_principal: Optional[str] = None,
        backend_type: Optional[str] = None,
        api_version: str = "2.0",
    ) -> Any:
        payload: dict[str, Any] = {"scope": scope}
        if initial_manage_principal:
            payload["initial_manage_principal"] = initial_manage_principal
        if backend_type:
            payload["scope_backend_type"] = backend_type
        return self.request_versioned(
            "POST",
            "secrets",
            endpoint="scopes/create",
            api_version=api_version,
            json_body=payload,
        )

    def list_secret_scopes(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "secrets",
            endpoint="scopes/list",
            api_version=api_version,
        )

    def delete_secret_scope(self, scope: str, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "secrets",
            endpoint="scopes/delete",
            api_version=api_version,
            json_body={"scope": scope},
        )
