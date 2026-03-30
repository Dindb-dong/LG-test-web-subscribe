"""Smoke tests for the HTML dashboard shell."""

import pytest


@pytest.mark.asyncio
async def test_root_returns_dashboard_shell(client) -> None:
    """Verify the main dashboard page renders the expected UI shell.

    Args:
        client: Async FastAPI test client fixture.

    Returns:
        None.
    """
    response = await client.get("/")

    assert response.status_code == 200
    assert "webOS Subscriber Control Center" in response.text
    assert "Requirement 2-C" in response.text
    assert 'id="subscriber-search"' in response.text
    assert "lucide" in response.text


@pytest.mark.asyncio
async def test_health_returns_ok_status(client) -> None:
    """Verify the health endpoint can be used by CI and Render checks.

    Args:
        client: Async FastAPI test client fixture.

    Returns:
        None.
    """
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
