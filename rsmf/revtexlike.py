import matplotlib as mpl
import matplotlib.pyplot as plt

from .abstract_formatter import AbstractFormatter
from .fontsizes import default_fontsizes


class RevtexLikeFormatter(AbstractFormatter):
    """
    A generic Formatter for revtex-like journals.

    Inherited classes should set the following:
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

        super().__init__()

    @property
    def width(self):
        """Width of the plot."""
        return self._widths[self.columns][self.paper]

    @property
    def wide_width(self):
        """Wide width of the plot."""
        return self._wide_widths[self.columns][self.paper]

    @property
    def fontsizes(self):
        """Fontsizes as specified by the underlying document."""
        return default_fontsizes[self.fontsize]

    def __eq__(self, other):
        return (
            self.fontsize == other.fontsize
            and self.columns == other.columns
            and self.paper == other.paper
        )


class RevtexLikeParser:
    def __init__(self, documentclass_identifiers, formatter_class):
        """Initializes the parser.

        Args:
            documentclass_identifiers (List[string]): Strings identifying the supported document class.
            formatter_class (class): Class object describing the formatter.
        """
        self.documentclass_identifiers = documentclass_identifiers
        self.formatter_class = formatter_class

    def __call__(self, preamble):
        """Parse the given preamble and extract the formatter.

        Args:
            preamble (string): Preamble of the target document.

        Returns:
            Union[NoneType,Formatter]: Either a formatter if the target document has the given
                document class or None.
        """
        # TODO: Add support for regexes to support things like \documentclass[rmp,aps]{revtex4-1}
        for documentclass_identifier in self.documentclass_identifiers:
            if documentclass_identifier in preamble:
                return self.formatter_class(**self._extract_kwargs(preamble))

        return None

    @staticmethod
    def _extract_kwargs(preamble):
        """Parse the preamble to extract the informations relevant for plot style.

        Args:
            preamble (str): The preamble, containing at least the \documentclass command.

        Returns:
            Dict: formatter_kwargs (columns, paper, fontsize)
        """
        formatter_kwargs = {}

        if "onecolumn" in preamble:
            formatter_kwargs["columns"] = "onecolumn"
        else:
            formatter_kwargs["columns"] = "twocolumn"

        if "letterpaper" in preamble:
            formatter_kwargs["paper"] = "letterpaper"
        else:
            formatter_kwargs["paper"] = "a4paper"

        if "11pt" in preamble:
            formatter_kwargs["fontsize"] = 11
        elif "12pt" in preamble:
            formatter_kwargs["fontsize"] = 12
        else:
            formatter_kwargs["fontsize"] = 10

        return formatter_kwargs
