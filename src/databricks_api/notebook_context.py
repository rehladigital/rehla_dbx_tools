"""Databricks notebook context helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class NotebookContextData:
    host: Optional[str] = None
    token: Optional[str] = None


def resolve_notebook_context(dbutils: Optional[Any] = None) -> NotebookContextData:
    """Try to read Databricks runtime context values (host/token)."""
    dbutils = dbutils or _lookup_dbutils()
    if dbutils is None:
        return NotebookContextData()

    try:
        context = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
    except Exception:
        return NotebookContextData()

    return NotebookContextData(
        host=_extract_option(context.apiUrl),
        token=_extract_option(context.apiToken),
    )


def _lookup_dbutils() -> Optional[Any]:
    try:
        from IPython import get_ipython
    except Exception:
        return None

    shell = get_ipython()
    if shell is None:
        return None
    return shell.user_ns.get("dbutils")


def _extract_option(callable_attr: Any) -> Optional[str]:
    """Handle Scala Option/Java Optional/Python wrapper values safely."""
    try:
        obj = callable_attr()
    except Exception:
        return None

    # Scala Option in Databricks context
    for method_name in ("get", "getOrElse", "orElse"):
        method = getattr(obj, method_name, None)
        if callable(method):
            try:
                if method_name == "getOrElse":
                    value = method(None)
                else:
                    value = method()
                if value:
                    return str(value)
            except Exception:
                continue

    text = str(obj).strip()
    if text and text.lower() not in {"none", "null"}:
        return text
    return None
