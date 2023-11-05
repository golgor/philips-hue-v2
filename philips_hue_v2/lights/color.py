"""Library for RGB / CIE1931 "x, y" coversion.

Based on Philips implementation guidance:
http://www.developers.meethue.com/documentation/color-conversions-rgb-xy
Copyright (c) 2016 Benjamin Knight / MIT License.

https://github.com/benknight/hue-python-rgb-converter/

A lot of noqa is used here, primarily to adhere to the standard naming used in the CIE1931 standard.
This might be migrated to the colour-package sometime: https://github.com/colour-science/colour
"""
import math
import random
from dataclasses import dataclass


__version__ = "0.5.1"


@dataclass(frozen=True)
class XYPoint:
    """Class for a XYPoint.

    Represents a CIE 1931 XY coordinate pair.
    """

    x: float
    y: float


Gamut = tuple[XYPoint, XYPoint, XYPoint]

# LivingColors Iris, Bloom, Aura, LightStrips
GamutA = (
    XYPoint(0.704, 0.296),
    XYPoint(0.2151, 0.7106),
    XYPoint(0.138, 0.08),
)

# Hue A19 bulbs
GamutB = (
    XYPoint(0.675, 0.322),
    XYPoint(0.4091, 0.518),
    XYPoint(0.167, 0.04),
)

# Hue BR30, A19 (Gen 3), Hue Go, LightStrips plus
GamutC = (
    XYPoint(0.692, 0.308),
    XYPoint(0.17, 0.7),
    XYPoint(0.153, 0.048),
)


def get_gamut_from_str(gamut_str: str) -> Gamut:
    """Gets the correct color gamut for the provided gamut string."""
    if gamut_str == "A":
        return GamutA
    if gamut_str == "B":
        return GamutB
    if gamut_str == "C":
        return GamutC
    raise ValueError


def get_light_gamut_for_model(model_id: str) -> Gamut:
    """Gets the correct color gamut for the provided model id.

    Docs: https://developers.meethue.com/develop/hue-api/supported-devices/
    """
    if model_id in {
        "LST001",
        "LLC005",
        "LLC006",
        "LLC007",
        "LLC010",
        "LLC011",
        "LLC012",
        "LLC013",
        "LLC014",
    }:
        return GamutA
    if model_id in {"LCT001", "LCT007", "LCT002", "LCT003", "LLM001"}:
        return GamutB
    if model_id in {
        "LCT010",
        "LCT011",
        "LCT012",
        "LCT014",
        "LCT015",
        "LCT016",
        "LLC020",
        "LST002",
    }:
        return GamutC
    raise ValueError


