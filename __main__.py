import os

from dotenv import load_dotenv

from philips_hue_v2.bridge import HueBridge
from philips_hue_v2.resource.network import Network
from philips_hue_v2.resource.requests import get_resources


load_dotenv()  # take environment variables from .env.


def main() -> None:
    """Main entry point."""
    bridge = HueBridge(
        ip_address="ecb5fa197557.home",
        client_key=os.getenv("CLIENT_KEY", ""),
        user_name=os.getenv("USER_NAME", ""),
    )
    resources_response = get_resources(bridge)
    network = Network(resources=resources_response.unwrap(), bridge=bridge)
    bibblan = network.get_light_by_id("23e8c74f-7c0e-40ae-b61d-f10df2f165be")
    # bibblan = network.get_light_by_name("pelare")

    if not bibblan:
        return

    bibblan.turn_on()
    # bibblan.set_brightness(brightness=100)
    bibblan.set_rgb_color({"red": 100, "green": 0, "blue": 100})


if __name__ == "__main__":
    main()
