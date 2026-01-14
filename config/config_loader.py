import yaml
from pathlib import Path

_CONFIG_CACHE = None


def load_config(path: str = "config/system.yaml") -> dict:
    global _CONFIG_CACHE

    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE

    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(config_path, "r", encoding="utf-8") as f:
        _CONFIG_CACHE = yaml.safe_load(f)

    return _CONFIG_CACHE
