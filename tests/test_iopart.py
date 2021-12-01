import matplotlib.pyplot as plt
import numpy as np
import pytest

from rsmf import setup
from rsmf.iopart import IOPArtFormatter, iopart_parser


class TestParse:
    """Ensure that parsing works as expected."""

    @pytest.mark.parametrize(
        "content",
        [
            r"\documentclass[10pt,notitlepage,prl]{revtex4-1}",
            r"\documentclass[10pt]{quantumarticles}",
            r"\documentclass[10pt]{IOPART}",
        ],
    )
    def test_parse_none(self, content):
        """Test that the parser returns None if the content is not for quantumarticle."""
        assert iopart_parser(content) is None

    def test_parse_default(self):
        """Test the default values."""
        content = r"\documentclass{iopart}"
        formatter = iopart_parser(content)

        assert formatter.columns == "onecolumn"
        assert formatter.fontsize == 10

    def test_parse_all(self):
        """Test the parsing of all options."""
        content = r"\documentclass[12pt]{iopart} \ioptwocol"
        formatter = iopart_parser(content)

        assert formatter.columns == "twocolumn"
        assert formatter.fontsize == 12

    def test_parse_some(self):
        """Test the parsing if only some options are present."""
        content = r"\documentclass[12pt]{iopart}"
        formatter = iopart_parser(content)

        assert formatter.columns == "onecolumn"
        assert formatter.fontsize == 12


class TestRcParams:
    """Test that rcParams are properly set."""

    def test_rcParams(self):
        preamble = r"\documentclass[12pt]{iopart}"
        formatter = setup(preamble)

        assert plt.rcParams["axes.labelsize"] == formatter.fontsizes.small
        assert plt.rcParams["axes.titlesize"] == formatter.fontsizes.large
        assert plt.rcParams["xtick.labelsize"] == formatter.fontsizes.footnotesize
        assert plt.rcParams["ytick.labelsize"] == formatter.fontsizes.footnotesize
        assert plt.rcParams["font.size"] == formatter.fontsizes.small

        assert plt.rcParams["pgf.texsystem"] == "pdflatex"
        assert plt.rcParams["text.usetex"] == True
        assert plt.rcParams["pgf.rcfonts"] == True
        assert plt.rcParams["pgf.preamble"] == ""

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
                {"columns": "twocolumn", "fontsize": 10},
                {"aspect_ratio": 1.0, "width_ratio": 1.0, "wide": False},
                (3.29, 3.29),
            ),
            (
                {"columns": "twocolumn", "fontsize": 10},
                {"aspect_ratio": 1.4, "width_ratio": 1.0, "wide": False},
                (3.29, 4.606),
            ),
            (
                {"columns": "twocolumn", "fontsize": 10},
                {"aspect_ratio": 1.0, "width_ratio": 2.0, "wide": True},
                (13.56, 13.56),
            ),
            (
                {"columns": "onecolumn", "fontsize": 12},
                {"aspect_ratio": 2.0, "width_ratio": 0.6, "wide": True},
                (3.72, 7.44),
            ),
            (
                {"columns": "onecolumn", "fontsize": 12},
                {"aspect_ratio": 2.0, "width_ratio": 1.0, "wide": False},
                (6.2, 12.4),
            ),
            (
                {"columns": "onecolumn", "fontsize": 12},
                {"aspect_ratio": 0.8, "width_ratio": 1.5, "wide": False},
                (9.3, 7.44),
            ),
        ],
    )
    def test_figure_format(self, paper_kwargs, figure_kwargs, expected_format):
        """Assert that the figure output has the correct dimensions."""
        formatter = IOPArtFormatter(**paper_kwargs)
        fig = formatter.figure(**figure_kwargs)
        assert np.allclose(fig.get_size_inches(), np.array(expected_format))
