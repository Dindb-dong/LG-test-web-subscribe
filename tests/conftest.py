"""Shared pytest fixtures for API and page tests."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Create an async test client for the FastAPI application.

    Args:
        None.

    Returns:
        An `AsyncClient` instance backed by the local ASGI app.
    """
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        yield async_client
