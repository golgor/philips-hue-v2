from ..bridge import HueBridge
from ..resource.requests import put_resources
from .lights import Lights


def turn_on(bridge: HueBridge, lights: list[Lights]):
    """Turn off lights."""
    for light in lights:
        url = f"/light/{light.id}"
        body = {"on": {"on": True}}
        put_resources(bridge=bridge, endpoint=url, body=body)


def turn_off(bridge: HueBridge, lights: list[Lights]):
    """Turn off lights."""
    for light in lights:
        url = f"/light/{light.id}"
        body = {"on": {"on": False}}
        put_resources(bridge=bridge, endpoint=url, body=body)


def set_brightness(bridge: HueBridge, lights: list[Lights], brightness: int):
    """Set brightness.

    A value between 0 and 100. It is typically not possible to dim to 0 and trying to dim to zero will set the
    brightness to the lowest possible value instead.
    """
    for light in lights:
        url = f"/light/{light.id}"
        body = {"dimming": {"brightness": brightness}}
        put_resources(bridge=bridge, endpoint=url, body=body)


def set_brightness_delta(bridge: HueBridge, lights: list[Lights], brightness: int):
    """Set the brightness delta.

    How fast should the light change when brightness is changed. This doesn't seem to be implemented in for some lights?

    Args:
        bridge (HueBridge): _description_
        lights (list[Lights]): _description_
        brightness (int): _description_
    """
    for light in lights:
        url = f"/light/{light.id}"
        body = {"dimming_delta": {"action": "on", "brightness_delta": brightness}}
        put_resources(bridge=bridge, endpoint=url, body=body)


def set_color(bridge: HueBridge, lights: list[Lights], color: str):
    """Set color.

    A value between 0 and 100. It is typically not possible to dim to 0 and trying to dim to zero will set the
    brightness to the lowest possible value instead.
    """
    for light in lights:
        url = f"/light/{light.id}"
        body = {"color": {"xy": {"x": 0.5, "y": 0.5}}}
        put_resources(bridge=bridge, endpoint=url, body=body)
