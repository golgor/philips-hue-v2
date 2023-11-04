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
