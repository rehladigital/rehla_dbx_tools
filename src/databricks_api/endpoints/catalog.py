"""Endpoint catalog starter for multi-version wrappers.

This is intentionally small in v0.1 and meant to be expanded/generated.
"""

ENDPOINT_CATALOG: dict[str, dict[str, dict[str, str]]] = {
    "workspace": {
        "2.0": {
            "clusters_create": "/api/2.0/clusters/create",
            "clusters_delete": "/api/2.0/clusters/delete",
            "clusters_edit": "/api/2.0/clusters/edit",
            "clusters_events": "/api/2.0/clusters/events",
            "clusters_get": "/api/2.0/clusters/get",
            "clusters_list": "/api/2.0/clusters/list",
            "clusters_permanent_delete": "/api/2.0/clusters/permanent-delete",
            "clusters_restart": "/api/2.0/clusters/restart",
            "clusters_start": "/api/2.0/clusters/start",
        },
        "2.1": {
            "jobs_create": "/api/2.1/jobs/create",
            "jobs_delete": "/api/2.1/jobs/delete",
            "jobs_get": "/api/2.1/jobs/get",
            "jobs_list": "/api/2.1/jobs/list",
            "jobs_reset": "/api/2.1/jobs/reset",
            "jobs_runs_cancel": "/api/2.1/jobs/runs/cancel",
            "jobs_runs_get": "/api/2.1/jobs/runs/get",
            "jobs_run_now": "/api/2.1/jobs/run-now",
        },
        "preview": {},
    },
    "account": {
        "2.0": {
            "workspaces_create": "/api/2.0/accounts/workspaces",
            "workspaces_delete": "/api/2.0/accounts/workspaces/{workspace_id}",
            "workspaces_get": "/api/2.0/accounts/workspaces/{workspace_id}",
            "workspaces_list": "/api/2.0/accounts/workspaces",
            "workspaces_update": "/api/2.0/accounts/workspaces/{workspace_id}",
        },
        "preview": {},
    },
}
