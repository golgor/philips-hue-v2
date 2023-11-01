import json
from pathlib import Path

from loguru import logger
from pydantic import BaseModel

from philips_hue_v2.authentication import get_access_token


class HueBridge(BaseModel):
    """Class representing a Philips Hue bridge."""

    client_key: str | None = None
    user_name: str | None = None
    ip_address: str
    path: Path = Path("bridge.json")


def load_bridge_from_file(filepath: Path) -> HueBridge:
    """Load a bridge from a file."""
    with filepath.open("r") as file:
        bridge_model = json.load(file)
        return HueBridge(**bridge_model)


def get_access_token_from_bridge(
    bridge: HueBridge, app_name: str, instance_name: str
) -> HueBridge:
    result = get_access_token(
        ip_address=bridge.ip_address,
        app_name=app_name,
        instance_name=instance_name,
    )
    if result.is_ok():
        data = result.unwrap()
        logger.info(
            f"Successfully got data from HueBridge!\n{json.dumps(data, indent=4)}"
        )
        bridge.client_key = data["clientkey"]
        bridge.user_name = data["username"]
        return bridge

    logger.error(result.unwrap_err())
    return bridge
