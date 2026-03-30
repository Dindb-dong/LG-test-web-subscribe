"""Business logic for the subscription dashboard."""

from app.core.exceptions import ResourceNotFoundError
from app.data.dummy_data import devices_by_user, subscribers, usage_by_device
from app.schemas.device import Device, UsageDetail
from app.schemas.subscriber import Subscriber


class SubscriptionService:
    """Serve dashboard data from the in-memory practice dataset.

    Args:
        None.

    Returns:
        A reusable service object for dashboard operations.
    """

    def list_subscribers(self) -> list[Subscriber]:
        """Return the full subscriber list.

        Args:
            None.

        Returns:
            The subscribers formatted by the response schema.
        """
        return [Subscriber.model_validate(item) for item in subscribers]

    def get_devices_by_user(self, user_id: str) -> list[Device]:
        """Return every device owned by a subscriber.

        Args:
            user_id: Subscriber identifier from the UI selection.

        Returns:
            A list of devices for the requested subscriber.

        Raises:
            ResourceNotFoundError: Raised when the subscriber does not exist.
        """
        if not any(subscriber["userId"] == user_id for subscriber in subscribers):
            raise ResourceNotFoundError("Subscriber", user_id)

        return [Device.model_validate(item) for item in devices_by_user.get(user_id, [])]

    def get_device_usage(self, device_id: str) -> UsageDetail:
        """Return detailed usage metrics for one device.

        Args:
            device_id: Device identifier from the UI selection.

        Returns:
            The detailed usage payload for the requested device.

        Raises:
            ResourceNotFoundError: Raised when the device does not exist.
        """
        usage = usage_by_device.get(device_id)
        if usage is None:
            raise ResourceNotFoundError("Device", device_id)

        return UsageDetail.model_validate(usage)


subscription_service = SubscriptionService()
