from typing import TYPE_CHECKING, Any

import httpx
from result import Err, Ok, Result


if TYPE_CHECKING:
    from philips_hue_v2.bridge import HueBridge


def get_resources(
    bridge: "HueBridge",
) -> Result[list[dict[str, Any]], Exception]:
    url = f"https://{bridge.ip_address}/clip/v2/resource"
    headers = {"hue-application-key": bridge.user_name}
    try:
        response = httpx.get(
            url,
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
