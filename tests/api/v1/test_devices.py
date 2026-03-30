"""API tests for device usage endpoints."""

import pytest


@pytest.mark.asyncio
async def test_get_device_usage_returns_usage_payload(client) -> None:
    """Verify usage detail responses include the expected chart data.

    Args:
        client: Async FastAPI test client fixture.

    Returns:
        None.
    """
    response = await client.get("/api/v1/devices/D001/usage")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Device usage retrieved successfully"
    assert payload["data"]["deviceId"] == "D001"
    assert payload["data"]["healthStatus"] == "Normal"
    assert payload["data"]["weeklyUsageTrend"] == [2, 3, 1, 4, 2, 3, 3]


@pytest.mark.asyncio
async def test_get_device_usage_returns_structured_not_found_error(client) -> None:
    """Verify missing devices return the standardized error shape.

    Args:
        client: Async FastAPI test client fixture.

    Returns:
        None.
    """
    response = await client.get("/api/v1/devices/D999/usage")

    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "NOT_FOUND"
    assert payload["error"]["details"][0]["field"] == "device_id"
