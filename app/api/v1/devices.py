"""Device-related API endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.exceptions import ResourceNotFoundError
from app.schemas.common import ErrorDetail, ErrorInfo, ErrorResponse
from app.schemas.device import UsageDetailResponse
from app.services.subscription_service import subscription_service

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get(
    "/{device_id}/usage",
    response_model=UsageDetailResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_device_usage(device_id: str) -> UsageDetailResponse | JSONResponse:
    """Return detailed usage information for one device.

    Args:
        device_id: Device identifier selected in the dashboard.

    Returns:
        A success response that wraps the usage detail payload.
    """
    try:
        data = subscription_service.get_device_usage(device_id)
    except ResourceNotFoundError as exc:
        error = ErrorResponse(
            error=ErrorInfo(
                code="NOT_FOUND",
                message=str(exc),
                details=[ErrorDetail(field="device_id", message=str(exc))],
            )
        )
        return JSONResponse(status_code=404, content=error.model_dump())

    return UsageDetailResponse(data=data, message="Device usage retrieved successfully")
