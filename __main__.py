import json
import os

from dotenv import load_dotenv
from loguru import logger

from philips_hue_v2.authentication import get_access_token


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


if __name__ == "__main__":
    main()
