"""Subscriber-related API endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.exceptions import ResourceNotFoundError
from app.schemas.common import ErrorDetail, ErrorInfo, ErrorResponse
from app.schemas.device import DeviceListResponse
from app.schemas.subscriber import SubscriberListResponse
from app.services.subscription_service import subscription_service

router = APIRouter(prefix="/subscribers", tags=["subscribers"])


@router.get("", response_model=SubscriberListResponse)
def get_subscribers() -> SubscriberListResponse:
    """Return every subscriber for the dashboard table.

    Args:
        None.

    Returns:
        A standardized list response with all subscribers.
    """
    data = subscription_service.list_subscribers()
    return SubscriberListResponse(data=data, total=len(data), page=1, page_size=len(data))


@router.get(
    "/{user_id}/devices",
    response_model=DeviceListResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_devices_by_user(user_id: str) -> DeviceListResponse | JSONResponse:
    """Return all registered devices for a subscriber.

    Args:
        user_id: Subscriber identifier selected in the dashboard.

    Returns:
        A standardized list response with the subscriber's devices.
    """
    try:
        data = subscription_service.get_devices_by_user(user_id)
    except ResourceNotFoundError as exc:
        error = ErrorResponse(
            error=ErrorInfo(
                code="NOT_FOUND",
                message=str(exc),
                details=[ErrorDetail(field="user_id", message=str(exc))],
            )
        )
        return JSONResponse(status_code=404, content=error.model_dump())

    return DeviceListResponse(data=data, total=len(data), page=1, page_size=len(data))
