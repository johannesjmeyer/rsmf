import matplotlib.pyplot as plt
from .fontsize import Fontsizes10, Fontsizes11, Fontsizes12

_widths = {
    # a4paper columnwidth = 426.79135 pt = 5.93 in
    # letterpaper columnwidth = 443.57848 pt = 6.16 in
    "onecolumn": {"a4paper": 5.93, "letterpaper": 6.16},
    # a4paper columnwidth = 231.84843 pt = 3.22 in
    # letterpaper columnwidth = 240.24199 pt = 3.34 in
    "twocolumn": {"a4paper": 3.22, "letterpaper": 3.34},
}

_wide_widths = {
    # a4paper wide columnwidth = 426.79135 pt = 5.93 in
    # letterpaper wide columnwidth = 443.57848 pt = 6.16 in
    "onecolumn": {"a4paper": 5.93, "letterpaper": 6.16},
    # a4paper wide linewidth = 483.69687 pt = 6.72 in
    # letterpaper wide linewidth = 500.48400 pt = 6.95 in
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


# Sets up the plot with the fitting arguments so that the font sizes of the plot
# and the font sizes of the document are well aligned
#
#     columns : string = ('onecolumn' | 'twocolumn')
#         the columns you used to set up your quantumarticle,
#         defaults to 'twocolumn'
#
#     paper : string = ('a4paper' | 'letterpaper')
#         the paper size you used to set up your quantumarticle,
#         defaults to 'a4paper'
#
#     fontsize : int = (10 | 11 | 12)
#         the fontsize you used to set up your quantumarticle as int
#
#     (returns) : dict
#         parameters that can be used for plot adjustments


class Quantumarticle:
    def __init__(self, columns="twocolumn", paper="a4paper", fontsize=10):
        self.width = _widths[columns][paper]
        self.wide_width = _wide_widths[columns][paper]

        # Use the default fontsize scaling of LaTeX
        self.fontsizes = _fontsizes[fontsize]

        plt.rcParams["axes.labelsize"] = self.fontsizes["small"]
        plt.rcParams["axes.titlesize"] = self.fontsizes["large"]
        plt.rcParams["xtick.labelsize"] = self.fontsizes["footnotesize"]
        plt.rcParams["ytick.labelsize"] = self.fontsizes["footnotesize"]
        plt.rcParams["font.size"] = self.fontsizes["small"]

    def plot_setup(self, aspect_ratio=1 / 1.62, width_ratio=1.0, wide=False):
        width = (self.wide_width if wide else self.width) * width_ratio
        height = width * aspect_ratio

        return plt.figure(figsize=(width, height), dpi=120, facecolor="white")


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

    return Quantumarticle(kwargs)
