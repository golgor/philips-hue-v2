from typing import TYPE_CHECKING, Any, TypedDict

import httpx
from result import Err, Ok, Result

from .. import OtherApiError


if TYPE_CHECKING:
    from philips_hue_v2.bridge import HueBridge


class ResponseObject(TypedDict):
    """Response object."""

    data: list[dict[str, str]]
    errors: list[dict[str, str]]


MULTI_VALUE_STATUS = 207


def get_resources(
    bridge: "HueBridge", endpoint: str = ""
) -> Result[list[dict[str, Any]], Exception]:
    """General function to get resources from the bridge.

    Used to abstract away the httpx.get() and authentication.
    """
    url = httpx.URL(url=f"https://{bridge.ip_address}/clip/v2/resource{endpoint}")
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

    Used to abstract away the httpx.put() and authentication. In some cases a 207 is raised, which means a multi-value
    status. This typically means that something worked out fine but, something also failed. An example of this is
    trying to change color on a light that doesn't support color. It successfully found the light resource, but could
    not find the color attribute. In that case, we raise an OtherApiError.
    """
    url = httpx.URL(url=f"https://{bridge.ip_address}/clip/v2/resource{endpoint}")
    headers = httpx.Headers({"hue-application-key": bridge.user_name})
    try:
        response = httpx.put(
            url=url,
            headers=headers,
            json=body,
            verify=False,  # noqa: S501 - This is only supposed to be used in a local network!
        )
        response.raise_for_status()
        if response.status_code == MULTI_VALUE_STATUS:
            raise OtherApiError(resource=endpoint, errors=response.json()["errors"])

        response_json: ResponseObject = response.json()
        resources = response_json["data"]

    except httpx.HTTPStatusError as err:
        return Err(err)
    except httpx.HTTPError as err:
        return Err(err)
    except Exception as err:
        return Err(err)
    else:
        return Ok(resources)
