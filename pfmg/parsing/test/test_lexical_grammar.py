"""Tests for NLTK lexical grammar export from realized forms."""

import re

import pytest
from frozendict import frozendict

from pfmg.lexique.forme.Forme import Forme
from pfmg.lexique.forme.FormeEntry import FormeEntry
from pfmg.lexique.lexicon import Lexicon
from pfmg.lexique.morpheme.Morphemes import Morphemes
from pfmg.lexique.morpheme.Radical import Radical
from pfmg.parsing.lexical_grammar import LexicalGrammarExporter
from pfmg.utils.paths import get_project_path
from pfmg.utils.stem_space import StemSpace


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
    return re.findall(r"-> '([^']*)'$", grammar, flags=re.MULTILINE)


def test_export_translation_is_stable(fx_exporter, fx_lexicon) -> None:
    """Exporting twice yields the same grammar: indexes must not drift."""
    first = fx_exporter.export_lexicon(fx_lexicon, "translation")
    second = fx_exporter.export_lexicon(fx_lexicon, "translation")
    assert first == second


def test_export_validation_is_stable(fx_exporter, fx_lexicon) -> None:
    """Exporting twice yields the same grammar: indexes must not drift."""
    first = fx_exporter.export_lexicon(fx_lexicon, "validation")
    second = fx_exporter.export_lexicon(fx_lexicon, "validation")
    assert first == second


def test_translation_terminals_match_source_indexes(fx_exporter, fx_lexicon) -> None:
    """Indexes handed out by the lexicon are terminals of the translation grammar."""
    terminals = set(_terminals(fx_exporter.export_lexicon(fx_lexicon, "translation")))
    indexes = {str(index) for index in fx_lexicon.get_indexes("des")}

    assert indexes
    assert indexes <= terminals


def test_validation_terminals_match_destination_indexes(
    fx_exporter, fx_lexicon
) -> None:
    """The validation grammar is indexed on the destination side."""
    terminals = set(_terminals(fx_exporter.export_lexicon(fx_lexicon, "validation")))
    indexes = {str(index) for index in fx_lexicon.get_indexes("tulol", "validation")}

    assert indexes
    assert indexes <= terminals


def test_export_entry(fx_exporter) -> None:
    """Validation export builds an NLTK lexical production from a FormeEntry."""
    entry = FormeEntry(
        index=3,
        pos="N",
        morphemes=Morphemes(
            radical=Radical(
                stems=StemSpace(stems=("a", "b", "c")),
                sigma=frozendict({"Genre": "m", "Nombre": "s"}),
            ),
            others=[],
        ),
        sigma=frozendict({"Genre": "m", "Nombre": "s"}),
    )
    assert fx_exporter.export_entry(entry) == "N[Genre='m',Nombre='s'] -> '3'"


def test_export_forme_translation(fx_exporter) -> None:
    """Translation export merges source and destination feature bundles."""
    source = FormeEntry(
        index=4,
        pos="N",
        morphemes=Morphemes(
            radical=Radical(
                stems=StemSpace(stems=("source",)),
                sigma=frozendict({"Genre": "m"}),
            ),
            others=[],
        ),
        sigma=frozendict({"Genre": "m"}),
    )
    destination = FormeEntry(
        index=4,
        pos="N",
        morphemes=Morphemes(
            radical=Radical(
                stems=StemSpace(stems=("dest",)),
                sigma=frozendict({"Genre": "f"}),
            ),
            others=[],
        ),
        sigma=frozendict({"Genre": "f"}),
    )
    forme = Forme(source=source, destination=destination)
    assert (
        fx_exporter.export_forme_translation(forme)
        == "N[SGenre='m',DGenre='f',translation='dest'] -> '4'"
    )
