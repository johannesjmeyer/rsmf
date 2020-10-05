from unittest.mock import patch

import matplotlib.pyplot as plt
import numpy as np
import pytest

from rsmf import setup
from rsmf.abstract_formatter import AbstractFormatter
from rsmf.fontsizes import default_fontsizes_10


@pytest.fixture(scope="function")
def abstract_formatter_mock(monkeypatch):
    """A function to create a mock formatter"""
    with monkeypatch.context() as m:
        m.setattr(AbstractFormatter, "__abstractmethods__", frozenset())
        m.setattr(AbstractFormatter, "wide_width", None)
        m.setattr(AbstractFormatter, "width", None)

        def formatter(**patch_dict):
            fmt = AbstractFormatter()

            for key, value in patch_dict.items():
                m.setattr(fmt, key, value)

            return fmt

        yield formatter


class TestRcParams:
    """Test that rcParams are properly set."""

    def test_rcParams(self, abstract_formatter_mock):
        formatter = abstract_formatter_mock()

        assert plt.rcParams["axes.labelsize"] == formatter.fontsizes.small
        assert plt.rcParams["axes.titlesize"] == formatter.fontsizes.large
        assert plt.rcParams["xtick.labelsize"] == formatter.fontsizes.footnotesize
        assert plt.rcParams["ytick.labelsize"] == formatter.fontsizes.footnotesize
        assert plt.rcParams["font.size"] == formatter.fontsizes.small

        assert plt.rcParams["pgf.texsystem"] == "pdflatex"
        assert plt.rcParams["font.family"] == ["sans-serif"]
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
    """Test the figure method."""

    @pytest.mark.parametrize(
        "patch_dict,figure_kwargs,expected_format",
        [
            (
                {"width": 1.0, "wide_width": 2.0},
                {"aspect_ratio": 1.0, "width_ratio": 1.0, "wide": False},
                (1.0, 1.0),
            ),
            (
                {"width": 1.0, "wide_width": 2.0},
                {"aspect_ratio": 0.5, "width_ratio": 1.0, "wide": True},
                (2.0, 1.0),
            ),
            (
                {"width": 1.0, "wide_width": 2.0},
                {"aspect_ratio": 1.0, "width_ratio": 1.0, "wide": True},
                (2.0, 2.0),
            ),
            (
                {"width": 0.5, "wide_width": 2.0},
                {"aspect_ratio": 2.0, "width_ratio": 1.0, "wide": False},
                (0.5, 1.0),
            ),
        ],
    )
    def test_figure_format(
        self, abstract_formatter_mock, patch_dict, figure_kwargs, expected_format
    ):
        """Assert that the figure output has the correct dimensions."""
        formatter = abstract_formatter_mock(**patch_dict)
        fig = formatter.figure(**figure_kwargs)
        assert np.allclose(fig.get_size_inches(), np.array(expected_format))

    def test_figure_error_width_not_set(self, abstract_formatter_mock):
        """Assert that the figure method throws the correct errors."""
        formatter = abstract_formatter_mock(width=None, wide_width=1.0)

        with pytest.raises(ValueError, match="The formatter's width was not set"):
            formatter.figure(wide=False)

    def test_figure_error_wide_width_not_set(self, abstract_formatter_mock):
        """Assert that the figure method throws the correct errors."""
        formatter = abstract_formatter_mock(width=1.0, wide_width=None)

        with pytest.raises(ValueError, match="The formatter's wide_width was not set"):
            formatter.figure(wide=True)
