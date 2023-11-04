from typing import Any

from .lights import Lights


class Network:
    """A class that will be used to parse the network resources.

    This is a quite complex task as for example lights can be part of rooms or scenes, and we need references to those.
    """

    lights: list[Lights] | None = None

    def __init__(self, resources: list[dict[str, Any]]) -> None:
        """Initialize the network class.

        This might very well be replaced by functions.

        Args:
            resources (list[dict[str, Any]]): A list of resources from the bridge. Typically the raw response from
                calling the /resource-endpoint.
        """
        self.lights = self.parse_lights(resources)

    def get_lights(self) -> list[Lights] | None:
        """Get a list of all lights."""
        return self.lights

    @staticmethod
    def parse_lights(resources: list[dict[str, Any]]) -> list[Lights]:
        """Get a list of all lights among the resources."""
        return [
            Lights(**resource)
            for resource in resources
            if resource["type"] == "light"
        ]
