import random
import string

from dpaster import util
from tests.fixtures import python_code


def test_get_syntax_stdin(python_code):
    assert "python" in util.get_syntax("<stdin>", python_code)


def test_get_syntax_java_file():
    assert util.get_syntax("HelloWorld.java", "") == "java"


def test_get_syntax_weird_filename():
    assert util.get_syntax("main.cthulhu", "") == "text"


def test_get_syntax_weird_content():
    random.seed(123)
    content = "".join(
        ch
        for ch in [
            random.choice(string.ascii_letters + string.digits + r"!@#$%^&*()_+-=[]{}\/")
            for _ in range(100)
        ]
    )
    assert util.get_syntax("<stdin>", content) == "text"
