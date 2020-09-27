import matplotlib as mpl
import matplotlib.pyplot as plt

from .fontsize import Fontsizes10


class Formatter:
    """
    Base class for formatter implementations.
    """

    def __init__(self):
        """Sets up the plotting environment."""
        self._widths = None
        self._wide_widths = None
        self._fontsizes = Fontsizes10()

        mpl.use("pgf")
        mpl.style.use("seaborn-white")
        self.set_rcParams()
        # TODO: Make sure set_rcParams is called after the fontsizes in the subclass are adjusted

    @property
    def width(self):
        if not self._widths:
            raise NotImplementedError("width is not implemented in subclass.")

        return self._widths[self.columns][self.paper]

    @property
    def wide_width(self):
        if not self._wide_widths:
            raise NotImplementedError("wide_width is not implemented in subclass.")

        return self._wide_widths[self.columns][self.paper]

    @property
    def fontsizes(self):
        if not self._fontsizes:
            raise NotImplementedError("fontsizes is not implemented in subclass.")

        return self._fontsizes

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
        width = (self.wide_width if wide else self.width) * width_ratio
        height = width * aspect_ratio

        return plt.figure(figsize=(width, height), dpi=120, facecolor="white")

    def __eq__(self, other):
        return (
            self._fontsizes == other._fontsizes
            and self._widths == other._widths
            and self._wide_widths == other._wide_widths
        )
