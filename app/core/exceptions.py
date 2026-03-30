"""Custom exceptions shared across the application."""


class ResourceNotFoundError(Exception):
    """Represent a missing resource looked up by an identifier.

    Args:
        resource: Human-readable resource name.
        identifier: Identifier used for the lookup.
    """

    def __init__(self, resource: str, identifier: str) -> None:
        """Store the missing resource context.

        Args:
            resource: Human-readable resource name.
            identifier: Identifier used for the lookup.

        Returns:
            None.
        """
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} '{identifier}' was not found.")
