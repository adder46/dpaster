import json
from pathlib import Path
from typing import IO, Dict, Optional, Union

import click
import click_aliases
import pygments.lexers
import pygments.util
import pyperclip
import requests

from dpaster import __version__


CONFIG_PATH = Path('~/.config').expanduser() / 'dpaster' / 'dpaster.conf'


@click.group(cls=click_aliases.ClickAliasedGroup)
@click.pass_context
@click.version_option(__version__)
def cli(ctx: click.Context) -> None:  # pylint: disable=unused-argument
    """
    Client interface for https://dpaste.com/ pastebin
    """


@cli.command(aliases=['p'])
@click.option('--syntax', '-s', help='Syntax highlighter', required=False, type=str)
@click.option('--expires', '-e', help='Expiry time in days', required=False, type=int)
@click.option('--title', '-t', help='Paste title', required=False, type=str)
@click.option('--raw', '-r', is_flag=True, help='Get raw URL', required=False)
@click.option('--copy', '-c', is_flag=True, help='Copy URL to clipboard', required=False)
@click.argument('file', type=click.File('r'), default='-', required=False)
def paste(file: IO, syntax: str, expires: int, title: str, raw: bool, copy: bool) -> None:
    """
    Paste to dpaste.com
    """
    config = _load_config()
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

    click.echo(url)

    if copy or config['autocp']:
        pyperclip.copy(url)


@cli.group(aliases=['c'])
def config() -> None:
    """
    Configure available config
    """


@config.command()
def show() -> None:
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = _create_default_config()
    finally:
        for option, value in config.items():
            click.echo('{}: {}'.format(option, value))


@config.command()
@click.option('--autocp', type=bool, required=False, is_flag=True)
@click.option('--raw', type=bool, required=False, is_flag=True)
@click.option('--syntax', type=str, required=False)
@click.option('--expires', type=int, required=False)
def add(
    autocp: Optional[bool],
    raw: Optional[bool],
    syntax: Optional[str],
    expires: Optional[int],
) -> None:
    config = _load_config()
    config = _add_config_option(
        config,
        **{
            'autocp': autocp,
            'raw': raw,
            'syntax': syntax,
            'expires': expires,
        }
    )
    _save_config(config)


@config.command()
@click.option('--autocp', required=False, is_flag=True)
@click.option('--raw', required=False, is_flag=True)
@click.option('--syntax', required=False, is_flag=True)
@click.option('--expires', required=False, is_flag=True)
def rm(
    autocp: Optional[bool],
    raw: Optional[bool],
    syntax: Optional[bool],
    expires: Optional[bool],
) -> None:
    config = _load_config()
    config = _rm_config_option(
        config,
        **{
            'autocp': autocp,
            'raw': raw,
            'syntax': syntax,
            'expires': expires,
        }
    )
    _save_config(config)

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


def _create_default_config() -> Dict[str, Union[bool, None]]:
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


def _load_config() -> Dict[str, Union[bool, int, str, None]]:
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = _create_default_config()
    return config


def _save_config(config: Dict[str, Union[bool, int, str, None]]) -> None:
    if not CONFIG_PATH.parent.exists():
        CONFIG_PATH.parent.mkdir(exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)


def _add_config_option(
    config: Dict[str, Union[bool, int, str, None]], **kwargs
) -> Dict[str, Union[bool, int, str, None]]:
    for option, value in kwargs.items():
        if value is not None:
            config[option] = value
    return config


def _rm_config_option(
    config: Dict[str, Union[bool, int, str, None]], **kwargs
) -> Dict[str, Union[bool, int, str, None]]:
    for name, value in kwargs.items():
        if value:
            config[name] = None
    return config
