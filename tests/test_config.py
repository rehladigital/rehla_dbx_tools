from databricks_api.config import UnifiedConfig


def test_from_env_uses_workspace_host(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    cfg = UnifiedConfig.from_env()
    assert cfg.workspace.host == "https://dbc-test.cloud.databricks.com"


def test_from_env_normalizes_host(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "dbc-test.cloud.databricks.com")
    cfg = UnifiedConfig.from_env()
    assert cfg.workspace.host == "https://dbc-test.cloud.databricks.com"
