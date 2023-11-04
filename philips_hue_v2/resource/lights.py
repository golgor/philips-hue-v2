from typing import Any, NotRequired

from pydantic import BaseModel
from typing_extensions import TypedDict


class LightsMetadata(TypedDict):
    """Meta data for a light."""

    name: str
    archetype: str
    fixed_mired: NotRequired[int]


class Lights(BaseModel):
    """Basemodel for a light resource."""

    id: str  # noqa: A003 - This is the id from the bridge
    id_v1: str
    # owner: dict[str, str]  # noqa: ERA001 - Not implemented yet
    metadata: LightsMetadata
    # identify: dict[str, Any]  # noqa: ERA001 - Not implemented yet
    on: dict[str, bool]
    dimming: dict[str, float]
    dimming_delta: dict[str, Any]
    # dynamics: dict[str, Any]  # noqa: ERA001 - Not implemented yet
    # alert: dict[str, Any]  # noqa: ERA001 - Not implemented yet
    # signaling: dict[str, Any]  # noqa: ERA001 - Not implemented yet
    # mode: str  # noqa: ERA001 - Not implemented yet
    # effects: dict[str, Any] | None = None  # noqa: ERA001 - Not implemented yet
    # powerup: dict[str, Any] | None = None  # noqa: ERA001 - Not implemented yet
    # color_temperature: dict[str, Any] | None = None  # noqa: ERA001 - Not implemented yet
    # color_temperature_delta: dict[str, Any] | None = None  # noqa: ERA001 - Not implemented yet

    @property
    def name(self) -> str:
        """Get the name of the light."""
        return self.metadata["name"]
