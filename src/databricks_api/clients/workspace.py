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

    def set_job_permissions(
        self,
        job_id: int,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_positive_int(job_id, "job_id")
        return self.request_versioned(
            "PUT",
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

    # SCIM scope
    def get_current_user(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "preview/scim/v2",
            endpoint="Me",
            api_version=api_version,
        )

    def list_scim_groups(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "preview/scim/v2",
            endpoint="Groups",
            api_version=api_version,
            paginate=True,
        )

    def create_scim_group(self, group_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "preview/scim/v2",
            endpoint="Groups",
            api_version=api_version,
            json_body=group_spec,
        )

    def get_scim_group(self, group_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(group_id, "group_id")
        return self.request_versioned(
            "GET",
            "preview/scim/v2",
            endpoint=f"Groups/{group_id}",
            api_version=api_version,
        )

    def replace_scim_group(self, group_id: str, group_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(group_id, "group_id")
        return self.request_versioned(
            "PUT",
            "preview/scim/v2",
            endpoint=f"Groups/{group_id}",
            api_version=api_version,
            json_body=group_spec,
        )

    def delete_scim_group(self, group_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(group_id, "group_id")
        return self.request_versioned(
            "DELETE",
            "preview/scim/v2",
            endpoint=f"Groups/{group_id}",
            api_version=api_version,
        )

    def update_scim_group(self, group_id: str, operations_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(group_id, "group_id")
        return self.request_versioned(
            "PATCH",
            "preview/scim/v2",
            endpoint=f"Groups/{group_id}",
            api_version=api_version,
            json_body=operations_spec,
        )

    def list_scim_service_principals(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "preview/scim/v2",
            endpoint="ServicePrincipals",
            api_version=api_version,
            paginate=True,
        )

    def create_scim_service_principal(self, service_principal_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "preview/scim/v2",
            endpoint="ServicePrincipals",
            api_version=api_version,
            json_body=service_principal_spec,
        )

    def get_scim_service_principal(self, service_principal_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(service_principal_id, "service_principal_id")
        return self.request_versioned(
            "GET",
            "preview/scim/v2",
            endpoint=f"ServicePrincipals/{service_principal_id}",
            api_version=api_version,
        )

    def replace_scim_service_principal(
        self, service_principal_id: str, service_principal_spec: dict[str, Any], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(service_principal_id, "service_principal_id")
        return self.request_versioned(
            "PUT",
            "preview/scim/v2",
            endpoint=f"ServicePrincipals/{service_principal_id}",
            api_version=api_version,
            json_body=service_principal_spec,
        )

    def delete_scim_service_principal(self, service_principal_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(service_principal_id, "service_principal_id")
        return self.request_versioned(
            "DELETE",
            "preview/scim/v2",
            endpoint=f"ServicePrincipals/{service_principal_id}",
            api_version=api_version,
        )

    def update_scim_service_principal(
        self, service_principal_id: str, operations_spec: dict[str, Any], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(service_principal_id, "service_principal_id")
        return self.request_versioned(
            "PATCH",
            "preview/scim/v2",
            endpoint=f"ServicePrincipals/{service_principal_id}",
            api_version=api_version,
            json_body=operations_spec,
        )

    def get_password_permissions(self, user_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(user_id, "user_id")
        return self.request_versioned(
            "GET",
            "permissions/passwords",
            endpoint=user_id,
            api_version=api_version,
        )

    def set_password_permissions(
        self, user_id: str, access_control_list: list[dict[str, Any]], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(user_id, "user_id")
        return self.request_versioned(
            "PUT",
            "permissions/passwords",
            endpoint=user_id,
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def update_password_permissions(
        self, user_id: str, access_control_list: list[dict[str, Any]], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(user_id, "user_id")
        return self.request_versioned(
            "PATCH",
            "permissions/passwords",
            endpoint=user_id,
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def get_password_permission_levels(self, user_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(user_id, "user_id")
        return self.request_versioned(
            "GET",
            "permissions/passwords",
            endpoint=f"{user_id}/permissionLevels",
            api_version=api_version,
        )

    def list_scim_users(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "preview/scim/v2",
            endpoint="Users",
            api_version=api_version,
            paginate=True,
        )

    def create_scim_user(self, user_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "preview/scim/v2",
            endpoint="Users",
            api_version=api_version,
            json_body=user_spec,
        )

    def get_scim_user(self, user_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(user_id, "user_id")
        return self.request_versioned(
            "GET",
            "preview/scim/v2",
            endpoint=f"Users/{user_id}",
            api_version=api_version,
        )

    def replace_scim_user(self, user_id: str, user_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(user_id, "user_id")
        return self.request_versioned(
            "PUT",
            "preview/scim/v2",
            endpoint=f"Users/{user_id}",
            api_version=api_version,
            json_body=user_spec,
        )

    def delete_scim_user(self, user_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(user_id, "user_id")
        return self.request_versioned(
            "DELETE",
            "preview/scim/v2",
            endpoint=f"Users/{user_id}",
            api_version=api_version,
        )

    def update_scim_user(self, user_id: str, operations_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(user_id, "user_id")
        return self.request_versioned(
            "PATCH",
            "preview/scim/v2",
            endpoint=f"Users/{user_id}",
            api_version=api_version,
            json_body=operations_spec,
        )

    # Workspace object scope
    def list_workspace_objects(self, path: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "GET",
            "workspace",
            endpoint="list",
            api_version=api_version,
            params={"path": path},
            paginate=True,
        )

    def create_workspace_directory(self, path: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "POST",
            "workspace",
            endpoint="mkdirs",
            api_version=api_version,
            json_body={"path": path},
        )

    def get_workspace_object_status(self, path: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "GET",
            "workspace",
            endpoint="get-status",
            api_version=api_version,
            params={"path": path},
        )

    def export_workspace_object(
        self,
        path: str,
        *,
        format: Optional[str] = None,
        direct_download: Optional[bool] = None,
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(path, "path")
        params: dict[str, Any] = {"path": path}
        if format:
            params["format"] = format
        if direct_download is not None:
            params["direct_download"] = direct_download
        return self.request_versioned(
            "GET",
            "workspace",
            endpoint="export",
            api_version=api_version,
            params=params,
        )

    def import_workspace_object(
        self,
        path: str,
        *,
        content: Optional[str] = None,
        format: Optional[str] = None,
        language: Optional[str] = None,
        overwrite: Optional[bool] = None,
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(path, "path")
        payload: dict[str, Any] = {"path": path}
        if content is not None:
            payload["content"] = content
        if format is not None:
            payload["format"] = format
        if language is not None:
            payload["language"] = language
        if overwrite is not None:
            payload["overwrite"] = overwrite
        return self.request_versioned(
            "POST",
            "workspace",
            endpoint="import",
            api_version=api_version,
            json_body=payload,
        )

    def delete_workspace_object(self, path: str, recursive: bool = False, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "POST",
            "workspace",
            endpoint="delete",
            api_version=api_version,
            json_body={"path": path, "recursive": recursive},
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
        self._require_non_empty_string(scope, "scope")
        self._require_non_empty_string(key, "key")
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

    def delete_secret(self, scope: str, key: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(scope, "scope")
        self._require_non_empty_string(key, "key")
        return self.request_versioned(
            "POST",
            "secrets",
            endpoint="delete",
            api_version=api_version,
            json_body={"scope": scope, "key": key},
        )

    def get_secret(self, scope: str, key: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(scope, "scope")
        self._require_non_empty_string(key, "key")
        return self.request_versioned(
            "GET",
            "secrets",
            endpoint="get",
            api_version=api_version,
            params={"scope": scope, "key": key},
        )

    def list_secret_keys(self, scope: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(scope, "scope")
        return self.request_versioned(
            "GET",
            "secrets",
            endpoint="list",
            api_version=api_version,
            params={"scope": scope},
            paginate=True,
        )

    def list_secret_acls(self, scope: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(scope, "scope")
        return self.request_versioned(
            "GET",
            "secrets",
            endpoint="acls/list",
            api_version=api_version,
            params={"scope": scope},
            paginate=True,
        )

    def get_secret_acl(self, scope: str, principal: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(scope, "scope")
        self._require_non_empty_string(principal, "principal")
        return self.request_versioned(
            "GET",
            "secrets",
            endpoint="acls/get",
            api_version=api_version,
            params={"scope": scope, "principal": principal},
        )

    def put_secret_acl(self, scope: str, principal: str, permission: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(scope, "scope")
        self._require_non_empty_string(principal, "principal")
        self._require_non_empty_string(permission, "permission")
        return self.request_versioned(
            "POST",
            "secrets",
            endpoint="acls/put",
            api_version=api_version,
            json_body={"scope": scope, "principal": principal, "permission": permission},
        )

    def delete_secret_acl(self, scope: str, principal: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(scope, "scope")
        self._require_non_empty_string(principal, "principal")
        return self.request_versioned(
            "POST",
            "secrets",
            endpoint="acls/delete",
            api_version=api_version,
            json_body={"scope": scope, "principal": principal},
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

    # Databricks Workspace: Git Credentials
    def list_git_credentials(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "git-credentials",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_git_credential(self, credential_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "git-credentials",
            endpoint="",
            api_version=api_version,
            json_body=credential_spec,
        )

    def get_git_credential(self, credential_id: int, api_version: str = "2.0") -> Any:
        self._require_positive_int(credential_id, "credential_id")
        return self.request_versioned(
            "GET",
            "git-credentials",
            endpoint=f"{credential_id}",
            api_version=api_version,
        )

    def update_git_credential(self, credential_id: int, credential_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_positive_int(credential_id, "credential_id")
        return self.request_versioned(
            "PATCH",
            "git-credentials",
            endpoint=f"{credential_id}",
            api_version=api_version,
            json_body=credential_changes,
        )

    def delete_git_credential(self, credential_id: int, api_version: str = "2.0") -> Any:
        self._require_positive_int(credential_id, "credential_id")
        return self.request_versioned(
            "DELETE",
            "git-credentials",
            endpoint=f"{credential_id}",
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

    # Databricks SQL Alerts (alerts scope)
    def list_sql_alerts(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "sql/alerts",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_sql_alert(self, alert_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "sql/alerts",
            endpoint="",
            api_version=api_version,
            json_body=alert_spec,
        )

    def get_sql_alert(self, alert_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(alert_id, "alert_id")
        return self.request_versioned(
            "GET",
            "sql/alerts",
            endpoint=alert_id,
            api_version=api_version,
        )

    def update_sql_alert(self, alert_id: str, alert_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(alert_id, "alert_id")
        return self.request_versioned(
            "PATCH",
            "sql/alerts",
            endpoint=alert_id,
            api_version=api_version,
            json_body=alert_changes,
        )

    def delete_sql_alert(self, alert_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(alert_id, "alert_id")
        return self.request_versioned(
            "DELETE",
            "sql/alerts",
            endpoint=alert_id,
            api_version=api_version,
        )

    # Databricks SQL Queries
    def list_sql_queries(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "sql/queries",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_sql_query(self, query_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "sql/queries",
            endpoint="",
            api_version=api_version,
            json_body=query_spec,
        )

    def get_sql_query(self, query_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(query_id, "query_id")
        return self.request_versioned(
            "GET",
            "sql/queries",
            endpoint=query_id,
            api_version=api_version,
        )

    def update_sql_query(self, query_id: str, query_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(query_id, "query_id")
        return self.request_versioned(
            "PATCH",
            "sql/queries",
            endpoint=query_id,
            api_version=api_version,
            json_body=query_changes,
        )

    def delete_sql_query(self, query_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(query_id, "query_id")
        return self.request_versioned(
            "DELETE",
            "sql/queries",
            endpoint=query_id,
            api_version=api_version,
        )

    # Lakeview Dashboards (dashboards scope)
    def list_dashboards(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "lakeview/dashboards",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_dashboard(self, dashboard_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "lakeview/dashboards",
            endpoint="",
            api_version=api_version,
            json_body=dashboard_spec,
        )

    def get_dashboard(self, dashboard_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(dashboard_id, "dashboard_id")
        return self.request_versioned(
            "GET",
            "lakeview/dashboards",
            endpoint=dashboard_id,
            api_version=api_version,
        )

    def update_dashboard(
        self, dashboard_id: str, dashboard_changes: dict[str, Any], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(dashboard_id, "dashboard_id")
        return self.request_versioned(
            "PATCH",
            "lakeview/dashboards",
            endpoint=dashboard_id,
            api_version=api_version,
            json_body=dashboard_changes,
        )

    def trash_dashboard(self, dashboard_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(dashboard_id, "dashboard_id")
        return self.request_versioned(
            "POST",
            "lakeview/dashboards",
            endpoint=f"{dashboard_id}/trash",
            api_version=api_version,
        )

    def publish_dashboard(self, dashboard_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(dashboard_id, "dashboard_id")
        return self.request_versioned(
            "POST",
            "lakeview/dashboards",
            endpoint=f"{dashboard_id}/published",
            api_version=api_version,
        )

    def unpublish_dashboard(self, dashboard_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(dashboard_id, "dashboard_id")
        return self.request_versioned(
            "DELETE",
            "lakeview/dashboards",
            endpoint=f"{dashboard_id}/published",
            api_version=api_version,
        )

    # Apps scope
    def list_apps(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "apps",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_app(self, app_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "apps",
            endpoint="",
            api_version=api_version,
            json_body=app_spec,
        )

    def get_app(self, app_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(app_name, "app_name")
        return self.request_versioned(
            "GET",
            "apps",
            endpoint=app_name,
            api_version=api_version,
        )

    def update_app(self, app_name: str, app_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(app_name, "app_name")
        return self.request_versioned(
            "PATCH",
            "apps",
            endpoint=app_name,
            api_version=api_version,
            json_body=app_changes,
        )

    def delete_app(self, app_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(app_name, "app_name")
        return self.request_versioned(
            "DELETE",
            "apps",
            endpoint=app_name,
            api_version=api_version,
        )

    def start_app(self, app_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(app_name, "app_name")
        return self.request_versioned(
            "POST",
            "apps",
            endpoint=f"{app_name}/start",
            api_version=api_version,
        )

    def stop_app(self, app_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(app_name, "app_name")
        return self.request_versioned(
            "POST",
            "apps",
            endpoint=f"{app_name}/stop",
            api_version=api_version,
        )

    def get_app_permissions(self, app_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(app_name, "app_name")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"apps/{app_name}",
            api_version=api_version,
        )

    def set_app_permissions(
        self, app_name: str, access_control_list: list[dict[str, Any]], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(app_name, "app_name")
        return self.request_versioned(
            "PUT",
            "permissions",
            endpoint=f"apps/{app_name}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def update_app_permissions(
        self, app_name: str, access_control_list: list[dict[str, Any]], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(app_name, "app_name")
        return self.request_versioned(
            "PATCH",
            "permissions",
            endpoint=f"apps/{app_name}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def get_app_permission_levels(self, app_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(app_name, "app_name")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"apps/{app_name}/permissionLevels",
            api_version=api_version,
        )

    # Authentication scope (token-management subset)
    def list_all_tokens(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "token-management",
            endpoint="tokens",
            api_version=api_version,
            paginate=True,
        )

    def get_token_info(self, token_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(token_id, "token_id")
        return self.request_versioned(
            "GET",
            "token-management",
            endpoint=f"tokens/{token_id}",
            api_version=api_version,
        )

    # Command Execution scope
    def create_execution_context(
        self,
        cluster_id: str,
        *,
        language: Optional[str] = None,
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
        payload: dict[str, Any] = {"cluster_id": cluster_id}
        if language:
            payload["language"] = language
        return self.request_versioned(
            "POST",
            "command-execution",
            endpoint="contexts/create",
            api_version=api_version,
            json_body=payload,
        )

    def run_command(
        self,
        context_id: str,
        command: str,
        *,
        language: Optional[str] = None,
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(context_id, "context_id")
        self._require_non_empty_string(command, "command")
        payload: dict[str, Any] = {"context_id": context_id, "command": command}
        if language:
            payload["language"] = language
        return self.request_versioned(
            "POST",
            "command-execution",
            endpoint="commands/execute",
            api_version=api_version,
            json_body=payload,
        )

    def get_command_status(self, context_id: str, command_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(context_id, "context_id")
        self._require_non_empty_string(command_id, "command_id")
        return self.request_versioned(
            "GET",
            "command-execution",
            endpoint="commands/status",
            api_version=api_version,
            params={"context_id": context_id, "command_id": command_id},
        )

    def cancel_command(self, context_id: str, command_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(context_id, "context_id")
        self._require_non_empty_string(command_id, "command_id")
        return self.request_versioned(
            "POST",
            "command-execution",
            endpoint="commands/cancel",
            api_version=api_version,
            json_body={"context_id": context_id, "command_id": command_id},
        )

    def delete_execution_context(self, context_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(context_id, "context_id")
        return self.request_versioned(
            "POST",
            "command-execution",
            endpoint="contexts/destroy",
            api_version=api_version,
            json_body={"context_id": context_id},
        )

    # Clean Rooms scope
    def list_clean_rooms(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "clean-rooms",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_clean_room(self, clean_room_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "clean-rooms",
            endpoint="",
            api_version=api_version,
            json_body=clean_room_spec,
        )

    def get_clean_room(self, clean_room_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(clean_room_name, "clean_room_name")
        return self.request_versioned(
            "GET",
            "clean-rooms",
            endpoint=clean_room_name,
            api_version=api_version,
        )

    def update_clean_room(
        self, clean_room_name: str, clean_room_changes: dict[str, Any], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(clean_room_name, "clean_room_name")
        return self.request_versioned(
            "PATCH",
            "clean-rooms",
            endpoint=clean_room_name,
            api_version=api_version,
            json_body=clean_room_changes,
        )

    def delete_clean_room(self, clean_room_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(clean_room_name, "clean_room_name")
        return self.request_versioned(
            "DELETE",
            "clean-rooms",
            endpoint=clean_room_name,
            api_version=api_version,
        )

    def list_clean_room_assets(self, clean_room_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(clean_room_name, "clean_room_name")
        return self.request_versioned(
            "GET",
            "clean-rooms",
            endpoint=f"{clean_room_name}/assets",
            api_version=api_version,
            paginate=True,
        )

    def create_clean_room_asset(
        self, clean_room_name: str, asset_spec: dict[str, Any], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(clean_room_name, "clean_room_name")
        return self.request_versioned(
            "POST",
            "clean-rooms",
            endpoint=f"{clean_room_name}/assets",
            api_version=api_version,
            json_body=asset_spec,
        )

    def get_clean_room_asset(self, clean_room_name: str, asset_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(clean_room_name, "clean_room_name")
        self._require_non_empty_string(asset_name, "asset_name")
        return self.request_versioned(
            "GET",
            "clean-rooms",
            endpoint=f"{clean_room_name}/assets/{asset_name}",
            api_version=api_version,
        )

    def update_clean_room_asset(
        self,
        clean_room_name: str,
        asset_name: str,
        asset_changes: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(clean_room_name, "clean_room_name")
        self._require_non_empty_string(asset_name, "asset_name")
        return self.request_versioned(
            "PATCH",
            "clean-rooms",
            endpoint=f"{clean_room_name}/assets/{asset_name}",
            api_version=api_version,
            json_body=asset_changes,
        )

    def delete_clean_room_asset(self, clean_room_name: str, asset_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(clean_room_name, "clean_room_name")
        self._require_non_empty_string(asset_name, "asset_name")
        return self.request_versioned(
            "DELETE",
            "clean-rooms",
            endpoint=f"{clean_room_name}/assets/{asset_name}",
            api_version=api_version,
        )

    # Data Quality Monitoring scope
    def list_monitors(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "data-quality-monitors",
            endpoint="monitors",
            api_version=api_version,
            paginate=True,
        )

    def create_monitor(self, monitor_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "data-quality-monitors",
            endpoint="monitors",
            api_version=api_version,
            json_body=monitor_spec,
        )

    def get_monitor(self, monitor_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        return self.request_versioned(
            "GET",
            "data-quality-monitors",
            endpoint=f"monitors/{monitor_id}",
            api_version=api_version,
        )

    def update_monitor(self, monitor_id: str, monitor_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        return self.request_versioned(
            "PATCH",
            "data-quality-monitors",
            endpoint=f"monitors/{monitor_id}",
            api_version=api_version,
            json_body=monitor_changes,
        )

    def delete_monitor(self, monitor_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        return self.request_versioned(
            "DELETE",
            "data-quality-monitors",
            endpoint=f"monitors/{monitor_id}",
            api_version=api_version,
        )

    def list_monitor_refreshes(self, monitor_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        return self.request_versioned(
            "GET",
            "data-quality-monitors",
            endpoint=f"monitors/{monitor_id}/refreshes",
            api_version=api_version,
            paginate=True,
        )

    def create_monitor_refresh(self, monitor_id: str, refresh_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        return self.request_versioned(
            "POST",
            "data-quality-monitors",
            endpoint=f"monitors/{monitor_id}/refreshes",
            api_version=api_version,
            json_body=refresh_spec,
        )

    def get_monitor_refresh(self, monitor_id: str, refresh_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        self._require_non_empty_string(refresh_id, "refresh_id")
        return self.request_versioned(
            "GET",
            "data-quality-monitors",
            endpoint=f"monitors/{monitor_id}/refreshes/{refresh_id}",
            api_version=api_version,
        )

    def delete_monitor_refresh(self, monitor_id: str, refresh_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        self._require_non_empty_string(refresh_id, "refresh_id")
        return self.request_versioned(
            "DELETE",
            "data-quality-monitors",
            endpoint=f"monitors/{monitor_id}/refreshes/{refresh_id}",
            api_version=api_version,
        )

    def update_monitor_refresh(
        self,
        monitor_id: str,
        refresh_id: str,
        refresh_changes: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        self._require_non_empty_string(refresh_id, "refresh_id")
        return self.request_versioned(
            "PATCH",
            "data-quality-monitors",
            endpoint=f"monitors/{monitor_id}/refreshes/{refresh_id}",
            api_version=api_version,
            json_body=refresh_changes,
        )

    def cancel_monitor_refresh(self, monitor_id: str, refresh_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        self._require_non_empty_string(refresh_id, "refresh_id")
        return self.request_versioned(
            "POST",
            "data-quality-monitors",
            endpoint=f"monitors/{monitor_id}/refreshes/{refresh_id}/cancel",
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

    def get_instance_pool_permissions(self, instance_pool_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(instance_pool_id, "instance_pool_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"instance-pools/{instance_pool_id}",
            api_version=api_version,
        )

    def set_instance_pool_permissions(
        self,
        instance_pool_id: str,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(instance_pool_id, "instance_pool_id")
        return self.request_versioned(
            "PUT",
            "permissions",
            endpoint=f"instance-pools/{instance_pool_id}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def update_instance_pool_permissions(
        self,
        instance_pool_id: str,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(instance_pool_id, "instance_pool_id")
        return self.request_versioned(
            "PATCH",
            "permissions",
            endpoint=f"instance-pools/{instance_pool_id}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def get_instance_pool_permission_levels(self, instance_pool_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(instance_pool_id, "instance_pool_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"instance-pools/{instance_pool_id}/permissionLevels",
            api_version=api_version,
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

    # Files scope
    def list_files_directory(self, path: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "GET",
            "files",
            endpoint="directories",
            api_version=api_version,
            params={"path": path},
            paginate=True,
        )

    def create_files_directory(self, path: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "POST",
            "files",
            endpoint="directories",
            api_version=api_version,
            json_body={"path": path},
        )

    def delete_files_directory(self, path: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "DELETE",
            "files",
            endpoint="directories",
            api_version=api_version,
            params={"path": path},
        )

    def get_files_directory_metadata(self, path: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "GET",
            "files",
            endpoint="directories/metadata",
            api_version=api_version,
            params={"path": path},
        )

    def download_file(self, path: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "GET",
            "files",
            endpoint="files",
            api_version=api_version,
            params={"path": path},
        )

    def upload_file(
        self,
        path: str,
        contents_base64: str,
        *,
        overwrite: bool = False,
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(path, "path")
        self._require_non_empty_string(contents_base64, "contents_base64")
        return self.request_versioned(
            "POST",
            "files",
            endpoint="files",
            api_version=api_version,
            json_body={"path": path, "contents": contents_base64, "overwrite": overwrite},
        )

    def delete_file(self, path: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "DELETE",
            "files",
            endpoint="files",
            api_version=api_version,
            params={"path": path},
        )

    def get_file_metadata(self, path: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(path, "path")
        return self.request_versioned(
            "GET",
            "files",
            endpoint="files/metadata",
            api_version=api_version,
            params={"path": path},
        )

    # Instance Profiles scope
    def list_instance_profiles(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "instance-profiles",
            endpoint="list",
            api_version=api_version,
            paginate=True,
        )

    def add_instance_profile(self, instance_profile_arn: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(instance_profile_arn, "instance_profile_arn")
        return self.request_versioned(
            "POST",
            "instance-profiles",
            endpoint="add",
            api_version=api_version,
            json_body={"instance_profile_arn": instance_profile_arn},
        )

    def edit_instance_profile(
        self,
        instance_profile_arn: str,
        *,
        is_meta_instance_profile: Optional[bool] = None,
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(instance_profile_arn, "instance_profile_arn")
        payload: dict[str, Any] = {"instance_profile_arn": instance_profile_arn}
        if is_meta_instance_profile is not None:
            payload["is_meta_instance_profile"] = is_meta_instance_profile
        return self.request_versioned(
            "POST",
            "instance-profiles",
            endpoint="edit",
            api_version=api_version,
            json_body=payload,
        )

    def remove_instance_profile(self, instance_profile_arn: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(instance_profile_arn, "instance_profile_arn")
        return self.request_versioned(
            "POST",
            "instance-profiles",
            endpoint="remove",
            api_version=api_version,
            json_body={"instance_profile_arn": instance_profile_arn},
        )

    # Libraries scope
    def get_all_library_statuses(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "libraries",
            endpoint="all-cluster-statuses",
            api_version=api_version,
            paginate=True,
        )

    def get_library_status(self, cluster_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
        return self.request_versioned(
            "GET",
            "libraries",
            endpoint="cluster-status",
            api_version=api_version,
            params={"cluster_id": cluster_id},
        )

    def install_libraries(self, cluster_id: str, libraries: list[dict[str, Any]], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
        return self.request_versioned(
            "POST",
            "libraries",
            endpoint="install",
            api_version=api_version,
            json_body={"cluster_id": cluster_id, "libraries": libraries},
        )

    def uninstall_libraries(self, cluster_id: str, libraries: list[dict[str, Any]], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(cluster_id, "cluster_id")
        return self.request_versioned(
            "POST",
            "libraries",
            endpoint="uninstall",
            api_version=api_version,
            json_body={"cluster_id": cluster_id, "libraries": libraries},
        )

    # Networking scope (IP access lists)
    def list_ip_access_lists(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "ip-access-lists",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_ip_access_list(self, access_list_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "ip-access-lists",
            endpoint="",
            api_version=api_version,
            json_body=access_list_spec,
        )

    def get_ip_access_list(self, list_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(list_id, "list_id")
        return self.request_versioned(
            "GET",
            "ip-access-lists",
            endpoint=list_id,
            api_version=api_version,
        )

    def replace_ip_access_list(self, list_id: str, access_list_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(list_id, "list_id")
        return self.request_versioned(
            "PUT",
            "ip-access-lists",
            endpoint=list_id,
            api_version=api_version,
            json_body=access_list_spec,
        )

    def update_ip_access_list(self, list_id: str, access_list_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(list_id, "list_id")
        return self.request_versioned(
            "PATCH",
            "ip-access-lists",
            endpoint=list_id,
            api_version=api_version,
            json_body=access_list_changes,
        )

    def delete_ip_access_list(self, list_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(list_id, "list_id")
        return self.request_versioned(
            "DELETE",
            "ip-access-lists",
            endpoint=list_id,
            api_version=api_version,
        )

    # Notifications scope
    def list_notification_destinations(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "notification-destinations",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_notification_destination(self, destination_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "notification-destinations",
            endpoint="",
            api_version=api_version,
            json_body=destination_spec,
        )

    def get_notification_destination(self, destination_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(destination_id, "destination_id")
        return self.request_versioned(
            "GET",
            "notification-destinations",
            endpoint=destination_id,
            api_version=api_version,
        )

    def update_notification_destination(
        self, destination_id: str, destination_changes: dict[str, Any], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(destination_id, "destination_id")
        return self.request_versioned(
            "PATCH",
            "notification-destinations",
            endpoint=destination_id,
            api_version=api_version,
            json_body=destination_changes,
        )

    def delete_notification_destination(self, destination_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(destination_id, "destination_id")
        return self.request_versioned(
            "DELETE",
            "notification-destinations",
            endpoint=destination_id,
            api_version=api_version,
        )

    # Pipelines scope
    def get_pipeline_permissions(self, pipeline_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"pipelines/{pipeline_id}",
            api_version=api_version,
        )

    def set_pipeline_permissions(
        self,
        pipeline_id: str,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "PUT",
            "permissions",
            endpoint=f"pipelines/{pipeline_id}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def update_pipeline_permissions(
        self,
        pipeline_id: str,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "PATCH",
            "permissions",
            endpoint=f"pipelines/{pipeline_id}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def get_pipeline_permission_levels(self, pipeline_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"pipelines/{pipeline_id}/permissionLevels",
            api_version=api_version,
        )

    def list_pipelines(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "pipelines",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_pipeline(self, pipeline_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "pipelines",
            endpoint="",
            api_version=api_version,
            json_body=pipeline_spec,
        )

    def get_pipeline(self, pipeline_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "GET",
            "pipelines",
            endpoint=pipeline_id,
            api_version=api_version,
        )

    def edit_pipeline(self, pipeline_id: str, pipeline_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "PUT",
            "pipelines",
            endpoint=pipeline_id,
            api_version=api_version,
            json_body=pipeline_changes,
        )

    def delete_pipeline(self, pipeline_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "DELETE",
            "pipelines",
            endpoint=pipeline_id,
            api_version=api_version,
        )

    def start_pipeline(self, pipeline_id: str, start_spec: Optional[dict[str, Any]] = None, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "POST",
            "pipelines",
            endpoint=f"{pipeline_id}/updates",
            api_version=api_version,
            json_body=start_spec,
        )

    def stop_pipeline(self, pipeline_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "POST",
            "pipelines",
            endpoint=f"{pipeline_id}/stop",
            api_version=api_version,
        )

    def list_pipeline_events(self, pipeline_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "GET",
            "pipelines",
            endpoint=f"{pipeline_id}/events",
            api_version=api_version,
            paginate=True,
        )

    def list_pipeline_updates(self, pipeline_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        return self.request_versioned(
            "GET",
            "pipelines",
            endpoint=f"{pipeline_id}/updates",
            api_version=api_version,
            paginate=True,
        )

    def get_pipeline_update(self, pipeline_id: str, update_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(pipeline_id, "pipeline_id")
        self._require_non_empty_string(update_id, "update_id")
        return self.request_versioned(
            "GET",
            "pipelines",
            endpoint=f"{pipeline_id}/updates/{update_id}",
            api_version=api_version,
        )

    # Query History scope
    def list_query_history(self, *, max_results: Optional[int] = None, api_version: str = "2.0") -> Any:
        params: dict[str, Any] = {}
        if max_results is not None:
            self._require_positive_int(max_results, "max_results")
            params["max_results"] = max_results
        return self.request_versioned(
            "GET",
            "sql/history/queries",
            endpoint="",
            api_version=api_version,
            params=params or None,
            paginate=True,
        )

    # Model Serving scope
    def get_serving_endpoint_permissions(self, endpoint_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"serving-endpoints/{endpoint_name}",
            api_version=api_version,
        )

    def set_serving_endpoint_permissions(
        self,
        endpoint_name: str,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "PUT",
            "permissions",
            endpoint=f"serving-endpoints/{endpoint_name}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def update_serving_endpoint_permissions(
        self,
        endpoint_name: str,
        access_control_list: list[dict[str, Any]],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "PATCH",
            "permissions",
            endpoint=f"serving-endpoints/{endpoint_name}",
            api_version=api_version,
            json_body={"access_control_list": access_control_list},
        )

    def get_serving_endpoint_permission_levels(self, endpoint_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "GET",
            "permissions",
            endpoint=f"serving-endpoints/{endpoint_name}/permissionLevels",
            api_version=api_version,
        )

    def list_serving_endpoints(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "serving-endpoints",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_serving_endpoint(self, endpoint_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "serving-endpoints",
            endpoint="",
            api_version=api_version,
            json_body=endpoint_spec,
        )

    def get_serving_endpoint(self, endpoint_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "GET",
            "serving-endpoints",
            endpoint=endpoint_name,
            api_version=api_version,
        )

    def update_serving_endpoint_config(
        self,
        endpoint_name: str,
        config_changes: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "PUT",
            "serving-endpoints",
            endpoint=f"{endpoint_name}/config",
            api_version=api_version,
            json_body=config_changes,
        )

    def delete_serving_endpoint(self, endpoint_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "DELETE",
            "serving-endpoints",
            endpoint=endpoint_name,
            api_version=api_version,
        )

    def query_serving_endpoint(self, endpoint_name: str, query_payload: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "POST",
            "serving-endpoints",
            endpoint=f"{endpoint_name}/invocations",
            api_version=api_version,
            json_body=query_payload,
        )

    # Marketplace scope
    def list_marketplace_listings(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "marketplace-consumer/listings",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def get_marketplace_listing(self, listing_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(listing_id, "listing_id")
        return self.request_versioned(
            "GET",
            "marketplace-consumer/listings",
            endpoint=listing_id,
            api_version=api_version,
        )

    def search_marketplace_listings(self, search_payload: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "marketplace-consumer/listings",
            endpoint="search",
            api_version=api_version,
            json_body=search_payload,
        )

    def list_marketplace_installations(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "marketplace-consumer/installations",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def install_marketplace_listing(self, installation_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "marketplace-consumer/installations",
            endpoint="",
            api_version=api_version,
            json_body=installation_spec,
        )

    def uninstall_marketplace_installation(self, installation_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(installation_id, "installation_id")
        return self.request_versioned(
            "DELETE",
            "marketplace-consumer/installations",
            endpoint=installation_id,
            api_version=api_version,
        )

    # Genie scope
    def list_genie_spaces(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "genie/spaces",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_genie_space(self, space_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "genie/spaces",
            endpoint="",
            api_version=api_version,
            json_body=space_spec,
        )

    def get_genie_space(self, space_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(space_id, "space_id")
        return self.request_versioned(
            "GET",
            "genie/spaces",
            endpoint=space_id,
            api_version=api_version,
        )

    def update_genie_space(self, space_id: str, space_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(space_id, "space_id")
        return self.request_versioned(
            "PATCH",
            "genie/spaces",
            endpoint=space_id,
            api_version=api_version,
            json_body=space_changes,
        )

    def delete_genie_space(self, space_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(space_id, "space_id")
        return self.request_versioned(
            "DELETE",
            "genie/spaces",
            endpoint=space_id,
            api_version=api_version,
        )

    # Global Init Scripts scope
    def list_global_init_scripts(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "global-init-scripts",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_global_init_script(self, script_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "global-init-scripts",
            endpoint="",
            api_version=api_version,
            json_body=script_spec,
        )

    def get_global_init_script(self, script_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(script_id, "script_id")
        return self.request_versioned(
            "GET",
            "global-init-scripts",
            endpoint=script_id,
            api_version=api_version,
        )

    def update_global_init_script(self, script_id: str, script_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(script_id, "script_id")
        return self.request_versioned(
            "PATCH",
            "global-init-scripts",
            endpoint=script_id,
            api_version=api_version,
            json_body=script_changes,
        )

    def delete_global_init_script(self, script_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(script_id, "script_id")
        return self.request_versioned(
            "DELETE",
            "global-init-scripts",
            endpoint=script_id,
            api_version=api_version,
        )

    # Settings scope
    def list_setting_keys_metadata(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "settings-v2",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def get_workspace_setting(self, setting_key: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(setting_key, "setting_key")
        return self.request_versioned(
            "GET",
            "settings-v2",
            endpoint=setting_key,
            api_version=api_version,
        )

    def update_workspace_setting(self, setting_key: str, setting_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(setting_key, "setting_key")
        return self.request_versioned(
            "PATCH",
            "settings-v2",
            endpoint=setting_key,
            api_version=api_version,
            json_body=setting_changes,
        )

    def get_workspace_conf(self, keys: Optional[list[str]] = None, api_version: str = "2.0") -> Any:
        params: Optional[dict[str, Any]] = None
        if keys:
            params = {"keys": ",".join(keys)}
        return self.request_versioned(
            "GET",
            "workspace-conf",
            endpoint="",
            api_version=api_version,
            params=params,
        )

    def set_workspace_conf(self, custom_config: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "PATCH",
            "workspace-conf",
            endpoint="",
            api_version=api_version,
            json_body={"custom_config": custom_config},
        )

    # Tags scope
    def list_tag_policies(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "tags/policies",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_tag_policy(self, policy_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "tags/policies",
            endpoint="",
            api_version=api_version,
            json_body=policy_spec,
        )

    def get_tag_policy(self, policy_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(policy_id, "policy_id")
        return self.request_versioned(
            "GET",
            "tags/policies",
            endpoint=policy_id,
            api_version=api_version,
        )

    def update_tag_policy(self, policy_id: str, policy_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(policy_id, "policy_id")
        return self.request_versioned(
            "PATCH",
            "tags/policies",
            endpoint=policy_id,
            api_version=api_version,
            json_body=policy_changes,
        )

    def delete_tag_policy(self, policy_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(policy_id, "policy_id")
        return self.request_versioned(
            "DELETE",
            "tags/policies",
            endpoint=policy_id,
            api_version=api_version,
        )

    def list_tag_assignments(self, entity_type: str, entity_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(entity_type, "entity_type")
        self._require_non_empty_string(entity_id, "entity_id")
        return self.request_versioned(
            "GET",
            "tags/assignments",
            endpoint=f"{entity_type}/{entity_id}",
            api_version=api_version,
            paginate=True,
        )

    def create_tag_assignment(
        self,
        entity_type: str,
        entity_id: str,
        assignment_spec: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(entity_type, "entity_type")
        self._require_non_empty_string(entity_id, "entity_id")
        return self.request_versioned(
            "POST",
            "tags/assignments",
            endpoint=f"{entity_type}/{entity_id}",
            api_version=api_version,
            json_body=assignment_spec,
        )

    def get_tag_assignment(self, entity_type: str, entity_id: str, assignment_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(entity_type, "entity_type")
        self._require_non_empty_string(entity_id, "entity_id")
        self._require_non_empty_string(assignment_id, "assignment_id")
        return self.request_versioned(
            "GET",
            "tags/assignments",
            endpoint=f"{entity_type}/{entity_id}/{assignment_id}",
            api_version=api_version,
        )

    def update_tag_assignment(
        self,
        entity_type: str,
        entity_id: str,
        assignment_id: str,
        assignment_changes: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(entity_type, "entity_type")
        self._require_non_empty_string(entity_id, "entity_id")
        self._require_non_empty_string(assignment_id, "assignment_id")
        return self.request_versioned(
            "PATCH",
            "tags/assignments",
            endpoint=f"{entity_type}/{entity_id}/{assignment_id}",
            api_version=api_version,
            json_body=assignment_changes,
        )

    def delete_tag_assignment(self, entity_type: str, entity_id: str, assignment_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(entity_type, "entity_type")
        self._require_non_empty_string(entity_id, "entity_id")
        self._require_non_empty_string(assignment_id, "assignment_id")
        return self.request_versioned(
            "DELETE",
            "tags/assignments",
            endpoint=f"{entity_type}/{entity_id}/{assignment_id}",
            api_version=api_version,
        )

    # Quality Monitor scope
    def list_quality_monitors(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "quality-monitor-v2/monitors",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_quality_monitor(self, monitor_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "quality-monitor-v2/monitors",
            endpoint="",
            api_version=api_version,
            json_body=monitor_spec,
        )

    def get_quality_monitor(self, monitor_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        return self.request_versioned(
            "GET",
            "quality-monitor-v2/monitors",
            endpoint=monitor_id,
            api_version=api_version,
        )

    def update_quality_monitor(self, monitor_id: str, monitor_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        return self.request_versioned(
            "PATCH",
            "quality-monitor-v2/monitors",
            endpoint=monitor_id,
            api_version=api_version,
            json_body=monitor_changes,
        )

    def delete_quality_monitor(self, monitor_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(monitor_id, "monitor_id")
        return self.request_versioned(
            "DELETE",
            "quality-monitor-v2/monitors",
            endpoint=monitor_id,
            api_version=api_version,
        )

    # Postgres scope (projects/branches)
    def list_postgres_projects(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "postgres/projects",
            endpoint="",
            api_version=api_version,
            paginate=True,
        )

    def create_postgres_project(self, project_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "postgres/projects",
            endpoint="",
            api_version=api_version,
            json_body=project_spec,
        )

    def get_postgres_project(self, project_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(project_id, "project_id")
        return self.request_versioned(
            "GET",
            "postgres/projects",
            endpoint=project_id,
            api_version=api_version,
        )

    def update_postgres_project(self, project_id: str, project_changes: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(project_id, "project_id")
        return self.request_versioned(
            "PATCH",
            "postgres/projects",
            endpoint=project_id,
            api_version=api_version,
            json_body=project_changes,
        )

    def delete_postgres_project(self, project_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(project_id, "project_id")
        return self.request_versioned(
            "DELETE",
            "postgres/projects",
            endpoint=project_id,
            api_version=api_version,
        )

    def list_postgres_branches(self, project_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(project_id, "project_id")
        return self.request_versioned(
            "GET",
            "postgres/projects",
            endpoint=f"{project_id}/branches",
            api_version=api_version,
            paginate=True,
        )

    def create_postgres_branch(self, project_id: str, branch_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        self._require_non_empty_string(project_id, "project_id")
        return self.request_versioned(
            "POST",
            "postgres/projects",
            endpoint=f"{project_id}/branches",
            api_version=api_version,
            json_body=branch_spec,
        )

    def get_postgres_branch(self, project_id: str, branch_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(project_id, "project_id")
        self._require_non_empty_string(branch_id, "branch_id")
        return self.request_versioned(
            "GET",
            "postgres/projects",
            endpoint=f"{project_id}/branches/{branch_id}",
            api_version=api_version,
        )

    def delete_postgres_branch(self, project_id: str, branch_id: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(project_id, "project_id")
        self._require_non_empty_string(branch_id, "branch_id")
        return self.request_versioned(
            "DELETE",
            "postgres/projects",
            endpoint=f"{project_id}/branches/{branch_id}",
            api_version=api_version,
        )

    # Unity Catalog scope (additional connections/external-locations wrappers)
    def list_uc_connections(self, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint="connections",
            api_version=api_version,
            paginate=True,
        )

    def create_uc_connection(self, connection_spec: dict[str, Any], api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "POST",
            "unity-catalog",
            endpoint="connections",
            api_version=api_version,
            json_body=connection_spec,
        )

    def get_uc_connection(self, name: str, api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint=f"connections/{name}",
            api_version=api_version,
        )

    def update_uc_connection(self, name: str, connection_changes: dict[str, Any], api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "PATCH",
            "unity-catalog",
            endpoint=f"connections/{name}",
            api_version=api_version,
            json_body=connection_changes,
        )

    def delete_uc_connection(self, name: str, api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "DELETE",
            "unity-catalog",
            endpoint=f"connections/{name}",
            api_version=api_version,
        )

    def list_uc_external_locations(self, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint="external-locations",
            api_version=api_version,
            paginate=True,
        )

    def create_uc_external_location(self, location_spec: dict[str, Any], api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "POST",
            "unity-catalog",
            endpoint="external-locations",
            api_version=api_version,
            json_body=location_spec,
        )

    def get_uc_external_location(self, name: str, api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint=f"external-locations/{name}",
            api_version=api_version,
        )

    def update_uc_external_location(self, name: str, location_changes: dict[str, Any], api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "PATCH",
            "unity-catalog",
            endpoint=f"external-locations/{name}",
            api_version=api_version,
            json_body=location_changes,
        )

    def delete_uc_external_location(self, name: str, api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "DELETE",
            "unity-catalog",
            endpoint=f"external-locations/{name}",
            api_version=api_version,
        )

    # Vector Search scope
    def list_vector_search_endpoints(self, api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "GET",
            "vector-search",
            endpoint="endpoints",
            api_version=api_version,
            paginate=True,
        )

    def create_vector_search_endpoint(self, endpoint_spec: dict[str, Any], api_version: str = "2.0") -> Any:
        return self.request_versioned(
            "POST",
            "vector-search",
            endpoint="endpoints",
            api_version=api_version,
            json_body=endpoint_spec,
        )

    def get_vector_search_endpoint(self, endpoint_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "GET",
            "vector-search",
            endpoint=f"endpoints/{endpoint_name}",
            api_version=api_version,
        )

    def update_vector_search_endpoint(
        self, endpoint_name: str, endpoint_changes: dict[str, Any], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "PATCH",
            "vector-search",
            endpoint=f"endpoints/{endpoint_name}",
            api_version=api_version,
            json_body=endpoint_changes,
        )

    def delete_vector_search_endpoint(self, endpoint_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "DELETE",
            "vector-search",
            endpoint=f"endpoints/{endpoint_name}",
            api_version=api_version,
        )

    def list_vector_search_indexes(self, endpoint_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "GET",
            "vector-search",
            endpoint=f"endpoints/{endpoint_name}/indexes",
            api_version=api_version,
            paginate=True,
        )

    def create_vector_search_index(
        self, endpoint_name: str, index_spec: dict[str, Any], api_version: str = "2.0"
    ) -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        return self.request_versioned(
            "POST",
            "vector-search",
            endpoint=f"endpoints/{endpoint_name}/indexes",
            api_version=api_version,
            json_body=index_spec,
        )

    def get_vector_search_index(self, endpoint_name: str, index_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        self._require_non_empty_string(index_name, "index_name")
        return self.request_versioned(
            "GET",
            "vector-search",
            endpoint=f"endpoints/{endpoint_name}/indexes/{index_name}",
            api_version=api_version,
        )

    def delete_vector_search_index(self, endpoint_name: str, index_name: str, api_version: str = "2.0") -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        self._require_non_empty_string(index_name, "index_name")
        return self.request_versioned(
            "DELETE",
            "vector-search",
            endpoint=f"endpoints/{endpoint_name}/indexes/{index_name}",
            api_version=api_version,
        )

    def query_vector_search_index(
        self,
        endpoint_name: str,
        index_name: str,
        query_payload: dict[str, Any],
        api_version: str = "2.0",
    ) -> Any:
        self._require_non_empty_string(endpoint_name, "endpoint_name")
        self._require_non_empty_string(index_name, "index_name")
        return self.request_versioned(
            "POST",
            "vector-search",
            endpoint=f"endpoints/{endpoint_name}/indexes/{index_name}/query",
            api_version=api_version,
            json_body=query_payload,
        )

    # Delta Sharing scope
    def list_sharing_providers(self, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint="providers",
            api_version=api_version,
            paginate=True,
        )

    def create_sharing_provider(self, provider_spec: dict[str, Any], api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "POST",
            "unity-catalog",
            endpoint="providers",
            api_version=api_version,
            json_body=provider_spec,
        )

    def get_sharing_provider(self, name: str, api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint=f"providers/{name}",
            api_version=api_version,
        )

    def update_sharing_provider(self, name: str, provider_changes: dict[str, Any], api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "PATCH",
            "unity-catalog",
            endpoint=f"providers/{name}",
            api_version=api_version,
            json_body=provider_changes,
        )

    def delete_sharing_provider(self, name: str, api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "DELETE",
            "unity-catalog",
            endpoint=f"providers/{name}",
            api_version=api_version,
        )

    def list_share_recipients(self, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint="recipients",
            api_version=api_version,
            paginate=True,
        )

    def create_share_recipient(self, recipient_spec: dict[str, Any], api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "POST",
            "unity-catalog",
            endpoint="recipients",
            api_version=api_version,
            json_body=recipient_spec,
        )

    def get_share_recipient(self, name: str, api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint=f"recipients/{name}",
            api_version=api_version,
        )

    def update_share_recipient(self, name: str, recipient_changes: dict[str, Any], api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "PATCH",
            "unity-catalog",
            endpoint=f"recipients/{name}",
            api_version=api_version,
            json_body=recipient_changes,
        )

    def delete_share_recipient(self, name: str, api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "DELETE",
            "unity-catalog",
            endpoint=f"recipients/{name}",
            api_version=api_version,
        )

    def list_shares(self, api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint="shares",
            api_version=api_version,
            paginate=True,
        )

    def create_share(self, share_spec: dict[str, Any], api_version: str = "2.1") -> Any:
        return self.request_versioned(
            "POST",
            "unity-catalog",
            endpoint="shares",
            api_version=api_version,
            json_body=share_spec,
        )

    def get_share(self, name: str, api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "GET",
            "unity-catalog",
            endpoint=f"shares/{name}",
            api_version=api_version,
        )

    def update_share(self, name: str, share_changes: dict[str, Any], api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "PATCH",
            "unity-catalog",
            endpoint=f"shares/{name}",
            api_version=api_version,
            json_body=share_changes,
        )

    def delete_share(self, name: str, api_version: str = "2.1") -> Any:
        self._require_non_empty_string(name, "name")
        return self.request_versioned(
            "DELETE",
            "unity-catalog",
            endpoint=f"shares/{name}",
            api_version=api_version,
        )
