"""Tests for Parser (NLTK-based parser with lexicon and grammar)."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pfmg.parsing.features.Features import Features
from pfmg.parsing.features.Percolation import Percolation
from pfmg.parsing.grammar.Grammar import Grammar
from pfmg.parsing.parser.Parser import Parser
from pfmg.parsing.production.Production import Production


def _make_mock_lexicon(lexicon_str: str = "") -> MagicMock:
    """Return a mock Lexicon with to_translation and to_validation returning lexicon_str."""
    mock = MagicMock()
    mock.to_translation.return_value = lexicon_str
    mock.to_validation.return_value = lexicon_str
    return mock


def _minimal_grammar_single_terminal() -> Grammar:
    """Grammar that accepts a single token 'a'."""
    prod = Production(
        lhs="S",
        phrases=['"a"'],
        agreements=Features(data=[{}]),
        percolation=Percolation(data={}),
    )
    return Grammar(start="S", productions=[prod])


def _minimal_grammar_two_terminals() -> Grammar:
    """Grammar that accepts two tokens 'a' and 'b'."""
    prod = Production(
        lhs="S",
        phrases=['"a"', '"b"'],
        agreements=Features(data=[{}, {}]),
        percolation=Percolation(data={}),
    )
    return Grammar(start="S", productions=[prod])


@pytest.fixture
def parser_single() -> Parser:
    """Parser that accepts only the sentence 'a'."""
    return Parser(
        lexique=_make_mock_lexicon(),
        grammar=_minimal_grammar_single_terminal(),
        how="translation",
    )


@pytest.fixture
def parser_two_tokens() -> Parser:
    """Parser that accepts the sentence 'a b'."""
    return Parser(
        lexique=_make_mock_lexicon(),
        grammar=_minimal_grammar_two_terminals(),
        how="translation",
    )


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"data": "a", "keep": "first"}, "Tree"),
        ({"data": "a", "keep": "all"}, "list"),
    ],
)
def test_parser_parse_str(parser_single, params, expected) -> None:
    """Parse string input with keep first/all returns Tree or list of Trees."""
    result = parser_single.parse(data=params["data"], keep=params["keep"])
    if expected == "Tree":
        assert result.__class__.__name__ == "Tree"
    else:
        assert isinstance(result, list)
        assert len(result) >= 1
        assert result[0].__class__.__name__ == "Tree"


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"data": "a b", "keep": "first"}, "Tree"),
        ({"data": "a b", "keep": "all"}, "list"),
    ],
)
def test_parser_parse_str_two_tokens(parser_two_tokens, params, expected) -> None:
    """Parse two-token sentence."""
    result = parser_two_tokens.parse(data=params["data"], keep=params["keep"])
    if expected == "Tree":
        assert result.__class__.__name__ == "Tree"
    else:
        assert isinstance(result, list)
        assert all(t.__class__.__name__ == "Tree" for t in result)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"data": ["a", "a"], "keep": "first"}, 2),
        ({"data": ["a"], "keep": "all"}, 1),
    ],
)
def test_parser_parse_list(parser_single, params, expected) -> None:
    """Parse list of sentences returns list of trees or flattened list."""
    result = parser_single.parse(data=params["data"], keep=params["keep"])
    assert isinstance(result, list)
    if isinstance(expected, int):
        assert len(result) == expected


def test_parser_to_file(parser_single, tmp_path: Path) -> None:
    """to_file writes grammar string to the given path."""
    out = tmp_path / "grammar.txt"
    parser_single.to_file(out)
    assert out.exists()
    content = out.read_text()
    assert "S" in content
    assert "a" in content or '"a"' in content
