import json
import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from philips_hue_v2.authentication import get_access_token
from philips_hue_v2.bridge import HueBridge, load_bridge_from_file


load_dotenv()  # take environment variables from .env.


def main() -> None:
    """Main entry point."""
    client_key = os.getenv("CLIENT_KEY")
    if client_key is None:
        result = get_access_token("10.0.0.37", "philips_hue_v2", "golgor")
        if result.is_ok():
            data = result.unwrap()
            logger.info(f"Access token:\n{json.dumps(data, indent=4)}")
        else:
            logger.error(result.unwrap_err())

    bridge_path = Path("bridge.json")
    bridge = load_bridge_from_file(bridge_path)
    print(bridge)


if __name__ == "__main__":
    main()
