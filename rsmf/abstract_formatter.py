"""
Abstract base class for all formatters.
"""

import abc

import matplotlib as mpl
import matplotlib.pyplot as plt

from .fontsizes import default_fontsizes_10


class AbstractFormatter(abc.ABC):
    """
    Base class for formatter implementations.
    """

    def __init__(self):
        """Sets up the plotting environment."""
        self._fontsizes = default_fontsizes_10

        mpl.use("pgf")
        mpl.style.use("seaborn-white")
        self.set_rcParams()
        # TODO: Make sure set_rcParams is called after the fontsizes in the subclass are adjusted

    # TODO: Adjust names to columnwidth and wide_columnwidth, advertise as part of API
    @abc.abstractproperty
    def width(self):
        raise NotImplementedError("width is not implemented in subclass.")

    @abc.abstractproperty
    def wide_width(self):
        raise NotImplementedError("wide_width is not implemented in subclass.")

    @property
    def fontsizes(self):
        return self._fontsizes

    # TODO: Brainstorm a better way to advertise additional info (like specific colors)
    #       in the API. Maybe through a "props" dict?

    def set_default_fontsizes(self):
        """Adjust the fontsizes in rcParams to the default values matching the surrounding document."""
        plt.rcParams["axes.labelsize"] = self.fontsizes.small
        plt.rcParams["axes.titlesize"] = self.fontsizes.large
        plt.rcParams["xtick.labelsize"] = self.fontsizes.footnotesize
        plt.rcParams["ytick.labelsize"] = self.fontsizes.footnotesize
        plt.rcParams["font.size"] = self.fontsizes.small

    def set_rcParams(self):
        """Adjust the rcParams to the default values."""
        self.set_default_fontsizes()

        plt.rcParams["pgf.texsystem"] = "pdflatex"
        plt.rcParams["text.usetex"] = False
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

    def figure(self, aspect_ratio=1 / 1.62, width_ratio=1.0, wide=False):
        """Sets up the plot with the fitting arguments so that the font sizes of the plot
        and the font sizes of the document are well aligned.

        Args:
            aspect_ratio (float, optional): the aspect ratio (width/height) of your plot. Defaults to the golden ratio.
            width_ratio (float, optional): the width of your plot in multiples of \columnwidth. Defaults to 1.0.
            wide (bool, optional): indicates if the figures spans two columns in twocolumn mode, 
                i.e. if the figure* environment is used, has no effect in onecolumn mode . Defaults to False.

        Returns:
            matplotlib.Figure: The matplotlib Figure object
        """
        if wide and not self.wide_width:
            raise ValueError("The formatter's wide_width was not set.")
        elif not wide and not self.width:
            raise ValueError("The formatter's width was not set.")

        base_width = self.wide_width if wide else self.width

        width = base_width * width_ratio
        height = width * aspect_ratio

        return plt.figure(figsize=(width, height), dpi=120, facecolor="white")
