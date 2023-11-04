import os

from dotenv import load_dotenv

from philips_hue_v2.bridge import HueBridge
from philips_hue_v2.lights import controller
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
    network = Network(resources=resources_response.unwrap())
    # pelare = network.get_light_by_id("3d719a7e-d47e-40d3-87e0-1bed496fa1a0")
    pelare = network.get_light_by_name("pelare")

    if not pelare:
        return

    controller.turn_on(bridge=bridge, lights=[pelare])
    controller.set_brightness(bridge=bridge, lights=[pelare], brightness=100)


if __name__ == "__main__":
    main()
