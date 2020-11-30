import random
import string

from dpaster import application
from tests.fixtures import python_code


def test_get_syntax_stdin(python_code):
    assert "python" in application.get_syntax("<stdin>", python_code)


def test_get_syntax_java_file():
    assert application.get_syntax("HelloWorld.java", "") == "java"


def test_get_syntax_weird_filename():
    assert application.get_syntax("main.cthulhu", "") == "text"


def test_get_syntax_weird_content():
    random.seed(123)
    content = "".join(
        ch
        for ch in [
            random.choice(string.ascii_letters + string.digits + r"!@#$%^&*()_+-=[]{}\/")
            for _ in range(100)
        ]
    )
    assert application.get_syntax("<stdin>", content) == "text"
