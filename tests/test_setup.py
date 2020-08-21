import pytest
from rsmf.setup import setup, clean_preamble


class TestHelperMethods:
    """Test that the helper methods function properly."""

    @pytest.mark.parametrize(
        "preamble",
        [
            r"\documentclass{quantumarticle}",
            r"\documentclass{revtex4-1}",
            r"""\documentclass{revtex4-1}
        \usepackage{biblatex}
        \usepackage{amsmath}
        \newcommand{\test}[1]{#1!!}""",
        ],
    )
    def test_no_clean(self, preamble):
        """Test that strings that need no cleaning are not altered."""

        assert preamble == clean_preamble(preamble)

    @pytest.mark.parametrize(
        "preamble,expected_output",
        [
            (
                r"\documentclass{quantumarticle} %\documentclass{revtex4-1}",
                r"\documentclass{quantumarticle} ",
            ),
            (r"\documentclass{quantumarticle}%{revtex4-1}", r"\documentclass{quantumarticle}"),
            (
                "%\\documentclass[prl]{revtex4-1}\n\\documentclass[noarxiv]{quantumarticle}",
                "\n\\documentclass[noarxiv]{quantumarticle}",
            ),
            (
                "%\\documentclass[prl]{revtex4-1}\n\\documentclass[noarxiv]{quantumarticle}\n%\\usepackage{amsmath}\n\\usepackage{doi}",
                "\n\\documentclass[noarxiv]{quantumarticle}\n\n\\usepackage{doi}",
            ),
        ],
    )
    def test_remove_comment(self, preamble, expected_output):
        """Test that strings that need no cleaning are not altered."""

        assert expected_output == clean_preamble(preamble)
