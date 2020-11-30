# dpaster

![build status](https://github.com/adder46/dpaster/workflows/dpaster/badge.svg) [![codecov](https://codecov.io/gh/adder46/dpaster/branch/master/graph/badge.svg?token=5DMJ1FT8SB)](https://codecov.io/gh/adder46/dpaster) [![PyPI](https://img.shields.io/badge/status-stable-brightgreen.svg)](https://pypi.org/project/thepaster/3.3.0/)

**dpaster** is a command-line client interface for [dpaste](https://dpaste.com/).

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
Usage: dpaster config [OPTIONS]

  Configure available settings

Options:
  --show                        Show current settings
  --enable-cp / --disable-cp    Copy the URL to clipboard
  --enable-raw / --disable-raw  Always get raw URL
  --default-syntax TEXT         Default syntax
  --default-expires INTEGER     Default expiry time in days
  --help                        Show this message and exit.
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


