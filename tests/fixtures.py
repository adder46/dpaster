import json
import textwrap

import pytest

from dpaster import application


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
def config(monkeypatch, tmp_path):
    config_path = tmp_path / "dpaster.conf"
    monkeypatch.setattr(
        application,
        "CONF_PATH",
        config_path
    )
    return config_path


@pytest.fixture
def default_options(config):
    options = {
        "enable-raw": False,
        "enable-autocp": False,
        "default-lexer": None,
        "default-expires": None
    }
    with open(config, "w") as f:
        json.dump(options, f)


@pytest.fixture
def fake_requests(monkeypatch):
    monkeypatch.setattr(application, "requests", FakeRequests())


@pytest.fixture
def fake_pyperclip(monkeypatch):
    monkeypatch.setattr(application, "pyperclip", FakePyperclip())


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
