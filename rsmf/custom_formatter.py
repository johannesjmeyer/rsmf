"""
Custom formatter that can be used if the intended document class is not supported.
"""

import matplotlib.pyplot as plt

from .abstract_formatter import AbstractFormatter
from .fontsizes import DEFAULT_FONTSIZES


class CustomFormatter(AbstractFormatter):
    """
    Allows to use rsmf even if the intended document class is not supported.

    Args:
        columnwidth (float, optional): Width of a single column (figure) plot in inches.
            Defaults to None.
        wide_columnwidth (float, optional): Width of a two column (figure*) plot in inches.
            Defaults to width.
        fontsizes (Union[int,Fontsizes], optional): Latex base fontsize or Fontsizes object.
            Defaults to 10.
        pgf_preamble (str, optional): Additional packages to include in the PGF preamble,
            e.g. for exchanging fonts or defining commands. Defaults to "".
    """

    def __init__(self, columnwidth=None, wide_columnwidth=None, fontsizes=10, pgf_preamble=""):
        self._columnwidth = columnwidth
        self._wide_columnwidth = wide_columnwidth
        self._pgf_preamble = pgf_preamble

        if isinstance(fontsizes, int):
            self._fontsizes = DEFAULT_FONTSIZES[fontsizes]
        else:
            self._fontsizes = fontsizes

        super().__init__()

    @property
    def columnwidth(self):
        return self._columnwidth

    @property
    def wide_columnwidth(self):
        return self._wide_columnwidth

    @property
    def fontsizes(self):
        return self._fontsizes

    def set_rcParams(self):
        """Adjust the rcParams to the default values."""
        super().set_rcParams()

        plt.rcParams["pgf.preamble"] = self._pgf_preamble
