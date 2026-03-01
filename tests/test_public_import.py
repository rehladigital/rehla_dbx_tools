from rehla_dbx_tools import DatabricksApiClient, detect_cloud_from_host
from rehla_dbx_tools.clients.workspace import WorkspaceClient
from rehladigital_aws_dbx_tools import DatabricksApiClient as LegacyDatabricksApiClient


def test_public_import_exposes_databricks_api_client():
    assert DatabricksApiClient is not None


def test_public_submodule_import_exposes_workspace_client():
    assert WorkspaceClient is not None


def test_legacy_namespace_remains_available_during_rename():
    assert LegacyDatabricksApiClient is not None


def test_public_import_exposes_cloud_detection_helper():
    assert detect_cloud_from_host("https://adb-12345.6.azuredatabricks.net") == "azure"
