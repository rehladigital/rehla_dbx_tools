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


def test_from_env_normalizes_cloud_databricks_net_host_typo(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "dbc-test.cloud.databricks.net")
    cfg = UnifiedConfig.from_env()
    assert cfg.workspace.host == "https://dbc-test.cloud.databricks.com"


def test_from_env_uses_dbx_host_alias_when_databricks_host_missing(monkeypatch):
    monkeypatch.delenv("DATABRICKS_HOST", raising=False)
    monkeypatch.setenv("DBX_HOST", "dbc-test.cloud.databricks.com")
    cfg = UnifiedConfig.from_env()
    assert cfg.workspace.host == "https://dbc-test.cloud.databricks.com"


def test_from_env_uses_dbx_cloud_alias(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.delenv("DATABRICKS_CLOUD", raising=False)
    monkeypatch.setenv("DBX_CLOUD", "aws")
    cfg = UnifiedConfig.from_env()
    assert cfg.workspace.cloud == "aws"


def test_from_env_reads_workspace_and_account_cloud(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://adb-12345.6.azuredatabricks.net")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_HOST", "https://accounts.gcp.databricks.com")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_ID", "acc-123")
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
    monkeypatch.setenv("DATABRICKS_ACCOUNT_ID", "acc-123")
    monkeypatch.delenv("DATABRICKS_CLOUD", raising=False)
    monkeypatch.delenv("DATABRICKS_ACCOUNT_CLOUD", raising=False)

    cfg = UnifiedConfig.from_env()

    assert cfg.account.cloud == "gcp"


def test_from_env_disables_strict_cloud_match_when_requested(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://adb-12345.6.azuredatabricks.net")
    monkeypatch.setenv("DATABRICKS_CLOUD", "aws")
    monkeypatch.setenv("DATABRICKS_STRICT_CLOUD_MATCH", "false")

    cfg = UnifiedConfig.from_env()

    assert cfg.strict_cloud_match is False
    assert cfg.workspace.cloud == "aws"


def test_from_env_requires_account_id_when_account_host_is_set(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_HOST", "https://accounts.cloud.databricks.com")
    monkeypatch.delenv("DATABRICKS_ACCOUNT_ID", raising=False)

    with pytest.raises(ValidationError):
        UnifiedConfig.from_env()


def test_with_cloud_overrides_workspace_and_account_cloud(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_HOST", "https://accounts.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_ACCOUNT_ID", "acc-123")

    cfg = UnifiedConfig.from_env().with_cloud("aws")

    assert cfg.workspace.cloud == "aws"
    assert cfg.account.cloud == "aws"


def test_from_env_rejects_invalid_strict_cloud_match(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.setenv("DATABRICKS_STRICT_CLOUD_MATCH", "not-a-bool")

    with pytest.raises(ValidationError):
        UnifiedConfig.from_env()


def test_from_env_uses_dbx_strict_cloud_match_alias(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://adb-12345.6.azuredatabricks.net")
    monkeypatch.setenv("DATABRICKS_CLOUD", "aws")
    monkeypatch.delenv("DATABRICKS_STRICT_CLOUD_MATCH", raising=False)
    monkeypatch.setenv("DBX_STRICT_CLOUD_MATCH", "false")

    cfg = UnifiedConfig.from_env()

    assert cfg.strict_cloud_match is False


def test_from_env_uses_dbx_token_alias_for_workspace_auth(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.delenv("DATABRICKS_TOKEN", raising=False)
    monkeypatch.setenv("DBX_TOKEN", "dbx-token")

    cfg = UnifiedConfig.from_env()

    assert cfg.workspace.auth.token == "dbx-token"


def test_from_env_uses_dbx_account_aliases(monkeypatch):
    monkeypatch.setenv("DATABRICKS_HOST", "https://dbc-test.cloud.databricks.com")
    monkeypatch.delenv("DATABRICKS_ACCOUNT_HOST", raising=False)
    monkeypatch.delenv("DATABRICKS_ACCOUNT_ID", raising=False)
    monkeypatch.delenv("DATABRICKS_ACCOUNT_TOKEN", raising=False)
    monkeypatch.setenv("DBX_ACCOUNT_HOST", "https://accounts.cloud.databricks.com")
    monkeypatch.setenv("DBX_ACCOUNT_ID", "acc-123")
    monkeypatch.setenv("DBX_ACCOUNT_TOKEN", "acc-token")

    cfg = UnifiedConfig.from_env()

    assert cfg.account.host == "https://accounts.cloud.databricks.com"
    assert cfg.account.account_id == "acc-123"
    assert cfg.account.auth.token == "acc-token"
