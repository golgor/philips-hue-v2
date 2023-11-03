import os

from dotenv import load_dotenv
from loguru import logger

from philips_hue_v2.bridge import HueBridge
from philips_hue_v2.resource.get_resources import get_resources
from philips_hue_v2.resource.network import Network


load_dotenv()  # take environment variables from .env.


def main() -> None:
    """Main entry point."""
    bridge = HueBridge(
        ip_address="10.0.0.37",
        client_key=os.getenv("CLIENT_KEY", ""),
        user_name=os.getenv("USER_NAME", ""),
    )
    test = get_resources(bridge)
    if test.is_err():
        logger.error(test.unwrap_err())

    network = Network(test.unwrap())


if __name__ == "__main__":
    main()
