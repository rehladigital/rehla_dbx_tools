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
    monkeypatch.setenv("DATABRICKS_HOST", "https://adb-12345.6.azuredatabricks.net")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_HOST", "https://accounts.gcp.databricks.com")
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


def test_from_env_rejects_workspace_host_cloud_mismatch(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://adb-12345.6.azuredatabricks.net")
    monkeypatch.setenv("DATABRICKS_CLOUD", "aws")

    with pytest.raises(ValidationError):
        UnifiedConfig.from_env()


def test_from_env_rejects_account_host_cloud_mismatch(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_HOST", "https://accounts.gcp.databricks.com")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_CLOUD", "azure")

    with pytest.raises(ValidationError):
        UnifiedConfig.from_env()


def test_from_env_infers_workspace_cloud_from_host_when_unset(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://adb-12345.6.azuredatabricks.net")
    monkeypatch.delenv("DATABRICKS_CLOUD", raising=False)

    cfg = UnifiedConfig.from_env()

    assert cfg.workspace.cloud == "azure"


def test_from_env_infers_account_cloud_from_host_when_unset(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_HOST", "https://accounts.gcp.databricks.com")
    monkeypatch.delenv("DATABRICKS_CLOUD", raising=False)
    monkeypatch.delenv("DATABRICKS_ACCOUNT_CLOUD", raising=False)

    cfg = UnifiedConfig.from_env()

    assert cfg.account.cloud == "gcp"
