"""Tests for NLTK lexical grammar export from realized forms."""

import re

import pytest

from pfmg.lexique.forme.builders import make_forme_entry
from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.lexicon import Lexicon
from pfmg.parsing.lexical_grammar import LexicalGrammarExporter, quote
from pfmg.utils.paths import get_project_path


@pytest.fixture
def fx_exporter() -> LexicalGrammarExporter:
    """Shared exporter instance."""
    return LexicalGrammarExporter()


@pytest.fixture
def fx_lexicon() -> Lexicon:
    """Lexicon built from the example grammar."""
    return Lexicon.from_yaml(get_project_path() / "examples" / "data")


def _terminals(grammar: str) -> list[str]:
    """Return the terminal of every lexical production of *grammar*."""
    return re.findall(r"-> ['\"](.*)['\"]$", grammar, flags=re.MULTILINE)


def test_export_translation_is_stable(fx_exporter, fx_lexicon) -> None:
    """Exporting twice yields the same grammar."""
    first = fx_exporter.export_lexicon(fx_lexicon, "translation")
    second = fx_exporter.export_lexicon(fx_lexicon, "translation")
    assert first == second


def test_export_validation_is_stable(fx_exporter, fx_lexicon) -> None:
    """Exporting twice yields the same grammar."""
    first = fx_exporter.export_lexicon(fx_lexicon, "validation")
    second = fx_exporter.export_lexicon(fx_lexicon, "validation")
    assert first == second


def test_translation_terminals_are_source_forms(fx_exporter, fx_lexicon) -> None:
    """The translation grammar is keyed on the French side."""
    terminals = set(_terminals(fx_exporter.export_lexicon(fx_lexicon, "translation")))

    assert "des" in terminals
    assert "tulol" not in terminals


def test_validation_terminals_are_destination_forms(fx_exporter, fx_lexicon) -> None:
    """The validation grammar is keyed on the Kalaba side."""
    terminals = set(_terminals(fx_exporter.export_lexicon(fx_lexicon, "validation")))

    assert "tulol" in terminals
    assert "des" not in terminals


def test_export_deduplicates_productions(fx_exporter, fx_lexicon) -> None:
    """Several source cells realize the same destination form with the same features.

    Those used to be distinct productions only because the terminal was a
    per-Forme index; keyed on the form they are the very same rule.
    """
    exported = fx_exporter.export_lexicon(fx_lexicon, "validation").splitlines()
    per_forme = [fx_exporter.export_forme_validation(f) for f in fx_lexicon]

    assert len(exported) == len(set(exported))
    assert len(exported) < len(per_forme)


def test_export_entry(fx_exporter) -> None:
    """Validation export builds an NLTK lexical production from a FormeEntry."""
    entry = make_forme_entry("N", ("a", "b", "c"), {"Genre": "m", "Nombre": "s"})

    assert fx_exporter.export_entry(entry) == "N[Genre='m',Nombre='s'] -> 'a'"


def test_export_forme_translation(fx_exporter) -> None:
    """Translation export merges source and destination feature bundles."""
    forme = Forme(
        source=make_forme_entry("N", ("source",), {"Genre": "m"}),
        destination=make_forme_entry("N", ("dest",), {"Genre": "f"}),
    )

    assert (
        fx_exporter.export_forme_translation(forme)
        == "N[SGenre='m',DGenre='f',translation='dest'] -> 'source'"
    )


def test_export_entry_quotes_around_an_apostrophe(fx_exporter) -> None:
    """A form holding an apostrophe is written with double quotes."""
    entry = make_forme_entry("N", ("aujourd'hui",), {"Genre": "m"})

    assert fx_exporter.export_entry(entry) == 'N[Genre=\'m\'] -> "aujourd\'hui"'


@pytest.mark.parametrize(
    "value, expected",
    [
        ("mot", "'mot'"),
        ("aujourd'hui", '"aujourd\'hui"'),
    ],
)
def test_quote(value, expected) -> None:
    """A value is quoted with whichever quote it does not contain."""
    assert quote(value) == expected


def test_quote_rejects_both_quotes() -> None:
    """The NLTK grammar reader has no escape, so such a form cannot be exported."""
    with pytest.raises(ValueError, match="guillemets"):
        quote("l'\"autre\"")
