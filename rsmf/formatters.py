import matplotlib as mpl
import matplotlib.pyplot as plt

from .fontsize import _fontsizes


class Formatter:
    """
    A generic Formatter for subtyping by journal-specific formatters.

    Inherited classes should set the following:
      self._documentclass_identifier
      self._widths
      self._wide_widths
      
    """

    def __init__(self, columns, paper, fontsize):
        """Sets up the plot with the fitting arguments so that the font sizes of the plot
        and the font sizes of the document are well aligned.

        Args:
            columns (str, optional):  the columns you used to set up your quantumarticle,
                either "onecolumn" or "twocolumn". Defaults to "twocolumn".
            paper (str, optional): the paper size you used to set up your quantumarticle,
                either "a4paper" or "letterpaper". Defaults to "a4paper".
            fontsize (int, optional): the fontsize you used to set up your quantumarticle,
                either 10, 11 or 12. Defaults to 10.
        """
        self.columns = columns
        self.paper = paper
        self.fontsize = fontsize

        mpl.use("pgf")
        mpl.style.use("seaborn-white")
        self.set_rcParams()

    @property
    def width(self):
        return self._widths[self.columns][self.paper]

    @property
    def wide_width(self):
        return self._wide_widths[self.columns][self.paper]

    @property
    def fontsizes(self):
        return _fontsizes[self.fontsize]

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
        plt.rcParams["font.family"] = "sans-serif"
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
            self.fontsize == other.fontsize
            and self.columns == other.columns
            and self.paper == other.paper
        )


def parse(preamble):
    """Parse the preamble to extract the informations relevant for plot style.

    Args:
        preamble (str): The preamble, containing at least the \documentclass command.

    Returns:
        Union[NoneType,Quantumarticle]: Quantumarticle object with the relevant properties if the preamble
            is for a quantumarticle document. None otherwise.
    """
    if not "{quantumarticle}" in preamble:
        return None

    kwargs = {}

    if "onecolumn" in preamble:
        kwargs["columns"] = "onecolumn"
    else:
        kwargs["columns"] = "twocolumn"

    if "letterpaper" in preamble:
        kwargs["paper"] = "letterpaper"
    else:
        kwargs["paper"] = "a4paper"

    if "11pt" in preamble:
        kwargs["fontsize"] = 11
    elif "12pt" in preamble:
        kwargs["fontsize"] = 12
    else:
        kwargs["fontsize"] = 10

    return QuantumarticleFormatter(**kwargs)
