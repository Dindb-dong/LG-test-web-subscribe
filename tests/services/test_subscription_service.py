"""Service-layer tests for dashboard data access."""

import pytest

from app.core.exceptions import ResourceNotFoundError
from app.services.subscription_service import subscription_service


def test_list_subscribers_returns_all_subscribers() -> None:
    """Verify the service returns every subscriber in the dataset.

    Args:
        None.

    Returns:
        None.
    """
    subscribers = subscription_service.list_subscribers()

    assert len(subscribers) == 5
    assert subscribers[0].user_id == "U001"
    assert subscribers[-1].status == "Expired"


def test_get_devices_by_user_returns_device_list() -> None:
    """Verify the service returns devices for a valid subscriber.

    Args:
        None.

    Returns:
        None.
    """
    devices = subscription_service.get_devices_by_user("U003")

    assert len(devices) == 3
    assert devices[1].device_id == "D005"
    assert devices[2].status == "Error"


def test_get_devices_by_user_returns_empty_list_for_subscriber_without_devices() -> None:
    """Verify the service supports subscribers with zero registered devices.

    Args:
        None.

    Returns:
        None.
    """
    devices = subscription_service.get_devices_by_user("U005")

    assert devices == []


def test_get_devices_by_user_raises_for_unknown_subscriber() -> None:
    """Verify missing subscribers raise a domain-specific error.

    Args:
        None.

    Returns:
        None.
    """
    with pytest.raises(ResourceNotFoundError):
        subscription_service.get_devices_by_user("U999")


def test_get_device_usage_returns_usage_details() -> None:
    """Verify the service returns usage metrics for a known device.

    Args:
        None.

    Returns:
        None.
    """
    usage = subscription_service.get_device_usage("D008")

    assert usage.device_id == "D008"
    assert usage.power_status == "Standby"
    assert usage.weekly_usage_count == 40


def test_get_device_usage_raises_for_unknown_device() -> None:
    """Verify missing devices raise a domain-specific error.

    Args:
        None.

    Returns:
        None.
    """
    with pytest.raises(ResourceNotFoundError):
        subscription_service.get_device_usage("D999")
