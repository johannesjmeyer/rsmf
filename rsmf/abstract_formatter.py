"""
Abstract base class for all formatters.
"""

import abc
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt

from .fontsizes import DEFAULT_FONTSIZES_10


class AbstractFormatter(abc.ABC):
    """
    Base class for formatter implementations.
    """

    def __init__(self):
        """Sets up the plotting environment."""
        if not hasattr(self, "_fontsizes"):
            self._fontsizes = DEFAULT_FONTSIZES_10

        mpl.use("pgf")
        mpl.style.use("seaborn-white")

        self.set_rcParams()

    @abc.abstractproperty
    def columnwidth(self):
        """columnwidth of the document."""
        raise NotImplementedError("columnwidth is not implemented in subclass.")

    def width(self):
        """columnwidth of the document. (Deprecated)"""
        warnings.warn("width is deprecated, use columnwidth instead.")

        return self.columnwidth

    @abc.abstractproperty
    def wide_columnwidth(self):
        """Wide columnwidth of the document."""
        raise NotImplementedError("wide_columnwidth is not implemented in subclass.")

    @property
    def wide_width(self):
        """Wide columnwidth of the document. (Deprecated)"""
        warnings.warn("wide_width is deprecated, use wide_columnwidth instead.")

        return self.wide_columnwidth

    @property
    def fontsizes(self):
        """Fontsizes as specified by the underlying document."""
        return self._fontsizes

    def set_default_fontsizes(self):
        """Adjust the fontsizes in rcParams to the default values matching
        the surrounding document."""
        plt.rcParams["axes.labelsize"] = self.fontsizes.small
        plt.rcParams["axes.titlesize"] = self.fontsizes.large
        plt.rcParams["xtick.labelsize"] = self.fontsizes.footnotesize
        plt.rcParams["ytick.labelsize"] = self.fontsizes.footnotesize
        plt.rcParams["font.size"] = self.fontsizes.small

    # pylint: disable=invalid-name
    def set_rcParams(self):
        """Adjust the rcParams to the default values."""
        self.set_default_fontsizes()

        plt.rcParams["pgf.texsystem"] = "pdflatex"
        plt.rcParams["text.usetex"] = True
        plt.rcParams["pgf.rcfonts"] = True

        plt.rcParams["xtick.major.width"] = 0.5
        plt.rcParams["ytick.major.width"] = 0.5
        plt.rcParams["xtick.direction"] = "in"
        plt.rcParams["ytick.direction"] = "in"
        plt.rcParams["xtick.major.size"] = 4
        plt.rcParams["ytick.major.size"] = 4
        plt.rcParams["lines.linewidth"] = 1
        plt.rcParams["axes.linewidth"] = 0.5
        plt.rcParams["grid.linewidth"] = 0.5
        plt.rcParams["lines.markersize"] = 3

        plt.rcParams["legend.frameon"] = True
        plt.rcParams["legend.framealpha"] = 1.0
        plt.rcParams["legend.fancybox"] = False

    def figure(self, aspect_ratio=1.62, width_ratio=1.0, wide=False):
        r"""Sets up the plot with the fitting arguments so that the font sizes of the plot
        and the font sizes of the document are well aligned.

        Args:
            aspect_ratio (float, optional): the aspect ratio (width/height) of your plot.
                Defaults to the golden ratio.
            width_ratio (float, optional): the width of your plot in multiples of \columnwidth.
                Defaults to 1.0.
            wide (bool, optional): indicates if the figures spans two columns in twocolumn mode,
                i.e. if the figure* environment is used, has no effect in onecolumn mode.
                Defaults to False.

        Returns:
            matplotlib.Figure: The matplotlib Figure object
        """
        if wide and not self.wide_columnwidth:
            raise ValueError("The formatter's wide_columnwidth was not set.")

        if not wide and not self.columnwidth:
            raise ValueError("The formatter's columnwidth was not set.")

        base_width = self.wide_columnwidth if wide else self.columnwidth

        width = base_width * width_ratio
        height = width / aspect_ratio

        return plt.figure(figsize=(width, height), dpi=120, facecolor="white")
