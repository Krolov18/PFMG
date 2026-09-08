"""Tests for Lexicon (realization and surface-form lookup)."""

import pytest

from pfmg.lexique.lexicon import Lexicon
from pfmg.utils.paths import get_project_path


@pytest.fixture
def fx_lexicon() -> Lexicon:
    """Lexicon built from the example grammar."""
    return Lexicon.from_yaml(get_project_path() / "examples" / "data")


def test_knows_sides_are_distinct(fx_lexicon) -> None:
    """A source form is unknown on the destination side, and vice versa."""
    assert fx_lexicon.knows("des", "translation")
    assert not fx_lexicon.knows("des", "validation")
    assert fx_lexicon.knows("tulol", "validation")
    assert not fx_lexicon.knows("tulol", "translation")


def test_knows_defaults_to_the_translation_side(fx_lexicon) -> None:
    """Without a side, lookup happens among the source forms."""
    assert fx_lexicon.knows("des")
    assert not fx_lexicon.knows("tulol")


def test_knows_rejects_unknown_side(fx_lexicon) -> None:
    """An unknown *how* is a programming error, not a False."""
    with pytest.raises(ValueError, match="translation"):
        fx_lexicon.knows("des", "gibberish")


def test_iter_yields_the_realized_formes(fx_lexicon) -> None:
    """Iterating returns the very Forme the lookup sets were built from."""
    formes = list(fx_lexicon)

    assert formes
    assert formes == fx_lexicon.formes
    assert {f.source.to_string() for f in formes} == fx_lexicon.source_forms
