from typing import IO, Optional

import click
import click_aliases
import pyperclip

from dpaster import __version__
from dpaster.config import (
    CONFIG_PATH,
    add_config_options,
    load_config,
    rm_config_options,
    save_config
)
from dpaster.paste import dpaste


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
    args = (file, syntax, expires, title, raw, copy)
    config = load_config()
    url = dpaste(config, *args)
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
    config = load_config()
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
    config = load_config()
    config = add_config_options(
        config,
        **{
            'autocp': autocp,
            'raw': raw,
            'syntax': syntax,
            'expires': expires,
        }
    )
    save_config(config)


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
    config = load_config()
    config = rm_config_options(
        config,
        **{
            'autocp': autocp,
            'raw': raw,
            'syntax': syntax,
            'expires': expires,
        }
    )
    save_config(config)
