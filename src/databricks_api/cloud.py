"""Cloud detection and host-alignment helpers."""

from __future__ import annotations

from typing import Literal, Optional

CloudType = Literal["aws", "azure", "gcp"]


def detect_cloud_from_host(host: Optional[str]) -> Optional[CloudType]:
    if not host:
        return None
    value = host.lower()
    if "azuredatabricks.net" in value:
        return "azure"
    if "gcp.databricks.com" in value:
        return "gcp"
    if "cloud.databricks.com" in value:
        return "aws"
    return None


def is_host_cloud_aligned(host: Optional[str], cloud: CloudType) -> bool:
    inferred = detect_cloud_from_host(host)
    if inferred is None:
        return True
    return inferred == cloud
