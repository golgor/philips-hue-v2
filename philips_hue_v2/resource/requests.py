from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx
from loguru import logger
from result import Err, Ok, Result

from .network import Lights


if TYPE_CHECKING:
    from philips_hue_v2.bridge import HueBridge


def get_resources(
    bridge: "HueBridge", endpoint: str = ""
) -> Result[list[dict[str, Any]], Exception]:
    """General function to get resources from the bridge.

    Used to abstract away the httpx.get() and authentication.
    """
    url = httpx.URL(
        url=f"https://{bridge.ip_address}/clip/v2/resource{endpoint}"
    )
    headers = httpx.Headers({"hue-application-key": bridge.user_name})
    try:
        response = httpx.get(
            url=url,
            headers=headers,
            verify=False,  # noqa: S501 - This is only supposed to be used in a local network!
        )
        response.raise_for_status()
        response_json: dict[str, list[Any]] = response.json()

        resources = response_json["data"]

    except httpx.HTTPStatusError as err:
        return Err(err)
    except httpx.HTTPError as err:
        return Err(err)
    except Exception as err:
        return Err(err)
    else:
        return Ok(resources)


def put_resources(
    bridge: "HueBridge", body: dict[str, Any], endpoint: str
) -> Result[list[dict[str, Any]], Exception]:
    """General function to put (update) resources from the bridge.

    Used to abstract away the httpx.put() and authentication.
    """
    url = httpx.URL(
        url=f"https://{bridge.ip_address}/clip/v2/resource{endpoint}"
    )
    headers = httpx.Headers({"hue-application-key": bridge.user_name})
    try:
        response = httpx.put(
            url=url,
            headers=headers,
            json=body,
            verify=False,  # noqa: S501 - This is only supposed to be used in a local network!
        )
        response.raise_for_status()
        response_json: dict[str, list[Any]] = response.json()

        resources = response_json["data"]

    except httpx.HTTPStatusError as err:
        return Err(err)
    except httpx.HTTPError as err:
        return Err(err)
    except Exception as err:
        return Err(err)
    else:
        return Ok(resources)


def get_lights(bridge: "HueBridge") -> list[Lights] | None:
    """Function to get all lights from the bridge."""
    response = get_resources(endpoint="/light", bridge=bridge)

    if response.is_ok():
        return [
            Lights(**resource)
            for resource in response.unwrap()
            if resource["type"] == "light"
        ]

    logger.error(response.unwrap_err())
    return None
