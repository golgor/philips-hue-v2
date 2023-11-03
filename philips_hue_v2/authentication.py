from typing import Any, TypedDict

import httpx
from result import Err, Ok, Result

from philips_hue_v2 import HueError, HueErrorDetails, OtherApiError


class HueAuthenticationDetail(TypedDict):
    """Client data."""

    username: str
    clientkey: str


class PressLinkButtonError(Exception):
    """Raised when the link button on the bridge has not been pressed."""


def get_access_token(
    ip_address: str, app_name: str, instance_name: str
) -> Result[HueAuthenticationDetail, Exception]:
    """Get access token from Philips Hue API.

    To get the access token, the link button on the bridge must be pressed before running this function. If not, an
    error will be returned.

    The app_name and instance_name is just for identification purposes. They can be anything.

    Args:
        ip_address (str): The ip-address of the Hue bridge.
        app_name (str): The name of the app that is requesting access.
        instance_name (str): The name of the instance that is requesting access.

    Returns:
        Result[HueAuthenticationDetail, Exception]: Either access information or an error.
    """
    url = f"https://{ip_address}/api/"
    body = {
        "devicetype": f"{app_name}#{instance_name}",
        "generateclientkey": True,
    }
    try:
        response = httpx.post(
            url,
            json=body,
            verify=False,  # noqa: S501 - This is only supposed to be used in a local network!
        )
        response.raise_for_status()
        response_data: list[dict[str, Any]] = response.json()

        if "error" in response_data[0]:
            error: HueErrorDetails = response_data[0]["error"]
            if error["type"] == HueError.LINK_BUTTON_NOT_PRESSED:
                return Err(PressLinkButtonError("Press link button on bridge"))
            return Err(
                OtherApiError(f"Error {error['type']}: {error['description']}")
            )

        client_data: HueAuthenticationDetail = response_data[0]["success"]
    except httpx.HTTPStatusError as err:
        return Err(err)
    except httpx.HTTPError as err:
        return Err(err)
    except Exception as err:
        return Err(err)
    else:
        return Ok(client_data)
