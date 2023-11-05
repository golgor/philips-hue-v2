import os

from dotenv import load_dotenv

from philips_hue_v2.bridge import HueBridge
from philips_hue_v2.resource.network import Network, unpickle_network
from philips_hue_v2.resource.requests import get_resources


load_dotenv()  # take environment variables from .env.


def main_load_pickled_network() -> None:
    """Main entry point when using a pickled network."""
    network = unpickle_network()
    bibblan = network.get_light_by_id("23e8c74f-7c0e-40ae-b61d-f10df2f165be")

    if not bibblan:
        return

    bibblan.turn_on()
    bibblan.set_color_temperature(6500)


def main() -> None:
    """Main entry point."""
    bridge = HueBridge(
        ip_address="ecb5fa197557.home",
        client_key=os.getenv("CLIENT_KEY", ""),
        user_name=os.getenv("USER_NAME", ""),
    )
    resources_response = get_resources(bridge)
    resources = resources_response.unwrap()
    network = Network(resources=resources, bridge=bridge)

    bibblan = network.get_light_by_id("23e8c74f-7c0e-40ae-b61d-f10df2f165be")

    if not bibblan:
        return

    bibblan.turn_on()
    bibblan.set_rgb_color({"red": 255, "green": 255, "blue": 255})


if __name__ == "__main__":
    main_load_pickled_network()
