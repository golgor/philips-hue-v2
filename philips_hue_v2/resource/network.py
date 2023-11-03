from typing import Any, NotRequired

from pydantic import BaseModel


class Lights(BaseModel):
    id: str
    id_v1: str
    # owner: dict[str, str]
    metadata: dict[str, str | int]
    # identify: dict[str, Any]
    on: dict[str, bool]
    dimming: dict[str, float]
    dimming_delta: dict[str, Any]
    # dynamics: dict[str, Any]
    # alert: dict[str, Any]
    # signaling: dict[str, Any]
    # mode: str
    # effects: dict[str, Any] | None = None
    # powerup: dict[str, Any] | None = None
    # color_temperature: dict[str, Any] | None = None
    # color_temperature_delta: dict[str, Any] | None = None
    # type: str


class Sensors(BaseModel):
    pass


class Network:
    lights: list[Lights] | None = None
    sensors: list[Sensors] | None = None

    def __init__(self, resources: list[dict[str, Any]]) -> None:
        self.lights = self.parse_lights(resources)
        print(resources)

    @staticmethod
    def parse_lights(resources: list[dict[str, Any]]) -> list[Lights]:
        """Get a list of all lights among the resources."""
        return [
            Lights(**resource)
            for resource in resources
            if resource["type"] == "light"
        ]
