import pytest
import numpy as np
from rsmf.quantumarticle import parse, Quantumarticle


class TestParse:
    """Ensure that parsing works as expected."""

    @pytest.mark.parametrize(
        "preamble",
        [
            r"\documentclass[10pt,notitlepage,prl]{revtex4-1}",
            r"\documentclass[10pt]{quantumarticles}",
            r"\documentclass[10pt]{Quantumarticle}",
        ],
    )
    def test_parse_none(self, preamble):
        assert parse(preamble) is None

    def test_parse_default(self):
        preamble = r"\documentclass{quantumarticle}"
        formatter = parse(preamble)

        assert formatter is not None

        assert formatter.paper == "a4paper"
        assert formatter.columns == "twocolumn"
        assert formatter.fontsize == 10

    def test_parse_all(self):
        preamble = r"\documentclass[onecolumn,unpublished,letterpaper,11pt]{quantumarticle}"
        formatter = parse(preamble)

        assert formatter is not None

        assert formatter.paper == "letterpaper"
        assert formatter.columns == "onecolumn"
        assert formatter.fontsize == 11

    def test_parse_some(self):
        preamble = r"\documentclass[a4paper,12pt,noarxiv]{quantumarticle}"
        formatter = parse(preamble)

        assert formatter is not None

        assert formatter.paper == "a4paper"
        assert formatter.columns == "twocolumn"
        assert formatter.fontsize == 12


class TestFigure:
    """Test that the constructed figures have the proper dimensions."""

    @pytest.mark.parametrize(
        "paper_kwargs,figure_kwargs,expected_format",
        [
            (
                {"columns": "twocolumn", "paper": "a4paper", "fontsize": 11},
                {"aspect_ratio": 1.0, "width_ratio": 1.0, "wide": False},
                (3.22, 3.22),
            ),
            (
                {"columns": "twocolumn", "paper": "letterpaper", "fontsize": 11},
                {"aspect_ratio": 1.4, "width_ratio": 1.0, "wide": False},
                (3.34, 4.676),
            ),
            (
                {"columns": "twocolumn", "paper": "a4paper", "fontsize": 11},
                {"aspect_ratio": 1.0, "width_ratio": 2.0, "wide": True},
                (13.44, 13.44),
            ),
            (
                {"columns": "twocolumn", "paper": "letterpaper", "fontsize": 11},
                {"aspect_ratio": 2.0, "width_ratio": 0.6, "wide": True},
                (4.17, 8.34),
            ),
            (
                {"columns": "onecolumn", "paper": "a4paper", "fontsize": 11},
                {"aspect_ratio": 2.0, "width_ratio": 1.0, "wide": False},
                (5.93, 11.86),
            ),
            (
                {"columns": "onecolumn", "paper": "letterpaper", "fontsize": 11},
                {"aspect_ratio": .8, "width_ratio": 1.5, "wide": False},
                (9.24, 7.392),
            ),
        ],
    )
    def test_figure_format(self, paper_kwargs, figure_kwargs, expected_format):
        formatter = Quantumarticle(**paper_kwargs)
        fig = formatter.figure(**figure_kwargs)
        assert np.allclose(fig.get_size_inches(), np.array(expected_format))

