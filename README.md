# dpaster

![build status](https://github.com/adder46/dpaster/workflows/dpaster/badge.svg) [![codecov](https://codecov.io/gh/adder46/dpaster/branch/master/graph/badge.svg?token=5DMJ1FT8SB)](https://codecov.io/gh/adder46/dpaster) [![PyPI](https://img.shields.io/badge/status-stable-brightgreen.svg)](https://pypi.org/project/thepaster/3.3.0/) ![Python Versions](https://img.shields.io/pypi/pyversions/thepaster?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj4KICA8ZGVmcz4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0icHlZZWxsb3ciIGdyYWRpZW50VHJhbnNmb3JtPSJyb3RhdGUoNDUpIj4KICAgICAgPHN0b3Agc3RvcC1jb2xvcj0iI2ZlNSIgb2Zmc2V0PSIwLjYiLz4KICAgICAgPHN0b3Agc3RvcC1jb2xvcj0iI2RhMSIgb2Zmc2V0PSIxIi8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJweUJsdWUiIGdyYWRpZW50VHJhbnNmb3JtPSJyb3RhdGUoNDUpIj4KICAgICAgPHN0b3Agc3RvcC1jb2xvcj0iIzY5ZiIgb2Zmc2V0PSIwLjQiLz4KICAgICAgPHN0b3Agc3RvcC1jb2xvcj0iIzQ2OCIgb2Zmc2V0PSIxIi8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogIDwvZGVmcz4KCiAgPHBhdGggZD0iTTI3LDE2YzAtNyw5LTEzLDI0LTEzYzE1LDAsMjMsNiwyMywxM2wwLDIyYzAsNy01LDEyLTExLDEybC0yNCwwYy04LDAtMTQsNi0xNCwxNWwwLDEwbC05LDBjLTgsMC0xMy05LTEzLTI0YzAtMTQsNS0yMywxMy0yM2wzNSwwbDAtM2wtMjQsMGwwLTlsMCwweiBNODgsNTB2MSIgZmlsbD0idXJsKCNweUJsdWUpIi8+CiAgPHBhdGggZD0iTTc0LDg3YzAsNy04LDEzLTIzLDEzYy0xNSwwLTI0LTYtMjQtMTNsMC0yMmMwLTcsNi0xMiwxMi0xMmwyNCwwYzgsMCwxNC03LDE0LTE1bDAtMTBsOSwwYzcsMCwxMyw5LDEzLDIzYzAsMTUtNiwyNC0xMywyNGwtMzUsMGwwLDNsMjMsMGwwLDlsMCwweiBNMTQwLDUwdjEiIGZpbGw9InVybCgjcHlZZWxsb3cpIi8+CgogIDxjaXJjbGUgcj0iNCIgY3g9IjY0IiBjeT0iODgiIGZpbGw9IiNGRkYiLz4KICA8Y2lyY2xlIHI9IjQiIGN4PSIzNyIgY3k9IjE1IiBmaWxsPSIjRkZGIi8+Cjwvc3ZnPgo=) ![License](https://img.shields.io/github/license/adder46/dpaster)

**dpaster** is a command-line client interface for [dpaste](https://dpaste.com/).

Since I caught myself often needing to share code or output of some command in a pastebin, I wrote dpaster to help me with that process and lift some of the burdens from my back. It reads from stdin by default if no file argument is passed, which means it perfectly fits in a UNIX pipeline. It is configurable and easy to use.

## Installation

This package depends on the latest version of click, which is not released yet, so it's best to clone the repo and install it with poetry.
When the new version of click is released, **dpaster** will be available as a package on PyPI, too.

## Usage

```
$ dpaster --help
Usage: dpaster [OPTIONS] COMMAND [ARGS]...

  Client interface for https://dpaste.com/ pastebin

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  config (c)  Configure available settings
  paste (p)   Paste to dpaste.com
```

## Configuring

```
$ dpaster config --help
Usage: dpaster config [OPTIONS] COMMAND [ARGS]...

  Configure available settings

Options:
  --help  Show this message and exit.

Commands:
  add
  rm
  show

$ dpaster config add --help
Usage: dpaster config add [OPTIONS]

Options:
  --autocp BOOLEAN
  --raw BOOLEAN
  --syntax TEXT
  --expires INTEGER
  --help             Show this message and exit.

$ dpaster config rm --help
Usage: dpaster config rm [OPTIONS]

Options:
  --autocp
  --raw
  --syntax
  --expires
  --help     Show this message and exit.
```

## Development

You will need [poetry](https://github.com/python-poetry/poetry), preferably with these options in config:

```toml
virtualenvs.create = true
virtualenvs.in-project = true
```

Then clone the repo, cd into it, make a venv, activate it, and install the project:

```sh
git clone https://github.com/adder46/dpaster
cd dpaster
poetry env use python3
. .venv/bin/activate
poetry install
```

To run tests, mypy checks, and style checks, you need to have Pythons:

- 3.6
- 3.7
- 3.8
- 3.9

For installing all the Python versions, I recommend [pyenv](https://github.com/pyenv/pyenv).

Once you have them, run:

```
tox
```

## Licensing

Licensed under the [MIT License](https://opensource.org/licenses/MIT). For details, see [LICENSE](https://github.com/adder46/dpaster/blob/master/LICENSE).


