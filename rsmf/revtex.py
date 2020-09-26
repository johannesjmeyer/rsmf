"""
Support for the revtex4-1 documentclass of the APS journals.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

from .formatters import Formatter


class RevtexFormatter:

    _documentclass_identifier = "{revtex}"

    _widths = {
        "onecolumn": {"a4paper": 7.08},
        "twocolumn": {"a4paper": 3.42},
    }

    _wide_widths = {
        "onecolumn": {"a4paper": 7.08},
        "twocolumn": {"a4paper": 7.08},
    }

    def __init__(self, columns="twocolumn", fontsize=10):
        """Sets up the plot with the fitting arguments so that the font sizes of the plot
        and the font sizes of the document are well aligned.

        Args:
            columns (str, optional):  the columns you used to set up your quantumarticle,
                either "onecolumn" or "twocolumn". Defaults to "twocolumn".
            fontsize (int, optional): the fontsize you used to set up your quantumarticle,
                either 10, 11 or 12. Defaults to 10.
        """
        super().__init__(columns, paper, fontsize)
