import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from dpaster import cli
from tests.fixtures import config, default_options, random_options


@pytest.mark.parametrize(
    "option, value",
    [
        ["--autocp", True],
        ["--raw", True],
        ["--expires", 10],
        ["--syntax", "python"],
    ],
)
def test_config_add(option, value, config, default_options):
    runner = CliRunner()
    runner.invoke(
        cli.add,
        [option, value] if not isinstance(value, bool) else [option]
    )
    with open(config, "r") as f:
        options = json.load(f)
    assert options[option[2:]] == value


@pytest.mark.parametrize(
    "option",
    [
        "--autocp",
        "--raw",
        "--expires",
        "--syntax",
    ],
)
def test_config_rm(option, config, random_options):
    runner = CliRunner()
    runner.invoke(cli.rm, [option])
    with open(config, "r") as f:
        options = json.load(f)
    assert options[option[2:]] is None


def test_config_no_arguments():
    runner = CliRunner()
    result = runner.invoke(cli.config, [])
    assert "Usage: config [OPTIONS] COMMAND [ARGS]" in result.output


def test_config_show(config, default_options):
    runner = CliRunner()
    result = runner.invoke(cli.show, [])
    assert "raw: False" in result.output
    assert "autocp: False" in result.output
    assert "syntax: None" in result.output
    assert "expires: None" in result.output

def test_config_file_creation(config):
    runner = CliRunner()
    runner.invoke(cli.show, [])
    assert Path(config).exists()
