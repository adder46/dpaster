# pylint: disable=unused-import

import pathlib

from click.testing import CliRunner
import pytest

from dpaster import application
from tests.fixtures import (
    config,
    default_options,
    fake_requests,
    fake_pyperclip,
    python_code,
)


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["--syntax", "python"],
        ["--expires", 2],
        ["--title", "Some title"],
        ["--raw"],
        ["--copy"],
        [
            "--syntax",
            "java",
            "--expires",
            10,
            "--title",
            "Another title",
            "--raw",
            "--copy",
        ],
    ],
)
def test_paste(arguments, config, default_options, fake_requests, fake_pyperclip):
    runner = CliRunner()
    result = runner.invoke(application.paste, arguments, input="spameggs")
    if "--raw" in arguments:
        assert ".txt" in result.output
    else:
        assert "dpaste" in result.output


def test_paste_config_file_creation(config):
    runner = CliRunner()
    runner.invoke(application.paste, ["--syntax", "java"])
    assert pathlib.Path(config).exists()
