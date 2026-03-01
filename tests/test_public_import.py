from rehladigital_aws_dbx_tools import DatabricksApiClient
from rehladigital_aws_dbx_tools.clients.workspace import WorkspaceClient


def test_public_import_exposes_databricks_api_client():
    assert DatabricksApiClient is not None


def test_public_submodule_import_exposes_workspace_client():
    assert WorkspaceClient is not None
