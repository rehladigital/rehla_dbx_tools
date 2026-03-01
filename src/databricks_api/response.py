"""Response wrappers and DataFrame conversion helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from .exceptions import ValidationError


_LIST_PAYLOAD_KEYS = (
    "items",
    "results",
    "data",
    "workspaces",
    "users",
    "jobs",
    "clusters",
    "runs",
    "schemas",
    "catalogs",
)


def _extract_list_payload(data: dict[str, Any]) -> Any:
    for key in _LIST_PAYLOAD_KEYS:
        value = data.get(key)
        if isinstance(value, list):
            return value
    for value in data.values():
        if isinstance(value, list):
            return value
    for value in data.values():
        if isinstance(value, dict):
            nested = _extract_list_payload(value)
            if nested is not None:
                return nested
    return None


def normalize_json(data: Any) -> list[dict[str, Any]]:
    """Normalize any JSON-like payload into row-oriented records."""
    if data is None:
        return []
    if isinstance(data, list):
        if not data:
            return []
        if all(isinstance(item, dict) for item in data):
            return pd.json_normalize(data, sep=".").to_dict(orient="records")
        return [{"value": item} for item in data]
    if isinstance(data, dict):
        # Databricks responses often wrap row lists under varying keys.
        extracted_list = _extract_list_payload(data)
        if extracted_list is not None:
            return normalize_json(extracted_list)
        return pd.json_normalize(data, sep=".").to_dict(orient="records")
    return [{"value": data}]


def to_pandas_df(data: Any) -> pd.DataFrame:
    return pd.DataFrame(normalize_json(data))


def to_spark_df(data: Any, spark_session: Any = None) -> Any:
    records = normalize_json(data)
    try:
        from pyspark.sql import SparkSession
    except Exception as exc:
        raise ValidationError(
            "PySpark is not installed. Install with `pip install rehladigital-aws-dbx-tools[spark]`."
        ) from exc

    spark = spark_session or SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    if not records:
        return spark.createDataFrame([], "value string")
    return spark.createDataFrame(records)


@dataclass
class ApiResponse:
    status_code: int
    url: str
    data: Any
    headers: dict[str, str]

    def to_pandas(self) -> pd.DataFrame:
        return to_pandas_df(self.data)

    def to_spark(self, spark_session: Any = None) -> Any:
        return to_spark_df(self.data, spark_session=spark_session)
