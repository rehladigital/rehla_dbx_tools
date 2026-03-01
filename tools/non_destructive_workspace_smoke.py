"""Non-destructive Databricks workspace smoke checks.

This script only performs read/list operations and optional metadata lookups.
It is designed for CI validation against real workspaces without changing state.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Callable

from databricks_api.client import DatabricksApiClient


def _count_records(payload: Any) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        for key in (
            "jobs",
            "runs",
            "clusters",
            "results",
            "items",
            "warehouses",
            "instance_pools",
            "policies",
            "repos",
            "catalogs",
            "schemas",
            "token_infos",
        ):
            value = payload.get(key)
            if isinstance(value, list):
                return len(value)
    return 0


def _first_from(payload: Any, key: str) -> Any:
    if isinstance(payload, dict):
        value = payload.get(key)
        if isinstance(value, list) and value:
            return value[0]
    return None


def _safe_call(
    name: str,
    fn: Callable[[], Any],
    required: bool = False,
) -> tuple[bool, Any]:
    try:
        response = fn()
        data = getattr(response, "data", response)
        print(f"[OK] {name} records={_count_records(data)}")
        return True, data
    except Exception as exc:  # pragma: no cover - integration safety path
        level = "ERROR" if required else "WARN"
        print(f"[{level}] {name} failed: {exc}")
        return False, None


def main() -> int:
    print("Starting non-destructive workspace smoke checks")
    print(
        json.dumps(
            {
                "has_DATABRICKS_HOST": bool(os.getenv("DATABRICKS_HOST")),
                "has_DBX_HOST": bool(os.getenv("DBX_HOST")),
                "has_DATABRICKS_TOKEN": bool(os.getenv("DATABRICKS_TOKEN")),
                "has_DBX_TOKEN": bool(os.getenv("DBX_TOKEN")),
            }
        )
    )

    client = DatabricksApiClient.from_env()
    if client.workspace is None:
        print("[ERROR] Workspace client not configured.")
        return 2
    workspace = client.workspace

    required_failures = 0

    jobs_ok, jobs_data = _safe_call("list_jobs", lambda: workspace.list_jobs(limit=5), required=True)
    if not jobs_ok:
        required_failures += 1

    _safe_call("list_job_runs", lambda: workspace.list_job_runs(limit=5))
    clusters_ok, clusters_data = _safe_call("list_clusters", workspace.list_clusters, required=True)
    if not clusters_ok:
        required_failures += 1

    _safe_call("list_sql_warehouses", workspace.list_sql_warehouses)
    _safe_call("list_instance_pools", workspace.list_instance_pools)
    _safe_call("list_cluster_policies", workspace.list_cluster_policies)
    repos_ok, repos_data = _safe_call("list_repos", lambda: workspace.list_repos(path_prefix="/"))
    catalogs_ok, catalogs_data = _safe_call("list_catalogs", lambda: workspace.list_catalogs(max_results=5))
    first_catalog = _first_from(catalogs_data, "catalogs")
    if catalogs_ok and isinstance(first_catalog, dict) and first_catalog.get("name"):
        catalog_name = str(first_catalog["name"])
        _safe_call("list_schemas", lambda: workspace.list_schemas(catalog_name=catalog_name, max_results=5))
    else:
        _safe_call("list_schemas", lambda: workspace.list_schemas(max_results=5))
    _safe_call("list_tokens", workspace.list_tokens)

    first_job = _first_from(jobs_data, "jobs")
    if isinstance(first_job, dict) and first_job.get("job_id"):
        job_id = int(first_job["job_id"])
        _safe_call("get_job", lambda: workspace.get_job(job_id))
        _safe_call("get_job_permissions", lambda: workspace.get_job_permissions(job_id))
        _safe_call("get_job_permission_levels", lambda: workspace.get_job_permission_levels(job_id))

    first_cluster = _first_from(clusters_data, "clusters")
    if isinstance(first_cluster, dict) and first_cluster.get("cluster_id"):
        cluster_id = str(first_cluster["cluster_id"])
        _safe_call("get_cluster", lambda: workspace.get_cluster(cluster_id))
        _safe_call("get_cluster_permissions", lambda: workspace.get_cluster_permissions(cluster_id))
        _safe_call("get_cluster_permission_levels", lambda: workspace.get_cluster_permission_levels(cluster_id))

    first_repo = _first_from(repos_data, "repos")
    if repos_ok and isinstance(first_repo, dict) and first_repo.get("id"):
        repo_id = int(first_repo["id"])
        _safe_call("get_repo", lambda: workspace.get_repo(repo_id))
        _safe_call("get_repo_permissions", lambda: workspace.get_repo_permissions(repo_id))
        _safe_call("get_repo_permission_levels", lambda: workspace.get_repo_permission_levels(repo_id))

    if required_failures > 0:
        print(f"[ERROR] Required smoke checks failed: {required_failures}")
        return 1

    print("[OK] Non-destructive workspace smoke checks completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
