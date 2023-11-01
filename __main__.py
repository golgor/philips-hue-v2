from dotenv import load_dotenv

from philips_hue_v2.bridge import (
    HueBridge,
    get_access_token_from_bridge,
)


load_dotenv()  # take environment variables from .env.


def main() -> None:
    """Main entry point."""
    bridge = HueBridge(ip_address="10.0.0.37")
    bridge = get_access_token_from_bridge(bridge, "philips_hue_v2", "golgor")

    # bridge_path = Path("bridge.json")
    # bridge = load_bridge_from_file(bridge_path)
    # print(bridge)


if __name__ == "__main__":
    main()
