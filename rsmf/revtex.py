"""
Support for the revtex4-1 and revtex4-2 documentclasses of the APS journals.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

from .revtexlike import RevtexLikeFormatter, RevtexLikeParser


class RevtexFormatter(RevtexLikeFormatter):

    _widths = {
        "onecolumn": {"a4paper": 3.42},
        "twocolumn": {"a4paper": 3.42},
    }

    _wide_widths = {
        "onecolumn": {"a4paper": 7.08},
        "twocolumn": {"a4paper": 7.08},
    }

    def __init__(self, columns="twocolumn", fontsize=10, **kwargs):
        """Sets up the plot with the fitting arguments so that the font sizes of the plot
        and the font sizes of the document are well aligned.

        Args:
            columns (str, optional):  the columns you used to set up your quantumarticle,
                either "onecolumn" or "twocolumn". Defaults to "twocolumn".
            fontsize (int, optional): the fontsize you used to set up your quantumarticle,
                either 10, 11 or 12. Defaults to 10.
        """
        super().__init__(columns, "a4paper", fontsize)

    def set_rcParams(self):
        """Adjust the rcParams to the default values for Quantumarticle."""
        super().set_rcParams()

        plt.rcParams["font.family"] = "serif"


revtex_parser = RevtexLikeParser(["{revtex4-1}", "{revtex4-2}"], RevtexFormatter)
