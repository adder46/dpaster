import json
from pathlib import Path
from typing import Any, Dict


CONFIG_PATH = Path('~/.config').expanduser() / 'dpaster' / 'dpaster.conf'


def create_default_config() -> Dict[str, Any]:
    Path.mkdir(CONFIG_PATH.parent, exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        config = {
            'autocp': False,
            'raw': False,
            'syntax': None,
            'expires': None,
        }
        json.dump(config, f)
    return config


def load_config() -> Dict[str, Any]:
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = create_default_config()
    return config


def save_config(config: Dict[str, Any]) -> None:
    if not CONFIG_PATH.parent.exists():
        CONFIG_PATH.parent.mkdir(exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)


def add_config_options(config: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    for option, value in kwargs.items():
        if value is not None:
            config[option] = value
    return config


def rm_config_options(config: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    for option, value in kwargs.items():
        if value:
            config[option] = None
    return config
