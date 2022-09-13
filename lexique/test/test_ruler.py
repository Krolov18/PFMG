import pytest
from frozendict import frozendict

from lexique.realizer import realize
from lexique.ruler import ruler
from lexique.structures import Phonology


@pytest.fixture(scope="module")
def phonology() -> Phonology:
    return Phonology(mutations=frozendict({'p': 'p', 't': 'p', 'k': 't', 'b': 'p', 'd': 'b', 'g': 'd',
                                           'm': 'm', 'n': 'm', 'N': 'n', 'f': 'f',
                                           's': 'f', 'S': 's', 'v': 'f', 'z': 'v', 'Z': 'z', 'r': 'w', 'l': 'r',
                                           'j': 'w', 'w': 'w'}),
                     apophonies=frozendict({'Ø': 'i', 'i': 'a', 'a': 'u', 'u': 'u', 'e': 'o', 'o': 'o'}),
                     derives=frozendict({'A': 'V', 'D': 'C'}),
                     consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
                     voyelles=frozenset("iueoa"))


@pytest.mark.parametrize("rule, sigma, expected", [
    ("e+X", frozendict(genre="m", nombre="sg"), "eRADICAL"),
    ])
def test_ruler_prefix(rule, sigma, expected) -> None:
    actual = ruler(rule=rule, sigma=sigma, voyelles=frozenset("aeiou"))
    assert realize(actual, accumulator="RADICAL") == expected


@pytest.mark.parametrize("rule, sigma, expected", [
    ("X+e", frozendict(genre="m", nombre="sg"), "RADICALe"),
    ])
def test_ruler_suffix(rule, sigma, expected) -> None:
    actual = ruler(rule=rule, sigma=sigma, voyelles=frozenset("aeiou"))
    assert realize(actual, accumulator="RADICAL") == expected


@pytest.mark.parametrize("rule, sigma, expected", [
    ("e+X+e", frozendict(genre="m", nombre="sg"), "eRADICALe"),
    ])
def test_ruler_circumfix(rule, sigma, expected) -> None:
    actual = ruler(rule=rule, sigma=sigma, voyelles=frozenset("aeiou"))
    assert realize(actual, accumulator="RADICAL") == expected


@pytest.mark.parametrize("rule, sigma, expected", [
    ("i4A1o2a3V", frozendict(genre="m", nombre="sg"), "iwarobani"),
    ])
def test_ruler_gabarit(phonology, rule, sigma, expected) -> None:
    actual = ruler(rule=rule, sigma=sigma, voyelles=frozenset("aeiou"))
    assert realize(actual, accumulator="rbin", phonology=phonology) == expected


@pytest.mark.parametrize("accumulator, rule, sigma, expected", [
    (("souris",), "X1", frozendict(genre="m", nombre="sg"), "souris"),
    (("blanc", "blanche"), "X2", frozendict(genre="m", nombre="sg"), "blanche"),
    ])
def test_ruler_selection(accumulator, rule, sigma, expected) -> None:
    actual = ruler(rule=rule, sigma=sigma, voyelles=frozenset("aeiou"))
    assert realize(actual, accumulator=accumulator) == expected


@pytest.mark.parametrize("accumulator, rule, sigma, expected", [
    (("souris",), "X2?X2:X1", frozendict(genre="m", nombre="sg"), "souris"),
    (("chat", "chatte"), "X2?X2:X1", frozendict(genre="m", nombre="sg"), "chatte"),
    ])
def test_ruler_ternary(accumulator, rule, sigma, expected) -> None:
    actual = ruler(rule=rule, sigma=sigma, voyelles=frozenset("aeiou"))
    assert realize(actual, accumulator=accumulator) == expected


@pytest.mark.parametrize("rule", [
    # "X2:",
    # ":X2",
    "X2?X1?X2",
    ])
def test_ruler_all_errors(rule) -> None:
    with pytest.raises(ValueError):
        _ = ruler(rule=rule,
                  sigma=frozendict(),
                  voyelles=frozenset("aeiou"))
