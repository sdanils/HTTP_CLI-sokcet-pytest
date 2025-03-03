import tomllib
from typing import Any

def get_config() -> dict[str, Any]:
    """
    Loads the program configuration data.
    """
    with open("app/config.toml", "rb") as f:
        config: dict[str, Any] = tomllib.load(f)
    return config