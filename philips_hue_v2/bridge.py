import json
from pathlib import Path

from loguru import logger
from pydantic import BaseModel


class HueBridge(BaseModel):
    """Class representing a Philips Hue bridge."""

    client_key: str
    user_name: str
    ip_address: str


def load_bridge_from_file(filepath: Path) -> HueBridge:
    """Load a bridge from a file."""
    with filepath.open("r") as file:
        bridge_model = json.load(file)
        return HueBridge(**bridge_model)