class ColorHelper:
    """Class with a lot of helper function to convert colors between RGB and CIE1931."""

    def __init__(self, gamut: Gamut = GamutB) -> None:
        """Initialize the ColorHelper class.

        Setting the different components of the Gamut.

        Args:
            gamut (Gamut, optional): The selected Gamut. Defaults to GamutB.
        """
        self.red = gamut[0]
        self.lime = gamut[1]
        self.blue = gamut[2]

    def hex_to_red(self, hex_value: str) -> int:
        """Parses a valid hex color string and returns the Red RGB integer value."""
        return int(hex_value[:2], 16)

    def hex_to_green(self, hex_value: str) -> int:
        """Parses a valid hex color string and returns the Green RGB integer value."""
        return int(hex_value[2:4], 16)

    def hex_to_blue(self, hex_value: str) -> int:
        """Parses a valid hex color string and returns the Blue RGB integer value."""
        return int(hex_value[4:6], 16)

    def hex_to_rgb(self, h: str) -> tuple[int, int, int]:
        """Converts a valid hex color string to an RGB array."""
        return self.hex_to_red(h), self.hex_to_green(h), self.hex_to_blue(h)

    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Converts RGB to hex."""
        return f"{r:02x}{g:02x}{b:02x}"

    def random_rgb_value(self) -> int:
        """Return a random Integer in the range of 0 to 255, representing an RGB color value."""
        return random.randrange(0, 256)  # noqa: S311

    def cross_product(self, p1: XYPoint, p2: XYPoint) -> float:
        """Returns the cross product of two XYPoints."""
        return p1.x * p2.y - p1.y * p2.x

    def check_point_in_lamps_reach(self, p: XYPoint) -> bool:
        """Check if the provided XYPoint can be recreated by a Hue lamp."""
        v1 = XYPoint(self.lime.x - self.red.x, self.lime.y - self.red.y)
        v2 = XYPoint(self.blue.x - self.red.x, self.blue.y - self.red.y)

        q = XYPoint(p.x - self.red.x, p.y - self.red.y)
        s = self.cross_product(q, v2) / self.cross_product(v1, v2)
        t = self.cross_product(v1, q) / self.cross_product(v1, v2)

        return (s >= 0.0) and (t >= 0.0) and (s + t <= 1.0)  # noqa: PLR2004

    def get_closest_point_to_line(
        self,
        A: XYPoint,  # noqa: N803
        B: XYPoint,  # noqa: N803
        P: XYPoint,  # noqa: N803
    ) -> XYPoint:
        """Find the closest point on a line. This point will be reproducible by a Hue lamp."""
        AP = XYPoint(P.x - A.x, P.y - A.y)  # noqa: N806
        AB = XYPoint(B.x - A.x, B.y - A.y)  # noqa: N806
        ab2 = AB.x * AB.x + AB.y * AB.y
        ap_ab = AP.x * AB.x + AP.y * AB.y
        t = ap_ab / ab2

        if t < 0.0:  # noqa: PLR2004
            t = 0.0
        elif t > 1.0:  # noqa: PLR2004
            t = 1.0

        return XYPoint(A.x + AB.x * t, A.y + AB.y * t)

    def get_closest_point_to_point(self, xy_point: XYPoint) -> XYPoint:
        """Find the closest point on each line in the CIE 1931 'triangle'.

        If a color is not reproduceable by the lamp, find the closest point on each line in the CIE 1931 'triangle'.
        First it calculates the closest points to each of the Gamut lines, it then calculates the distances. It then
        returns the point which is closest.

        Args:
            xy_point (XYPoint): A XYPoint object corresponding to the color to convert.

        Returns:
            (XYPoint): The closest point on the CIE1931 triangle the lamp can reproduce.
        """
        pAB = self.get_closest_point_to_line(  # noqa: N806
            self.red, self.lime, xy_point
        )
        pAC = self.get_closest_point_to_line(  # noqa: N806
            self.blue, self.red, xy_point
        )
        pBC = self.get_closest_point_to_line(  # noqa: N806
            self.lime, self.blue, xy_point
        )

        # Get the distances per point and see which point is closer to our Point.
        dAB = self.get_distance_between_two_points(xy_point, pAB)  # noqa: N806
        dAC = self.get_distance_between_two_points(xy_point, pAC)  # noqa: N806
        dBC = self.get_distance_between_two_points(xy_point, pBC)  # noqa: N806

        lowest = dAB
        closest_point = pAB

        if dAC < lowest:
            lowest = dAC
            closest_point = pAC

        if dBC < lowest:
            lowest = dBC
            closest_point = pBC

        # Change the xy value to a value which is within the reach of the lamp.
        cx = closest_point.x
        cy = closest_point.y

        return XYPoint(cx, cy)

    def get_distance_between_two_points(self, one: XYPoint, two: XYPoint) -> float:
        """Returns the distance between two XYPoints."""
        dx = one.x - two.x
        dy = one.y - two.y
        return math.sqrt(dx * dx + dy * dy)

    def get_xy_point_from_rgb(self, red_i: int, green_i: int, blue_i: int) -> XYPoint:
        """Get XYPoint representing the closest available CIE 1931 coordinates based on the RGB input values."""
        red = red_i / 255.0
        green = green_i / 255.0
        blue = blue_i / 255.0

        r = (
            ((red + 0.055) / (1.0 + 0.055)) ** 2.4
            if (red > 0.04045)  # noqa: PLR2004
            else (red / 12.92)
        )
        g = (
            ((green + 0.055) / (1.0 + 0.055)) ** 2.4
            if (green > 0.04045)  # noqa: PLR2004
            else (green / 12.92)
        )
        b = (
            ((blue + 0.055) / (1.0 + 0.055)) ** 2.4
            if (blue > 0.04045)  # noqa: PLR2004
            else (blue / 12.92)
        )

        X = r * 0.664511 + g * 0.154324 + b * 0.162028  # noqa: N806
        Y = r * 0.283881 + g * 0.668433 + b * 0.047685  # noqa: N806
        Z = r * 0.000088 + g * 0.072310 + b * 0.986039  # noqa: N806

        cx = X / (X + Y + Z)
        cy = Y / (X + Y + Z)

        # Check if the given XY value is within the colourreach of our lamps.
        xy_point = XYPoint(cx, cy)
        in_reach = self.check_point_in_lamps_reach(xy_point)

        if not in_reach:
            xy_point = self.get_closest_point_to_point(xy_point)

        return xy_point

    def get_rgb_from_xy_and_brightness(self, x: float, y: float, bri: int = 1) -> tuple[int, int, int]:
        """Inverse of `get_xy_point_from_rgb`.

        Returns (r, g, b) for given x, y values. Implementation of the instructions found on the
        Philips Hue iOS SDK docs: http://goo.gl/kWKXKl

        The xy to color conversion is almost the same, but in reverse order.
        1. Check if the xy value is within the color gamut of the lamp.
        2. If not continue with step 2, otherwise step 3.
        3. We do this to calculate the most accurate color the given light can actually do.
        """
        xy_point = XYPoint(x, y)

        if not self.check_point_in_lamps_reach(xy_point):
            # Calculate the closest point on the color gamut triangle
            # and use that as xy value See step 6 of color to xy.
            xy_point = self.get_closest_point_to_point(xy_point)

        # Calculate XYZ values Convert using the following formulas:
        Y = bri  # noqa: N806
        X = (Y / xy_point.y) * xy_point.x  # noqa: N806
        Z = (Y / xy_point.y) * (1 - xy_point.x - xy_point.y)  # noqa: N806

        # Convert to RGB using Wide RGB D65 conversion
        r = X * 1.656492 - Y * 0.354851 - Z * 0.255038
        g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
        b = X * 0.051713 - Y * 0.121364 + Z * 1.011530

        # Apply reverse gamma correction
        r, g, b = (
            (12.92 * x)
            if (x <= 0.0031308)  # noqa: PLR2004
            else ((1.0 + 0.055) * pow(x, (1.0 / 2.4)) - 0.055)
            for x in [r, g, b]
        )

        # Bring all negative components to zero
        r, g, b = (max(0, x) for x in [r, g, b])

        # If one component is greater than 1, weight components by that value.
        max_component = max(r, g, b)
        if max_component > 1:
            r, g, b = (x / max_component for x in [r, g, b])

        r, g, b = (int(x * 255) for x in [r, g, b])

        # Convert the RGB values to your color object The rgb values from the above formulas are between 0.0 and 1.0.
        return (r, g, b)


class Converter:
    """A Converter class used to convert colors between RGB and CIE1931."""

    def __init__(self, gamut: Gamut = GamutB):
        """Initialize a Converter object."""
        self.color = ColorHelper(gamut)

    def hex_to_xy(self, h: str) -> tuple[float, float]:
        """Converts hexadecimal colors represented as a String to approximate CIE 1931 x and y coordinates."""
        rgb = self.color.hex_to_rgb(h)
        return self.rgb_to_xy(rgb[0], rgb[1], rgb[2])

    def rgb_to_xy(self, red: int, green: int, blue: int) -> tuple[float, float]:
        """Converts red, green and blue integer values to approximate CIE 1931 x and y coordinates."""
        point = self.color.get_xy_point_from_rgb(red, green, blue)
        return (point.x, point.y)

    def xy_to_hex(self, x: float, y: float, bri: int = 1) -> str:
        """Converts CIE 1931 x and y coordinates and brightness value from 0 to 1 to a CSS hex color."""
        r, g, b = self.color.get_rgb_from_xy_and_brightness(x, y, bri)
        return self.color.rgb_to_hex(r, g, b)

    def xy_to_rgb(self, x: float, y: float, bri: int = 1) -> tuple[int, int, int]:
        """Converts CIE 1931 x and y coordinates and brightness value from 0 to 1 to a CSS hex color."""
        r, g, b = self.color.get_rgb_from_xy_and_brightness(x, y, bri)
        return (r, g, b)

    def get_random_xy_color(self) -> tuple[float, float]:
        """Returns the approximate CIE 1931 x,y coordinates by the supplied hexColor parameter or a random color."""
        r = self.color.random_rgb_value()
        g = self.color.random_rgb_value()
        b = self.color.random_rgb_value()
        return self.rgb_to_xy(r, g, b)
