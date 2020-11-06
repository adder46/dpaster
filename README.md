# dpaster

[![Build Status](https://travis-ci.org/adder46/dpaster.svg?branch=master)](https://travis-ci.org/adder46/dpaster) [![Coverage Status](https://coveralls.io/repos/github/adder46/dpaster/badge.svg?branch=master)](https://coveralls.io/github/adder46/dpaster?branch=master) [![PyPI version](https://badge.fury.io/py/thepaster.svg)](https://pypi.org/project/thepaster/3.0.2/) [![PyPI](https://img.shields.io/badge/status-stable-brightgreen.svg)](https://pypi.org/project/thepaster/3.0.2/)

**dpaster** is a command-line client interface for [dpaste](https://dpaste.com/).

## Installing dpaster

```sh
pip install thepaster
```

## Using dpaster

```sh
$ dpaster --help
Usage: dpaster [OPTIONS] COMMAND [ARGS]...

  Client interface for https://dpaste.com/ pastebin

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  config  Configure available settings
  paste   Paste to dpaste.com
```

## Configuring dpaster

```sh
$ dpaster config --help
Usage: dpaster config [OPTIONS]

  Configure available settings

Options:
  --show                          View current settings
  --enable-autocp / --disable-autocp
                                  Automatically copy the URL to clipboard
  --enable-raw / --disable-raw    Always get raw URL
  --default-syntax OPT            Choose default syntax (e.g. python, java,
                                  bash)

  --default-expires OPT           Choose default expiry time in days (e.g. 10)
  --help                          Show this message and exit.
```

## Licensing

Licensed under the [MIT License](https://opensource.org/licenses/MIT). For details, see [LICENSE](https://github.com/adder46/dpaster/blob/master/LICENSE).


