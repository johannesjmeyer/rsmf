"""
Main routines to invoke the module from code.
"""

import re
from pathlib import Path

from .quantumarticle import quantumarticle_parser
from .revtex import revtex_parser
from .iopart import iopart_parser

_PARSERS = [quantumarticle_parser, revtex_parser, iopart_parser]

_COMMENT_REGEX = re.compile("(%.*)")


def _clean_content(content):
    """Clean the content.

    This removes comments that could contain spurious information.

    Args:
        content (str): The content to be cleaned

    Returns:
        str: The cleaned content
    """
    content = _COMMENT_REGEX.sub("", content)
    return content


def _extract_content(path):
    """Extract the content of a tex document.

    Args:
        path (Union[str,pathlib.Path]): Path to the tex file

    Returns:
        str: The content of the tex file
    """
    lines = []

    with open(path, "r") as file:
        for line in file:
            lines.append(line)

    return "".join(lines)


def setup(arg):
    """Get a formatter corresponding to the document's class.

    Args:
        arg (str): Either path to a tex file or some content (most of the time the preamble) 
            of a tex file, containing at least the \\documentclass command.

    Raises:
        Exception: When no formatter for the given document was found.

    Returns:
        object: A formatter for the given document/preamble.
    """
    if Path(arg).exists():
        content = _extract_content(arg)
    else:
        content = arg

    content = _clean_content(content)

    result = None
    for parser in _PARSERS:
        result = parser(content)

        if result:
            return result

    raise Exception(
        "No formatter was found for the given argument. This means either there is no formatter,"
        + " or, if you gave a file path that it does not exist."
    )
