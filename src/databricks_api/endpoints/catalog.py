"""Endpoint catalog starter for multi-version wrappers.

This is intentionally small in v0.1 and meant to be expanded/generated.
"""

ENDPOINT_CATALOG: dict[str, dict[str, dict[str, str]]] = {
    "workspace": {
        "2.0": {
            "clusters_list": "/api/2.0/clusters/list",
        },
        "2.1": {
            "jobs_list": "/api/2.1/jobs/list",
        },
        "preview": {},
    },
    "account": {
        "2.0": {
            "workspaces_list": "/api/2.0/accounts/workspaces",
        },
        "preview": {},
    },
}
