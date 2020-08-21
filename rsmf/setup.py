from .quantumarticle import parse as quantumarticle_parse

_PARSERS = [quantumarticle_parse]


def clean_preamble(preamble):
    # TODO: remove comments
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
