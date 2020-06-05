import json
import os

import click
import pygments.lexers
import pygments.util
import pyperclip
import requests

from dpaster import __version__


CONF_PATH = os.path.join(os.path.expanduser("~/.config"), "dpaster", "dpaster.conf")
PRETTY_TIME = {
    "onetime": "onetime",
    "hour": "3600",
    "day": "86400",
    "week": "604800",
}

@click.group()
@click.pass_context
@click.version_option(__version__)
def cli(ctx):
    """
    Client interface for https://dpaste.org/ pastebin
    """

@cli.command()
@click.option(
    "--lexer", "-l",
    help="Choose a lexer (e.g. python, java, bash)",
    required=False,
    metavar="OPT"
)
@click.option(
    "--expires", "-e",
    help="Choose expiry time (e.g. onetime, hour, day, week)",
    required=False,
    metavar="OPT",
    type=click.Choice(["onetime", "hour", "day", "week"])
)
# @click.option(
#     "--raw", "-r",
#     is_flag=True,
#     help="Get raw URL",
#     required=False,
#     metavar="OPT"
# )
@click.argument('file', type=click.File("r"), default="-", required=False)
# def paste(file, lexer, expires, raw):
def paste(file, lexer, expires):
    """
    Paste to dpaste.org
    """
    try:
        with open(CONF_PATH, "r") as conf_file:
            options = json.load(conf_file)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(CONF_PATH), exist_ok=True)
        with open(CONF_PATH, "w") as conf_file:
            options = {
                "enable_autocp": False,
                "enable_raw": False,
                "default_lexer": None,
                "default_expires": None
            }
            json.dump(options, conf_file)

    content = file.read()

    req = requests.post(
        "https://dpaste.org/api/",
        data={
            "content": content,
            "format": "url",
            "lexer": lexer if lexer else options["default_lexer"] or get_lexer(file.name, content),
            "expires": (
                PRETTY_TIME.get(expires) if expires else
                PRETTY_TIME.get(options["default_expires"])
            )
        }
    )

    req.raise_for_status()

    # url = req.text.strip() + ("/raw" if raw or options["enable_raw"] else "")
    url = req.text.strip()
    click.echo(url)

    if options["enable_autocp"]:
        pyperclip.copy(url)

@cli.command()
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
# @click.option(
#     "--enable-raw/--disable-raw",
#     default=None,
#     help="Always get raw URL",
#     metavar="OPT",
# )
@click.option(
    "--default-lexer",
    help="Choose default lexer (e.g. python, java, bash)",
    metavar="OPT"
)
@click.option(
    "--default-expires",
    help="Choose default expiry time (e.g. onetime, hour, day, week)",
    metavar="OPT",
    type=click.Choice(["onetime", "hour", "day", "week"])
)
# def config(show, enable_autocp, enable_raw, default_lexer, default_expires):
def config(show, enable_autocp, default_lexer, default_expires):
    """
    Configure available settings
    """
    if show:
        with open(CONF_PATH, "r") as conf_file:
            options = json.load(conf_file)
            for key, value in options.items():
                print("{}: {}".format(key, value))
            return

    # if all(x is None for x in {enable_autocp, enable_raw, default_lexer, default_expires}):
    if all(x is None for x in {enable_autocp, default_lexer, default_expires}):
        click.echo("Try 'dpaster config --help' for help")
        return

    with open(CONF_PATH, "r") as conf_file:
        options = json.load(conf_file)
        for name, value in {
            "enable_autocp": enable_autocp,
            # "enable_raw": enable_raw,
            "default_lexer": default_lexer,
            "default_expires": default_expires
        }.items():
            if value is not None:
                options[name] = value

    with open(CONF_PATH, "w") as conf_file:
        json.dump(options, conf_file)


def get_lexer(filename, content):
    if filename != "<stdin>":
        try:
            lexer = pygments.lexers.guess_lexer_for_filename(filename, content)
        except pygments.util.ClassNotFound:
            return "_text"
    else:
        try:
            lexer = pygments.lexers.guess_lexer(content)
        except pygments.util.ClassNotFound:
            return "_text"
    return {
        "plain text": "_text",
        "markdown": "_markdown",
        "restructuredtext": "_rst",
        "plain code": "_code",
        "arduino": "arduino",
        "bash": "bash",
        "batchfile": "bat",
        "c": "c",
        "clojure": "clojure",
        "cmake": "cmake",
        "coffeescript": "coffee-script",
        "common lisp": "common-lisp",
        "console/bash session": "console",
        "c#": "csharp",
        "css": "css",
        "cuda": "cuda",
        "dart": "dart",
        "delphi": "delphi",
        "diff": "diff",
        "django/jinja": "django",
        "docker": "docker",
        "elixir": "elixir",
        "erlang": "erlang",
        "go": "go",
        "handlebars": "handlebars",
        "haskell": "haskell",
        "html": "html",
        "html + django/jinja": "html+django",
        "ini": "ini",
        "ipython console session": "ipythonconsole",
        "irc logs": "irc",
        "java": "java",
        "javascript": "js",
        "json": "json",
        "jsx/react": "jsx",
        "kotlin": "kotlin",
        "lesscss": "less",
        "lua": "lua",
        "makefile": "make",
        "matlab": "matlab",
        "nginx configuration file": "nginx",
        "numpy": "numpy",
        "objective-c": "objective-c",
        "perl": "perl",
        "php": "php",
        "postgresql sql dialect": "postgresql",
        "python 2.x": "python",
        "python": "python",
        "ruby": "rb",
        "rust": "rust",
        "sass": "sass",
        "scss": "scss",
        "solidity": "sol",
        "sql": "sql",
        "swift": "swift",
        "tex": "tex",
        "typoscript": "typoscript",
        "viml": "vim",
        "xml": "xml",
        "xslt": "xslt",
        "yaml": "yaml",
    }.get(lexer.name.lower(), "_text")