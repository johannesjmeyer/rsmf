import pytest
import numpy as np
from rsmf.revtex import parse, Revtex
import matplotlib.pyplot as plt


class TestParse:
    """Ensure that parsing works as expected."""

    @pytest.mark.parametrize(
        "preamble",
        [
            r"\documentclass[10pt,notitlepage,prl]{quantumarticle}",
            r"\documentclass[10pt]{revtex}",
            r"\documentclass[10pt]{REXTEX}",
        ],
    )
    def test_parse_none(self, preamble):
        """Test that the parser returns None if the preamble is not for quantumarticle."""
        assert parse(preamble) is None

    def test_parse_default(self):
        """Test the default values."""
        preamble = r"\documentclass{revtex4-1}"
        formatter = parse(preamble)

        assert formatter is not None

        assert formatter.columns == "twocolumn"
        assert formatter.fontsize == 10

    def test_parse_all(self):
        """Test the parsing of all options."""
        preamble = r"\documentclass[onecolumn,unpublished,letterpaper,11pt]{revtex4-1}"
        formatter = parse(preamble)

        assert formatter is not None

        assert formatter.columns == "onecolumn"
        assert formatter.fontsize == 11

    def test_parse_some(self):
        """Test the parsing if only some options are present."""
        preamble = r"\documentclass[a4paper,12pt,noarxiv]{revtex4-1}"
        formatter = parse(preamble)

        assert formatter is not None

        assert formatter.columns == "twocolumn"
        assert formatter.fontsize == 12


class TestRcParams:
    """Test that rcParams are properly set."""

    def test_rcParams(self):
        preamble = r"\documentclass[a4paper,12pt,noarxiv]{revtex4-1}"
        formatter = parse(preamble)

        assert plt.rcParams["axes.labelsize"] == formatter.fontsizes.small
        assert plt.rcParams["axes.titlesize"] == formatter.fontsizes.large
        assert plt.rcParams["xtick.labelsize"] == formatter.fontsizes.footnotesize
        assert plt.rcParams["ytick.labelsize"] == formatter.fontsizes.footnotesize
        assert plt.rcParams["font.size"] == formatter.fontsizes.small

        assert plt.rcParams["pgf.texsystem"] == "pdflatex"
        assert plt.rcParams["font.family"] == ["serif"]
        assert plt.rcParams["text.usetex"] == False
        assert plt.rcParams["pgf.rcfonts"] == True

        assert plt.rcParams["xtick.direction"] == "in"
        assert plt.rcParams["ytick.direction"] == "in"
        assert plt.rcParams["xtick.major.size"] == 4
        assert plt.rcParams["ytick.major.size"] == 4
        assert plt.rcParams["lines.linewidth"] == 1
        assert plt.rcParams["axes.linewidth"] == 0.5
        assert plt.rcParams["grid.linewidth"] == 0.5
        assert plt.rcParams["lines.markersize"] == 3

        assert plt.rcParams["legend.frameon"] == True
        assert plt.rcParams["legend.framealpha"] == 1.0
        assert plt.rcParams["legend.fancybox"] == False


class TestFigure:
    """Test that the constructed figures have the proper dimensions."""

    @pytest.mark.parametrize(
        "paper_kwargs,figure_kwargs,expected_format",
        [
            (
                {"columns": "twocolumn", "fontsize": 11},
                {"aspect_ratio": 1.0, "width_ratio": 1.0, "wide": False},
                (3.42, 3.42),
            ),
            (
                {"columns": "twocolumn", "fontsize": 11},
                {"aspect_ratio": 1.4, "width_ratio": 1.0, "wide": False},
                (3.42, 4.788),
            ),
            (
                {"columns": "twocolumn", "fontsize": 11},
                {"aspect_ratio": 1.0, "width_ratio": 2.0, "wide": True},
                (14.16, 14.16),
            ),
            (
                {"columns": "twocolumn", "fontsize": 11},
                {"aspect_ratio": 2.0, "width_ratio": 0.6, "wide": True},
                (4.248, 8.496),
            ),
            (
                {"columns": "onecolumn", "fontsize": 11},
                {"aspect_ratio": 2.0, "width_ratio": 1.0, "wide": False},
                (3.42, 6.84),
            ),
            (
                {"columns": "onecolumn", "fontsize": 11},
                {"aspect_ratio": 0.8, "width_ratio": 1.5, "wide": False},
                (5.13, 4.104),
            ),
        ],
    )
    def test_figure_format(self, paper_kwargs, figure_kwargs, expected_format):
        """Assert that the figure output has the correct dimensions."""
        formatter = Revtex(**paper_kwargs)
        fig = formatter.figure(**figure_kwargs)
        assert np.allclose(fig.get_size_inches(), np.array(expected_format))
