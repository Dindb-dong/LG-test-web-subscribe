"""Subscriber response schemas."""

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import CamelModel


class Subscriber(CamelModel):
    """Represent one subscriber row in the dashboard.

    Args:
        None.

    Returns:
        A normalized subscriber payload.
    """

    user_id: str = Field(alias="userId")
    name: str
    organization: str
    plan: Literal["Basic", "Premium", "Family"]
    status: Literal["Active", "Paused", "Expired"]
    device_count: int = Field(alias="deviceCount")


class SubscriberListResponse(BaseModel):
    """Represent the standardized subscriber list response.

    Args:
        None.

    Returns:
        A paginated subscriber list response.
    """

    data: list[Subscriber]
    total: int
    page: int
    page_size: int
