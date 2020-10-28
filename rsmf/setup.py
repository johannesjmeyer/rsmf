"""
Main routines to invoke the module from code.
"""

import re
from pathlib import Path

from .quantumarticle import quantumarticle_parser
from .revtex import revtex_parser

_PARSERS = [quantumarticle_parser, revtex_parser]

_COMMENT_REGEX = re.compile("(%.*)")


def _clean_preamble(preamble):
    """Clean the preamble.

    This removes comments that could contain spurious information.

    Args:
        preamble (str): The preamble to be cleaned

    Returns:
        str: The cleaned preamble
    """
    preamble = _COMMENT_REGEX.sub("", preamble)
    return preamble


def _extract_preamble(path):
    """Extract the preamble of a tex document.

    Args:
        path (Union[str,pathlib.Path]): Path to the tex file

    Returns:
        str: The preamble of the tex file
    """
    lines = []

    with open(path, "r") as file:
        for line in file:
            if "\\begin{document}" in line:
                break

            lines.append(line)

    return "".join(lines)


def setup(arg):
    """Get a formatter corresponding to the document's class.

    Args:
        arg (str): Either path to a tex file or preamble of a tex file,
            containing at least the \\documentclass command.

    Raises:
        Exception: When no formatter for the given document was found.

    Returns:
        object: A formatter for the given document/preamble.
    """
    if Path(arg).exists():
        preamble = _extract_preamble(arg)
    else:
        preamble = arg

    preamble = _clean_preamble(preamble)

    result = None
    for parser in _PARSERS:
        result = parser(preamble)

        if result:
            return result

    raise Exception(
        "No formatter was found for the given argument. This means either there is no formatter,"
        + " or, if you gave a file path that it does not exist."
    )
