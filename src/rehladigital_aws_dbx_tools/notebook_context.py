"""Compatibility module for notebook context exports."""

from databricks_api.notebook_context import NotebookContext, resolve_notebook_context

__all__ = ["NotebookContext", "resolve_notebook_context"]
