"""Device and usage response schemas."""

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import CamelModel


class Device(CamelModel):
    """Represent one device row in the dashboard.

    Args:
        None.

    Returns:
        A normalized device payload.
    """

    device_id: str = Field(alias="deviceId")
    type: str
    model: str
    location: str
    status: Literal["Online", "Offline", "Standby", "Error"]
    last_seen: str = Field(alias="lastSeen")


class DeviceListResponse(BaseModel):
    """Represent the standardized device list response.

    Args:
        None.

    Returns:
        A paginated device list response.
    """

    data: list[Device]
    total: int
    page: int
    page_size: int


class UsageDetail(CamelModel):
    """Represent detailed usage metrics for a device.

    Args:
        None.

    Returns:
        A normalized device usage payload.
    """

    device_id: str = Field(alias="deviceId")
    device_name: str = Field(alias="deviceName")
    power_status: Literal["On", "Off", "Standby", "Error", "Cleaning"] = Field(alias="powerStatus")
    last_used_at: str = Field(alias="lastUsedAt")
    total_usage_hours: int = Field(alias="totalUsageHours")
    weekly_usage_count: int = Field(alias="weeklyUsageCount")
    health_status: Literal["Normal", "Warning"] = Field(alias="healthStatus")
    remark: str
    weekly_usage_trend: list[int] = Field(alias="weeklyUsageTrend")


class UsageDetailResponse(BaseModel):
    """Wrap device usage in the standard success format.

    Args:
        None.

    Returns:
        A success response for one usage detail payload.
    """

    data: UsageDetail
    message: str
