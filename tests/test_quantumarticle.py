import pytest
from rsmf.quantumarticle import parse, Quantumarticle

class TestParse:
    """Ensure that parsing works as expected."""

    @pytest.mark.parametrize("preamble", [
        r"\documentclass[10pt,notitlepage,prl]{revtex4-1}",
        r"\documentclass[10pt]{quantumarticles}",
        r"\documentclass[10pt]{Quantumarticle}",
    ])
    def test_parse_none(self, preamble):
        assert parse(preamble) is None

    def test_parse_default(self):
        preamble = r"\documentclass{quantumarticle}"
        result = parse(preamble)

        assert result is not None

        assert result.paper == "a4paper"
        assert result.columns == "twocolumn"
        assert result.fontsize == 10

    def test_parse_all(self):
        preamble = r"\documentclass[onecolumn,unpublished,letterpaper,11pt]{quantumarticle}"
        result = parse(preamble)

        assert result is not None

        assert result.paper == "letterpaper"
        assert result.columns == "onecolumn"
        assert result.fontsize == 11

    def test_parse_some(self):
        preamble = r"\documentclass[a4paper,12pt,noarxiv]{quantumarticle}"
        result = parse(preamble)

        assert result is not None

        assert result.paper == "a4paper"
        assert result.columns == "twocolumn"
        assert result.fontsize == 12