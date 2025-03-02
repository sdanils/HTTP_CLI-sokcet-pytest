import tomllib
from typing import Any

def get_config() -> dict[str, Any]:
    """
    Загружает данные конфигурации программы.
    """
    with open("app/config.toml", "rb") as f:
        config: dict[str, Any] = tomllib.load(f)
    return config