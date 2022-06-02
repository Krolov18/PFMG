import re

import pytest
from frozendict import frozendict
from multimethod import DispatchError

from lexique.decoupeur import decoupe
from lexique.structures import Prefix, Suffix, Circumfix, Gabarit, Radical, Forme


@pytest.mark.parametrize("term, accumulator, expected", [
    (Prefix(rule=re.compile(r"(\w+)\+X").fullmatch("e+X"), sigma=frozendict({"genre": "m"})), "qqch", "e-qqch"),
    (Suffix(rule=re.compile(r"X\+(\w+)").fullmatch("X+e"), sigma=frozendict({"genre": "m"})), "qqch", "qqch-e"),
    (Circumfix(rule=re.compile(r"(\w+)\+X\+(\w+)").fullmatch("e+X+e"), sigma=frozendict({"genre": "m"})), "qqch", "e+qqch+e"),
    # (Gabarit(rule=re.compile(r"(\w+)\+X\+(\w+)").fullmatch("e+X+e"), sigma=frozendict()), "", ""),
    (Radical(stem="banane", rule=None, sigma=frozendict()), "", "banane"),
    (Forme(pos="N",
           morphemes=[
               Radical(stem="qqch", rule=None, sigma=frozendict()),
               Prefix(rule=re.compile(r"(\w+)\+X").fullmatch("i+X"), sigma=frozendict({"genre": "m"})),
               Prefix(rule=re.compile(r"(\w+)\+X").fullmatch("a+X"), sigma=frozendict({"genre": "m"})),
               Circumfix(rule=re.compile(r"(\w+)\+X\+(\w+)").fullmatch("e+X+e"), sigma=frozendict({"genre": "m"}))],
           sigma=frozendict()), None, "e+a-i-qqch+e"),
])
def test_decoupe(term, accumulator, expected) -> None:
    try:
        actual = decoupe(term, accumulator)
    except DispatchError:
        actual = decoupe(term)
    assert actual == expected
