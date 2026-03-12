"""Tests for Rulable (via concrete subclass)."""

import pytest

from pfmg.conftest import _assert_compare
from pfmg.lexique.rulable.Rulable import Rulable


@pytest.mark.parametrize(
    "params, expected",
    [
        ({}, "NP -> D N"),
    ],
)
def test_rulable_subclass_to_lexical(params, expected) -> None:
    class ConcreteRulable(Rulable):
        def to_lexical(self) -> str:
            return "NP -> D N"

    r = ConcreteRulable(**params)
    _assert_compare(r.to_lexical(), expected)
