from unittest.mock import patch

import pytest
from frozendict import frozendict
from nltk.grammar import FeatStructNonterminal, Production

from lexique.validate import validate


@pytest.mark.parametrize("term, att_values", [
    (FeatStructNonterminal(gene="f"), frozendict({"f": "genre"})),

    ((FeatStructNonterminal(gene="f"),
      FeatStructNonterminal(gene="fr")), frozendict({"f": "genre"})),

    (Production(lhs=FeatStructNonterminal(gene="f"),
                rhs=(FeatStructNonterminal(genre="f"),)), frozendict({"f": "genre"})),

    (Production(lhs=FeatStructNonterminal(genre="f"),
                rhs=(FeatStructNonterminal(gene="f"),)), frozendict({"f": "genre"})),

    ([Production(lhs=FeatStructNonterminal(genre="f"),
                 rhs=(FeatStructNonterminal(gene="f"),))], frozendict({"f": "genre"})),

    ([Production(lhs=FeatStructNonterminal(genre="f"),
                 rhs=(FeatStructNonterminal(genre="f"),)),
      Production(lhs=FeatStructNonterminal(genre="f"),
                 rhs=(FeatStructNonterminal(gene="f"),))], frozendict({"f": "genre"})),

    ([Production(lhs=FeatStructNonterminal(genre="f"),
                 rhs=(FeatStructNonterminal(gene="f"),)),
      Production(lhs=FeatStructNonterminal(genre="f"),
                 rhs=(FeatStructNonterminal(genre="f"),))], frozendict({"f": "genre"})),

    ("S -> N[gene=f]", frozendict({"f": "genre"})),
    ("S -> N[genre=m]", frozendict({"f": "genre"})),
    ("S -> N[gene=?a] VER[genre=?a]", frozendict({"f": "genre"})),
])
def test_validate_errors(term, att_values) -> None:
    with pytest.raises(AssertionError):
        validate(term, att_values)


@pytest.mark.skipif(reason="revoir ce test")
@pytest.mark.parametrize("sentences", [["toto mange une pomme"]])
@patch("nltk.parse.FeatureEarleyChartParser", return_value=[])
def test_validate_sentences(mock_parser, sentences) -> None:
    validate(mock_parser, sentences)


@pytest.mark.parametrize("term, att_values", [
    ("S -> N[Genre='f']", frozendict({"f": "Genre"})),
    # On vérifie les clés Genre de N et Genre de VER, mais on ne vérifie pas les variables
    ("S -> N[Genre=?a] VER[Genre=?a]", frozendict({"f": "Genre"})),
    (FeatStructNonterminal(Genre="f"), frozendict({"f": "Genre"})),
    (Production(lhs=FeatStructNonterminal(Genre="f"),
                rhs=(FeatStructNonterminal(Genre="f"),
                     FeatStructNonterminal(Genre="f"))), frozendict({"f": "Genre"})),
    ((FeatStructNonterminal(Genre="f"), FeatStructNonterminal(Genre="f")), frozendict({"f": "Genre"}))
])
def test_validate(term, att_values) -> None:
    assert validate(term, att_values) is None
