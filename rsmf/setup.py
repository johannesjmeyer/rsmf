"""
Main routines to invoke the module from code.
"""

import re
import sys
from pathlib import Path

from .quantumarticle import QuantumarticleFormatter
from .revtex import RevtexFormatter

_FORMATTERS = [QuantumarticleFormatter, RevtexFormatter]

_comment_regex = re.compile("(%.*)")


def _clean_preamble(preamble):
    """Clean the preamble.

    This removes comments that could contain spurious information.

    Args:
        preamble (str): The preamble to be cleaned

    Returns:
        str: The cleaned preamble
    """
    preamble = _comment_regex.sub("", preamble)
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


def _parse(preamble):
    """Parse the preamble to extract the informations relevant for plot style.

    Args:
        preamble (str): The preamble, containing at least the \documentclass command.

    Returns:
        Dict: formatter_kwargs (columns, paper, fontsize)
    """
    formatter_kwargs = {}

    if "onecolumn" in preamble:
        formatter_kwargs["columns"] = "onecolumn"
    else:
        formatter_kwargs["columns"] = "twocolumn"

    if "letterpaper" in preamble:
        formatter_kwargs["paper"] = "letterpaper"
    else:
        formatter_kwargs["paper"] = "a4paper"

    if "11pt" in preamble:
        formatter_kwargs["fontsize"] = 11
    elif "12pt" in preamble:
        formatter_kwargs["fontsize"] = 12
    else:
        formatter_kwargs["fontsize"] = 10

    return formatter_kwargs


def setup(arg):
    """Get a formatter corresponding to the document's class.

    Args:
        arg (str): Either path to a tex file or preamble of a tex file, containing at least the \documentclass command.

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
    formatter_kwargs = _parse(preamble)

    result = None
    for CustomFormatter in _FORMATTERS:
        if CustomFormatter._documentclass_identifier in preamble:
            return CustomFormatter(**formatter_kwargs)

    raise Exception(
            "No formatter was found for the given argument. This means either there is no formatter, or, if you gave a file path that it does not exist."
        )
