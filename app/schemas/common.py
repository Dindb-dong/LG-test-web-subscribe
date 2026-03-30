"""Common response schemas shared across endpoints."""

from pydantic import BaseModel, ConfigDict


class CamelModel(BaseModel):
    """Base model that accepts Python field names and emits aliases.

    Args:
        None.

    Returns:
        A configured Pydantic model base class.
    """

    model_config = ConfigDict(populate_by_name=True)


class ErrorDetail(BaseModel):
    """Represent one validation or lookup issue.

    Args:
        None.

    Returns:
        A structured error detail entry.
    """

    field: str
    message: str


class ErrorInfo(BaseModel):
    """Represent the error envelope returned by the API.

    Args:
        None.

    Returns:
        A top-level error object with optional details.
    """

    code: str
    message: str
    details: list[ErrorDetail]


class ErrorResponse(BaseModel):
    """Wrap structured API errors under the `error` key.

    Args:
        None.

    Returns:
        A standardized API error response model.
    """

    error: ErrorInfo
