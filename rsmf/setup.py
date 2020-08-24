from .quantumarticle import parse as quantumarticle_parse
import re
from pathlib import Path
import sys

_PARSERS = [quantumarticle_parse]

_comment_regex = re.compile("(%.*)")


def clean_preamble(preamble):
    preamble = _comment_regex.sub("", preamble)
    return preamble


def extract_preamble(path):
    lines = []

    with open(path, "r") as file:
        for line in file:
            if "\\begin{document}" in line:
                break

            lines.append(line)

    return "".join(lines)


def setup(arg):
    if Path(arg).exists():
        preamble = extract_preamble(arg)
    else:
        preamble = arg

    preamble = clean_preamble(preamble)

    result = None
    for parser in _PARSERS:
        result = parser(preamble)

        if result:
            break

    if result is None:
        raise Exception(
            "No formatter was found for the given argument. This means either there is no formatter, or, if you gave a file path that it does not exist."
        )

    return result
