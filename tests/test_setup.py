import pytest
from pathlib import Path
import rsmf
from rsmf.setup import setup, _clean_preamble, _extract_preamble

DUMMY_PATH = Path(__file__).parent / "dummy.tex"


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

        assert preamble == _clean_preamble(preamble)

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

        assert expected_output == _clean_preamble(preamble)

    def test_extract_preamble(self):
        preamble = _extract_preamble(DUMMY_PATH)

        assert (
            preamble
            == r"""\documentclass[
	twoside,
	a4paper, 						% A4 Format benutzen
%	headsepline,						% Linie nach Kopfzeile
]{quantumarticle}							% oder auch "scrartcl"

\pdfoutput=1

\usepackage{amsmath} 					% Paket 
\usepackage{amssymb} 					% Paket
\usepackage[a4paper, left=2.5cm, right=2.5cm, top=3cm, bottom=3cm,bindingoffset=5mm]{geometry}

\hyphenation{awe-some}

"""
        )

    def test_extract_and_clean_preamble(self):
        preamble = _clean_preamble(_extract_preamble(DUMMY_PATH))

        assert (
            preamble
            == r"""\documentclass[
	twoside,
	a4paper, 						

]{quantumarticle}							

\pdfoutput=1

\usepackage{amsmath} 					
\usepackage{amssymb} 					
\usepackage[a4paper, left=2.5cm, right=2.5cm, top=3cm, bottom=3cm,bindingoffset=5mm]{geometry}

\hyphenation{awe-some}

"""
        )


class TestSetup:
    """Test that setup works as expected."""

    def test_setup_equivalence(self):
        """Test that setup from file is equivalent to string setup."""
        result1 = setup(r"\documentclass[twoside,a4paper,headsepline]{quantumarticle}")
        result2 = setup(DUMMY_PATH)

        assert result1 == result2
