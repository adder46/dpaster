import json
from pathlib import Path
from typing import IO, Optional

import click
import click_aliases
import pygments.lexers
import pygments.util
import pyperclip
import requests

from dpaster import __version__


CONF_PATH = Path("~/.config").expanduser() / "dpaster" / "dpaster.conf"


@click.group(cls=click_aliases.ClickAliasedGroup)
@click.pass_context
@click.version_option(__version__)
def cli(ctx: click.Context) -> None: # pylint: disable=unused-argument
    """
    Client interface for https://dpaste.com/ pastebin
    """

@cli.command(aliases=['p'])
@click.option(
    "--syntax", "-s",
    help="Choose syntax (e.g. python, java, bash)",
    required=False,
    metavar="OPT",
    type=str
)
@click.option(
    "--expires", "-e",
    help="Choose expiry time in days (e.g. 10)",
    required=False,
    metavar="OPT",
    type=int
)
@click.option(
    "--title", "-t",
    help="Choose title",
    required=False,
    metavar="OPT",
    type=str
)
@click.option(
    "--raw", "-r",
    is_flag=True,
    help="Get raw URL",
    required=False,
    metavar="OPT"
)
@click.option(
    "--copy", "-c",
    is_flag=True,
    help="Copy URL to clipboard",
    required=False,
    metavar="OPT"
)
@click.argument('file', type=click.File("r"), default="-", required=False)
def paste(file: IO, syntax: str, expires: int, title: str, raw: bool, copy: bool) -> None:
    """
    Paste to dpaste.com
    """
    try:
        with open(CONF_PATH, "r") as conf_file:
            options = json.load(conf_file)
    except FileNotFoundError:
        Path.mkdir(CONF_PATH.parent, exist_ok=True)
        with open(CONF_PATH, "w") as conf_file:
            options = {
                "enable-autocp": False,
                "enable-raw": False,
                "default-syntax": None,
                "default-expires": None
            }
            print("in with")
            json.dump(options, conf_file)

    content = file.read()

    req = requests.post(
        "http://dpaste.com/api/v2/",
        data={
            "title": title,
            "content": content,
            "syntax": syntax or options.get("default_syntax") or get_syntax(file.name, content),
            "expiry_days": expires or options.get("default_expires")
        }
    )

    req.raise_for_status()

    url: str = req.text.strip()

    if raw or options.get("enable_raw"):
        url += ".txt"

    click.echo(url)

    if copy or options["enable_autocp"]:
        pyperclip.copy(url)


@cli.command(aliases=['c'])
@click.option(
    "--show",
    is_flag=True,
    help="View current settings"
)
@click.option(
    "--enable-autocp/--disable-autocp",
    default=None,
    help="Automatically copy the URL to clipboard"
)
@click.option(
    "--enable-raw/--disable-raw",
    default=None,
    help="Always get raw URL",
    metavar="OPT",
)
@click.option(
    "--default-syntax",
    help="Choose default syntax (e.g. python, java, bash)",
    metavar="OPT"
)
@click.option(
    "--default-expires",
    help="Choose default expiry time in days (e.g. 10)",
    metavar="OPT",
    type=int
)
def config(
    show: bool,
    enable_autocp: Optional[bool],
    enable_raw: Optional[bool],
    default_syntax: Optional[str],
    default_expires: Optional[int]
) -> None:
    """
    Configure available settings
    """
    if show:
        with open(CONF_PATH, "r") as conf_file:
            options = json.load(conf_file)
        for key, value in options.items():
            click.echo("{}: {}".format(key, value))
        return None

    if all(x is None for x in {enable_autocp, enable_raw, default_syntax, default_expires}):
        click.echo("Try 'dpaster config --help' for help")
        return None

    with open(CONF_PATH, "r") as conf_file:
        options = json.load(conf_file)
        for name, value in {
            "enable-autocp": enable_autocp,
            "enable-raw": enable_raw,
            "default-syntax": default_syntax,
            "default-expires": default_expires
        }.items():
            if value is not None:
                options[name] = value

    with open(CONF_PATH, "w") as conf_file:
        json.dump(options, conf_file)


def get_syntax(filename: str, content: str) -> str:
    if filename != "<stdin>":
        try:
            syntax = pygments.lexers.guess_lexer_for_filename(filename, content)
        except pygments.util.ClassNotFound:
            return "text"
    else:
        try:
            syntax = pygments.lexers.guess_lexer(content)
        except pygments.util.ClassNotFound: # pragma: no cover
            return "text"
    syntaxes_path = Path(__file__).parent / "syntaxes.json"
    with open(syntaxes_path, "r") as f:
        syntaxes = json.load(f)
    return syntaxes.get(syntax.name, "text")
