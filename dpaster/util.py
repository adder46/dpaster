import json
from pathlib import Path

import pygments.lexers
import pygments.util


def get_syntax(filename: str, content: str) -> str:
    if filename != '<stdin>':
        try:
            syntax = pygments.lexers.guess_lexer_for_filename(filename, content)
        except pygments.util.ClassNotFound:
            return 'text'
    else:
        try:
            syntax = pygments.lexers.guess_lexer(content)
        except pygments.util.ClassNotFound:  # pragma: no cover
            return 'text'
    syntaxes_path = Path(__file__).parent / 'syntaxes.json'
    with open(syntaxes_path, 'r') as f:
        syntaxes = json.load(f)
    return syntaxes.get(syntax.name, 'text')
