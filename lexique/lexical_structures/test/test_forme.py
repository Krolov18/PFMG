import pytest

from lexique.lexical_structures.Factory import create_morpheme
from lexique.lexical_structures.Forme import Forme
from lexique.lexical_structures.Morphemes import Morphemes
from lexique.lexical_structures.Phonology import Phonology
from lexique.lexical_structures.Radical import Radical
from lexique.lexical_structures.StemSpace import StemSpace
from frozendict import frozendict


def test_to_string() -> None:
    phonology = Phonology(apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
                          mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                                               g="d", m="m", n="m", N="n", f="f",
                                               s="f", S="s", v="f", z="v", Z="z",
                                               r="w", l="r", j="w", w="w"),
                          derives=frozendict(A="V", D="C"),
                          consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
                          voyelles=frozenset("iueoa"))

    forme = Forme(
        pos="N",
        morphemes=Morphemes(radical=Radical(stems=StemSpace(stems=["a", "b", "c"])),
                            others=[]),
        sigma=frozendict({"Genre": "m", "Nombre": "s"})
    )
    actual = forme.to_string(None)
    expected = "a"
    assert actual == expected

    forme = Forme(
        pos="N",
        morphemes=Morphemes(radical=Radical(stems=StemSpace(stems=["a", "b", "c"])),
                            others=[create_morpheme(rule="a+X",
                                                    sigma=frozendict({"Genre": "m", "Nombre": "s"}),
                                                    phonology=phonology)]),
        sigma=frozendict({"Genre": "m", "Nombre": "s"})
    )

    actual = forme.to_string(None)
    expected = "aa"
    assert actual == expected

    with pytest.raises(NotImplementedError):
        _ = forme.to_string("")

    with pytest.raises(NotImplementedError):
        _ = forme.to_string(StemSpace(stems=["a", "b", "c"]))


def test_get_sigma() -> None:
    forme = Forme(
        pos="N",
        morphemes=Morphemes(radical=Radical(stems=StemSpace(stems=["a", "b", "c"])),
                            others=[]),
        sigma=frozendict({"Genre": "m", "Nombre": "s"})
    )
    actual = forme.get_sigma()
    expected = frozendict({"Genre": "m", "Nombre": "s"})
    assert actual == expected


def test_to_unary() -> None:
    phonology = Phonology(apophonies=frozendict(Ø="i", i="a", a="u", u="u", e="o", o="o"),
                          mutations=frozendict(p="p", t="p", k="t", b="p", d="b",
                                               g="d", m="m", n="m", N="n", f="f",
                                               s="f", S="s", v="f", z="v", Z="z",
                                               r="w", l="r", j="w", w="w"),
                          derives=frozendict(A="V", D="C"),
                          consonnes=frozenset("ptkbdgmnNfsSvzZrljw"),
                          voyelles=frozenset("iueoa"))

    forme = Forme(
        pos="N",
        morphemes=Morphemes(radical=Radical(stems=StemSpace(stems=["a", "b", "c"])),
                            others=[]),
        sigma=frozendict({"Genre": "m", "Nombre": "s"})
    )
    actual = forme.to_unary()
    expected = "N[Genre='m',Nombre='s'] -> 'a'"
    assert actual == expected

    forme = Forme(
        pos="N",
        morphemes=Morphemes(radical=Radical(stems=StemSpace(stems=["a", "b", "c"])),
                            others=[create_morpheme(rule="a+X",
                                                    sigma=frozendict({"Genre": "m", "Nombre": "s"}),
                                                    phonology=phonology)]),
        sigma=frozendict({"Genre": "m", "Nombre": "s"})
    )

    actual = forme.to_unary()
    expected = "N[Genre='m',Nombre='s'] -> 'aa'"
    assert actual == expected
