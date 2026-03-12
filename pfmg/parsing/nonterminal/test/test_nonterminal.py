"""Tests for Nonterminal and FSNonterminal."""

import pytest

from pfmg.conftest import _assert_compare
from pfmg.parsing.nonterminal.FSNonterminal import FSNonterminal
from pfmg.parsing.nonterminal.Nonterminal import Nonterminal


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"symbol": "NP"}, "NP"),
        ({"symbol": 42}, 42),
    ],
)
def test_nonterminal_symbol(params, expected) -> None:
    nt = Nonterminal(**params)
    _assert_compare(nt.symbol, expected)


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"symbol": "NP", "features": {"Genre": "m"}}, ("NP", {"Genre": "m"})),
        ({"symbol": "S", "features": {}}, ("S", {})),
    ],
)
def test_fs_nonterminal_symbol_and_features(params, expected) -> None:
    fs = FSNonterminal(**params)
    symbol_expected, features_expected = expected
    _assert_compare(fs.symbol, symbol_expected)
    _assert_compare(fs.features, features_expected)
