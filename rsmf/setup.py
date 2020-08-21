from .quantumarticle import parse as quantumarticle_parse
import re

_PARSERS = [quantumarticle_parse]

_comment_regex = re.compile("(%.*)")


def clean_preamble(preamble):
    preamble = _comment_regex.sub("", preamble)
    return preamble


def setup(arg):
    # TODO: if the argument is a file path, read file until \begin{document}
    preamble = clean_preamble(arg)

    result = None
    for parser in _PARSERS:
        result = parser(preamble)

        if result:
            break

    return result
