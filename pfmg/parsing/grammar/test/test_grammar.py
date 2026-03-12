"""Tests for Grammar and Grammar.to_nltk."""

from pfmg.parsing.features.Features import Features
from pfmg.parsing.features.Percolation import Percolation
from pfmg.parsing.grammar.Grammar import Grammar
from pfmg.parsing.production.Production import Production


def test_grammar_to_nltk() -> None:
    prod = Production(
        lhs="S",
        phrases=["NP"],
        agreements=Features(data=[{}]),
        percolation=Percolation(data={}),
    )
    g = Grammar(start="S", productions=[prod])
    out = g.to_nltk()
    assert "% start S" in out
    assert "S" in out and "NP" in out


def test_grammar_to_nltk_with_term() -> None:
    prod = Production(
        lhs="S",
        phrases=["NP"],
        agreements=Features(data=[{}]),
        percolation=Percolation(data={}),
    )
    g = Grammar(start="S", productions=[prod])
    out = g.to_nltk(term="dummy")
    assert "% start S" in out
