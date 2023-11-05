from typing import Any, NotRequired

from pydantic import BaseModel
from typing_extensions import TypedDict

from ..bridge import HueBridge
from .color import Converter, get_gamut_from_str


class LightsMetadata(TypedDict):
    """Meta data for a light."""

    name: str
    archetype: str
    fixed_mired: NotRequired[int]


class Color(TypedDict):
    """Color attribute for a light."""

    xy: dict[str, float]
    gamut: dict[str, dict[str, float]]
    gamut_type: str


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
    color: Color | None = None
    # color_temperature: dict[str, Any] | None = None  # noqa: ERA001 - Not implemented yet
    # color_temperature_delta: dict[str, Any] | None = None  # noqa: ERA001 - Not implemented yet
    bridge: HueBridge

    @property
    def name(self) -> str:
        """Get the name of the light."""
        return self.metadata["name"]

    def turn_on(self) -> None:
        """Turn on the light."""
        url = f"/light/{self.id}"
        body = {"on": {"on": True}}
        self.bridge.update_resource(body=body, endpoint=url)

    def turn_off(self) -> None:
        """Turn on the light."""
        url = f"/light/{self.id}"
        body = {"on": {"on": False}}
        self.bridge.update_resource(body=body, endpoint=url)

    def set_brightness(self, brightness: int) -> None:
        """Set brightness.

        A value between 0 and 100. It is typically not possible to dim to 0 and trying to dim to zero will set the
        brightness to the lowest possible value instead.
        """
        url = f"/light/{self.id}"
        body = {"dimming": {"brightness": brightness}}
        self.bridge.update_resource(body=body, endpoint=url)

    def set_rgb_color(self, rgb: dict[str, int]) -> None:
        """Set color.

        The rgb values should be between 0 and 255 and will be converted to xy values.

        Args:
            rgb (dict[str, int]): A dict with the rgb-values. For example {"red": 255, "green": 0, "blue": 0}.
        """
        if not hasattr(self, "color") or self.color is None:
            raise ValueError("The light does not support color.")

        gamut = get_gamut_from_str(self.color["gamut_type"])
        converter = Converter(gamut=gamut)
        x, y = converter.rgb_to_xy(**rgb)
        url = f"/light/{self.id}"
        body = {"color": {"xy": {"x": x, "y": y}}}
        self.bridge.update_resource(body=body, endpoint=url)
