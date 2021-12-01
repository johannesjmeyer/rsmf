"""
Formatter for iopart document class.
"""


from .abstract_formatter import AbstractFormatter
from .fontsizes import DEFAULT_FONTSIZES


class IOPArtFormatter(AbstractFormatter):
    """
    A Formatter for the iopart document class.
    """

    _columnwidths = {
        (10, "onecolumn") : 5.17,
        (10, "twocolumn") : 3.29,
        (12, "onecolumn") : 6.2,
    }

    _wide_columnwidths = {
        (10, "onecolumn") : 5.17,
        (10, "twocolumn") : 6.78,
        (12, "onecolumn") : 6.2,
    }

    def __init__(self, columns="onecolumn", fontsize=10):
        """Sets up the plot with the fitting arguments so that the font sizes of the plot
        and the font sizes of the document are well aligned.

        Args:
            columns (str, optional):  the columns you used to set up your quantumarticle,
                either "onecolumn" or "twocolumn". Defaults to "onecolumn".
            fontsize (int, optional): the fontsize you used to set up your quantumarticle,
                either 10 or 12. Defaults to 10.
        """
        self.columns = columns
        self.fontsize = fontsize

        super().__init__()

    @property
    def columnwidth(self):
        """columnwidth of the document."""
        return self._columnwidths[(self.fontsize, self.columns)]

    @property
    def wide_columnwidth(self):
        """Wide columnwidth of the document."""
        return self._wide_columnwidths[(self.fontsize, self.columns)]

    @property
    def fontsizes(self):
        """Fontsizes as specified by the underlying document."""
        return DEFAULT_FONTSIZES[self.fontsize]

    def __eq__(self, other):
        return (
            self.fontsize == other.fontsize
            and self.columns == other.columns
        )


class IOPArtParser:
    """A parser for the iopart document class.
    """

    # pylint: disable=too-few-public-methods
    def __call__(self, content):
        """Parse the given content and extract the formatter.

        Args:
            content (string): Content of the target document.

        Returns:
            Union[NoneType,Formatter]: Either a formatter if the target document has the given
                document class or None.
        """
        # IDEA: Add support for regexes to support things like \documentclass[rmp,aps]{revtex4-1}
        for documentclass_identifier in self.documentclass_identifiers:
            if documentclass_identifier in content:
                return self.formatter_class(**self._extract_kwargs(content))

        return None

    @staticmethod
    def _extract_kwargs(content):
        r"""Parse the content to extract the informations relevant for plot style.

        Args:
            content (str): The content, containing at least the \documentclass command.

        Returns:
            Dict: formatter_kwargs (columns, paper, fontsize)
        """
        formatter_kwargs = {}

        if "\\ioptwocol" in content:
            formatter_kwargs["columns"] = "twocolumn"
        else:
            formatter_kwargs["columns"] = "onecolumn"

        if "12pt" in content:
            formatter_kwargs["fontsize"] = 12
        else:
            formatter_kwargs["fontsize"] = 10

        return formatter_kwargs

# pylint: disable=invalid-name
iopart_parser = IOPArtParser()
"""Parser for the iopart document class."""