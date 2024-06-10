from typing import Any
import os.path
import json

settings = dict()

if os.path.exists('config.json'):
    with open('config.json', 'r') as f:
        try:
            settings = json.load(f)
        except ValueError:
            pass

def get(key: str, default: Any = None) -> Any:
    """Get a value from the settings file."""
    return settings.get(key, default)

def set(key: str, value: Any) -> None:
    """Set a value in the settings file."""
    settings[key] = value

    with open('config.json', 'w') as f:
        json.dump(settings, f)