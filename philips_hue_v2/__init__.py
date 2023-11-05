import json
from enum import IntEnum
from typing import TypedDict

from loguru import logger


class HueError(IntEnum):
    """Hue error codes."""

    LINK_BUTTON_NOT_PRESSED = 101
    PARAMETER_NOT_AVAILABLE = 6
    INVALID_VALUE = 7


class HueErrorDetails(TypedDict):
    """Client data."""

    type: int
    address: str
    description: str


class OtherApiError(Exception):
    """Raised for any other errors in the API communication."""

    def __init__(self, resource: str, errors: list[dict[str, str]]) -> None:
        """Initialize."""
        self.errors = errors
        for error in errors:
            logger.error(json.dumps({"resource": resource, "error": error["description"]}))
            super().__init__(json.dumps({"resource": resource, "error": error["description"]}))

    def __str__(self) -> str:
        """Return string representation."""
        return json.dumps(self.errors)
