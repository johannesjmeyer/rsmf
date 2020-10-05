class Fontsizes:
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


default_fontsizes_10 = Fontsizes()

default_fontsizes_11 = Fontsizes(
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

default_fontsizes_12 = Fontsizes(
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

default_fontsizes = {
    10: default_fontsizes_10,
    11: default_fontsizes_11,
    12: default_fontsizes_12,
}
