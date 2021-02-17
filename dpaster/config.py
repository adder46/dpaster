import json
from pathlib import Path
from typing import Any, Dict


CONFIG_PATH = Path('~/.config').expanduser() / 'dpaster' / 'dpaster.conf'


def load_config() -> Dict[str, Any]:
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return create_default_config()


def create_default_config() -> Dict[str, Any]:
    config = {
        'autocp': False,
        'raw': False,
        'syntax': None,
        'expires': None,
    }
    save_config(config)
    return config


def save_config(config: Dict[str, Any]) -> None:
    _ensure_config_folder()
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)


def _ensure_config_folder() -> None:
    if not CONFIG_PATH.parent.exists():
        CONFIG_PATH.parent.mkdir(exist_ok=True)


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
