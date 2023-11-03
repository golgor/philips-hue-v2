import os

from dotenv import load_dotenv
from loguru import logger

from philips_hue_v2.bridge import HueBridge


load_dotenv()  # take environment variables from .env.


def main() -> None:
    """Main entry point."""
    bridge = HueBridge(
        ip_address="10.0.0.37",
        client_key=os.getenv("CLIENT_KEY", ""),
        user_name=os.getenv("USER_NAME", ""),
    )


if __name__ == "__main__":
    main()
