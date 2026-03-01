import pytest

from databricks_api.config import UnifiedConfig
from databricks_api.exceptions import ValidationError


def test_from_env_uses_workspace_host(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    cfg = UnifiedConfig.from_env()
    assert cfg.workspace.host == "https://dbc-test.cloud.databricks.com"


def test_from_env_normalizes_host(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "dbc-test.cloud.databricks.com")
    cfg = UnifiedConfig.from_env()
    assert cfg.workspace.host == "https://dbc-test.cloud.databricks.com"


def test_from_env_reads_workspace_and_account_cloud(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_CLOUD", "azure")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_CLOUD", "gcp")

    cfg = UnifiedConfig.from_env()

    assert cfg.workspace.cloud == "azure"
    assert cfg.account.cloud == "gcp"


def test_from_env_rejects_invalid_cloud(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_CLOUD", "invalid-cloud")

    with pytest.raises(ValidationError):
        UnifiedConfig.from_env()
