import json
import textwrap

import pytest

from dpaster import (
    cli,
    core,
)


class FakeRequests:
    def post(self, *args, **kwargs):
        return FakeResponse()


class FakeResponse:
    text = "http://dpaste.com/"

    def raise_for_status(self):
        pass


class FakePyperclip:
    def copy(self, text, *args, **kwargs):
        assert text == FakeResponse.text


@pytest.fixture
def config_path(monkeypatch, tmp_path):
    path = tmp_path / "dpaster.conf"
    monkeypatch.setattr(core, "CONFIG_PATH", path)
    return path


@pytest.fixture
def default_options(config_path):
    options = {
        "raw": False,
        "autocp": False,
        "syntax": None,
        "expires": None,
    }
    with open(config_path, "w") as f:
        json.dump(options, f)


@pytest.fixture
def random_options(config_path):
    options = {
        "raw": True,
        "autocp": True,
        "syntax": "python",
        "expires": 10,
    }
    with open(config_path, "w") as f:
        json.dump(options, f)


@pytest.fixture
def fake_requests(monkeypatch):
    monkeypatch.setattr(core, "requests", FakeRequests())


@pytest.fixture
def fake_pyperclip(monkeypatch):
    monkeypatch.setattr(cli, "pyperclip", FakePyperclip())


@pytest.fixture
def python_code():
    return textwrap.dedent(
        """\
        import math

        def x_plus_2pi(x: int) -> float:
            return x + math.pi

        if __name__ == "__main__":
            print(x_plus_2pi(1))
        """
    )
