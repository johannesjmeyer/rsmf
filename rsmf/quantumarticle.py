import matplotlib as mpl
import matplotlib.pyplot as plt
from .fontsize import Fontsizes10, Fontsizes11, Fontsizes12

_widths = {
    "onecolumn": {"a4paper": 5.93, "letterpaper": 6.16},
    "twocolumn": {"a4paper": 3.22, "letterpaper": 3.34},
}

_wide_widths = {
    "onecolumn": {"a4paper": 5.93, "letterpaper": 6.16},
    "twocolumn": {"a4paper": 6.72, "letterpaper": 6.95},
}

_fontsizes = {
    10: Fontsizes10,
    11: Fontsizes12,
    12: Fontsizes12,
}


class QuantumColors:
    quantumviolet = "#53257F"
    quantumgray = "#555555"


class Quantumarticle:
    def __init__(self, columns="twocolumn", paper="a4paper", fontsize=10):
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

        self.width = _widths[columns][paper]
        self.wide_width = _wide_widths[columns][paper]

        self.fontsizes = _fontsizes[fontsize]
        self.colors = QuantumColors

        mpl.use("pgf")
        mpl.style.use("seaborn-white")
        self.set_rcParams()

    def set_default_fontsizes(self):
        plt.rcParams["axes.labelsize"] = self.fontsizes.small
        plt.rcParams["axes.titlesize"] = self.fontsizes.large
        plt.rcParams["xtick.labelsize"] = self.fontsizes.footnotesize
        plt.rcParams["ytick.labelsize"] = self.fontsizes.footnotesize
        plt.rcParams["font.size"] = self.fontsizes.small

    def set_rcParams(self):
        self.set_default_fontsizes()

        plt.rcParams["pgf.texsystem"] = "pdflatex"
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["text.usetex"] = False
        plt.rcParams["pgf.rcfonts"] = True 
        plt.rcParams["pgf.preamble"] = r"\usepackage{lmodern} \usepackage[utf8x]{inputenc} \usepackage[T1]{fontenc}"

        plt.rcParams["xtick.major.width"] = .5
        plt.rcParams["ytick.major.width"] = .5
        plt.rcParams["xtick.direction"] = "in"
        plt.rcParams["ytick.direction"] = "in"
        plt.rcParams["xtick.major.size"] = 4
        plt.rcParams["ytick.major.size"] = 4    
        plt.rcParams["lines.linewidth"] = 1
        plt.rcParams["axes.linewidth"] = .5
        plt.rcParams["grid.linewidth"] = .5
        plt.rcParams["lines.markersize"] = 3

        plt.rcParams["legend.frameon"] = True
        plt.rcParams["legend.framealpha"] = 1.0
        plt.rcParams["legend.fancybox"] = False

        plt.rcParams["axes.edgecolor"] = self.colors.quantumgray

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

    return Quantumarticle(**kwargs)
