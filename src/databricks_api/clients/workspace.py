"""Workspace-scoped Databricks API client."""

from __future__ import annotations

from typing import Any, Optional

from ..config import WorkspaceConfig
from ..exceptions import ValidationError
from .base import BaseDatabricksClient, ClientOptions


class WorkspaceClient(BaseDatabricksClient):
    def __init__(self, config: WorkspaceConfig):
        options = ClientOptions(default_api_version=config.default_api_version)
        super().__init__(host=config.host or "", auth=config.auth, options=options)

    @staticmethod
    def _require_positive_int(value: int, field_name: str) -> None:
        if value <= 0:
            raise ValidationError(f"{field_name} must be > 0.")

    @staticmethod
    def _require_non_empty_string(value: str, field_name: str) -> None:
        if not value or not str(value).strip():
            raise ValidationError(f"{field_name} is required.")

    def list_jobs(self, api_version: str = "2.1", limit: int = 25) -> Any:
        self._require_positive_int(limit, "limit")
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
        self._require_positive_int(job_id, "job_id")
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
        self._require_positive_int(job_id, "job_id")
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
        self._require_positive_int(job_id, "job_id")
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
        self._require_positive_int(run_id, "run_id")
        return self.request_versioned(
            "GET",
            "jobs",
            endpoint="runs/get",
            api_version=api_version,
            params={"run_id": run_id},
        )

    def cancel_job_run(self, run_id: int, api_version: str = "2.1") -> Any:
        self._require_positive_int(run_id, "run_id")
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="runs/cancel",
            api_version=api_version,
            json_body={"run_id": run_id},
        )

    def list_job_runs(
        self,
        *,
        job_id: Optional[int] = None,
        active_only: Optional[bool] = None,
        completed_only: Optional[bool] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = 25,
        api_version: str = "2.1",
    ) -> Any:
        params: dict[str, Any] = {}
        if job_id is not None:
            self._require_positive_int(job_id, "job_id")
            params["job_id"] = job_id
        if active_only is not None:
            params["active_only"] = active_only
        if completed_only is not None:
            params["completed_only"] = completed_only
        if offset is not None:
            if offset < 0:
                raise ValidationError("offset must be >= 0.")
            params["offset"] = offset
        if limit is not None:
            self._require_positive_int(limit, "limit")
            params["limit"] = limit
        return self.request_versioned(
            "GET",
            "jobs",
            endpoint="runs/list",
            api_version=api_version,
            params=params or None,
            paginate=True,
        )

    def cancel_all_job_runs(
        self,
        job_id: int,
        *,
        all_queued_runs: bool = False,
        api_version: str = "2.1",
    ) -> Any:
        self._require_positive_int(job_id, "job_id")
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="runs/cancel-all",
            api_version=api_version,
            json_body={"job_id": job_id, "all_queued_runs": all_queued_runs},
        )

    def export_job_run(
        self,
        run_id: int,
        *,
        views_to_export: Optional[str] = None,
        api_version: str = "2.1",
    ) -> Any:
        self._require_positive_int(run_id, "run_id")
        params: dict[str, Any] = {"run_id": run_id}
        if views_to_export:
            params["views_to_export"] = views_to_export
        return self.request_versioned(
            "GET",
            "jobs",
            endpoint="runs/export",
            api_version=api_version,
            params=params,
        )

    def get_job_run_output(self, run_id: int, api_version: str = "2.1") -> Any:
        self._require_positive_int(run_id, "run_id")
        return self.request_versioned(
            "GET",
            "jobs",
            endpoint="runs/get-output",
            api_version=api_version,
            params={"run_id": run_id},
        )

    def submit_job_run(self, run_spec: dict[str, Any], api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="runs/submit",
            api_version=api_version,
            json_body=run_spec,
        )

    def delete_job_run(self, run_id: int, api_version: str = "2.1") -> Any:
        self._require_positive_int(run_id, "run_id")
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="runs/delete",
            api_version=api_version,
            json_body={"run_id": run_id},
        )

    def repair_job_run(
        self,
        run_id: int,
        *,
        rerun_all_failed_tasks: bool = False,
        latest_repair_id: Optional[int] = None,
        api_version: str = "2.1",
    ) -> Any:
        self._require_positive_int(run_id, "run_id")
        payload: dict[str, Any] = {
            "run_id": run_id,
            "rerun_all_failed_tasks": rerun_all_failed_tasks,
        }
        if latest_repair_id is not None:
            self._require_positive_int(latest_repair_id, "latest_repair_id")
            payload["latest_repair_id"] = latest_repair_id
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="runs/repair",
            api_version=api_version,
            json_body=payload,
        )

    def delete_job(self, job_id: int, api_version: str = "2.1") -> Any:
        self._require_positive_int(job_id, "job_id")
        return self.request_versioned(
            "POST",
            "jobs",
            endpoint="delete",
            api_version=api_version,
            json_body={"job_id": job_id},
        )

    def get_job_permissions(self, job_id: int, api_version: str = "2.0") -> Any:
        self._require_positive_int(job_id, "job_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"jobs/{job_id}",
            api_version=api_version,
        )

    def update_job_permissions(
        self,
        job_id: int,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_positive_int(job_id, "job_id")
        return self.request_versioned(
            "PATCH",
            "permissions",
            endpoint=f"jobs/{job_id}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def get_job_permission_levels(self, job_id: int, api_version: str = "2.0") -> Any:
        self._require_positive_int(job_id, "job_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"jobs/{job_id}/permissionLevels",
            api_version=api_version,
        )

    def get_cluster_permissions(self, cluster_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"clusters/{cluster_id}",
            api_version=api_version,
        )

    def update_cluster_permissions(
        self,
        cluster_id: str,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
        return self.request_versioned(
            "PATCH",
            "permissions",
            endpoint=f"clusters/{cluster_id}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def get_cluster_permission_levels(self, cluster_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"clusters/{cluster_id}/permissionLevels",
            api_version=api_version,
        )

    def get_repo_permissions(self, repo_id: int, api_version: str = "2.0") -> Any:
        self._require_positive_int(repo_id, "repo_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"repos/{repo_id}",
            api_version=api_version,
        )

    def update_repo_permissions(
        self,
        repo_id: int,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_positive_int(repo_id, "repo_id")
        return self.request_versioned(
            "PATCH",
            "permissions",
            endpoint=f"repos/{repo_id}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def get_repo_permission_levels(self, repo_id: int, api_version: str = "2.0") -> Any:
        self._require_positive_int(repo_id, "repo_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"repos/{repo_id}/permissionLevels",
            api_version=api_version,
        )

    def get_object_permissions(self, object_type: str, object_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(object_type, "object_type")
        self._require_non_empty_string(object_id, "object_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"{object_type}/{object_id}",
            api_version=api_version,
        )

    def set_object_permissions(
        self,
        object_type: str,
        object_id: str,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(object_type, "object_type")
        self._require_non_empty_string(object_id, "object_id")
        return self.request_versioned(
            "PUT",
            "permissions",
            endpoint=f"{object_type}/{object_id}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def update_object_permissions(
        self,
        object_type: str,
        object_id: str,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(object_type, "object_type")
        self._require_non_empty_string(object_id, "object_id")
        return self.request_versioned(
            "PATCH",
            "permissions",
            endpoint=f"{object_type}/{object_id}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def get_object_permission_levels(self, object_type: str, object_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(object_type, "object_type")
        self._require_non_empty_string(object_id, "object_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"{object_type}/{object_id}/permissionLevels",
            api_version=api_version,
        )

    def get_cluster(self, cluster_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
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
        self._require_non_empty_string(cluster_id, "cluster_id")
        payload = {"cluster_id": cluster_id, **cluster_spec}
        return self.request_versioned(
            "POST",
            "clusters",
            endpoint="edit",
            api_version=api_version,
            json_body=payload,
        )

    def start_cluster(self, cluster_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
        return self.request_versioned(
            "POST",
            "clusters",
            endpoint="start",
            api_version=api_version,
            json_body={"cluster_id": cluster_id},
        )

    def restart_cluster(self, cluster_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
        return self.request_versioned(
            "POST",
            "clusters",
            endpoint="restart",
            api_version=api_version,
            json_body={"cluster_id": cluster_id},
        )

    def delete_cluster(self, cluster_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
        return self.request_versioned(
            "POST",
            "clusters",
            endpoint="delete",
            api_version=api_version,
            json_body={"cluster_id": cluster_id},
        )

    def permanent_delete_cluster(self, cluster_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
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
        self._require_non_empty_string(cluster_id, "cluster_id")
        self._require_positive_int(limit, "limit")
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
        self._require_positive_int(repo_id, "repo_id")
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
        self._require_positive_int(repo_id, "repo_id")
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
        self._require_positive_int(repo_id, "repo_id")
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

    def get_catalog(self, catalog_name: str, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint=f"catalogs/{catalog_name}",
            api_version=api_version,
        )

    def get_schema(self, full_name: str, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint=f"schemas/{full_name}",
            api_version=api_version,
        )

    def list_tokens(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "token",
            endpoint="list",
            api_version=api_version,
        )

    def revoke_token(self, token_id: str, api_version: str = "2.0") -> Any:
        if not token_id or not str(token_id).strip():
            raise ValidationError("token_id is required to revoke token.")
        return self.delete_token(token_id=token_id, api_version=api_version)

    def rotate_token(
        self,
        token_id_to_revoke: str,
        *,
        lifetime_seconds: Optional[int] = None,
        comment: Optional[str] = None,
        api_version: str = "2.0",
    ) -> Any:
        if not token_id_to_revoke or not str(token_id_to_revoke).strip():
            raise ValidationError("token_id_to_revoke is required to rotate token.")
        created_token = self.create_token(
            lifetime_seconds=lifetime_seconds,
            comment=comment,
            api_version=api_version,
        )
        self.revoke_token(token_id=token_id_to_revoke, api_version=api_version)
        return created_token

    def list_sql_warehouses(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "sql/warehouses",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def get_sql_warehouse(self, warehouse_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(warehouse_id, "warehouse_id")
        return self.request_versioned(
            "GET",
            "sql/warehouses",
            endpoint=warehouse_id,
            api_version=api_version,
        )

    def create_sql_warehouse(self, warehouse_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "sql/warehouses",
            endpoint="",
            api_version=api_version,
            json_body=warehouse_spec,
        )

    def edit_sql_warehouse(self, warehouse_id: str, warehouse_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(warehouse_id, "warehouse_id")
        return self.request_versioned(
            "POST",
            f"sql/warehouses/{warehouse_id}",
            endpoint="edit",
            api_version=api_version,
            json_body=warehouse_changes,
        )

    def delete_sql_warehouse(self, warehouse_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(warehouse_id, "warehouse_id")
        return self.request_versioned(
            "DELETE",
            "sql/warehouses",
            endpoint=warehouse_id,
            api_version=api_version,
        )

    def list_instance_pools(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "instance-pools",
            endpoint="list",
            api_version=api_version,
        )

    def get_instance_pool(self, instance_pool_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(instance_pool_id, "instance_pool_id")
        return self.request_versioned(
            "GET",
            "instance-pools",
            endpoint="get",
            api_version=api_version,
            params={"instance_pool_id": instance_pool_id},
        )

    def create_instance_pool(self, instance_pool_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "instance-pools",
            endpoint="create",
            api_version=api_version,
            json_body=instance_pool_spec,
        )

    def edit_instance_pool(
        self,
        instance_pool_id: str,
        instance_pool_changes: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(instance_pool_id, "instance_pool_id")
        payload = {"instance_pool_id": instance_pool_id, **instance_pool_changes}
        return self.request_versioned(
            "POST",
            "instance-pools",
            endpoint="edit",
            api_version=api_version,
            json_body=payload,
        )

    def delete_instance_pool(self, instance_pool_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(instance_pool_id, "instance_pool_id")
        return self.request_versioned(
            "POST",
            "instance-pools",
            endpoint="delete",
            api_version=api_version,
            json_body={"instance_pool_id": instance_pool_id},
        )

    def list_cluster_policies(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "policies/clusters",
            endpoint="list",
            api_version=api_version,
            paginate=True,
        )

    def get_cluster_policy(self, policy_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(policy_id, "policy_id")
        return self.request_versioned(
            "GET",
            "policies/clusters",
            endpoint="get",
            api_version=api_version,
            params={"policy_id": policy_id},
        )

    def create_cluster_policy(self, policy_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "policies/clusters",
            endpoint="create",
            api_version=api_version,
            json_body=policy_spec,
        )

    def edit_cluster_policy(self, policy_id: str, policy_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(policy_id, "policy_id")
        payload = {"policy_id": policy_id, **policy_changes}
        return self.request_versioned(
            "POST",
            "policies/clusters",
            endpoint="edit",
            api_version=api_version,
            json_body=payload,
        )

    def delete_cluster_policy(self, policy_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(policy_id, "policy_id")
        return self.request_versioned(
            "POST",
            "policies/clusters",
            endpoint="delete",
            api_version=api_version,
            json_body={"policy_id": policy_id},
        )

    def list_dbfs(self, path: str, api_version: str = "2.0") -> Any:
        if not path or not str(path).strip():
            raise ValidationError("path is required for DBFS list.")
        return self.request_versioned(
            "GET",
            "dbfs",
            endpoint="list",
            api_version=api_version,
            params={"path": path},
        )

    def get_dbfs_status(self, path: str, api_version: str = "2.0") -> Any:
        if not path or not str(path).strip():
            raise ValidationError("path is required for DBFS get-status.")
        return self.request_versioned(
            "GET",
            "dbfs",
            endpoint="get-status",
            api_version=api_version,
            params={"path": path},
        )

    def read_dbfs(self, path: str, *, offset: int = 0, length: int = 1048576, api_version: str = "2.0") -> Any:
        if not path or not str(path).strip():
            raise ValidationError("path is required for DBFS read.")
        if offset < 0:
            raise ValidationError("offset must be >= 0 for DBFS read.")
        if length <= 0:
            raise ValidationError("length must be > 0 for DBFS read.")
        return self.request_versioned(
            "GET",
            "dbfs",
            endpoint="read",
            api_version=api_version,
            params={"path": path, "offset": offset, "length": length},
        )

    def delete_dbfs(self, path: str, *, recursive: bool = False, api_version: str = "2.0") -> Any:
        if not path or not str(path).strip():
            raise ValidationError("path is required for DBFS delete.")
        return self.request_versioned(
            "POST",
            "dbfs",
            endpoint="delete",
            api_version=api_version,
            json_body={"path": path, "recursive": recursive},
        )

    def mkdirs_dbfs(self, path: str, api_version: str = "2.0") -> Any:
        if not path or not str(path).strip():
            raise ValidationError("path is required for DBFS mkdirs.")
        return self.request_versioned(
            "POST",
            "dbfs",
            endpoint="mkdirs",
            api_version=api_version,
            json_body={"path": path},
        )
