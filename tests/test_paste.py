from pathlib import Path

import pytest
from click.testing import CliRunner

from dpaster import cli
from tests.fixtures import (
    config_path,
    default_options,
    fake_pyperclip,
    fake_requests,
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
def test_paste(arguments, config_path, default_options, fake_requests, fake_pyperclip):
    runner = CliRunner()
    result = runner.invoke(cli.paste, arguments, input="spameggs")
    if "--raw" in arguments:
        assert ".txt" in result.output
    else:
        assert "dpaste" in result.output


def test_paste_config_file_creation(config_path):
    runner = CliRunner()
    runner.invoke(cli.paste, ["--syntax", "java"])
    assert config_path.exists()
