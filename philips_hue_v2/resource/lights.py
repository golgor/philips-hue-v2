from typing import Any, NotRequired

from pydantic import BaseModel
from typing_extensions import TypedDict


class LightsMetadata(TypedDict):
    """Meta data for a light."""

    name: str
    archetype: str
    fixed_mired: NotRequired[int]


class Lights(BaseModel):
    id: str
    id_v1: str
    # owner: dict[str, str]
    metadata: LightsMetadata
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

    @property
    def name(self) -> str:
        """Get the name of the light."""
        return self.metadata["name"]
