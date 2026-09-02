"""Tests for Lexicon (realization and index maps)."""

import pytest

from pfmg.lexique.lexicon import Lexicon
from pfmg.utils.paths import get_project_path


@pytest.fixture
def fx_lexicon() -> Lexicon:
    """Lexicon built from the example grammar."""
    return Lexicon.from_yaml(get_project_path() / "examples" / "data")


def test_get_indexes_sides_are_distinct(fx_lexicon) -> None:
    """A source form is unknown on the destination side, and vice versa."""
    assert fx_lexicon.get_indexes("des", "translation")
    assert not fx_lexicon.get_indexes("des", "validation")
    assert fx_lexicon.get_indexes("tulol", "validation")
    assert not fx_lexicon.get_indexes("tulol", "translation")


def test_getitem_is_the_translation_side(fx_lexicon) -> None:
    """Subscripting keeps looking tokens up among the source forms."""
    assert fx_lexicon["des"] == fx_lexicon.get_indexes("des", "translation")


def test_get_indexes_rejects_unknown_side(fx_lexicon) -> None:
    """An unknown *how* is a programming error, not an empty result."""
    with pytest.raises(ValueError, match="translation"):
        fx_lexicon.get_indexes("des", "gibberish")


def test_iter_yields_the_realized_formes(fx_lexicon) -> None:
    """Iterating returns the very Forme the index maps were built from."""
    formes = list(fx_lexicon)

    assert formes
    assert [f.source.index for f in formes] == [
        f.source.index for f in fx_lexicon.lexicon2
    ]
