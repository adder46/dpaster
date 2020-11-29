import json

from click.testing import CliRunner
import pytest

from dpaster import application
from tests.fixtures import config, default_options  # pylint: disable=unused-import


@pytest.mark.parametrize(
    "option, value",
    [
        ["--enable-cp", True],
        ["--enable-raw", True],
        ["--default-expires", 10],
        ["--default-syntax", "python"],
    ],
)
def test_config_setting_options(option, value, config, default_options):
    runner = CliRunner()
    runner.invoke(
        application.config,
        [option] + [value] if not isinstance(value, bool) else [option],
    )
    with open(config, "r") as f:
        options = json.load(f)
    assert options[option[2:]] == value


def test_config_no_arguments():
    runner = CliRunner()
    result = runner.invoke(application.config, [])
    assert result.output == "Try 'dpaster config --help' for help\n"


def test_config_show(config, default_options):
    runner = CliRunner()
    result = runner.invoke(application.config, ["--show"])
    assert "enable-raw: False" in result.output
    assert "enable-autocp: False" in result.output
    assert "default-lexer: None" in result.output
    assert "default-expires: None" in result.output
