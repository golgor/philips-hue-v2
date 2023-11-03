from enum import IntEnum
from typing import TypedDict


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
