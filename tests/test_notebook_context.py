from databricks_api.notebook_context import _extract_option, resolve_notebook_context


class _OptionGet:
    def get(self):
        return "value-from-get"


class _OptionGetOrElse:
    def getOrElse(self, default):
        return "value-from-getorelse"


def test_extract_option_prefers_get_then_get_or_else():
    assert _extract_option(lambda: _OptionGet()) == "value-from-get"
    assert _extract_option(lambda: _OptionGetOrElse()) == "value-from-getorelse"


def test_resolve_notebook_context_returns_empty_when_dbutils_unavailable():
    data = resolve_notebook_context(dbutils=None)
    assert data.host is None
    assert data.token is None
