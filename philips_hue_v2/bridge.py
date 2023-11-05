import json
from pathlib import Path
from typing import Any

from loguru import logger
from pydantic import BaseModel

from .authentication import get_access_token
from .resource.requests import put_resources


class HueBridge(BaseModel):
    """Class representing a Philips Hue bridge."""

    client_key: str
    user_name: str
    ip_address: str
    path: Path = Path("bridge.json")

    def update_resource(self, body: dict[str, Any], endpoint: str) -> None:
        put_resources(
            bridge=self,
            body=body,
            endpoint=endpoint,
        )


def get_access_token_from_bridge(
    ip_address: str, app_name: str, instance_name: str
) -> None:
    """Wrapper function for getting access token from a bridge.

    It outputs the result to the console.
    """
    result = get_access_token(
        ip_address=ip_address,
        app_name=app_name,
        instance_name=instance_name,
    )
    if result.is_ok():
        data = result.unwrap()
        logger.info(
            f"Successfully got data from HueBridge!\n{json.dumps(data, indent=4)}"
        )
        return
    logger.error(result.unwrap_err())
