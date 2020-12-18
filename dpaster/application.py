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
def cli(ctx: click.Context) -> None:  # pylint: disable=unused-argument
    """
    Client interface for https://dpaste.com/ pastebin
    """


@cli.command(aliases=["p"])
@click.option("--syntax", "-s", help="Syntax highlighter", required=False, type=str)
@click.option("--expires", "-e", help="Expiry time in days", required=False, type=int)
@click.option("--title", "-t", help="Paste title", required=False, type=str)
@click.option("--raw", "-r", is_flag=True, help="Get raw URL", required=False)
@click.option("--copy", "-c", is_flag=True, help="Copy URL to clipboard", required=False)
@click.argument("file", type=click.File("r"), default="-", required=False)
def paste(file: IO, syntax: str, expires: int, title: str, raw: bool, copy: bool) -> None:
    """
    Paste to dpaste.com
    """
    try:
        with open(CONF_PATH, "r") as conf_file:
            options = json.load(conf_file)
    except FileNotFoundError:
        options = _create_default_config()

    content = file.read()

    req = requests.post(
        "http://dpaste.com/api/v2/",
        data={
            "title": title,
            "content": content,
            "syntax": (syntax or options.get("syntax") or get_syntax(file.name, content)),
            "expiry_days": expires or options.get("expires"),
        },
    )

    req.raise_for_status()

    url: str = req.text.strip()

    if raw or options.get("raw"):
        url += ".txt"

    click.echo(url)

    if copy or options["autocp"]:
        pyperclip.copy(url)


@cli.group(aliases=["c"])
def config() -> None:
    """
    Configure available settings
    """


@config.command()
def show():
    try:
        with open(CONF_PATH, "r") as conf_file:
            options = json.load(conf_file)
        for key, value in options.items():
            click.echo("{}: {}".format(key, value))
    except FileNotFoundError:
        _create_default_config()

@config.command()
@click.option("--autocp", type=bool, required=False)
@click.option("--raw", type=bool, required=False)
@click.option("--syntax", type=str, required=False)
@click.option("--expires", type=int, required=False)
def add(
    autocp: Optional[bool],
    raw: Optional[bool],
    syntax: Optional[str],
    expires: Optional[int],
):
    with open(CONF_PATH, "r") as conf_file:
        options = json.load(conf_file)
        for name, value in {
            "autocp": autocp,
            "raw": raw,
            "syntax": syntax,
            "expires": expires,
        }.items():
            if value is not None:
                options[name] = value

    with open(CONF_PATH, "w") as conf_file:
        json.dump(options, conf_file)


@config.command()
@click.option("--autocp", required=False, is_flag=True)
@click.option("--raw", required=False, is_flag=True)
@click.option("--syntax", required=False, is_flag=True)
@click.option("--expires", required=False, is_flag=True)
def rm(
    autocp: Optional[str],
    raw: Optional[str],
    syntax: Optional[str],
    expires: Optional[str],
):
    with open(CONF_PATH, "r") as conf_file:
        options = json.load(conf_file)

    for name, value in {
        "autocp": autocp,
        "raw": raw,
        "syntax": syntax,
        "expires": expires,
    }.items():
        if value:
            options[name] = None

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
        except pygments.util.ClassNotFound:  # pragma: no cover
            return "text"
    syntaxes_path = Path(__file__).parent / "syntaxes.json"
    with open(syntaxes_path, "r") as f:
        syntaxes = json.load(f)
    return syntaxes.get(syntax.name, "text")


def _create_default_config():
    Path.mkdir(CONF_PATH.parent, exist_ok=True)
    with open(CONF_PATH, "w") as conf_file:
        options = {
            "autocp": False,
            "raw": False,
            "syntax": None,
            "expires": None,
        }
        json.dump(options, conf_file)
    return options
