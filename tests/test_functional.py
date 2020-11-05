import json
import os

import click
from click.testing import CliRunner

from dpaster import application
from dpaster.application import paste, config

class FakeRequests:
    def post(self, *args, **kwargs):
        return FakeResponse

class FakeResponse:
    text = "Text response"    
    def raise_for_status():
        pass

class FakePyperclip:
    def copy(self, text): 
        assert text == FakeResponse.text

def test_paste(monkeypatch, tmp_path):
    FAKE_CONF_PATH = os.path.join(str(tmp_path), "dpaster.conf")
    monkeypatch.setattr(application, "CONF_PATH", FAKE_CONF_PATH)
    monkeypatch.setattr(application, "pyperclip", FakePyperclip())
    with open(FAKE_CONF_PATH, "w") as f:
        options = {
            "enable_raw": True,
            "enable_autocp": True,
            "default_lexer": None,
            "default_expires": None
        }
        json.dump(options, f)
    monkeypatch.setattr(application, "requests", FakeRequests())
    runner = CliRunner()
    result = runner.invoke(paste, ["--syntax", "java", "--expires", 10])
    assert "Text response" in result.output
    runner.invoke(paste, ["config", "--enable-autocp"]) 

def test_paste_file_creation(monkeypatch, tmp_path):
    FAKE_CONF_PATH = os.path.join(str(tmp_path), "dpaster.conf")
    monkeypatch.setattr(application, "CONF_PATH", FAKE_CONF_PATH)
    runner = CliRunner()
    result = runner.invoke(paste, ["--syntax", "java"])
    assert os.path.exists(FAKE_CONF_PATH)

def test_config(monkeypatch, tmp_path):
    FAKE_CONF_PATH = os.path.join(str(tmp_path), "dpaster.conf")
    monkeypatch.setattr(application, "CONF_PATH", FAKE_CONF_PATH)
    with open(FAKE_CONF_PATH, "w") as f:
        options = {
            "enable_autocp": False,
            "default_lexer": None,
            "default_expires": None,
            "enable_raw": False
        }
        json.dump(options, f)

    runner = CliRunner()
    runner.invoke(config, ["--default-syntax", "java"])
    runner.invoke(config, ["--default-expires", 10])
    runner.invoke(config, ["--disable-autocp"])
   
    with open(FAKE_CONF_PATH, "r") as f:
        options = json.load(f)
        assert options["default_syntax"] == "java"
        assert options["default_expires"] == 10
        assert not options["enable_autocp"]

    result = runner.invoke(config, ["--show"])
    assert "enable_autocp: False" in result.output
    assert "default_expires: 10" in result.output
    assert "default_syntax: java" in result.output

    result = runner.invoke(config, [])
    assert "Try 'dpaster config --help' for help" in result.output

def test_default_expires_none_bug(monkeypatch, tmp_path):
    """this is supposed to raise KeyError when there is a bug"""
    FAKE_CONF_PATH = os.path.join(str(tmp_path), "dpaster.conf")
    monkeypatch.setattr(application, "CONF_PATH", FAKE_CONF_PATH)
    monkeypatch.setattr(application, "requests", FakeRequests())
    monkeypatch.setattr(application, "pyperclip", FakePyperclip())
    runner = CliRunner()
    result = runner.invoke(paste, ["--syntax", "java"], catch_exceptions=False)
    