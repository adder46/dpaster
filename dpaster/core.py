import json
from pathlib import Path
from typing import IO, Any, Dict

import pygments.lexers
import pygments.util
import requests


CONFIG_PATH = Path('~/.config').expanduser() / 'dpaster' / 'dpaster.conf'


def paste_to_dpaste(
    config: Dict[str, Any],
    file: IO,
    syntax: str,
    expires: int,
    title: str,
    raw: bool,
    copy: bool
) -> str:
    content = file.read()

    r = requests.post(
        'http://dpaste.com/api/v2/',
        data={
            'title': title,
            'content': content,
            'syntax': syntax or config.get('syntax') or get_syntax(file.name, content),
            'expiry_days': expires or config.get('expires'),
        },
    )
    r.raise_for_status()

    url: str = r.text.strip()
    if raw or config.get('raw'):
        url += '.txt'
    return url


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


def get_syntax(filename: str, content: str) -> str:
    if filename != '<stdin>':
        try:
            syntax = pygments.lexers.guess_lexer_for_filename(filename, content)
        except pygments.util.ClassNotFound:
            return 'text'
    else:
        try:
            syntax = pygments.lexers.guess_lexer(content)
        except pygments.util.ClassNotFound:  # pragma: no cover
            return 'text'
    syntaxes_path = Path(__file__).parent / 'syntaxes.json'
    with open(syntaxes_path, 'r') as f:
        syntaxes = json.load(f)
    return syntaxes.get(syntax.name, 'text')
