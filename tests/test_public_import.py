from rehladigital_aws_dbx_tools import DatabricksApiClient


def test_public_import_exposes_databricks_api_client():
    assert DatabricksApiClient is not None
