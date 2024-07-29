import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pytest

import rsmf.abstract_formatter
from rsmf.abstract_formatter import AbstractFormatter


@pytest.fixture(scope="function")
def abstract_formatter_mock(monkeypatch):
    """A function to create a mock formatter"""
    with monkeypatch.context() as m:
        m.setattr(AbstractFormatter, "__abstractmethods__", frozenset())
        m.setattr(AbstractFormatter, "wide_columnwidth", None)
        m.setattr(AbstractFormatter, "columnwidth", None)

        def formatter(**patch_dict):
            fmt = AbstractFormatter()

            for key, value in patch_dict.items():
                m.setattr(fmt, key, value)

            return fmt

        yield formatter


class TestInit:
    """Test that the initialization of the AbstractFormatter class is properly executed."""

    @pytest.mark.parametrize(
        "styles,target",
        [
            (
                ["test", "seaborn-white", "seaborn"],
                "seaborn-white",
            ),
            (
                ["test", "seaborn-white", "seaborn", "seaborn-v0_8-white"],
                "seaborn-white",
            ),
            (
                ["test", "seaborn", "test2", "seaborn-v0_8-white"],
                "seaborn-v0_8-white",
            ),
            (
                ["test", "seaborn", "test2"],
                None,
            ),
        ],
    )
    def test_style_selection(self, monkeypatch, abstract_formatter_mock, mocker, styles, target):
        mocker.patch("rsmf.abstract_formatter.mpl.style.use")

        with monkeypatch.context() as m:
            m.setattr(rsmf.abstract_formatter.mpl.style, "available", styles)

            formatter = abstract_formatter_mock()

            if target is None:
                rsmf.abstract_formatter.mpl.style.use.assert_not_called()
            else:
                rsmf.abstract_formatter.mpl.style.use.assert_called_once_with(target)


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
        assert plt.rcParams["text.usetex"] == True
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
                {"columnwidth": 1.0, "wide_columnwidth": 2.0},
                {"aspect_ratio": 1.0, "width_ratio": 1.0, "wide": False},
                (1.0, 1.0),
            ),
            (
                {"columnwidth": 1.0, "wide_columnwidth": 2.0},
                {"aspect_ratio": 0.5, "width_ratio": 1.0, "wide": True},
                (2.0, 1.0),
            ),
            (
                {"columnwidth": 1.0, "wide_columnwidth": 2.0},
                {"aspect_ratio": 1.0, "width_ratio": 1.0, "wide": True},
                (2.0, 2.0),
            ),
            (
                {"columnwidth": 0.5, "wide_columnwidth": 2.0},
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
        formatter = abstract_formatter_mock(columnwidth=None, wide_columnwidth=1.0)

        with pytest.raises(ValueError, match="The formatter's columnwidth was not set"):
            formatter.figure(wide=False)

    def test_figure_error_wide_columnwidth_not_set(self, abstract_formatter_mock):
        """Assert that the figure method throws the correct errors."""
        formatter = abstract_formatter_mock(columnwidth=1.0, wide_columnwidth=None)

        with pytest.raises(ValueError, match="The formatter's wide_columnwidth was not set"):
            formatter.figure(wide=True)
