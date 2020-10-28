"""
Provides an encapsulation for the different named fontsizes in LaTeX.
"""


class Fontsizes:
    """Encapsulates the standard named fontsizes used in LaTeX.

    Defaults to the default LaTeX fontsizes based on normal size 10.

    Args:
        tiny (int, optional): Tiny text. Defaults to 5.
        scriptsize (int, optional): Scriptsize text. Defaults to 7.
        footnotesize (int, optional): Footnotesize text. Defaults to 8.
        small (int, optional): Small text. Defaults to 9.
        normalsize (int, optional): Normal text. Defaults to 10.
        large (int, optional): Larger text. Defaults to 12.
        Large (int, optional): Even larger text. Defaults to 14.
        LARGE (int, optional): Even more large text. Defaults to 17.
        huge (int, optional): Huge text. Defaults to 20.
        Huge (int, optional): Even more huge text. Defaults to 25.
    """

    # pylint: disable=invalid-name,too-many-instance-attributes,too-many-arguments
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        tiny=5,
        scriptsize=7,
        footnotesize=8,
        small=9,
        normalsize=10,
        large=12,
        Large=14,
        LARGE=17,
        huge=20,
        Huge=25,
    ):
        self.tiny = tiny
        self.scriptsize = scriptsize
        self.footnotesize = footnotesize
        self.small = small
        self.normalsize = normalsize
        self.large = large
        self.Large = Large
        self.LARGE = LARGE
        self.huge = huge
        self.Huge = Huge


DEFAULT_FONTSIZES_10 = Fontsizes()
"""Default fontsize palette based on normal size 10."""

DEFAULT_FONTSIZES_11 = Fontsizes(
    tiny=6,
    scriptsize=8,
    footnotesize=9,
    small=10,
    normalsize=11,
    large=12,
    Large=14,
    LARGE=17,
    huge=20,
    Huge=25,
)
"""Default fontsize palette based on normal size 11."""

DEFAULT_FONTSIZES_12 = Fontsizes(
    tiny=6,
    scriptsize=8,
    footnotesize=10,
    small=11,
    normalsize=12,
    large=14,
    Large=17,
    LARGE=20,
    huge=25,
    Huge=25,
)
"""Default fontsize palette based on normal size 12."""

DEFAULT_FONTSIZES = {
    10: DEFAULT_FONTSIZES_10,
    11: DEFAULT_FONTSIZES_11,
    12: DEFAULT_FONTSIZES_12,
}
"""Default fontsize palettes for a given normal size."""
