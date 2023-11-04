from typing import Any

from .lights import Lights


class Network:
    lights: list[Lights] | None = None

    def __init__(self, resources: list[dict[str, Any]]) -> None:
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
