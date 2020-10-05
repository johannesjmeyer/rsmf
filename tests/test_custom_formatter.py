import matplotlib.pyplot as plt
import numpy as np
import pytest

from rsmf import setup
from rsmf.custom_formatter import CustomFormatter


class TestRcParams:
    """Test that rcParams are properly set."""

    def test_rcParams(self):
        pgf_preamble = r"\usepackage{times}"
        formatter = CustomFormatter(width=2.4, pgf_preamble=pgf_preamble)

        assert plt.rcParams["axes.labelsize"] == formatter.fontsizes.small
        assert plt.rcParams["axes.titlesize"] == formatter.fontsizes.large
        assert plt.rcParams["xtick.labelsize"] == formatter.fontsizes.footnotesize
        assert plt.rcParams["ytick.labelsize"] == formatter.fontsizes.footnotesize
        assert plt.rcParams["font.size"] == formatter.fontsizes.small

        assert plt.rcParams["pgf.texsystem"] == "pdflatex"
        assert plt.rcParams["font.family"] == ["sans-serif"]
        assert plt.rcParams["text.usetex"] == False
        assert plt.rcParams["pgf.rcfonts"] == True
        assert plt.rcParams["pgf.preamble"] == pgf_preamble

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
                {"width": 1.0, "fontsizes": 11},
                {"aspect_ratio": 1.0, "width_ratio": 1.0, "wide": False},
                (1.0, 1.0),
            ),
            (
                {"wide_width": 2.0, "fontsizes": 11},
                {"aspect_ratio": 0.5, "width_ratio": 1.0, "wide": True},
                (2.0, 1.0),
            ),
            (
                {"width": 1.0, "wide_width": 2.0, "fontsizes": 11},
                {"aspect_ratio": 1.0, "width_ratio": 1.0, "wide": True},
                (2.0, 2.0),
            ),
            (
                {"width": 0.5, "wide_width": 2.0, "fontsizes": 11},
                {"aspect_ratio": 2.0, "width_ratio": 1.0, "wide": False},
                (0.5, 1.0),
            ),
        ],
    )
    def test_figure_format(self, paper_kwargs, figure_kwargs, expected_format):
        """Assert that the figure output has the correct dimensions."""
        formatter = CustomFormatter(**paper_kwargs)
        fig = formatter.figure(**figure_kwargs)
        assert np.allclose(fig.get_size_inches(), np.array(expected_format))
