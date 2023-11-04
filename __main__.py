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
    network = Network(resources=resources_response.unwrap())
    network_lights = network.get_lights()
    if not network_lights:
        return
    bridge.turn_off(lights=[network_lights[7]])


if __name__ == "__main__":
    main()
