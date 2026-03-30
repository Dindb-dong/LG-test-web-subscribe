"""API tests for subscriber endpoints."""

import pytest


@pytest.mark.asyncio
async def test_get_subscribers_returns_paginated_list(client) -> None:
    """Verify the subscriber endpoint returns the required table payload.

    Args:
        client: Async FastAPI test client fixture.

    Returns:
        None.
    """
    response = await client.get("/api/v1/subscribers")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 5
    assert payload["page"] == 1
    assert payload["page_size"] == 5
    assert payload["data"][0] == {
        "userId": "U001",
        "name": "Kim Minsoo",
        "organization": "Yonsei University",
        "plan": "Premium",
        "status": "Active",
        "deviceCount": 2,
    }


@pytest.mark.asyncio
async def test_get_subscriber_devices_returns_registered_devices(client) -> None:
    """Verify the device list is returned for an existing subscriber.

    Args:
        client: Async FastAPI test client fixture.

    Returns:
        None.
    """
    response = await client.get("/api/v1/subscribers/U001/devices")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 2
    assert payload["data"][0]["deviceId"] == "D001"
    assert payload["data"][0]["status"] == "Online"


@pytest.mark.asyncio
async def test_get_subscriber_devices_returns_empty_list_when_no_device_exists(client) -> None:
    """Verify subscribers without devices still return a valid empty list response.

    Args:
        client: Async FastAPI test client fixture.

    Returns:
        None.
    """
    response = await client.get("/api/v1/subscribers/U005/devices")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 0
    assert payload["data"] == []


@pytest.mark.asyncio
async def test_get_subscriber_devices_returns_structured_not_found_error(client) -> None:
    """Verify missing subscribers return the standardized error shape.

    Args:
        client: Async FastAPI test client fixture.

    Returns:
        None.
    """
    response = await client.get("/api/v1/subscribers/U999/devices")

    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "NOT_FOUND"
    assert payload["error"]["details"][0]["field"] == "user_id"
