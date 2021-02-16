from typing import IO, Any, Dict
import requests
from dpaster.util import get_syntax


def dpaste(
    config: Dict[str, Any],
    file: IO,
    syntax: str,
    expires: int,
    title: str,
    raw: bool,
    copy: bool
) -> str:
    content = file.read()
    r = requests.post(
        'http://dpaste.com/api/v2/',
        data={
            'title': title,
            'content': content,
            'syntax': syntax or config.get('syntax') or get_syntax(file.name, content),
            'expiry_days': expires or config.get('expires'),
        },
    )
    r.raise_for_status()
    url: str = r.text.strip()
    if raw or config.get('raw'):
        url += '.txt'
    return url
